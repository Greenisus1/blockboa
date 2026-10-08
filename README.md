# Blockboa 1.1.2

Offline Unicode-block Snake. Terminal-first: runs over an interactive SSH connection, no Tk or desktop needed. Optional desktop GUI remains.

    python3 blockboa.py
    bash app-store.sh install
    bash app-store.sh run

Arrows/WASD turn, Space starts/pauses, R restarts, 1/2/3 chooses Slow/Normal/Fast, q/Esc quits. Eat food to grow. Walls/body collision ends the game; filling every square wins. One turn per tick prevents reverse-key exploits. No account/network/telemetry/saved scores.

Colored Unicode block board uses stdlib curses and a Unicode-capable monospace terminal. Board fills available terminal width and height on start/restart (two character columns per cell). Minimum 20 columns x14 rows, 80x24 or larger recommended. A resize that no longer fits pauses; enlarge or R to fit a fresh board. Noninteractive/no-TTY terminals fail clearly rather than pretending to play. Default terminal mode needs Python3+curses, not python3-tk or a display.

Optional GUI:

    python3 blockboa.py --gui
    bash app-store.sh gui

GUI requires python3-tk + desktop/VNC. The gui hook prints before adding missing Tk only root+apt, then checks the display. Terminal install never adds Tk or a desktop.

Marker line3 is # pi-app-store-category: games. Category-aware store puts it under Games; older versions still launch it as a normal app. Version JSON included.

    python3 -m unittest -v
    python3 blockboa.py --version

Linux core tests, terminal PTY preview and virtual-display GUI checked. Physical Pi and non-Linux untested. MIT license.

1.1.2: reconciled terminal board width with actual right-border drawing so full-screen board does not clip the edge. GUI title now uses the version constant.
