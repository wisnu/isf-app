# docs/ — isf-app ZISWAF

Panduan navigasi untuk developer dan AI agents.

## Navigasi Cepat

| Folder | Isi | Untuk |
|--------|-----|-------|
| [`todos/`](todos/README.md) | Feature pipeline: MIGRATION_ANALYSIS, specs, plan, ADR | Agent + Dev |
| [`reference/`](reference/) | Arsitektur, PRD, runbook, data dictionary, history | Dev + onboarding |
| [`nuwis-agents/`](nuwis-agents/README.md) | Skill files dan config agent (claude/codex/gemini) | Agent |
| [`legacy-apps/`](legacy-apps/) | Source code DAF legacy untuk analisis migrasi | nuwis-legacy-reader |

## Konvensi `todos/`

- **Format nama folder**: `YYYY-MM-DD-NNN-slug/`
- **Status** tercatat di `README.md` tiap folder: `AKTIF` / `SELESAI` / `DITUNDA`
- **File standar** per folder: `MIGRATION_ANALYSIS.md`, `specs.md`, `plan.md`, `README.md`
- **ADR** (Architecture Decision Record) diberi prefix `adr-NNN-*.md`

## Konvensi `reference/`

| Subfolder | Isi |
|-----------|-----|
| `architecture/` | Arsitektur sistem, topologi, tech stack |
| `prd/` | Product Requirements Documents |
| `runbooks/` | Panduan operasional (local dev, deployment) |
| `datadictionary/` | Schema DB per modul (`transaction`, `accounting`, dll) |
| `history/` | Dokumen lama / arsip keputusan yang sudah digantikan |
