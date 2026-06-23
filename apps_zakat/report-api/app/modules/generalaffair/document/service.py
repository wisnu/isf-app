"""General Affair document reports service — laporan dokumen masuk & keluar."""

from __future__ import annotations

from datetime import date, timedelta

from app.shared.db import fetch_all, ping


def _parse_date(ts: str | None) -> str | None:
    if not ts:
        return None
    if isinstance(ts, str):
        return ts[:10]
    return None


async def incoming_document_rows(
    date_from: str, date_to: str, id_jenis_dokumen: int | None = None, branch: str | None = None
) -> list[dict] | None:
    if not await ping():
        return None

    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to) + timedelta(days=1)
    args: list = [df, dt]
    clause = "dm.tanggalterima >= $1 AND dm.tanggalterima < $2"

    if id_jenis_dokumen:
        args.append(id_jenis_dokumen)
        clause += f" AND d.idjenisdokumen = ${len(args)}"

    if branch:
        args.append(branch)
        clause += f" AND d.branchcode = ${len(args)}"

    rows = await fetch_all(
        f"""
        SELECT
            d.nomor,
            jd.namajenisdokumen AS nama_jenis_dokumen,
            dm.pengirim,
            d.perihal,
            CAST(d.tanggaldokumen AS VARCHAR) AS tanggal_dokumen,
            CAST(dm.tanggalterima AS VARCHAR) AS tanggal_terima,
            d.keterangan,
            d.branchcode
        FROM personalia.dokumenmasuk dm
        JOIN personalia.dokumen d ON dm.dokumenid = d.dokumenid
        JOIN personalia.jenisdokumen jd ON d.idjenisdokumen = jd.idjenisdokumen
        WHERE {clause}
        ORDER BY dm.tanggalterima DESC, d.dokumenid DESC
        """,
        *args,
    )

    if rows:
        for r in rows:
            r["tanggal_dokumen"] = _parse_date(r.get("tanggal_dokumen"))
            r["tanggal_terima"] = _parse_date(r.get("tanggal_terima"))

    return rows


async def outgoing_document_rows(
    date_from: str, date_to: str, id_jenis_dokumen: int | None = None, branch: str | None = None
) -> list[dict] | None:
    if not await ping():
        return None

    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to) + timedelta(days=1)
    args: list = [df, dt]
    clause = "d.tipedokumen = 'K' AND d.tanggaldokumen >= $1 AND d.tanggaldokumen < $2"

    if id_jenis_dokumen:
        args.append(id_jenis_dokumen)
        clause += f" AND d.idjenisdokumen = ${len(args)}"

    if branch:
        args.append(branch)
        clause += f" AND d.branchcode = ${len(args)}"

    rows = await fetch_all(
        f"""
        SELECT
            d.nomor,
            jd.namajenisdokumen AS nama_jenis_dokumen,
            dk.tujuan,
            d.perihal,
            CAST(d.tanggaldokumen AS VARCHAR) AS tanggal_dokumen,
            CAST(dk.tanggalkirim AS VARCHAR) AS tanggal_kirim,
            d.keterangan,
            dk.workunitid,
            dk.statuskirim
        FROM personalia.dokumenkeluar dk
        JOIN personalia.dokumen d ON dk.dokumenid = d.dokumenid
        JOIN personalia.jenisdokumen jd ON d.idjenisdokumen = jd.idjenisdokumen
        WHERE {clause}
        ORDER BY d.tanggaldokumen DESC, d.dokumenid DESC
        """,
        *args,
    )

    if rows:
        for r in rows:
            r["tanggal_dokumen"] = _parse_date(r.get("tanggal_dokumen"))
            r["tanggal_kirim"] = _parse_date(r.get("tanggal_kirim"))

    return rows
