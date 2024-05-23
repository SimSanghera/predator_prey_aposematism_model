#----- The Predator Model Outline   -----


import random
from typing import List, Tuple


class Predator:
    """
        A class  representing a predator in a predator-prey simulation.

        The predator class models the behaviour and characteristics of a predator, including:
        - its ability to move
        - detect prey
        - hunt prey
        - learn from past experiences
        - reproduce
        It takes into account the following attributes:
        - hunting success
        - learning rate
        - reproduction rate
        - detection probability
        - visual range
        - memory size
        - toxicity threshold
        - sickness duration

        Attributes:
            - hunting_success (float): probability of a successful hunt (i.e. capture and eating) of prey when the predator attempts a hunt
            - learning_rate (float): rate at which the predator learns from hunting experiences
            - reproduction_rate (float): probability of the predator reproducing at each time step
            - detection_probability (float): probability that the predator detects prey within its visual range
            - visual_range (int): the maximum distance at which the predator can detect prey
            - memory_size (int): the number of past hunting experiences the predator remembers
            - toxicity_threshold (float): the toxicity level at which the predator will avoid a prey if it recognises it as apoesmatic warning signal
            - sickness_duration (int): the number of time steps the predator is sick after consuming toxic prey
            - memory (List[Tuple[float, str]]): a list of past hunting experiences, each tuple containing the toxicity level of the prey and the outcome of the hunt
            - position (Tuple[int, int]): the current position of the predator on the grid
            - sick_timer (int): a timer that counts down the duration of the predator's sickness after consuming toxic prey

        Methods:
            - move(grid_size: int) -> None:
                Moves the predator to a new position on the grid, within the bounds of the grid size.
                Movement is based on current position and a random direction and step size.
                If the predator is sick, it does not move.
            
            - detect_prey(prey: Prey, distance: int) -> bool:
                Determines if the predator can detect the prey based on the distance between them.
                Detection is based on the detection probability and the distance between predator and prey.
                If the predator is sick, it cannot detect prey.
            
            - hunt(prey: Prey, distance: int) -> bool:
                Determines if the predator successfull hunts the prey based on prey detection and hunting success probability
                If the predator is sick, it cannot hunt prey.

            - avoid_prey(prey: Prey) -> bool:
                Determines if the predator avoids the prey based on the prey's aposematic warning signal and the predator's toxicity threshold.
                
            - learn(prey_pattern: float, outcome: str) -> None:
                Updates the predator's memory with the outcome of the hunt and toxicity threshold based on the success rate.
                The memory is updated based on the learning rate and the outcome of the hunt.
            
            - get_sick() -> None:
                Makes the predator sick after consuming toxic prey.
                The predator is sick for a duration of time steps equal to the sickness duration.
            
            - reproduce() -> bool:
                Determines if the predator reproduces based on the reproduction rate.
                If the predator reproduces, a new predator is created with the same characteristics as the parent predator.
    """

    def __init__(self,
                 hunting_success: float,
                 learning_rate: float,
                 reproduction_rate: float,
                 detection_probability: float,
                 visual_range: int,
                 memory_size: int,
                 toxicity_threshold: float,
                 sickness_duration: int
                 ):
        """
        The __init__ method (constructor) of the Predator class.
        This is automatically called when a new instance of the class is created.
        The purpose of the constructor is to initialise the attributes of the Predator object with the values provided as arguments.
        It takes several parameters as input and assigns them to the corresponding attributes of the object.
        The self parameter is a reference to the current instance of the class, and is used to access attributes and methods of the object.
        We have included type hints to help Python check the types of the arguments and return values.
        The self.hunting_success = hunting_success assigns the value of the parameter to the attribute in the instance
        """
        self.hunting_success = hunting_success
        self.learning_rate = learning_rate
        self.reproduction_rate = reproduction_rate
        self.detection_probability = detection_probability
        self.visual_range = visual_range
        self.memory_size = memory_size
        self.toxicity_threshold = toxicity_threshold
        self.sickness_duration = sickness_duration
        self.prey_eaten = 0 # number of prey eaten, start at 0
        self.memory: List[Tuple[float, str]] = [] # list of past hunting experiences, as a list of tuples
        self.position: Tuple[int, int] = (0, 0) # current position of the predator
        self.sick_timer = 0 # timer for sickness duration


    def move(self,
                grid_size: int) -> None:
        """
        Moves the predator to a new position on the grid, within the bounds of the grid size.
        Movement is based on current position and a random direction and step size.
        If the predator is sick, it does not move.

        Args:
            grid_size (int): the size of the grid (number of cells)
        """
        if self.sick_timer > 0:
            x, y, = self.position
            new_x = max(0, min(x + random.randint(-1, 1), grid_size - 1)
            new_y = max(0, min(y + random.randint(-1, 1), grid_size - 1)
            self.position = (new_x, new_y)
        else:
            self.sick_timer -= 1
    
    def detect_prey(self,
                    prey: Prey,
                    distance: int) -> bool:
        """
        Determine if the predator detects the prey based on distance, camouflage and aposematic pattern.
        If the distance is within the camo_aposematic_pattern visual range, the prey is always detected.
        If the distance is greater than the camo_aposematic_pattern visual range, the detection probability is used.

        Args:
            prey (Prey): the prey object to detect
            distance (int): the distance between the predator and the prey

        Returns:
            bool: True if the predator detects the prey, False otherwise
        """

        if distance <= self.visual_range:
            if distance > prey.camo_aposematic_distance:
                return random.randint() < (self.detection_probability * prey.camouflage)
            else:
                return True
        return False
    
    def hunt(self,
             prey: Prey,
             distance: int) -> bool:
        """
        Determine if the predator successfully hunts the prey based on detection and hunting success probability.
        Checks if the predator detects the prey using the detect_prey method.
        If the prey is detected, checks if the predator avoids the prey using the avoid_prey method.
        If the predator does not avoid the prey, checks if the predator successfully hunts the prey based on the hunting success probability.
        Increment the number of prey eaten if the predator successfully hunts the prey.

        Args:
            prey (Prey): Prey objec
            distance (int): distance between predator and prey

        Returns:
            bool: True if the predator successfully hunts the prey, False otherwise
        """
        if self.detect_prey(prey, distance):
            if self.avoid_prey(prey):
                return False
            if random.random() < self.hunting_success:
                self.prey_eaten += 1 # increment the number of prey eaten
                return True
        return False
    
    def avoid_prey(self,
                   prey: Prey) -> bool:
        """
        Determine if the predator avoids the prey based on the prey's aposematic warning signal and the predator's toxicity threshold.

        Args:
            prey (Prey): Prey object

        Returns:
            bool: True if the predator avoids the prey, False otherwise
        """
        if prey.aposematic and prey.aposematic_pattern >= self.toxicity_threshold:
            return True
        return False
    
    def learn(self,
              prey_pattern: float,
              outcome: str) -> None:
        """
        Stores both the prey's aposematic pattern and the outcome of the hunting attempt into memory.
        The outcome can be "satisfied" (predator eats prey), "death", "sickness"
        If the memory size exceeds the maximum memory size, the oldest memory is removed.
        If the success rate of recent hunting attempts is below the learning rate, both hunting success and toxicity threshold are decreased by 10%.
        
        Args:
            prey_pattern (float): aposematic pattern of the prey
            outcome (str): outcome of the hunting attempt
        """
        self.memory.append((prey_pattern, outcome))
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)
        if len(self.memory) == self.memory_size:
            success_rate = sum(1 for _,
                               outcome in self.memory if outcome == "satisfied") / self.memory_size
            if success_rate < self.learning_rate:
                self.hunting_success *= 0.9 # decrease hunting success by 10%
                self.toxicity_threshold *= 0.9 # decrease toxicity threshold by 10%
    
    def get_sick(self) -> None:
        """
        Makes the predator sick after consuming toxic prey.
        The predator is sick for a duration of time steps equal to the sickness duration.
        """
        self.sick_timer = self.sickness_duration

    def reproduce(self,
                  min_prey_eaten: int) -> bool:
        """
        Determines if the predator reproduces based on the reproduction rate and the number of prey eaten.
        
        Args: 
            min_prey_eaten (int): the minimum number of prey eaten required for the predator to reproduce

        Returns:
            bool: True if the predator reproduces, False otherwise
        """
        if self.prey_eaten >= min_prey_eaten:
            if random.random() < self.reproduction_rate:
                self.prey_eaten = 0 # reset the number of prey eaten
                return True
        return False