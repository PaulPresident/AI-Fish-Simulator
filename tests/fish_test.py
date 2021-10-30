from typing import Type
from src.fish import Fish
from src.dna import DNA

def test_fish_creates_DNA():
    fish = Fish((1, 4))
    assert isinstance(fish.dna, DNA), "failed"
    fish.temp_char = 'hi'
    assert fish.CHAR == 'hi', "failed"

# class FishTest(unittest.TestCase):
#     # def test_fish_creates_DNA(self):
#     #     fish = Fish((1, 4))
#     #     self.assertIsInstance(fish.dna, DNA)
#     def test_fish_has_attr_coor_and_old_coor(self):
#         fish = Fish((9, 9))
#         self.assertEqual(fish.coor, (9, 9))
#         self.assertEqual(fish.old_coor, (None, None))
#     def test_fish_coor_setter(self):
#         fish = Fish((1, 4))
#         fish.coor = (3, 4)
#         self.assertEqual(fish.coor, (3, 4))
#         self.assertEqual(fish.old_coor, (1, 4))
#     def test_fish_target(self):
#         fish = Fish((2, 4))
#         self.assertEqual(fish._target([5, 6]), (1, 0))
#         self.assertEqual(fish._target([1, 5]), (-1, 0))     # if they are equal the negative will be favored
#         self.assertEqual(fish._target([3, 6]), (0, 1))
#         self.assertEqual(fish._target([3, 1]), (0, -1))
#     def test_fish_move_moves_exceeded(self):
#         fish = Fish((1, 4))
#         with self.assertRaises(ValueError):
#             fish.move(x=1)
#     def test_fish_move_invalid_move(self):
#         fish = Fish((1, 4))
#         with self.assertRaises(ValueError):
#             fish.move(1, 1)
#     def test_fish_move(self):
#         fish = Fish((1, 4))
#         fish._moves = 1
#         fish.move(y=-1)
#         self.assertEqual(fish.coor, (0, 4))
#         self.assertEqual(fish._moves, 0)
#     def test_fish_eat(self):
#         fish = Fish((1, 4))
#         fish.eat()
#         self.assertEqual(fish.food, 1)