#----- The Prey Model Outline ------

import random
from typing import List, Tuple


class Prey:
    """
    Prey class that represents the prey in the simulation.
    Defined with the specified attributes as parameters in the __init__ method.
    """

    def __init__(self,
                 camouflage: float,
                 aposematic: bool,
                 aposematic_pattern: float,
                 toxicity: float,
                 camo_aposematic_distance: int,
                 movement_probability: float,
                 evolution_threshold: float,
                 evolution_probability: float,
                 reproduction_rate: float
                 ):
        """_summary_

        Args:
            camouflage (float): a probability value representing the probability a prey is detected by a predator
            aposematic (bool): defines whether prey is toxic or not
            aposematic_pattern (float): a continuous variable representing the degree of warning signal (i.e. bright red warning signal, or subtle warning)
            toxicity (float): Continuous variable representing the toxicity of the prey
            camo_aposematic_distance (int): a value representing the distance at which pattern is camouflage or warning signal
            movement_probability (float): probability that prey will move during a time step
            evolution_threshold (float): threshold of predation pressure that triggers evolution
            evolution_probability (float): probability that aposematic pattern evolves if evolution threshold is met
        """

        self.camouflage = camouflage
        self.aposematic = aposematic
        self.aposematic_pattern = aposematic_pattern
        self.toxicity = toxicity
        self.camo_aposematic_distance = camo_aposematic_distance
        self.movement_probability = movement_probability
        self.evolution_threshold = evolution_threshold
        self.evolution_probability = evolution_probability
        self.reproduction_rate = reproduction_rate
        self.path: List[Tuple[int, int]] = []
        self.outcome: str = ""

    
    def is_visible(self, 
                   predator_distance: int) -> bool:
        """
        Determines if prey is visible to predator based on camo-aposematic distance logic.
        If the predator is further away than the camo-aposematic distance, the prey is camouflaged and visibility is determined by camouflage probability.
        If the predator is closer than the camo-aposematic distance, the prey is aposematic and visible to the predator.

        Args:
            predator_distance (int): distance in cells/metres between predator and prey

        Returns:
            bool: True - prey is visible, False - prey visibility determined by camouflage probability
        """
        if predator_distance > self.camo_aposematic_distance:
            return random.random() < self.camouflage
        else:
            return True
    
    
    def is_warning(self,
                   predator_distance: int) -> bool:
        """
        Checks if the prey pattern acts as a warning signal based on the predator's distance

        Args:
            predator_distance (int): Distance between predator and prey (cells or metres)

        Returns:
            bool: True = warning signal, False = not a warning signal
        """
        return predator_distance <= self.camo_aposematic_distance
    

    def move(self,
             grid_size: Tuple[int, int]) -> None:
        """
        Uses the movement_probability to determine if the prey will move during a time step.
        If the prey moves, it randomly selects a new position within the grid.

        Args:
            grid_size Tuple[int, int]: Size of grid width and height
        """
        if random.random() < self.movement_probability:
            current_position = self.path[-1] if self.path else (0, 0)
            new_position = self._get_new_position(current_position,
                                                  grid_size)
            self.path.append(new_position)
    

    def _get_new_position(self,
                          current_position: Tuple[int, int],
                          grid_size: Tuple[int, int]) -> Tuple[int, int]:
        """
        This is a helper function that calculates the new position of the prey based on the current position and grid size.

        Args:
            current_position (Tuple[int, int]): x, y coordinates
            grid_size (int): size of grid

        Returns:
            Tuple[int, int]: New coordinates, x, y
        """
        x, y = current_position
        new_x = max(0, min(x + random.randint(-1, 1), grid_size[0] - 1))
        new_y = max(0, min(y + random.randint(-1, 1), grid_size[1] - 1))
        return new_x, new_y
    

    def toxicity_level(self) -> float:
        """
        Returns the toxicity level of the prey based on the aposematic pattern and toxicity

        Returns:
            float: toxicity level
        """
        return self.toxicity * self.aposematic_pattern
    

    def evolve(self,
               predation_pressure: float) -> None:
        """
        If the predation pressure is above the evolution_threshold, the prey's aposematic pattern evolves with a certain evolution_probability
        The aposematic pattern is updated to represent more toxicity.

        Args:
            predation_pressure (float): Continuous value of predation pressure
        """
        if predation_pressure > self.evolution_threshold:
            if random.random() < self.evolution_probability:
                self.aposematic_pattern = min(1.0,
                                              self.aposematic_pattern + random.uniform(0.01, 0.1)) # increase aposematic pattern
                self.toxicity = min(1.0, 
                                    self.toxicity + random.uniform(0.01, 0.1)) # increase toxicity
    

    def reproduce(self,
                  reproduction_rate: float) -> bool:
        """
        Determines if the prey reproduces based on the reproduction rate.

        Args:
            reproduction_rate (float): probability of reproduction

        Returns:
            bool: True - prey reproduces, False - prey does not reproduce
        """
        return random.random() < self.reproduction_rate
    

    def reproduce(self) -> 'Prey':
        """
        Reproduces a new prey based on the reproduction rate, if reproduction is successful.
        It uses the same parameters as the parent prey.

        Returns:
            Prey: New prey object. Return type has been updated to Prey.
        """
        if random.random() < self.reproduction_rate:
            return Prey(
                camouflage = self.camouflage,
                aposematic = self.aposematic,
                aposematic_pattern = self.aposematic_pattern,
                toxicity = self.toxicity,
                camo_aposematic_distance = self.camo_aposematic_distance,
                movement_probability = self.movement_probability,
                evolution_threshold = self.evolution_threshold,
                evolution_probability = self.evolution_probability,
                reproduction_rate = self.reproduction_rate
                )
        return None
    

    def set_outcome(self,
                    outcome: str) -> None:
        """
        Sets the outcome of the prey (survived, eaten, attacked)
        The outcome logic will be defined during the simulation logic

        Args:
            outcome (str): string denoting outcome
        """
        self.outcome = outcome