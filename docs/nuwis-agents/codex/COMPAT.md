# Kompatibilitas nuwis-* dengan OpenAI Codex CLI

## Kesimpulan Singkat

| Aspek | Claude Code | Codex CLI | Kompatibel? |
|---|---|---|---|
| **Konten domain** (rules, conventions, stack) | Skills + CLAUDE.md | AGENTS.md | ✅ Bisa diport |
| **Workflow steps** (7-layer pipeline) | commands/*.md + @agent syntax | AGENTS.md sections | ✅ Bisa diport |
| **Multi-agent orchestration** | Agent/Workflow tool | ❌ Tidak ada | ❌ Harus sequential |
| **Model routing per-agent** | `model: haiku/sonnet/opus` | ❌ Tidak ada | ❌ Hilang |
| **Skill tool** | `Skill` tool invocation | ❌ Tidak ada | ❌ Embed ke AGENTS.md |
| **Slash commands** | `.claude/commands/*.md` | ❌ Format berbeda | ⚠️ Perlu tulis ulang |
| **Agent frontmatter** | `name/model/color` YAML | ❌ Tidak dibaca | ❌ Harus dihapus |

**Kesimpulan**: Konten nuwis-* bisa dipakai Codex, tapi mekanisme eksekusi berbeda.
Codex tidak bisa run parallel agents — semua steps harus sequential dalam satu sesi.

---

## Perbedaan Arsitektur

```
Claude Code                          Codex CLI
─────────────────────────────────    ─────────────────────────────────
.claude/
  agents/nuwis-architect.md  ──►    AGENTS.md (satu file di project root)
  skills/nuwis-skill-vue.md  ──►    Section di AGENTS.md atau @file ref
  commands/nuwis-build.md    ──►    Template prompt (copy-paste)
  settings.json              ──►    ~/.codex/config.yaml

Entry: /nuwis-build <fitur>          Entry: user ketik instruksi + AGENTS.md
                                     dibaca otomatis setiap sesi

Multi-agent: Agent tool, parallel    Sequential: satu LLM, satu konteks
Model routing: per-agent frontmatter Model: satu model per sesi (gpt-4o, dll)
```

---

## Cara Kerja Codex CLI

Codex membaca file-file ini secara otomatis:
1. `AGENTS.md` — di project root, parent dirs, sampai `~/`
2. `~/.codex/instructions.md` — global user instructions
3. File yang di-@ reference dalam AGENTS.md

Codex **tidak** membaca `.claude/` sama sekali.

---

## Implementasi Step-by-Step

### Step 1 — Buat `AGENTS.md` di project root

File ini adalah entry point Codex untuk project isf-app.
Isi dengan konsolidasi semua nuwis-* domain knowledge.

```bash
# Dari root project isf-app
cp docs/nuwis-agents/templates/AGENTS.md.template AGENTS.md
# — atau generate manual per step 2 di bawah
```

Template tersedia di: `docs/nuwis-agents/templates/AGENTS.md.template`

### Step 2 — Struktur AGENTS.md

AGENTS.md untuk isf-app harus punya section ini (urutan penting):

```markdown
# isf-app ZISWAF — Agent Instructions

## Project Context
[Ringkasan dari CLAUDE.md: topology, tech stack, 2-portal 2-DB]

## Non-Negotiable Rules
[10 rules dari CLAUDE.md: pagination, TypeScript, DateField, dll]

## Workflow: Fitur Baru
[Dari nuwis-architect.md: 7-layer pipeline, sequential]

## Workflow: Migrasi Legacy
[Dari nuwis-architect.md + legacy-reader.md]

## Domain Knowledge: Vue ISF
[Dari nuwis-skill-vue-isf.md]

## Domain Knowledge: FastAPI ISF
[Dari nuwis-skill-fastapi-isf.md]

## Domain Knowledge: BFF Proxy
[Dari nuwis-skill-bff-proxy.md]

## Domain Knowledge: DB Migration
[Dari nuwis-skill-pg-migration.md]

## Domain Knowledge: Seed SQL
[Dari nuwis-skill-seed-sql.md]
```

### Step 3 — Jalankan generator script

```bash
bash docs/nuwis-agents/install-codex.sh
```

Script ini:
1. Membaca semua `agents/*.md` dan `skills/*.md`
2. Menghapus Claude Code frontmatter (name/model/color)
3. Menghapus `@agentname` syntax dan `Skill tool` references
4. Menggabungkan ke satu `AGENTS.md` dengan section headers

### Step 4 — Tambah ke `.codexignore` (opsional)

Agar Codex tidak membaca file-file besar yang tidak perlu:

```
node_modules/
.git/
infra/db/backups/
docs/legacy-apps/
```

### Step 5 — Verifikasi

```bash
codex "Jelaskan arsitektur isf-app"
# Codex harus bisa describe portal zakat/wakaf, tech stack, non-negotiable rules
```

---

## Perbedaan Cara Pakai

### Claude Code
```
# Slash command
/nuwis-build MuzakkiPage

# Agent invocation (dalam conversation)
@nuwis-architect analisis kebutuhan modul muzakki
```

### Codex CLI
```bash
# Semua lewat prompt biasa — AGENTS.md sudah load context
codex "Build modul muzakki: halaman CRUD, endpoint BFF, seed menu"

# Atau interaktif
codex
> Buat fitur penghimpunan batch upload sesuai workflow nuwis-architect
```

---

## Keterbatasan Codex vs Claude Code

| Fitur | Claude Code | Codex | Dampak |
|---|---|---|---|
| Parallel agents | ✅ | ❌ | Build lebih lambat (sequential) |
| Model routing | sonnet/haiku per layer | Satu model | Cost lebih tinggi per step |
| Skill tool | Load on demand | Semua di AGENTS.md | AGENTS.md jadi besar |
| Agent memory | Terpisah per agent | Satu shared context | Context bisa penuh di fitur besar |
| `/nuwis-verify` (auto-run E2E) | ✅ Shell tool | ✅ Shell tool | Bisa jalan di keduanya |
| Otonom multi-file write | ✅ | ✅ | Sama |

---

## Files yang Dibuat oleh `install-codex.sh`

```
isf-app/
├── AGENTS.md                          ← Entry point Codex (auto-generated)
└── docs/nuwis-agents/
    ├── CODEX-COMPAT.md                ← File ini
    ├── install-codex.sh               ← Generator script
    └── templates/
        └── AGENTS.md.template         ← Template manual (jika tidak mau auto-gen)
```

---

## FAQ

**Q: Apakah AGENTS.md dan CLAUDE.md bisa hidup berdampingan?**
A: Ya. Claude Code membaca CLAUDE.md (diabaikan oleh Codex), Codex membaca AGENTS.md
   (diabaikan oleh Claude Code). Keduanya bisa ada di project root sekaligus.

**Q: Apakah nuwis-skill-*.md bisa di-@reference langsung dari AGENTS.md?**
A: Ya, Codex mendukung `@path/to/file.md` reference. Contoh:
   `See @docs/nuwis-agents/skills/nuwis-skill-vue-isf.md for Vue conventions.`
   Ini lebih bersih daripada embed semua konten.

**Q: Model apa yang paling baik untuk Codex di isf-app?**
A: `gpt-4o` atau `o1` untuk architect/validator. `gpt-4o-mini` untuk
   builder steps sederhana. Tapi ini tidak bisa di-set per-step seperti nuwis-*.

**Q: Apakah bisa pakai Gemini CLI juga?**
A: Gemini CLI menggunakan `GEMINI.md` dan punya `activate_skill` tool.
   Adaptasi serupa tapi perlu file `GEMINI.md` terpisah. Format lebih dekat
   ke Claude Code daripada Codex.
