from math import trunc
from random import uniform

class DNA():    #! test
    MAX_SPEED = 5               # max speed value for the speed strand
    MAX_TARGETING_CHANCE = 1    # max chance value for target strand
    MAX_VIEW_DISTANCE = 3       # max view distance value for vision strand
    EVOLUTION_DIFFICULTY = 3    # [0, ∞) from easy to difficult || controls convergence/speed of evolution @ higher strand values
    def __init__(self, min_spd:float, min_tar:float, min_vis:float, evl_spd:int=1):
        '''
        creates dna strands based on rndm_val_generator algorithm
        considers evl spd set by the user in the game module
        > evl spd is a number [1, ∞) controls overall convergence/speed of evolution @ all strand values -> higher values increase convergence
        '''
        self.speed = self.rndm_num_gen(min_spd, self.MAX_SPEED, self.EVOLUTION_DIFFICULTY, (self.MAX_SPEED)*evl_spd)
        self._target = self.rndm_num_gen(min_tar, self.MAX_TARGETING_CHANCE, self.EVOLUTION_DIFFICULTY, (self.MAX_SPEED/self.MAX_TARGETING_CHANCE)*evl_spd)
        self._vision = self.rndm_num_gen(min_vis, self.MAX_VIEW_DISTANCE, self.EVOLUTION_DIFFICULTY, (self.MAX_SPEED/self.MAX_VIEW_DISTANCE)*evl_spd)

    @property
    def target(self):
        return self._target > uniform(0, 1)

    @property
    def vision(self):
        return round(self._vision)

    @staticmethod
    def rndm_num_gen(min_:float, max_:float, difficulty:float, spd:float)->float:
        '''random number generator algorithm that keeps the values generated closer to the min to avoid early convergence'''
        first = uniform(min_, max_)
        val2min_diff = trunc(first*spd-(min_/difficulty)*spd)    # number of times random.uniform will be run
        return min([
            uniform(min_, max_)
            for _ in range(max(sorted([0, val2min_diff])))
        ]+[first])