#----- Environment Class    ------

import random
from typing import List, Tuple
import numpy as np


class Environment:
    def __init__(
            self,
            width: int,
            height: int,
            num_predators: int,
            num_prey: int
    ):
        """
        Summary: Environment class that represents the environment in the simulation.
        Defined with the specified attributes as parameters in the __init__ method.
        The grid is initialized using a 2D numpy array with the specified width and height.


        Args:
            width (int): the width of the environment
            height (int): the height of the environment
            num_predators (int): the number of predators
            num_prey (int): the number of prey
        """

        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.predators = [Predator() for _ in range(num_predators)]
        self.prey = [Prey() for _ in range(num_prey)]
        self.place_creatures()
    
    
    def place_creatures(self):
        """
        Places the predators and prey in the environment grid.
        This can also handle overlapping positions by using a set to keep track of occupied positions, ensuring each predator and prey is placed on a unique position.

        """
        positions = set()
        for predator in self.predators:
            while True:
                x, y = self.get_random_location()
                if (x, y) not in positions:
                    predator.position = (x, y)
                    positions.add((x, y))
                    self.grid[y][x] = predator
                    break
        for prey in self.prey:
            while True:
                x, y = self.get_random_location()
                if (x, y) not in positions:
                    prey.position = (x, y)
                    positions.add((x, y))
                    self.grid[y][x] = prey
                    break
    

    def get_random_location(self):
        """
        Returns a random location within the environment grid.

        Returns:
            Tuple[int, int]: a tuple containing the x and y coordinates of the random location
        """
        return np.random.randint(0, self.width - 1), np.random.randint(0, self.height - 1)
    

    def is_within_bounds(self, 
                         position: Tuple[int, int]):
        """
        Checks if the given position is within the bounds of the environment grid.

        Args:
            position (Tuple[int, int]): a tuple containing the x and y coordinates

        Returns:
            bool: True if the position is within bounds, False otherwise
        """
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height
    

    def __repr__(self):
        """
        Returns a string representation of the Environment object.
        Returns:
            _type_: _description_
        """
        return f"Environment(width={self.width}, height={self.height}, num_predators={len(self.predators)}, num_prey={len(self.prey)})"