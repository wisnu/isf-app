# nuwis-* Agent & Skill System
## isf-app ZISWAF Platform — Claude Code Automation Kit

> **Status**: Template — belum diinstall. Lihat [RUNBOOK.md](RUNBOOK.md) untuk cara install.

---

## Latar Belakang

`nuwis-*` adalah evolusi dari sistem `isf-*` yang sudah ada, terinspirasi dari pola
[migration-agents](../referensi/migration-agents/) di docs/referensi. Perbedaannya:

| Aspek | isf-* (existing) | nuwis-* (baru) |
|---|---|---|
| Format | Skills (Skill tool) + Agents terpisah | Unified: Agents + Skills + Commands |
| Scope | Per-layer (UI, BFF, Python, DB, Seed) | Full pipeline + validator + doc-gen |
| Entry point | `isf-architect` (skill) | `nuwis-architect` (agent otonom) |
| Testing | Manual / `testing/*.sh` | `nuwis-test-gen` menghasilkan script otomatis |
| Validasi parity | Tidak ada | `nuwis-validator` cek legacy vs baru |
| Dokumentasi | Manual | `nuwis-doc-gen` hasilkan specs + ADR |
| Model routing | Ad-hoc | Eksplisit per-agent berdasarkan kompleksitas |

---

## Arsitektur

```
┌────────────────────────────────────────────────────────────────┐
│                    nuwis-architect                              │
│          (Orchestrator — entry point utama)                     │
└──────┬───────┬───────┬──────┬─────┬──────┬──────┬─────────────┘
       │       │       │      │     │      │      │
  ┌────▼──┐ ┌──▼──┐ ┌──▼──┐ ┌▼───┐ ┌▼───┐ ┌▼───┐ ┌▼──────────┐
  │legacy │ │sch  │ │py   │ │bff │ │db  │ │seed│ │ui         │
  │reader │ │anal │ │build│ │bld │ │mig │ │gen │ │builder    │
  └───────┘ └─────┘ └──┬──┘ └────┘ └────┘ └────┘ └───────────┘
                        │
              ┌─────────▼──────────┐
              │  nuwis-test-gen    │
              │  nuwis-validator   │
              │  nuwis-doc-gen     │
              └────────────────────┘

            SKILLS LAYER (reference docs dibaca oleh agents)
  ┌──────────────────────────────────────────────────────────────┐
  │ daf-reader │ vue-isf │ fastapi-isf │ pg-migration │ bff-proxy │
  │ seed-sql   │ parity-check          │ e2e-script               │
  └──────────────────────────────────────────────────────────────┘
```

---

## Daftar Agent

| Agent | File | Model | Fungsi |
|---|---|---|---|
| **nuwis-architect** | `agents/nuwis-architect.md` | sonnet | Orchestrator: fitur baru + migrasi |
| **nuwis-legacy-reader** | `agents/nuwis-legacy-reader.md` | sonnet† | Baca & analisis kode DAF legacy |
| **nuwis-schema-analyst** | `agents/nuwis-schema-analyst.md` | sonnet | Analisis schema PostgreSQL + DWH |
| **nuwis-python-builder** | `agents/nuwis-python-builder.md` | haiku | Generate modul api-python |
| **nuwis-ui-builder** | `agents/nuwis-ui-builder.md` | haiku | Generate halaman Vue 3 (ISF stack) |
| **nuwis-bff-builder** | `agents/nuwis-bff-builder.md` | haiku | Generate routes BFF-API |
| **nuwis-db-migrator** | `agents/nuwis-db-migrator.md` | haiku | Migrations + DWH views |
| **nuwis-seed-gen** | `agents/nuwis-seed-gen.md` | haiku | Seed SQL menu + role_menu |
| **nuwis-test-gen** | `agents/nuwis-test-gen.md` | haiku | E2E curl scripts + pytest |
| **nuwis-validator** | `agents/nuwis-validator.md` | sonnet | Parity check legacy vs baru |
| **nuwis-doc-gen** | `agents/nuwis-doc-gen.md` | haiku | specs.md + plan.md + ADR |
| **nuwis-userguide** | `agents/nuwis-userguide.md` | haiku | Panduan pengguna MkDocs untuk operator |

† escalate ke opus untuk modul >5 dialog atau logika akuntansi kompleks

---

## Daftar Skills (reference docs)

| Skill | File | Dipakai oleh |
|---|---|---|
| **nuwis-skill-daf-reader** | `skills/nuwis-skill-daf-reader.md` | legacy-reader |
| **nuwis-skill-vue-isf** | `skills/nuwis-skill-vue-isf.md` | ui-builder |
| **nuwis-skill-fastapi-isf** | `skills/nuwis-skill-fastapi-isf.md` | python-builder |
| **nuwis-skill-pg-migration** | `skills/nuwis-skill-pg-migration.md` | db-migrator |
| **nuwis-skill-bff-proxy** | `skills/nuwis-skill-bff-proxy.md` | bff-builder |
| **nuwis-skill-seed-sql** | `skills/nuwis-skill-seed-sql.md` | seed-gen |
| **nuwis-skill-parity-check** | `skills/nuwis-skill-parity-check.md` | validator |
| **nuwis-skill-e2e-script** | `skills/nuwis-skill-e2e-script.md` | test-gen |
| **nuwis-skill-mkdocs-isf** | `skills/nuwis-skill-mkdocs-isf.md` | docs-writer |

---

## Daftar Commands (slash commands)

| Command | File | Fungsi |
|---|---|---|
| `/nuwis-analyze` | `commands/nuwis-analyze.md` | Analisis modul legacy |
| `/nuwis-migrate` | `commands/nuwis-migrate.md` | Full pipeline migrasi |
| `/nuwis-build` | `commands/nuwis-build.md` | Build fitur baru dari specs |
| `/nuwis-verify` | `commands/nuwis-verify.md` | Jalankan E2E + validasi parity |
| `/nuwis-userguide` | `commands/nuwis-userguide.md` | Generate panduan MkDocs untuk operator |
| `/nuwis-doc` | `commands/nuwis-doc.md` | Generate docs untuk fitur |

---

## Alur Kerja

### Migrasi Legacy

```
/nuwis-migrate KasHarian
   ↓
nuwis-architect → nuwis-legacy-reader (baca docs/legacy-apps/)
                → nuwis-doc-gen (specs.md + plan.md)
                → nuwis-db-migrator (DWH view jika laporan)
                → nuwis-python-builder (modul api-python)
                → nuwis-bff-builder (routes BFF)
                → nuwis-seed-gen (menu + role_menu SQL)
                → nuwis-ui-builder (halaman Vue)
                → nuwis-test-gen (e2e script)
                → nuwis-validator (parity check)
```

### Fitur Baru

```
/nuwis-build MutasiTabungan
   ↓
nuwis-architect → nuwis-doc-gen (specs.md + plan.md)
                → nuwis-python-builder
                → nuwis-bff-builder
                → nuwis-seed-gen
                → nuwis-ui-builder
                → nuwis-test-gen
```

### Tambah Laporan

```
/nuwis-build "Laporan Realisasi Program" --type=report
   ↓
nuwis-architect → nuwis-schema-analyst (analisis kolom DWH)
                → nuwis-db-migrator (buat dwh.v_*)
                → nuwis-python-builder (report-api module)
                → nuwis-bff-builder (stream xlsx route)
                → nuwis-seed-gen
                → nuwis-ui-builder (laporan page)
```

---

## Relasi dengan isf-* Existing

nuwis-* **bukan pengganti** isf-* yang sudah ada. Keduanya bisa hidup berdampingan:

- `isf-architect` (Skill tool) → tetap dipakai untuk review interaktif di conversation
- `isf-agent-*` (Skill tool) → tetap dipakai sebagai guidance context saat menulis kode manual
- `nuwis-architect` (Agent tool / Workflow) → dipakai untuk eksekusi otonom multi-layer
- `nuwis-*` builders → dipakai sebagai `subagent_type` di Workflow scripts
