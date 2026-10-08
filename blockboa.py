#!/usr/bin/env python3
"""Blockboa: Unicode-block Snake with a testable, offline game core."""
import random

VERSION = '1.0.0'
DIRECTIONS = {'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}

class Game:
 def __init__(self, width=24, height=18, rng=None):
  if width<6 or height<6:raise ValueError('Board must be at least 6 by 6.')
  self.width=width;self.height=height;self.rng=rng or random.Random()
  x,y=width//2,height//2;self.snake=[(x,y),(x-1,y),(x-2,y)]
  self.direction='right';self.queued=None;self.score=0;self.over=False;self.won=False;self.food=self.new_food()
 def new_food(self):
  free=[(x,y) for y in range(self.height) for x in range(self.width) if (x,y) not in self.snake]
  return self.rng.choice(free) if free else None
 def turn(self,name):
  if name not in DIRECTIONS or self.over or self.queued is not None:return False
  dx,dy=DIRECTIONS[self.direction];nx,ny=DIRECTIONS[name]
  if (nx,ny)==(-dx,-dy):return False
  self.queued=name;return True
 def step(self):
  if self.over:return
  if self.queued:self.direction=self.queued;self.queued=None
  dx,dy=DIRECTIONS[self.direction];x,y=self.snake[0];head=(x+dx,y+dy);eat=head==self.food
  body=self.snake if eat else self.snake[:-1]
  if not (0<=head[0]<self.width and 0<=head[1]<self.height) or head in body:self.over=True;return
  self.snake.insert(0,head)
  if eat:
   self.score+=1;self.food=self.new_food()
   if self.food is None:self.won=True;self.over=True
  else:self.snake.pop()
 def text(self):
  parts=['░░'*(self.width+2)]
  body=set(self.snake[1:]);head=self.snake[0]
  for y in range(self.height):
   line=['░░']
   for x in range(self.width):
    p=(x,y);line.append('▓▓' if p==head else '██' if p in body else '▒▒' if p==self.food else '  ')
   parts.append(''.join(line)+'░░')
  return '\n'.join(parts+['░░'*(self.width+2)])

class App:
 def __init__(self,root):
  import tkinter as tk
  from tkinter import ttk
  self.root=root;root.title('Blockboa 1.0.0');root.configure(bg='#101f2d');root.resizable(False,False)
  self.game=Game();self.paused=False;self.running=False;self.timer=None;self.interval=140
  tk.Label(root,text='BLOCKBOA',font=('DejaVu Sans Mono',20,'bold'),bg='#101f2d',fg='#a7ed7a').pack(pady=(15,4))
  self.status=tk.StringVar();tk.Label(root,textvariable=self.status,font=('DejaVu Sans Mono',11),bg='#101f2d',fg='#f7efcc').pack(pady=5)
  self.board=tk.Label(root,font=('DejaVu Sans Mono',13),bg='#101f2d',fg='#a7ed7a',justify='left',padx=12,pady=8);self.board.pack()
  tk.Label(root,text='Arrow keys / WASD: turn | Space: pause | R: restart\n▓▓ Head    ██ Snake    ▒▒ Food    ░░ Wall',font=('DejaVu Sans Mono',10),bg='#101f2d',fg='#cfdfec').pack(pady=8)
  buttons=ttk.Frame(root);buttons.pack(pady=(0,15))
  ttk.Button(buttons,text='Start / Pause',command=self.toggle).pack(side='left',padx=5)
  ttk.Button(buttons,text='Restart',command=self.restart).pack(side='left',padx=5)
  ttk.Label(buttons,text='Speed').pack(side='left',padx=5)
  self.speed=tk.StringVar(value='Normal');box=ttk.Combobox(buttons,textvariable=self.speed,values=('Slow','Normal','Fast'),state='readonly',width=8);box.pack(side='left',padx=5)
  box.bind('<<ComboboxSelected>>',lambda e:self.set_speed())
  root.bind('<KeyPress>',self.key);root.protocol('WM_DELETE_WINDOW',self.close);self.render();root.focus_force()
 def set_speed(self):self.interval={'Slow':220,'Normal':140,'Fast':85}[self.speed.get()]
 def key(self,event):
  k=event.keysym.lower()
  if k=='space':self.toggle()
  elif k=='r':self.restart()
  else:
   d={'w':'up','a':'left','s':'down','d':'right'}.get(k,k)
   if d in DIRECTIONS:self.game.turn(d)
 def render(self):
  g=self.game
  state='Board cleared! Press R.' if g.won else 'Game over. Press R.' if g.over else 'Paused' if self.paused else 'Playing' if self.running else 'Press Start or Space'
  self.status.set(f'Score: {g.score}   |   {state}');self.board.config(text=g.text())
 def tick(self):
  self.timer=None
  if self.running and not self.paused and not self.game.over:self.game.step()
  self.render()
  if self.running and not self.game.over:self.timer=self.root.after(self.interval,self.tick)
 def toggle(self):
  if self.game.over:return
  if not self.running:self.running=True;self.tick()
  else:self.paused=not self.paused;self.render()
 def restart(self):
  if self.timer:self.root.after_cancel(self.timer);self.timer=None
  self.game=Game();self.running=False;self.paused=False;self.render()
 def close(self):
  if self.timer:self.root.after_cancel(self.timer)
  self.root.destroy()

def main():
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--version',action='version',version=VERSION);p.parse_args()
 import tkinter as tk
 root=tk.Tk();App(root);root.mainloop()

if __name__=='__main__':main()
