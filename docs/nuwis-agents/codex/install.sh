#!/usr/bin/env bash
# install.sh — Generate AGENTS.md untuk OpenAI Codex CLI
# Menggabungkan nuwis-* agents + skills ke satu file AGENTS.md di project root
#
# Usage:
#   bash docs/nuwis-agents/codex/install.sh [--dry-run] [--refs-only]
#
# Options:
#   --dry-run    Print hasil ke stdout saja, tidak tulis file
#   --refs-only  Pakai @file references, tidak embed konten (AGENTS.md lebih kecil)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
NUWIS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT="$PROJECT_ROOT/AGENTS.md"
DRY_RUN=0
REFS_ONLY=0

for arg in "$@"; do
  case $arg in
    --dry-run)   DRY_RUN=1 ;;
    --refs-only) REFS_ONLY=1 ;;
  esac
done

# Hapus frontmatter YAML (--- ... ---) dan @agentname syntax dari file
strip_claude_specific() {
  local file="$1"
  # 1. Hapus frontmatter (baris pertama sampai --- penutup)
  # 2. Hapus baris berisi @nuwis-* (agent invocation syntax)
  # 3. Hapus referensi ke "Skill tool", ".claude/", "TaskCreate", "TodoWrite"
  sed '/^---$/,/^---$/d' "$file" \
    | sed 's/@nuwis-[a-z-]*/[agent]/g' \
    | grep -v 'Skill tool\|\.claude/\|TaskCreate\|TodoWrite\|EnterPlanMode'
}

# Build output ke variable atau file
build_agents_md() {
  cat <<'HEADER'
# isf-app ZISWAF — Agent Instructions for Codex CLI
# Generated from docs/nuwis-agents/ — do not edit manually
# Regenerate: bash docs/nuwis-agents/install-codex.sh

> This file is read automatically by Codex CLI at session start.
> For Claude Code, see CLAUDE.md instead.

HEADER

  # ── Project Context ─────────────────────────────────────────────────
  cat <<'SECTION'
## Project Context

**App**: isf-app — ZISWAF Platform (Zakat + Wakaf)
**Service**: web-vue (Vue 3 SPA), bff-api (BFF gateway), api-python (business logic), report-api (laporan)
**Portal Zakat**: port 5173 / bff 7000 / api 8000 / report 8010
**Portal Wakaf**: port 5174 / bff 7001 / api 8001 / report 8011

2 portals, 2 databases each:
- Business DB: `mziss_laz` (zakat) / `mziss_wakaf` (wakaf)
- Auth DB: `isf_auth_zakat` / `isf_auth_wakaf`
- DB credentials on this host: `transaction:solusi`

Frontend ONLY talks to bff-api via `VITE_API_BASE_URL`. Never call api-python directly.

SECTION

  # ── Non-Negotiable Rules ──────────────────────────────────────────
  cat <<'SECTION'
## Non-Negotiable Rules

1. **Pagination on top** — never `:paginator="true"` on DataTable; use standalone `<Paginator>` above table; default 25 rows
2. **TypeScript everywhere** — `.vue` with `<script setup lang="ts">`, no Options API, no `.js` in src/
3. **API via client.ts only** — `GET()/POST()/blob()` from `lib/api/client.ts`; never raw fetch/axios
4. **Date: dmy() for display, ISO for storage** — `DateField.vue` for input, `dmy()` from `lib/date.ts` for display
5. **Report pages no auto-load** — data fetched only when user clicks "Tampilkan"
6. **Menu keys in registry** — all keys in `lib/menu/registry.ts`, every route needs `meta.menu_key`
7. **Async feedback mandatory** — loading=true → success toast → error toast → finally reset; no alert()/console.log
8. **Role-based UI via v-if** — check auth store `menus[]`, never CSS display:none
9. **Use existing components first** — DateField, SearchSelect, TablePagination, Modal, Button, Card from `components/ui/`
10. **Portal isolation** — never cross-apply zakat seed/migration to wakaf; process separately

SECTION

  # ── Workflows ────────────────────────────────────────────────────
  if [ $REFS_ONLY -eq 1 ]; then
    echo "## Workflows (nuwis-* Agents)"
    echo ""
    echo "See the following files for detailed workflow instructions:"
    echo ""
    for f in "$NUWIS_DIR/claude/agents"/nuwis-*.md; do
      local name
      name="$(basename "$f" .md)"
      echo "- @docs/nuwis-agents/claude/agents/$(basename "$f") — $name"
    done
    echo ""
  else
    for f in "$NUWIS_DIR/claude/agents"/nuwis-architect.md \
             "$NUWIS_DIR/claude/agents"/nuwis-legacy-reader.md \
             "$NUWIS_DIR/claude/agents"/nuwis-schema-analyst.md; do
      [ -f "$f" ] || continue
      local name
      name="$(basename "$f" .md | sed 's/nuwis-//')"
      echo "## Workflow: $name"
      echo ""
      strip_claude_specific "$f"
      echo ""
      echo "---"
      echo ""
    done
  fi

  # ── Domain Skills ─────────────────────────────────────────────────
  if [ $REFS_ONLY -eq 1 ]; then
    echo "## Domain Knowledge (nuwis-* Skills)"
    echo ""
    echo "See the following files for detailed conventions:"
    echo ""
    for f in "$NUWIS_DIR/claude/skills"/nuwis-skill-*.md; do
      local name
      name="$(basename "$f" .md | sed 's/nuwis-skill-//')"
      echo "- @docs/nuwis-agents/claude/skills/$(basename "$f") — $name conventions"
    done
    echo ""
  else
    for f in "$NUWIS_DIR/claude/skills"/nuwis-skill-*.md; do
      [ -f "$f" ] || continue
      local name
      name="$(basename "$f" .md | sed 's/nuwis-skill-//')"
      echo "## Domain: $name"
      echo ""
      strip_claude_specific "$f"
      echo ""
      echo "---"
      echo ""
    done
  fi

  # ── Builder Agents ────────────────────────────────────────────────
  if [ $REFS_ONLY -eq 1 ]; then
    echo "## Builder Instructions"
    echo ""
    for f in "$NUWIS_DIR/claude/agents"/nuwis-*-builder.md \
             "$NUWIS_DIR/claude/agents"/nuwis-*-gen.md \
             "$NUWIS_DIR/claude/agents"/nuwis-*-migrator.md; do
      [ -f "$f" ] || continue
      echo "- @docs/nuwis-agents/claude/agents/$(basename "$f")"
    done
    echo ""
  else
    for f in "$NUWIS_DIR/claude/agents"/nuwis-*.md; do
      [ -f "$f" ] || continue
      [[ "$f" == *"nuwis-architect"* ]] && continue
      [[ "$f" == *"nuwis-legacy-reader"* ]] && continue
      [[ "$f" == *"nuwis-schema-analyst"* ]] && continue
      local name
      name="$(basename "$f" .md | sed 's/nuwis-//')"
      echo "## Builder: $name"
      echo ""
      strip_claude_specific "$f"
      echo ""
      echo "---"
      echo ""
    done
  fi

  # ── Commit Convention ────────────────────────────────────────────
  cat <<'SECTION'
## Commit Convention

Format wajib: `[TAG] type(scope): subject`

- TAG: UPPER-KEBAB, relevan dengan perubahan (UX, DASHBOARD, UPLOAD-PENGHIMPUNAN, dll)
- Type: feat / fix / chore / docs / refactor
- Scope: nama fitur/konteks
- Check history: `git log --grep='\['`

Active tags: UX, PRIMEVUE, INDEPENDENT-LOAD, DASHBOARD, DASHBOARD-KEUANGAN, ETL, DWH,
DOCS, RECOVERY, ADMIN-USERS, CHANGE-PASSWORD, AUTH-PG, MIGRATE-AUTHDB, PENYALURAN

SECTION

  # ── Common Prompts ───────────────────────────────────────────────
  cat <<'SECTION'
## Common Task Prompts

Use these as starting points (paste into codex prompt):

### Build fitur baru
```
Build fitur baru [NamaFitur] untuk portal [zakat|wakaf]:
- Tipe: [CRUD|Report|Approval]
- Ikuti 7-layer workflow: specs → db → python → bff → seed → ui → test
- Tanyakan klarifikasi sebelum mulai implementasi
```

### Migrasi legacy
```
Migrasi modul [NamaModul] dari docs/legacy-apps/ ke isf-app:
- Baca docs/legacy-apps/[path] dulu
- Analisis dialog, fields, business logic
- Buat specs.md dan plan.md di docs/todos/
- Tunggu konfirmasi sebelum implementasi
```

### Tambah laporan
```
Tambah laporan [NamaLaporan] untuk portal [zakat|wakaf]:
- Ikuti 5-step pattern: DWH view → report-api → BFF → frontend → seed
- Filter: DateField.vue (ISO), preview: dmy()
- No auto-load saat mount
```

SECTION
}

# ── Main ──────────────────────────────────────────────────────────────
if [ $DRY_RUN -eq 1 ]; then
  echo "=== DRY RUN — output ke stdout ==="
  echo ""
  build_agents_md
else
  if [ -f "$OUTPUT" ]; then
    echo "⚠  AGENTS.md sudah ada di $OUTPUT"
    read -r -p "   Overwrite? [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || { echo "Dibatalkan."; exit 0; }
  fi
  build_agents_md > "$OUTPUT"
  echo "✓ AGENTS.md digenerate ke $OUTPUT"
  echo ""
  SIZE=$(wc -c < "$OUTPUT")
  LINES=$(wc -l < "$OUTPUT")
  echo "  Size : ${SIZE} bytes / ${LINES} lines"
  echo ""
  if [ $REFS_ONLY -eq 1 ]; then
    echo "  Mode: refs-only — agents/skills direferensikan, tidak di-embed"
    echo "  Codex akan baca file saat dibutuhkan via @path"
  else
    echo "  Mode: full-embed — semua konten ada di AGENTS.md"
  fi
  echo ""
  echo "Selanjutnya:"
  echo "  1. Review AGENTS.md — pastikan tidak ada info sensitif"
  echo "  2. Test: codex 'Jelaskan arsitektur isf-app'"
  echo "  3. Jika terlalu besar, regenerate dengan --refs-only"
  echo ""
  echo "Untuk update:"
  echo "  bash docs/nuwis-agents/codex/install.sh --dry-run"
fi
