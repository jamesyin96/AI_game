import pygame
from world.Heading import Heading
from world.Color import Color
from world.LightCycle import LightCycle

class Program(object):
    '''
    A user program
    '''
    
    def __init__(self, Id, Avatar):
        '''
        Initializes a new instance of the Program class.
        '''
        
        self._Health = 1
        self._Id = Id
        self._AI = None
        self.LightCycle = None
        self._Avatar = Avatar
    
    def Derezz(self):
        '''
        Returns a value indicating whether the program should derezz.
        '''
        
        # Decrease health by one.
        self._Health = self._Health - 1
        
        # Return boolean indicating whether to derezz the player.
        return self._Health == 0
    
    def Name(self):
        '''
        Returns the programs name.
        '''
        
        return "Player " + self._Id

    def UseAI(self, AI):
        self._AI = AI
    
    def UseBaton(self, Direction, Coordinate):
        '''
        Use the baton to generate the light cycle.
        '''

        color = Color.RED

        if self._Id == 1:
            color = Color.RED
        elif self._Id == 2:
            color = Color.BLUE
        elif self._Id == 3:
            color = Color.GREEN
        elif self._Id == 4:
            color = Color.YELLOW
        elif self._Id == 5:
            color = Color.WHITE

        self.LightCycle = LightCycle(color, Direction, Coordinate[0], Coordinate[1])


    def IsHuman(self):
        return self._AI.get_name() == 'Human'


    def HandleEvent(self, e):
        # Program navigation.
        if e.key == pygame.K_LEFT:
            self.LightCycle.ChangeDirection(Heading.WEST)
        elif e.key == pygame.K_DOWN:
            self.LightCycle.ChangeDirection(Heading.SOUTH)
        elif e.key == pygame.K_RIGHT:
            self.LightCycle.ChangeDirection(Heading.EAST)
        elif e.key == pygame.K_UP:
            self.LightCycle.ChangeDirection(Heading.NORTH)
        

    # modified to add an input opponentsheadlsit to to AI.react method
    def HandleAI(self, opponentsheadlist, sandbox):
        self._AI.react(self.LightCycle, opponentsheadlist, sandbox)

