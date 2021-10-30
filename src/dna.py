import random
from math import trunc

class DNA():    #! test
    MAX_SPEED = 5
    MAX_TARGETING_CHANCE = 1
    MAX_VIEW_DISTANCE = 1
    EVOLUTION_DIFFICULTY = 2 # [1, ∞) from easy to difficult
    def __init__(self, min_spd:float, min_tar:float, min_vis:int):
        this = max((sorted([1, trunc(random.uniform(min_spd, self.MAX_SPEED)-(min_spd/self.EVOLUTION_DIFFICULTY))])))
        self.speed = min([
            random.uniform(min_spd, self.MAX_SPEED)
            for _ in range(this)
        ])
        # self.speed = random.uniform(min_spd, self.MAX_SPEED)
        # self.speed = 5
        self._targeting = random.uniform(min_tar, self.MAX_TARGETING_CHANCE)
        # self._targeting = 1
        self.vision = random.randint(min_vis, self.MAX_VIEW_DISTANCE)
        # self.vision = 3

        @property
        def targeting(self)->bool:
            return self._targeting > random.random()