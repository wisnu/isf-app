# RUNBOOK: Install & Penggunaan nuwis-* Agent System

---

## Prasyarat

- Claude Code CLI terinstall: `npm install -g @anthropic-ai/claude-code`
- Berada di root project: `cd ~/workshop/isf-app`
- Session aktif: `claude` atau buka dari IDE extension

---

## Struktur Target setelah Install

```
.claude/
├── agents/                          ← sub-agents (dipanggil dengan @nama atau sebagai subagent_type)
│   ├── nuwis-architect.md
│   ├── nuwis-legacy-reader.md
│   ├── nuwis-schema-analyst.md
│   ├── nuwis-python-builder.md
│   ├── nuwis-ui-builder.md
│   ├── nuwis-bff-builder.md
│   ├── nuwis-db-migrator.md
│   ├── nuwis-seed-gen.md
│   ├── nuwis-test-gen.md
│   ├── nuwis-validator.md
│   └── nuwis-doc-gen.md
├── skills/                          ← reference docs (dibaca oleh agents atau via Skill tool)
│   ├── nuwis-skill-daf-reader.md
│   ├── nuwis-skill-vue-isf.md
│   ├── nuwis-skill-fastapi-isf.md
│   ├── nuwis-skill-pg-migration.md
│   ├── nuwis-skill-bff-proxy.md
│   ├── nuwis-skill-seed-sql.md
│   ├── nuwis-skill-parity-check.md
│   └── nuwis-skill-e2e-script.md
└── commands/                        ← slash commands (/nuwis-analyze, dll)
    ├── nuwis-analyze.md
    ├── nuwis-migrate.md
    ├── nuwis-build.md
    ├── nuwis-verify.md
    └── nuwis-doc.md
```

---

## Cara Install

### Opsi A: Script Otomatis (direkomendasikan)

```bash
# Dari root project:
bash docs/nuwis-agents/install.sh
```

> File `install.sh` ada di bagian bawah RUNBOOK ini — copy ke `docs/nuwis-agents/install.sh` dulu.

### Opsi B: Manual

```bash
cd ~/workshop/isf-app

# Buat direktori
mkdir -p .claude/agents .claude/skills .claude/commands

# Copy agents
for f in docs/nuwis-agents/agents/nuwis-*.md; do
  cp "$f" ".claude/agents/$(basename $f)"
done

# Copy skills
for f in docs/nuwis-agents/skills/nuwis-skill-*.md; do
  cp "$f" ".claude/skills/$(basename $f)"
done

# Copy commands
for f in docs/nuwis-agents/commands/nuwis-*.md; do
  cp "$f" ".claude/commands/$(basename $f)"
done

echo "✓ nuwis-* agents, skills, commands installed"
```

### Opsi C: Selective Install

Install hanya agent tertentu yang diperlukan:

```bash
# Hanya agent untuk migrasi legacy:
cp docs/nuwis-agents/agents/nuwis-architect.md    .claude/agents/
cp docs/nuwis-agents/agents/nuwis-legacy-reader.md .claude/agents/
cp docs/nuwis-agents/skills/nuwis-skill-daf-reader.md .claude/skills/

# Hanya builders (tanpa migrasi/validator):
for agent in python-builder ui-builder bff-builder db-migrator seed-gen test-gen doc-gen; do
  cp "docs/nuwis-agents/agents/nuwis-${agent}.md" ".claude/agents/"
done
```

---

## Verifikasi Install

```bash
# Cek agents:
ls .claude/agents/nuwis-*.md

# Cek skills:
ls .claude/skills/nuwis-skill-*.md

# Cek commands:
ls .claude/commands/nuwis-*.md
```

Setelah install, **restart Claude Code session** agar agent baru terdeteksi.

---

## Cara Penggunaan

### 1. Via Slash Commands (cara paling mudah)

```
# Analisis modul legacy:
/nuwis-analyze KasHarian

# Migrasi lengkap:
/nuwis-migrate PenyaluranUmum --portal=zakat

# Build fitur baru:
/nuwis-build "Mutasi Tabungan" --type=crud --portal=wakaf

# Build laporan baru:
/nuwis-build "Laporan Realisasi Program" --type=report

# Verifikasi implementasi:
/nuwis-verify penghimpunan-dana

# Generate docs:
/nuwis-doc kas-masuk --type=runbook
```

### 2. Via @agent (panggil langsung)

```
# Analisis satu file legacy:
@nuwis-legacy-reader baca docs/legacy-apps/fund/dialogs/Penghimpunan/fFundCollection/
dan hasilkan MIGRATION_ANALYSIS. Gunakan skill .claude/skills/nuwis-skill-daf-reader.md

# Generate modul Python:
@nuwis-python-builder generate modul api-python untuk penghimpunan zakat.
Portal: zakat. Endpoints: GET /api/transaksi/penghimpunan, POST /api/transaksi/penghimpunan
Menu key: keuangan.transaksi.penghimpunan
Discriminator: accounttitype = 'D' (WAJIB hardcoded di query)

# Generate halaman Vue:
@nuwis-ui-builder buat halaman list untuk penghimpunan.
Portal: zakat. Menu key: keuangan.transaksi.penghimpunan
API: GET /api/transaksi/penghimpunan (returns {rows, pagination})
Fields: tanggal (Date), donatur (String), jumlah (Currency), keterangan (String)
Gunakan skill .claude/skills/nuwis-skill-vue-isf.md
```

### 3. Via Workflow Script (untuk automation penuh)

```javascript
// .claude/workflows/migrate-full.js
export const meta = {
  name: 'nuwis-migrate-full',
  description: 'Full pipeline migrasi modul legacy ke isf-app',
  phases: [
    { title: 'Analisis' },
    { title: 'Implementasi' },
    { title: 'Verifikasi' }
  ]
}

const modul = args.modul      // contoh: "KasHarian"
const portal = args.portal    // contoh: "zakat"

phase('Analisis')
const analysis = await agent(
  `Analisis modul ${modul} di docs/legacy-apps/. Hasilkan MIGRATION_ANALYSIS lengkap.`,
  { agentType: 'nuwis-legacy-reader', model: 'sonnet' }
)

const specs = await agent(
  `Buat specs.md dan plan.md untuk migrasi ${modul} berdasarkan:\n${analysis}`,
  { agentType: 'nuwis-doc-gen', model: 'haiku' }
)

phase('Implementasi')
// Layer 1+2 paralel:
const [db, python] = await parallel([
  () => agent(
    `Buat migration/DWH view untuk ${modul} (portal: ${portal}) berdasarkan specs:\n${specs}`,
    { agentType: 'nuwis-db-migrator', model: 'haiku' }
  ),
  () => agent(
    `Buat modul api-python untuk ${modul} (portal: ${portal}) berdasarkan specs:\n${specs}
     Discriminators dari MIGRATION_ANALYSIS: [sertakan dari analysis]`,
    { agentType: 'nuwis-python-builder', model: 'haiku' }
  )
])

const bff = await agent(
  `Buat BFF routes untuk ${modul} (portal: ${portal}) berdasarkan:\n${python}`,
  { agentType: 'nuwis-bff-builder', model: 'haiku' }
)

const seed = await agent(
  `Generate menu + role seed SQL untuk ${modul} (portal: ${portal}) berdasarkan:\n${specs}`,
  { agentType: 'nuwis-seed-gen', model: 'haiku' }
)

const ui = await agent(
  `Buat halaman Vue untuk ${modul} (portal: ${portal}).
   Menu key: [dari seed]. API endpoint: [dari bff]. Fields: [dari analysis].`,
  { agentType: 'nuwis-ui-builder', model: 'haiku' }
)

const tests = await agent(
  `Generate E2E script untuk ${modul} (portal: ${portal}) berdasarkan:\n${bff}`,
  { agentType: 'nuwis-test-gen', model: 'haiku' }
)

phase('Verifikasi')
const validation = await agent(
  `Validasi parity untuk ${modul}. MIGRATION_ANALYSIS:\n${analysis}
   Implementasi: ${python}\n${ui}`,
  { agentType: 'nuwis-validator', model: 'sonnet' }
)

return { analysis, specs, python, bff, seed, ui, tests, validation }
```

**Jalankan workflow:**
```javascript
// Di Claude Code conversation:
// Workflow({ name: 'nuwis-migrate-full', args: { modul: 'KasHarian', portal: 'zakat' } })
```

---

## Contoh Sesi Kerja Lengkap

### Contoh 1: Migrasi Modul Kas Harian

```
Step 1 — Analisis:
/nuwis-analyze KasHarian

→ Hasil: MIGRATION_ANALYSIS + specs.md di docs/todos/2026-06-15-001-kas-harian/

Step 2 — Review specs (manual):
Buka docs/todos/2026-06-15-001-kas-harian/specs.md
Konfirmasi endpoint, menu key, roles

Step 3 — Implementasi:
/nuwis-migrate KasHarian --portal=zakat

→ Hasil: semua file di 5 layer dibuat

Step 4 — Apply:
psql -U transaction -d mziss_laz -f infra/db/migrations/dwh/v_kas_harian.sql
psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/kas-harian-seed.sql
cd infra && podman-compose -f docker-compose.zakat.yml restart api-python bff-api web-vue

Step 5 — Test:
bash testing/e2e-kas-harian.sh

Step 6 — Verifikasi parity:
/nuwis-verify kas-harian
```

### Contoh 2: Fitur Baru (tanpa legacy reference)

```
Step 1 — Architect:
/nuwis-build "Monitoring Saldo Rekening" --type=report --portal=zakat

→ nuwis-architect bertanya: kolom apa yang diperlukan?

Step 2 — Schema analyst (jika perlu):
@nuwis-schema-analyst analisis schema mziss_laz untuk data saldo rekening.
Apa view DWH yang tersedia dan apa yang perlu dibuat baru?

Step 3 — Konfirmasi specs dan build:
/nuwis-build "Monitoring Saldo Rekening" --type=report --portal=zakat
```

---

## Update Agent / Skill

Jika ada perubahan pada template di `docs/nuwis-agents/`:

```bash
# Update satu agent:
cp docs/nuwis-agents/agents/nuwis-ui-builder.md .claude/agents/

# Update semua:
bash docs/nuwis-agents/install.sh --update
```

---

## Troubleshooting

### Agent tidak ditemukan

```
# Pastikan file ada:
ls .claude/agents/nuwis-architect.md

# Restart Claude Code session setelah install
```

### Skill tidak dibaca agent

Agent perlu eksplisit diarahkan ke skill path:
```
@nuwis-python-builder generate modul untuk {domain}.
Ikuti panduan di .claude/skills/nuwis-skill-fastapi-isf.md
```

### Model tidak tersedia

Ubah model di frontmatter agent file:
```yaml
# .claude/agents/nuwis-legacy-reader.md
---
model: sonnet  ← ubah ke opus jika perlu
---
```

### Output agent terpotong

Pecah per entitas kecil:
```
# Jangan: migrate seluruh modul core/ sekaligus
# Lakukan: /nuwis-migrate KasMasuk dulu, baru /nuwis-migrate KasKeluar
```

---

## Install Script

Simpan sebagai `docs/nuwis-agents/install.sh`:

```bash
#!/usr/bin/env bash
# install.sh — Install nuwis-* agents, skills, commands ke .claude/
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Installing nuwis-* to $PROJECT_ROOT/.claude/"
mkdir -p "$PROJECT_ROOT/.claude/agents" \
         "$PROJECT_ROOT/.claude/skills" \
         "$PROJECT_ROOT/.claude/commands"

# Agents
for f in "$SCRIPT_DIR/agents"/nuwis-*.md; do
  cp "$f" "$PROJECT_ROOT/.claude/agents/$(basename "$f")"
  echo "  ✓ agents/$(basename $f)"
done

# Skills
for f in "$SCRIPT_DIR/skills"/nuwis-skill-*.md; do
  cp "$f" "$PROJECT_ROOT/.claude/skills/$(basename "$f")"
  echo "  ✓ skills/$(basename $f)"
done

# Commands
for f in "$SCRIPT_DIR/commands"/nuwis-*.md; do
  cp "$f" "$PROJECT_ROOT/.claude/commands/$(basename "$f")"
  echo "  ✓ commands/$(basename $f)"
done

echo ""
echo "Done! Restart Claude Code session agar agent terdeteksi."
echo ""
echo "Quick test:"
echo "  /nuwis-analyze KasHarian"
```

---

## Perbedaan isf-* vs nuwis-*

| | isf-* (existing) | nuwis-* (baru) |
|---|---|---|
| **Lokasi** | `.claude/skills/` (Skill tool) | `.claude/agents/` + `.claude/skills/` + `.claude/commands/` |
| **Cara panggil** | `Skill` tool di conversation | `@agent`, slash command, atau `subagent_type` |
| **Kerjasama** | Guidance untuk Claude utama | Agent otonom yang bisa di-spawn |
| **Tetap dipakai?** | **Ya** — isf-architect, isf-agent-ui dll tetap relevan untuk interaksi manual | — |

Kedua sistem bisa dipakai bersamaan. isf-* untuk interaksi manual dengan Claude;
nuwis-* untuk pipeline otonom yang dimulai dengan slash command atau Workflow.
