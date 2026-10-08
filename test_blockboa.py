import unittest,random
from blockboa import Game
class Tests(unittest.TestCase):
 def g(self):return Game(rng=random.Random(2))
 def test_initial(self):
  g=self.g();self.assertEqual(len(g.snake),3);self.assertNotIn(g.food,g.snake)
 def test_step(self):
  g=self.g();x,y=g.snake[0];g.step();self.assertEqual(g.snake[0],(x+1,y));self.assertEqual(len(g.snake),3)
 def test_reverse(self):
  g=self.g();self.assertFalse(g.turn('left'));g.step();self.assertEqual(g.direction,'right')
 def test_one_turn(self):
  g=self.g();self.assertTrue(g.turn('up'));self.assertFalse(g.turn('left'));g.step();self.assertEqual(g.direction,'up')
 def test_growth(self):
  g=self.g();x,y=g.snake[0];g.food=(x+1,y);g.step();self.assertEqual(g.score,1);self.assertEqual(len(g.snake),4);self.assertNotIn(g.food,g.snake)
 def test_wall(self):
  g=self.g();g.snake=[(23,0),(22,0),(21,0)];g.step();self.assertTrue(g.over)
 def test_body(self):
  g=self.g();g.snake=[(2,2),(2,3),(3,3),(3,2),(3,1)];g.step();self.assertTrue(g.over)
 def test_tail_allowed(self):
  g=self.g();g.snake=[(2,2),(2,3),(3,3),(3,2)];g.food=(0,0);g.step();self.assertFalse(g.over);self.assertEqual(g.snake[0],(3,2))
 def test_invalid_turn(self):self.assertFalse(self.g().turn('banana'))
 def test_stopped(self):
  g=self.g();g.over=True;before=list(g.snake);g.step();self.assertEqual(g.snake,before);self.assertFalse(g.turn('up'))
 def test_grid(self):
  g=self.g();t=g.text().splitlines();self.assertEqual(len(t),20);self.assertTrue(all(len(x)==52 for x in t));self.assertIn('▓▓',g.text());self.assertIn('▒▒',g.text())
 def test_winning(self):
  g=Game(6,6);g.snake=[(x,y) for y in range(6) for x in range(6) if (x,y)!=(5,5)];g.snake.remove((4,5));g.snake.insert(0,(4,5));g.food=(5,5);g.step();self.assertTrue(g.won);self.assertTrue(g.over);self.assertIsNone(g.food)
 def test_invalid_board(self):self.assertRaises(ValueError,Game,3,3)
 def test_seed(self):self.assertEqual(self.g().food,self.g().food)
if __name__=='__main__':unittest.main()
