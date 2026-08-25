#!/bin/bash
# Installs the plain-register and plain-check skills, plus the shared rules
# file, into ~/.claude/. Existing files are left alone unless you pass --force.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
FORCE=0; [ "$1" = "--force" ] && FORCE=1
copy() {
  src="$1"; dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ -e "$dst" ] && [ "$FORCE" -eq 0 ]; then
    echo "skip (exists): $dst"
  else
    cp "$src" "$dst"; echo "installed:     $dst"
  fi
}
copy "$HERE/claude/skills/plain-register/SKILL.md" "$HOME/.claude/skills/plain-register/SKILL.md"
copy "$HERE/claude/skills/plain-register/stamp.py" "$HOME/.claude/skills/plain-register/stamp.py"
copy "$HERE/claude/skills/plain-check/SKILL.md"    "$HOME/.claude/skills/plain-check/SKILL.md"
copy "$HERE/claude/skills/plain-check/check.py"    "$HOME/.claude/skills/plain-check/check.py"
copy "$HERE/claude/output-styles/plain-register.md" "$HOME/.claude/output-styles/plain-register.md"
echo
echo "Done. Restart Claude Code, then type /plain-register or /plain-check."
echo "To make the register always on, run /output-style and pick 'Plain register'."
