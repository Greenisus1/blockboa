# Blockboa

Offline Snake drawn with Unicode block characters. No account, network, payment, score telemetry, or saved user data.

Python 3, Tk (on Raspberry Pi OS: python3-tk), a desktop or VNC session, and a monospace font with Unicode block glyphs are required. Linux core tests and an actual Tk desktop preview were checked. Physical Raspberry Pi and non-Linux platforms are untested.

## Run

    python3 blockboa.py

Arrow keys or WASD turn. Space starts or pauses. R restarts. Eat the shaded block to grow, avoid walls and your body. Darker shaded blocks are the head. Score is food eaten. Clearing every square wins. Pick Slow, Normal or Fast speed. A single turn is accepted per tick so key repeats cannot reverse the snake.

## Pi App Store

    bash app-store.sh install
    bash app-store.sh run

The category marker is `games` on line 3. A category-aware App Store places this app in Games; older versions can still list and launch it normally. This package does not modify the App Store or move its existing games by itself.

    python3 -m unittest -v
    python3 blockboa.py --version

Version 1.0.0. MIT license.
