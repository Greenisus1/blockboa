#!/bin/bash
# pi-app-store: 1
# pi-app-store-category: games
set -eu
cd -- "$(dirname -- "$0")"
case "${1:-}" in
 install) python3 -c 'import tkinter' || { echo 'Install python3-tk and use a desktop or VNC.'; exit 1; } ;;
 run) exec python3 blockboa.py ;;
 *) echo 'Usage: bash app-store.sh install|run'; exit 2 ;;
esac
