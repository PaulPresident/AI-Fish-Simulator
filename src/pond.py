from itertools import permutations
from typing import List

from src.fish import Fish
from src.food import Food

class Pond():
    CLEAR = '⚪'
    ADJACENT_NODES = list(set(permutations([1, 1, -1, -1], 2)))     # produces the coors of all adjacent nodes to a centerpoint

    def __init__(self, row:int, column:int):
        self._size = row * column
        self._max_coor = row, column
        self._pond = [[[self.CLEAR] for _ in range(column)] for _ in range(row)]     # creates a map based on given size

    def __str__(self):
        '''creates a string version of the nested map variable'''
        pond_string = []
        for row in self._pond:
            pond_string.append(''.join([obj[-1].CHAR if hasattr(obj[-1], 'CHAR') else obj[-1] for obj in row ]))
        return '\n'.join(pond_string) + '\n'

    def get(self, coor:List[int], r:int, idx:int=1):
        '''
        returns a list containing all of the nodes within a radius
        starting with the closest to a given object (centerpoint)
        '''
        result = []

        if r == idx-1:      # recursion exit statement
            return result

        coor[0] -= 1        # sets pointer above the centerpoint
        for i in [2, 1, 3, 0]:      # list for splicing adjacent nodes in a clockwise fashion
            for move_y, move_x in (self.ADJACENT_NODES*idx)[i::4]:      # produces adequate # of the adjacent nodes and splice to get next adjacent node in the clockwise rotation
                coor = [coor[0] + move_y, coor[1] + move_x]         # moves the pointer to the next closest node
                if coor[0] in range(len(self._pond[0])) and coor[1] in range(len(self._pond[1])):       # makes sure the coor is not less than 0
                    #! causes indexOutOfRange Error when coordinates are different e.g. 7, 8
                    result.append(self._pond[coor[0]][coor[1]])

        return result + self.get(coor, r, idx+1)

    def update(self, obj):      #! test
        '''updates the specified object in the pond'''
        # print(obj.coor)   #! print test
        if hasattr(obj, 'old_coor') and isinstance(obj.old_coor[0], int):
            self._pond[obj.old_coor[0]][obj.old_coor[1]].pop(self._pond[obj.old_coor[0]][obj.old_coor[1]].index(obj))
        self._pond[obj.coor[0]][obj.coor[1]].append(obj)
        if isinstance(obj, Fish) and any(isinstance(obj, Food) for obj in self._pond[obj.coor[0]][obj.coor[1]]):
            obj.eat()
            food_eaten = [(idx, item) for idx, item in enumerate(self._pond[obj.coor[0]][obj.coor[1]]) if isinstance(item, Food)][0]
            self._pond[obj.coor[0]][obj.coor[1]].pop(food_eaten[0])
            return food_eaten[-1]

    def get_clear(self):
        '''returns a list will all clear nodes in the pond'''
        return [
            (y, x)
            for y, row in enumerate(self._pond)
            for x, node in enumerate(row)
            if node[-1] == self.CLEAR
        ]

    def reset(self):        #! test
        self._pond = [[[self.CLEAR] for _ in range(self._max_coor[1])] for _ in range(self._max_coor[0])]