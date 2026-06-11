#!/usr/bin/env bash
# install.sh — Install nuwis-* untuk Gemini CLI
# - Copy GEMINI.md ke project root
# - Copy adapted skills ke .gemini/skills/
#
# Usage: bash docs/nuwis-agents/gemini/install.sh [--update] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
NUWIS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DRY_RUN=0
UPDATE=0

for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=1 ;;
    --update)  UPDATE=1  ;;
  esac
done

echo "nuwis-* Install (Gemini CLI)"
echo "  Source : $SCRIPT_DIR"
echo "  Target : $PROJECT_ROOT/ + $PROJECT_ROOT/.gemini/"
[ $DRY_RUN -eq 1 ] && echo "  Mode   : DRY RUN"
echo ""

copy_file() {
  local src="$1"
  local dst="$2"
  local name
  name="$(basename "$src")"

  if [ $DRY_RUN -eq 1 ]; then
    echo "  [dry] $dst"
    return
  fi

  if [ -f "$dst" ] && [ $UPDATE -eq 0 ]; then
    echo "  skip  $name (sudah ada, gunakan --update untuk overwrite)"
  else
    cp "$src" "$dst"
    echo "  ✓ $name"
  fi
}

# GEMINI.md ke project root
echo "── GEMINI.md ─────────────────────────────────────────────"
GEMINI_TEMPLATE="$SCRIPT_DIR/GEMINI.md.template"
GEMINI_TARGET="$PROJECT_ROOT/GEMINI.md"

if [ -f "$GEMINI_TEMPLATE" ]; then
  copy_file "$GEMINI_TEMPLATE" "$GEMINI_TARGET"
else
  echo "  ⚠ GEMINI.md.template tidak ditemukan di $GEMINI_TEMPLATE"
fi

# Skills ke .gemini/skills/
echo ""
echo "── Skills ───────────────────────────────────────────────"
mkdir -p "$PROJECT_ROOT/.gemini/skills"

# Gunakan skills dari claude/ sebagai source, strip Claude-specific syntax
for src in "$NUWIS_DIR/claude/skills"/nuwis-skill-*.md; do
  [ -f "$src" ] || continue
  name="$(basename "$src")"
  # Nama dikonversi: nuwis-skill-vue-isf.md → nuwis-vue-isf.md (sesuai GEMINI.md)
  gemini_name="$(basename "$src" | sed 's/nuwis-skill-/nuwis-/')"
  dst="$PROJECT_ROOT/.gemini/skills/$gemini_name"

  if [ $DRY_RUN -eq 1 ]; then
    echo "  [dry] .gemini/skills/$gemini_name"
    continue
  fi

  if [ -f "$dst" ] && [ $UPDATE -eq 0 ]; then
    echo "  skip  $gemini_name"
  else
    # Strip Claude-specific references saat copy
    sed '/^---$/,/^---$/d' "$src" \
      | sed 's/Skill tool/activate_skill/g' \
      | sed 's/\.claude\//\.gemini\//g' \
      | sed 's/TaskCreate\|TodoWrite\|EnterPlanMode//g' \
      > "$dst"
    echo "  ✓ $gemini_name"
  fi
done

echo ""
if [ $DRY_RUN -eq 0 ]; then
  echo "✓ Install selesai!"
  echo ""
  echo "Selanjutnya:"
  echo "  1. Review GEMINI.md di project root"
  echo "  2. Test: gemini 'Jelaskan arsitektur isf-app'"
  echo "  3. Untuk skill on-demand: activate_skill(\"nuwis-vue-isf\")"
  echo ""
  echo "Untuk update: bash docs/nuwis-agents/gemini/install.sh --update"
else
  echo "Dry run selesai."
fi
