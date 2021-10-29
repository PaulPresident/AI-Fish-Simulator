# import unittest
# from unittest.mock import MagicMock
# from src.food import Food
# from src.pond import Pond

# class PondTest(unittest.TestCase):
#     def test_pond_attr_size(self):
#         pond = Pond(5, 5)
#         self.assertEqual(pond._size, 25)
#     def test_pond_attr_max_coor(self):
#         pond = Pond(5, 5)
#         self.assertEqual(pond._max_coor, (4, 4))
#     def test_pond_attr_pond(self):
#         pond = Pond(5, 5)
#         self.assertEqual(pond._pond, [
#             ['⚪', '⚪', '⚪', '⚪', '⚪'],
#             ['⚪', '⚪', '⚪', '⚪', '⚪'],
#             ['⚪', '⚪', '⚪', '⚪', '⚪'],
#             ['⚪', '⚪', '⚪', '⚪', '⚪'],
#             ['⚪', '⚪', '⚪', '⚪', '⚪']
#         ])
#     def test_pond_str(self):
#         pond = Pond(5, 5)
#         self.assertEqual(str(pond), '⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪')
#     def test_pond_get(self):
#         pond = Pond(5, 5)
#         pond._pond = [
#             [10, 11, 12, 13, 14, 15, 16],
#             [20, 21, 22, 23, 24, 25, 26],
#             [30, 31, 32, 33, 34, 35, 36],
#             [40, 41, 42, 'O', 44, 45, 46],
#             [50, 51, 52, 53, 54, 55, 56],
#             [60, 61, 62, 63, 64, 65, 66],
#             [70, 71, 72, 73, 74, 75, 76]
#         ]
#         self.assertEqual(pond.get([3, 3], 3), [44, 53, 42, 33, 34, 45, 54, 63, 52, 41, 32, 23, 24, 35, 46, 55, 64, 73, 62, 51, 40, 31, 22, 13])
#         self.assertEqual(len(pond.get([0, 0], 3)), 9)
#         self.assertEqual(len(pond.get([6, 6], 3)), 9)
#     def test_pond_update_error(self):
#         pond = Pond(2, 3)
#         fish = MagicMock(coor=(2,2))
#         with self.assertRaises(ValueError):
#             pond.update(fish)
#     def test_pond_update_fish(self):
#         pond = Pond(5, 5)
#         fish = MagicMock(coor=(3, 2))
#         pond.update(fish)
#         self.assertIsInstance(pond._pond[3][2], MagicMock)
#         fish.configure_mock(**{'old_coor': (3, 2)})
#         fish.coor = (4, 4)
#         pond.update(fish)
#         self.assertIsInstance(pond._pond[3][2], str)
#         self.assertIsInstance(pond._pond[4][4], MagicMock)
#     def test_pond_update_eat(self):
#         pond = Pond(5, 5)
#         food = MagicMock(coor=(3, 2), spec=Food)
#         pond.update(food)
#         fish = MagicMock(coor=(3, 2))
#         fish.configure_mock(**{'eat.return_value': 1})
#         pond.update(fish)
#         MagicMock.assert_called_once(fish.eat)
#     def test_pond_get_clear_nodes(self):
#         pond = Pond(5, 5)
#         pond._pond = [
#             ['⚪', 11, 12, 13],
#             ['⚪', '⚪', '⚪', '⚪'],
#             [30, '⚪', 32, 33],
#             ['⚪', 41, 42, '⚪']
#         ]
#         self.assertEqual(len(pond.get_clear()), 8)