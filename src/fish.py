import random
from typing import List, Tuple

class DNA():    #! test
    def __init__(self, min_spd:float, min_tar:float, min_vis:int):
        self.speed = random.uniform(min_spd, 2)
        # self.speed = 5
        self._targeting = random.uniform(min_tar, 1)
        # self._targeting = 1
        self.vision = random.randint(min_vis, 3)
        # self.vision = 3

        @property
        def targeting(self)->bool:
            return self._targeting > random.random()

class Fish():
    _CHAR = '🟠'

    def __init__(self, coor:Tuple[int, int], min_dna_values:Tuple[float, float, int]=(0.1, 0, 0)):
        self.dna = DNA(*min_dna_values)
        self._coor = coor       # (y, x)
        self.old_coor = (None, None)
        self._moves = 0
        self.food = 0
        self.temp_char = ''

    @property
    def CHAR(self):
        return self.temp_char if self.temp_char else self._CHAR

    @property
    def coor(self):
        return self._coor

    @coor.setter
    def coor(self, coor:Tuple[int, int]):
        self.old_coor = self._coor
        self._coor = coor

    def _target(self, target):
        '''creates a coor to move self closer to an object starting with the furthest distance'''
        dist = [t-s for t, s in zip(target, self.coor)]
        if dist == [0, 0]: return dist      #! test
        if max(dist) > 0 and abs(min(dist)) < max(dist):
            return (0, 1) if dist.index(max(dist)) else (1, 0)
        return (0, -1) if dist.index(min(dist)) else (-1, 0)

    def move(self, y:int=0, x:int=0, target:List=None):
        if not self._moves:
            raise ValueError('moves exceeded')
        if y + x > 1:
            raise ValueError('invalid move')
        if target:      #! test
            y, x = self._target(target)
        self.coor = self.coor[0] + y, self.coor[1] + x
        self._moves -= 1

    def eat(self):
        self.food += 1

    def reset_old_coor(self):       #! test
        self.old_coor = (None, None)