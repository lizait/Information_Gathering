#!/usr/bin/env bash

fluxion_startup() {

  local banner=()

  format_center_literals \
    " ⌠▓▒▓▒   ⌠▓╗     ⌠█┐ ┌█   ┌▓\  /▓┐   ⌠▓╖   ⌠◙▒▓▒◙   ⌠█\  ☒┐test"
  banner+=("$FormatCenterLiterals")
  format_center_literals \
    " ║▒_     │▒║     │▒║ ║▒    \▒\/▒/    │☢╫   │▒┌╤┐▒   ║▓▒\ ▓║"
  banner+=("$FormatCenterLiterals")
  format_center_literals \
    " ≡◙◙     ║◙║     ║◙║ ║◙      ◙◙      ║¤▒   ║▓║☯║▓   ♜◙\✪\◙♜"
  banner+=("$FormatCenterLiterals")
  format_center_literals \
    " ║▒      │▒║__   │▒└_┘▒    /▒/\▒\    │☢╫   │▒└╧┘▒   ║█ \▒█║"
  banner+=("$FormatCenterLiterals")
  format_center_literals \
    " ⌡▓      ⌡◘▒▓▒   ⌡◘▒▓▒◘   └▓/  \▓┘   ⌡▓╝   ⌡◙▒▓▒◙   ⌡▓  \▓┘"
  banner+=("$FormatCenterLiterals")
  format_center_literals \
    "¯¯¯     ¯¯¯¯¯¯  ¯¯¯¯¯¯¯  ¯¯¯    ¯¯¯ ¯¯¯¯  ¯¯¯¯¯¯¯  ¯¯¯¯¯¯¯¯"
  banner+=("$FormatCenterLiterals")

  clear

  # shellcheck disable=SC2078
  #if [ 0 ]; then echo -e "$CBlu"; else echo -e "$CRed"; fi

  for line in "${banner[@]}"; do
    echo "$line"; sleep 0.05
  done

  echo # Do not remove.


}

fluxion_startup