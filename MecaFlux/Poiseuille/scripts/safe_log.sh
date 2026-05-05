#!/usr/bin/env bash

# Small logging helper for bash scripts.
# Avoids patterns like `printf "--- ..."` that can be interpreted as options.

log_ts() {
  date +"%Y-%m-%d %H:%M:%S"
}

log_line() {
  # Always pass user text through a fixed format string.
  printf '%s\n' "$*"
}

log_info() {
  printf '[%s] [INFO] %s\n' "$(log_ts)" "$*"
}

log_warn() {
  printf '[%s] [WARN] %s\n' "$(log_ts)" "$*"
}

log_error() {
  printf '[%s] [ERROR] %s\n' "$(log_ts)" "$*" >&2
}

log_hr() {
  printf '%s\n' '------------------------------------------------------------'
}

log_section() {
  log_hr
  printf '%s\n' "$*"
  log_hr
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  log_section "safe_log.sh demo"
  log_info "This helper is ready."
  log_warn "Use: source scripts/safe_log.sh"
  log_error "Example error output"
  log_line "Literal separator text: --- no option parsing issue"
fi
