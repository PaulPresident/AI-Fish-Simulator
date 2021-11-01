from random import choice, sample
import time
from typing import Tuple
from math import trunc, ceil
import re

from src.pond import Pond
from src.fish import Fish
from src.food import Food

class Game():       #! test
    def __init__(self, size:Tuple[int, int]):
        self._max = tuple(x-1 for x in size)
        self._pond = Pond(*size)
        self._fish_school = [Fish(choice(self._pond.get_clear())) for _ in range(trunc(self._pond._size*.1))]
        self._food = [Food(choice(self._pond.get_clear())) for _ in range(trunc(len(self._fish_school)/2))]

    def _start(self):
        self._pond.reset()
        for food in self._food:
            self._pond.update(food)
            print(str(self._pond))
        for fish in self._fish_school:
            fish.reset_old_coor()
            self._pond.update(fish)
            print(str(self._pond))

    def _ai(self, fish):
        '''responsible for moving fish towards food if has targeting capability and vision allows'''
        if fish.dna.target and fish.dna.vision:
            vision = self._pond.get(list(fish.coor), fish.dna.vision)
            for objs in vision:
                for obj in objs:
                    if isinstance(obj, Food):
                        fish.move(target=obj.coor)
                        return fish
        fish.move(*self._rndm_move(fish.coor))
        return fish

    def _rndm_move(self, fish_coor:Tuple[int, int]):
        move = [0, 0]
        axis = choice([0, 1])
        if 0 < fish_coor[axis] < self._max[axis]:
            move[axis] = choice([1, -1])
        elif fish_coor[axis] == self._max[axis]:
            move[axis] = -1
        else:
            move[axis] = 1
        return move

    def _top_up_food(self):
        self._food += [
            Food(choice(self._pond.get_clear()))
            for _ in range(trunc(len(self._fish_school)/2) - len(self._food))
        ]

    def _round(self, slow:bool=False):
        '''passes each fish through the ai function and deletes eaten food'''
        for fish in self._fish_school:
            fish._moves += fish.dna.speed
            while fish._moves >= 1:
                fish.temp_char = '🔴'
                food_eaten = self._pond.update(self._ai(fish))
                if food_eaten:
                    self._food.remove(food_eaten)
                if slow: time.sleep(.75)
                print(str(self._pond))
            fish.temp_char = ''
        self._top_up_food()

    def _natural_selection(self):
        '''removes bad fish from existence'''
        self._fish_school.sort(key= lambda fish: fish.food)
        self._fish_school = self._fish_school[ceil(len(self._fish_school)*.25):]
        for fish in self._fish_school:
            fish.food = 0

    def _evolve(self):      #! change to averages = mins instead of mins
        '''breeds good fish creating new fish with better DNA'''
        self._fish_school += [
            Fish(choice(self._pond.get_clear()), (
                min(genes)
                for genes in zip(*[
                    [fish.dna.speed, fish.dna._target, fish.dna._vision]
                    for fish in self._fish_school
                ])
            ))
            for _ in range(trunc(self._pond._size*.1) - trunc(len(self._fish_school)))
        ]

    def play(self):
        while True:
            command = input("continue? y/n/skipx\n")
            if command == "y":
                self._start()
                self._round(slow=True)        # will be done multiple times before evolution
                self._natural_selection()
                self._evolve()
            if command == "n":
                break
            elif "skip" in command:
                i = 0
                while i < int(''.join(re.findall('\d+', command))):
                    self._start()
                    self._round()        # will be done multiple times before evolution
                    self._natural_selection()
                    self._evolve()
                    i += 1
            print(list(zip(["speed", "target", "vision"], [
                sum(genes)/len(genes)
                for genes in zip(*[
                    [fish.dna.speed, fish.dna._target, fish.dna._vision]
                    for fish in self._fish_school
                ])
            ])))

    # def play(self):
    #     self._start()
    #     self._round()

'''
create fish
create food
update pond
move fish ... [for every in move in fish moves] update pond print pond ... [for every fish in fish list]
'''