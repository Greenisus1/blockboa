"""Unicode-block Snake over an interactive SSH terminal, no desktop."""
import curses
import time
from blockboa import Game
from terminal_ui import run

def play(ui):
 interval=0.14;paused=False;started=False;game=None;next_tick=0
 def reset():
  nonlocal game,paused,started,next_tick
  h,w=ui.s.getmaxyx();width=(w-5)//2; height=h-7
  if width<6 or height<6:game=None;return
  game=Game(width,height);paused=False;started=False;next_tick=time.monotonic()+interval
 reset();ui.s.timeout(30)
 try:
  while True:
   h,w=ui.s.getmaxyx()
   if game is None:
    ui.draw('Terminal too small. Resize to at least 20 columns x 14 rows.',[],footer='Resize to play  q Quit')
   else:
    state='Won! R to restart' if game.won else 'Game over. R to restart' if game.over else 'Paused' if paused else 'Playing' if started else 'Space to start'
    ui.s.erase();ui.put(0,0,'█ BLOCKBOA 1.1.2 █',curses.color_pair(1) if curses.has_colors() else curses.A_BOLD)
    ui.put(1,0,f'Score {game.score} | {state} | Speed {interval:.2f}s')
    if w<2*(game.width+2)+1 or h<game.height+7:
     paused=True;ui.put(3,0,'Board no longer fits. Enlarge terminal or press R to fit a new board.')
    else:
     for y,line in enumerate(game.text().splitlines()):ui.put(y+3,0,line,curses.color_pair(1) if curses.has_colors() else 0)
    ui.put(h-2,0,'Arrows/WASD Turn | Space Start/Pause | R Restart | 1/2/3 Speed')
    ui.put(h-1,0,'q Quit | ▓▓ Head  ██ Body  ▒▒ Food  ░░ Wall');ui.s.refresh()
   try:k=ui.s.get_wch()
   except curses.error:k=None
   if k in ('q','\x1b'):return
   if k==curses.KEY_RESIZE:
    if game is None:reset()
    continue
   if k in ('r','R'):reset()
   if k in ('1','2','3'):interval={'1':0.22,'2':0.14,'3':0.085}[k];next_tick=time.monotonic()+interval
   if game is not None:
    if k==' ' and not game.over:
     if started:paused=not paused
     else:started=True
     next_tick=time.monotonic()+interval
    # Explicit toggle state separately to avoid advancing on initial start.
    if k in (curses.KEY_UP,curses.KEY_DOWN,curses.KEY_LEFT,curses.KEY_RIGHT,'w','a','s','d'):
     direction={curses.KEY_UP:'up',curses.KEY_DOWN:'down',curses.KEY_LEFT:'left',curses.KEY_RIGHT:'right','w':'up','a':'left','s':'down','d':'right'}[k];game.turn(direction)
    now=time.monotonic()
    if started and not paused and not game.over and now>=next_tick:game.step();next_tick=now+interval
 finally:ui.s.timeout(-1)
def launch():return run('Blockboa',play)
