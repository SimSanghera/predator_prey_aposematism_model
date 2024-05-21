#----- The Prey Model Outline ------

import random
from typing import List, Tuple

class Prey:
    """
    Prey class that represents the prey in the simulation.


    """

    def __init__(self,
                 camouflage: float,
                 aposematic: bool,
                 aposematic_pattern: float,
                 toxicity: float,
                 camo_aposematic_distance: int,
                 movement_probability: float,
                 evolution_threshold: float,
                 evolution_probability: float):
        """_summary_

        Args:
            camouflage (float): _description_
            aposematic (bool): _description_
            aposematic_pattern (float): _description_
            toxicity (float): _description_
            camo_aposematic_distance (int): _description_
            movement_probability (float): _description_
            evolution_threshold (float): _description_
            evolution_probability (float): _description_
        """

        self.camouflage = camouflage
        self.aposematic = aposematic
        self.aposematic_pattern = aposematic_pattern
        self.toxicity = toxicity
        self.camo_aposematic_distance = camo_aposematic_distance
        self.movement_probability = movement_probability
        self.evolution_threshold = evolution_threshold
        self.evolution_probability = evolution_probability
        self.path: List[Tuple[int, int]] = []
        self.outcome: str = ""

    
    def is_visible(self, 
                   predator_distance: int) -> bool:
        """_summary_

        Args:
            predator_distance (int): _description_

        Returns:
            bool: _description_
        """
        if predator_distance > self.camo_aposematic_distance:
            return random.random() < self.camouflage
        else:
            return True
    
    
    def is_warning(self,
                   predator_distance: int) -> bool:
        """_summary_

        Args:
            predator_distance (int): _description_

        Returns:
            bool: _description_
        """
        return predator_distance <= self.camo_aposematic_distance
    

    def move(self,
             grid_size: int) -> None:
        """_summary_

        Args:
            grid_size (int): _description_
        """
        if random.random() < self.movement_probability:
            current_position = self.path[-1] if self.path else (0, 0)
            new_position = self._get_new_position(current_position,
                                                  grid_size)
            self.path.append(new_position)
    

    def _get_new_position(self,
                          current_position: Tuple[int, int],
                          grid_size: int) -> Tuple[int, int]:
        """_summary_

        Args:
            current_position (Tuple[int, int]): _description_
            grid_size (int): _description_

        Returns:
            Tuple[int, int]: _description_
        """
        x, y = current_position
        new_x = max(0, min(x + random.randint(-1, 1), grid_size - 1))
        new_y = max(0, min(y + random.randint(-1, 1), grid_size - 1))
        return new_x, new_y
    

    def evolve(self,
               predation_pressure: float) -> None:
        """_summary_

        Args:
            predation_pressure (float): _description_
        """
        if predation_pressure > self.evolution_threshold:
            if random.random() < self.evolution_probability:
                self.aposematic_pattern = min(1.0,
                                               self.aposematic_pattern + random.uniform(0.01, 0.1))
    

    def set_outcome(self,
                    outcome: str) -> None:
        """_summary_

        Args:
            outcome (str): _description_
        """
        self.outcome = outcome