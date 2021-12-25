from random import choice
import time
from typing import Tuple
from math import trunc, ceil

from src.pond import Pond
from src.fish import Fish
from src.food import Food
from src.dna import DNA

class Game():       #! test
    def __init__(self, size:Tuple[int, int], evolution_speed:int=1):
        self._max_coor = tuple(x-1 for x in size)
        self._pond = Pond(*size)
        self._fish_school = [Fish(choice(self._pond.get_clear()), evl_spd=evolution_speed) for _ in range(trunc(self._pond._size*.1))]
        self._food = [Food(choice(self._pond.get_clear())) for _ in range(trunc(len(self._fish_school)/2))]
        self._dna_progress = [
            [],     # speed
            [],     # target
            [],     # vision
            []      # best
        ]
        self._food_eaten = [0, 0]
        self._gen = 0
        self._last_recorded_gen = 0

    def _start(self):
        self._pond.reset()
        for food in self._food:
            self._pond.update(food)
        for fish in self._fish_school:
            fish.reset_old_coor()
            self._pond.update(fish)

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
        if 0 < fish_coor[axis] < self._max_coor[axis]:
            move[axis] = choice([1, -1])
        elif fish_coor[axis] == self._max_coor[axis]:
            move[axis] = -1
        else:
            move[axis] = 1
        return move

    def __add_food__(self):
        new_food = Food(choice(self._pond.get_clear()))
        self._food.append(new_food)
        self._pond.update(new_food)

    def _round(self, slow:bool=False):
        '''passes each fish through the ai function allowing them to exhaust their moves and deletes eaten food'''
        for fish in self._fish_school:
            fish._moves += fish.dna.speed
            while fish._moves >= 1:
                fish.temp_char = '🔴'
                food_eaten = self._pond.update(self._ai(fish))
                if food_eaten:
                    self._food.remove(food_eaten)
                    self._food_eaten[0] += 1
                    self.__add_food__()
                time.sleep((1*slow))
                print(str(self._pond))
            fish.temp_char = ''

    def _natural_selection(self):
        '''removes bad fish from existence'''
        self._fish_school.sort(key= lambda fish: fish.food)
        self._fish_school = self._fish_school[ceil(len(self._fish_school)*.25):]
        for fish in self._fish_school:
            fish.food = 0

    def _evolve(self):
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

    def _collect_data(self):
        zipped_genes = zip(*[
            [fish.dna.speed, fish.dna._target, fish.dna._vision]
            for fish in self._fish_school
        ])

        self._dna_progress[3] = []
        for i, genes in enumerate(zipped_genes):
            self._dna_progress[i].append(sum(genes)/len(genes))
            self._dna_progress[3].append(max(genes))

        self._pond._pond[0].append(["\tavg\tmoves\ttarget\tvision"])
        self._pond._pond[1].append([f"\tgen {self._gen}\t{round(self._dna_progress[0][-1], 3)}\t{round(self._dna_progress[1][-1], 3)}\t{round(self._dna_progress[2][-1], 3)}"])
        next_ = 0
        if len(self._dna_progress[0]) > 1:
            self._pond._pond[2].append([f"\tgen {self._last_recorded_gen}\t{round(self._dna_progress[0][-2], 3)}\t{round(self._dna_progress[1][-2], 3)}\t{round(self._dna_progress[2][-2], 3)}"])
            next_ += 1
        self._pond._pond[2+next_].append([f"\tmax\t{DNA.MAX_SPEED}\t{DNA.MAX_TARGETING_CHANCE}\t{DNA.MAX_VIEW_DISTANCE}"])
        self._pond._pond[3+next_].append([f"\tbest\t{round(self._dna_progress[3][0], 3)}\t{round(self._dna_progress[3][1], 3)}\t{round(self._dna_progress[3][2], 3)}"])
        self._last_recorded_gen = self._gen
        self._food_eaten[1] += self._food_eaten[0]      # set total food eaten

    def play(self):
        while True:
            command = input("continue? y/n/skipx\n")
            if command == "y":
                self._start()
                self._round(slow=True)
                self._natural_selection()
                self._evolve()
                self._gen += 1
            elif command == "n":
                break
            elif "skip" in command and command[4::].isnumeric():
                i = 0
                while i < int(command[4::]):
                    self._start()
                    self._round()
                    self._natural_selection()
                    self._evolve()
                    self._gen += 1
                    i += 1
            else:
                print("That command does not exist!")
                continue

            self._collect_data()
            print(f"\ncurrent generation: {self._gen}\nfood eaten: {self._food_eaten[0]}/{self._food_eaten[1]}\n")
            print(str(self._pond))
            self._food_eaten[0] = 0     # reset curr gen food count