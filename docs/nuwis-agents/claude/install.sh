#!/usr/bin/env bash
# install.sh — Install nuwis-* agents, skills, commands ke .claude/ (Claude Code)
# Usage: bash docs/nuwis-agents/claude/install.sh [--update] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
DRY_RUN=0
UPDATE=0

for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=1 ;;
    --update)  UPDATE=1  ;;
  esac
done

echo "nuwis-* Install (Claude Code)"
echo "  Source : $SCRIPT_DIR"
echo "  Target : $PROJECT_ROOT/.claude/"
[ $DRY_RUN -eq 1 ] && echo "  Mode   : DRY RUN (tidak ada yang diinstall)"
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

mkdir -p "$PROJECT_ROOT/.claude/agents" \
         "$PROJECT_ROOT/.claude/skills" \
         "$PROJECT_ROOT/.claude/commands"

echo "── Agents ───────────────────────────────────────────────"
for f in "$SCRIPT_DIR/agents"/nuwis-*.md; do
  copy_file "$f" "$PROJECT_ROOT/.claude/agents/$(basename "$f")"
done

echo ""
echo "── Skills ───────────────────────────────────────────────"
for f in "$SCRIPT_DIR/skills"/nuwis-skill-*.md; do
  copy_file "$f" "$PROJECT_ROOT/.claude/skills/$(basename "$f")"
done

echo ""
echo "── Commands ─────────────────────────────────────────────"
for f in "$SCRIPT_DIR/commands"/nuwis-*.md; do
  copy_file "$f" "$PROJECT_ROOT/.claude/commands/$(basename "$f")"
done

echo ""
if [ $DRY_RUN -eq 0 ]; then
  echo "✓ Install selesai!"
  echo ""
  echo "Selanjutnya:"
  echo "  1. Restart Claude Code session agar agent terdeteksi"
  echo "  2. Test: /nuwis-analyze KasHarian"
  echo ""
  echo "Untuk update setelah template berubah:"
  echo "  bash docs/nuwis-agents/claude/install.sh --update"
else
  echo "Dry run selesai — jalankan tanpa --dry-run untuk install."
fi
