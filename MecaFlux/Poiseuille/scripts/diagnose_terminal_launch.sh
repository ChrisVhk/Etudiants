#!/usr/bin/env bash
set -euo pipefail

OUT_ROOT="${1:-$HOME/terminal-launch-diagnostics}"
TS="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="$OUT_ROOT/$TS"
mkdir -p "$OUT_DIR"

log() {
  printf '[diag] %s\n' "$1"
}

safe_cmd() {
  local name="$1"
  shift
  {
    echo "===== $name ====="
    "$@"
  } >"$OUT_DIR/$name.txt" 2>&1 || true
}

safe_grep_logs() {
  local src_dir="$1"
  local dst="$2"
  if [[ -d "$src_dir" ]]; then
    {
      echo "===== grep in $src_dir ====="
      grep -RInE "Troubleshoot Terminal launch failures|terminal|pty|launch|spawn|ENOENT|EACCES|shell|bashrc|profile|failed|error" "$src_dir" || true
    } >"$dst" 2>&1
  fi
}

log "Writing diagnostics to $OUT_DIR"

safe_cmd env_info bash -lc 'echo USER=$USER; echo SHELL=$SHELL; echo PWD=$PWD; uname -a; date -Is'
safe_cmd shell_check bash -lc 'getent passwd "$USER" | cut -d: -f1,7; command -v bash; bash --version | head -n1; /bin/bash -lc "echo non_interactive_ok"; /bin/bash -lic "echo interactive_login_ok"'
safe_cmd bashrc_tail bash -lc 'nl -ba ~/.bashrc | tail -n 120'
safe_cmd profile_tail bash -lc 'nl -ba ~/.profile | tail -n 120'
safe_cmd vscode_settings bash -lc 'for f in "$HOME/.vscode-server/data/Machine/settings.json" "$HOME/.vscode-server/data/User/settings.json"; do echo "===== $f ====="; [ -f "$f" ] && nl -ba "$f" || echo "missing"; done'
safe_cmd pty_prereq bash -lc 'ls -la /bin/bash /usr/bin/bash; stat -c "%a %U:%G %n" /dev/ptmx /dev/pts /tmp; mount | grep -E " /tmp |devpts" || true'

LOG_BASE="$HOME/.vscode-server/data/logs"
if [[ -d "$LOG_BASE" ]]; then
  safe_cmd vscode_log_dirs bash -lc "ls -1dt '$LOG_BASE'/* | head -n 10"
  mkdir -p "$OUT_DIR/recent_logs"

  latest="$(ls -1dt "$LOG_BASE"/* 2>/dev/null | head -n 1 || true)"
  if [[ -n "$latest" && -d "$latest" ]]; then
    mkdir -p "$OUT_DIR/latest_logs"
    [[ -f "$latest/ptyhost.log" ]] && cp "$latest/ptyhost.log" "$OUT_DIR/latest_logs/ptyhost.log"
    [[ -f "$latest/remoteagent.log" ]] && cp "$latest/remoteagent.log" "$OUT_DIR/latest_logs/remoteagent.log"
    safe_grep_logs "$latest" "$OUT_DIR/latest_logs/grep_latest_logs.txt"
  fi

  session_idx=0
  while IFS= read -r log_dir; do
    [[ -z "$log_dir" || ! -d "$log_dir" ]] && continue
    session_idx=$((session_idx + 1))
    session_name="$(basename "$log_dir")"
    session_out="$OUT_DIR/recent_logs/session_${session_idx}_${session_name}"
    mkdir -p "$session_out"

    [[ -f "$log_dir/ptyhost.log" ]] && cp "$log_dir/ptyhost.log" "$session_out/ptyhost.log"
    [[ -f "$log_dir/remoteagent.log" ]] && cp "$log_dir/remoteagent.log" "$session_out/remoteagent.log"
    safe_grep_logs "$log_dir" "$session_out/grep_session_logs.txt"
  done < <(ls -1dt "$LOG_BASE"/* 2>/dev/null | head -n 5)
fi

WS_BASE="$HOME/.vscode-server/data/User/workspaceStorage"
if [[ -d "$WS_BASE" ]]; then
  safe_cmd copilot_debug_roots bash -lc "find '$WS_BASE' -maxdepth 4 -type d -path '*GitHub.copilot-chat/debug-logs*'"
  first_debug_dir="$(find "$WS_BASE" -maxdepth 5 -type d -path '*GitHub.copilot-chat/debug-logs/*' | head -n 1 || true)"
  if [[ -n "$first_debug_dir" && -d "$first_debug_dir" ]]; then
    mkdir -p "$OUT_DIR/copilot_debug"
    find "$first_debug_dir" -maxdepth 1 -type f -name '*.json*' -exec cp {} "$OUT_DIR/copilot_debug/" \; || true
    safe_grep_logs "$first_debug_dir" "$OUT_DIR/copilot_debug/grep_copilot_debug.txt"
  fi
fi

cat > "$OUT_DIR/README.txt" <<EOF
Terminal launch diagnostics bundle

Created: $(date -Is)
Location: $OUT_DIR

How to use:
1. Reproduce the terminal launch failure in VS Code.
2. Run: bash scripts/diagnose_terminal_launch.sh
3. Share files from this directory, especially:
   - recent_logs/session_*/grep_session_logs.txt
   - recent_logs/session_*/ptyhost.log
   - recent_logs/session_*/remoteagent.log
   - latest_logs/ptyhost.log
   - latest_logs/remoteagent.log
   - latest_logs/grep_latest_logs.txt
   - env_info.txt and shell_check.txt
EOF

log "Done. Bundle created at: $OUT_DIR"
