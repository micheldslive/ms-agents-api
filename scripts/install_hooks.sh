#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# install_hooks.sh — installs git hooks for this project.
# Run: bash scripts/install_hooks.sh   OR   make install_hooks
# ─────────────────────────────────────────────────────────────────────────────

set -e

HOOKS_DIR=".git/hooks"
SCRIPTS_DIR="scripts"

if [ ! -d "$HOOKS_DIR" ]; then
    echo "❌  .git/hooks directory not found. Are you inside a git repository?"
    exit 1
fi

echo "📦  Installing git hooks…"

# ── pre-push ──────────────────────────────────────────────────────────────────
cp "$SCRIPTS_DIR/pre-push" "$HOOKS_DIR/pre-push"
chmod +x "$HOOKS_DIR/pre-push"
echo "  ✅  pre-push hook installed → blocks push if tests fail"

echo ""
echo "🎉  Done! All hooks are active."
echo "    To bypass (not recommended): git push --no-verify"
echo ""
