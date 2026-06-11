# nuwis-* Agent & Skill System
## isf-app ZISWAF — Multi-Platform AI Automation Kit

Sistem `nuwis-*` menyediakan agent/skill specs untuk build fitur isf-app secara
otonom. Tersedia untuk tiga platform AI CLI:

```
docs/nuwis-agents/
├── claude/          ← Claude Code (Anthropic) — full multi-agent support
├── codex/           ← OpenAI Codex CLI — single-context, AGENTS.md
└── gemini/          ← Gemini CLI — activate_skill pattern, GEMINI.md
```

---

## Platform Comparison

| Fitur | Claude Code | Codex CLI | Gemini CLI |
|---|---|---|---|
| Multi-agent / parallel | ✅ Agent + Workflow tools | ❌ Sequential only | ⚠️ Limited |
| Skill on-demand | ✅ `Skill` tool | ❌ Embed ke AGENTS.md | ✅ `activate_skill` |
| Model routing per-agent | ✅ frontmatter `model:` | ❌ Satu model/sesi | ❌ Satu model/sesi |
| Slash commands | ✅ `.claude/commands/` | ❌ Prompt template | ⚠️ Berbeda format |
| Entry point | `CLAUDE.md` | `AGENTS.md` | `GEMINI.md` |
| Install dir | `.claude/` | project root | `.gemini/` |

---

## Install

### Claude Code
```bash
bash docs/nuwis-agents/claude/install.sh
# Opsional: --update (overwrite), --dry-run
```
Files di-copy ke `.claude/agents/`, `.claude/skills/`, `.claude/commands/`.
Restart Claude Code session setelah install.

### Codex CLI
```bash
bash docs/nuwis-agents/codex/install.sh
# Opsional: --refs-only (AGENTS.md lebih kecil, pakai @file refs)
```
Generates `AGENTS.md` di project root — dibaca otomatis oleh Codex setiap sesi.

### Gemini CLI
```bash
bash docs/nuwis-agents/gemini/install.sh
# Opsional: --update
```
Copy `GEMINI.md` ke project root + skills ke `.gemini/skills/`.

---

## Cara Pakai

### Claude Code — Slash Commands
```
/nuwis-analyze KasHarian        ← analisis legacy
/nuwis-migrate PenerimaanAmil   ← full pipeline migrasi
/nuwis-build MuzakkiPage        ← fitur baru
/nuwis-verify                   ← E2E + parity check
/nuwis-doc                      ← generate docs
```

### Codex CLI — Natural language
```bash
codex "Build fitur Muzakki CRUD untuk portal zakat, ikuti workflow nuwis-architect"
codex "Migrasi modul KasHarian dari docs/legacy-apps/"
```

### Gemini CLI — activate_skill pattern
```
activate_skill("nuwis-vue-isf")
Buat halaman MuzakkiPage untuk portal zakat
```

---

## Folder Detail

- [`claude/`](claude/README.md) — Full nuwis-* system untuk Claude Code: agents, skills, commands, model routing
- [`codex/`](codex/COMPAT.md) — AGENTS.md template + install script + analisis kompatibilitas
- [`gemini/`](gemini/README.md) — GEMINI.md template + adapted skills + install script
