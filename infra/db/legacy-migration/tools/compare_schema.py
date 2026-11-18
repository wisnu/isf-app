#!/usr/bin/env python3
"""Bandingkan struktur dua database PostgreSQL via katalog.

Pemakaian:
  python3 -I compare_schema.py --source mziss_laz_origin --target mziss_laz \
      --out-dir <dir>

  source = DB legacy (hasil restore backup produksi)
  target = DB isf-app (struktur yang diinginkan)

Output (di --out-dir):
  catalog-<db>.json      snapshot katalog tiap DB
  diff.json              hasil diff terstruktur (dipakai gen_migration.py)
  diff-summary.txt       ringkasan angka
"""
import argparse
import hashlib
import json
import os
import re

import psycopg2

EXCLUDE_SCHEMAS = ("pg_catalog", "information_schema", "pg_toast")


def conn(db, args, port=None):
    return psycopg2.connect(host=args.host, port=port or args.port, user=args.user,
                            password=args.password, dbname=db)


def q(cur, sql, params=None):
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def h(s):
    return hashlib.md5(norm(s).encode()).hexdigest()[:12]


def snapshot(db, args, port=None):
    c = conn(db, args, port)
    cur = c.cursor()
    ex = "('" + "','".join(EXCLUDE_SCHEMAS) + "')"
    snap = {}
    snap["extensions"] = sorted(r["extname"] for r in q(cur, "select extname from pg_extension"))
    snap["schemas"] = sorted(r["nspname"] for r in q(cur, f"""
        select nspname from pg_namespace
        where nspname not in {ex} and nspname not like 'pg_temp%' and nspname not like 'pg_toast%'"""))

    rels = q(cur, f"""
        select n.nspname s, c.relname t, c.relkind k, c.reltuples::bigint est,
               pg_total_relation_size(c.oid) sz
        from pg_class c join pg_namespace n on n.oid=c.relnamespace
        where n.nspname not in {ex} and c.relkind in ('r','p','v','m','S','f')""")
    snap["tables"] = {f'{r["s"]}.{r["t"]}': {"est_rows": max(r["est"], 0), "size": r["sz"]}
                      for r in rels if r["k"] in ("r", "p", "f")}
    snap["sequences"] = sorted(f'{r["s"]}.{r["t"]}' for r in rels if r["k"] == "S")

    cols = q(cur, f"""
        select n.nspname s, c.relname t, a.attname col, a.attnum pos,
               format_type(a.atttypid, a.atttypmod) typ, a.attnotnull nn,
               pg_get_expr(d.adbin, d.adrelid) def, a.attidentity ident
        from pg_attribute a
        join pg_class c on c.oid=a.attrelid join pg_namespace n on n.oid=c.relnamespace
        left join pg_attrdef d on d.adrelid=a.attrelid and d.adnum=a.attnum
        where n.nspname not in {ex} and c.relkind in ('r','p','f')
          and a.attnum>0 and not a.attisdropped
        order by 1,2,4""")
    snap["columns"] = {}
    for r in cols:
        snap["columns"].setdefault(f'{r["s"]}.{r["t"]}', {})[r["col"]] = {
            "pos": r["pos"], "type": r["typ"], "notnull": r["nn"],
            "default": r["def"], "identity": r["ident"] or None}

    cons = q(cur, f"""
        select n.nspname s, c.relname t, co.conname AS name, co.contype typ,
               pg_get_constraintdef(co.oid) def
        from pg_constraint co join pg_class c on c.oid=co.conrelid
        join pg_namespace n on n.oid=c.relnamespace
        where n.nspname not in {ex} and co.contype in ('p','u','f','c','x')""")
    snap["constraints"] = {f'{r["s"]}.{r["t"]}.{r["name"]}':
                           {"table": f'{r["s"]}.{r["t"]}', "type": r["typ"], "def": r["def"]}
                           for r in cons}

    idx = q(cur, f"""
        select n.nspname s, t.relname t, i.relname AS name, pg_get_indexdef(i.oid) def,
               exists(select 1 from pg_constraint co where co.conindid=i.oid
                      and co.contype in ('p','u','x')) is_con
        from pg_index x join pg_class i on i.oid=x.indexrelid
        join pg_class t on t.oid=x.indrelid join pg_namespace n on n.oid=t.relnamespace
        where n.nspname not in {ex}""")
    snap["indexes"] = {f'{r["s"]}.{r["name"]}': {"table": f'{r["s"]}.{r["t"]}', "def": r["def"]}
                       for r in idx if not r["is_con"]}

    views = q(cur, f"""
        select n.nspname s, c.relname t, c.relkind k, pg_get_viewdef(c.oid) def
        from pg_class c join pg_namespace n on n.oid=c.relnamespace
        where n.nspname not in {ex} and c.relkind in ('v','m')""")
    snap["views"] = {f'{r["s"]}.{r["t"]}': {"kind": r["k"], "hash": h(r["def"])} for r in views}

    funcs = q(cur, f"""
        select n.nspname s, p.proname AS name, pg_get_function_identity_arguments(p.oid) args,
               p.prokind k, md5(pg_get_functiondef(p.oid)) hash
        from pg_proc p join pg_namespace n on n.oid=p.pronamespace
        left join pg_depend d on d.objid=p.oid and d.deptype='e'
        where n.nspname not in {ex} and p.prokind in ('f','p') and d.objid is null""")
    snap["functions"] = {f'{r["s"]}.{r["name"]}({r["args"]})': {"hash": r["hash"][:12]} for r in funcs}

    trg = q(cur, f"""
        select n.nspname s, c.relname t, tg.tgname AS name, pg_get_triggerdef(tg.oid) def
        from pg_trigger tg join pg_class c on c.oid=tg.tgrelid
        join pg_namespace n on n.oid=c.relnamespace
        where n.nspname not in {ex} and not tg.tgisinternal""")
    snap["triggers"] = {f'{r["s"]}.{r["t"]}.{r["name"]}': {"def": r["def"]} for r in trg}

    types = q(cur, f"""
        select n.nspname s, t.typname AS name, t.typtype k
        from pg_type t join pg_namespace n on n.oid=t.typnamespace
        left join pg_class c on c.oid=t.typrelid
        where n.nspname not in {ex} and t.typtype in ('e','d','c')
          and (c.oid is null or c.relkind='c')""")
    snap["types"] = sorted(f'{r["s"]}.{r["name"]}:{r["k"]}' for r in types)
    c.close()
    return snap


def diff_keys(a, b):
    a, b = set(a), set(b)
    return sorted(b - a), sorted(a - b), sorted(a & b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--host", default=os.environ.get("PGHOST", "localhost"))
    ap.add_argument("--port", default=os.environ.get("PGPORT", "5432"))
    ap.add_argument("--user", default=os.environ.get("PGUSER", "transaction"))
    ap.add_argument("--source-port", help="port server source bila beda dari --port")
    ap.add_argument("--target-port", help="port server target bila beda dari --port")
    ap.add_argument("--password", default=os.environ.get("PGPASSWORD", "solusi"))
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    src = snapshot(args.source, args, args.source_port)
    tgt = snapshot(args.target, args, args.target_port)
    for name, s in (("source-" + args.source, src), ("target-" + args.target, tgt)):
        with open(os.path.join(args.out_dir, f"catalog-{name}.json"), "w") as f:
            json.dump(s, f, indent=1, sort_keys=True, default=str)

    d = {"source": args.source, "target": args.target}
    for k in ("extensions", "schemas", "sequences", "types"):
        add, rem, _ = diff_keys(src[k], tgt[k])
        d[k] = {"only_target": add, "only_source": rem}

    add, rem, both = diff_keys(src["tables"], tgt["tables"])
    d["tables"] = {"only_target": add, "only_source": rem}

    col_add, col_rem, col_chg = [], [], []
    for t in both:
        sc, tc = src["columns"].get(t, {}), tgt["columns"].get(t, {})
        for c in sorted(set(tc) - set(sc)):
            col_add.append({"table": t, "column": c, **tc[c]})
        for c in sorted(set(sc) - set(tc)):
            col_rem.append({"table": t, "column": c, **sc[c]})
        for c in sorted(set(sc) & set(tc)):
            ch = {f: [sc[c][f], tc[c][f]] for f in ("type", "notnull", "default", "identity")
                  if sc[c][f] != tc[c][f]}
            if ch:
                col_chg.append({"table": t, "column": c, "changes": ch})
    d["columns"] = {"only_target": col_add, "only_source": col_rem, "changed": col_chg}

    for k in ("constraints", "indexes", "triggers"):
        add, rem, both_k = diff_keys(src[k], tgt[k])
        d[k] = {
            "only_target": [{"name": n, **tgt[k][n]} for n in add],
            "only_source": [{"name": n, **src[k][n]} for n in rem],
            "changed": [{"name": n, "source": src[k][n]["def"], "target": tgt[k][n]["def"]}
                        for n in both_k if src[k][n]["def"] != tgt[k][n]["def"]],
        }
    for k in ("views", "functions"):
        add, rem, both_k = diff_keys(src[k], tgt[k])
        d[k] = {"only_target": add, "only_source": rem,
                "changed": [n for n in both_k if src[k][n]["hash"] != tgt[k][n]["hash"]]}

    d["row_estimates"] = {t: {"source": src["tables"][t]["est_rows"],
                              "target": tgt["tables"][t]["est_rows"]}
                          for t in sorted(set(src["tables"]) & set(tgt["tables"]))}

    with open(os.path.join(args.out_dir, "diff.json"), "w") as f:
        json.dump(d, f, indent=1, default=str)

    lines = [f"source={args.source}  target={args.target}"]
    for k, v in d.items():
        if isinstance(v, dict) and k != "row_estimates":
            lines.append(f"{k:12s} " + "  ".join(f"{kk}={len(vv)}" for kk, vv in v.items()))
    txt = "\n".join(lines)
    with open(os.path.join(args.out_dir, "diff-summary.txt"), "w") as f:
        f.write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
