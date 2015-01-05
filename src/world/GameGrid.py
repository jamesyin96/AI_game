import pygame
import numpy as np
from pygame.locals import *
from world.Color import Color
from world.Heading import Heading


FRAME_PER_SECOND = 10


class GameGrid(object):
    '''
    The Game Grid is where programs compete for their survival.
    '''
    
    def __init__(self, Width, Height):
        '''
        Initializes a new instance of the GameGrid class.
        '''
        
        # Initialize the game grid.
        self.Height = Height
        self.Width = Width
        self.Sandbox = np.zeros((Width, Height))
        self._FrameRate = FRAME_PER_SECOND
        self._Programs = []
        
        # Initialize pyGame.
        pygame.init()
        pygame.display.set_caption("Racing Baby!")
        self._Clock = pygame.time.Clock()
        self._Screen = pygame.display.set_mode((self.Width*10, self.Height*10), 0, 32)
        self._Background = pygame.Surface(self._Screen.get_size())
        self._Background.fill(Color.BLACK)
    
    def DoWork(self):
        # Tick-Tock.
        self._Clock.tick(self._FrameRate)
        
        # Clear screen (or possibly don't?).
        self._Screen.blit(self._Background, (0, 0))
        
        # Peek at inputs.
        self._HandleEvents(pygame.event.get())
        self._HandleAI()
        
        removed = False
        for prog in self._Programs:
            # Move and draw.
            self._DrawLightRibbon(prog._Id, prog._Avatar, prog.LightCycle.Move(), prog.LightCycle.RibbonColor)
            
            # Collision checking.
            if prog.LightCycle.CollisionWithWall(self.Width, self.Height):
                if prog.Derezz():
                    self._Programs.remove(prog)
                    removed = True
            else:
                # For each opponent check if program collided with their light ribbon.
                # If so, determine if program should derezz.
                
                if prog.LightCycle.CollisionWithLightRibbonInSandbox(prog._Id, self.Sandbox):
                    if prog.Derezz():
                        self._Programs.remove(prog)
                        removed = True

        if removed:
            # Clean up sandbox
            X, Y = np.where(self.Sandbox == prog._Id)
            for i in range(len(X)):
                self.Sandbox[X[i]][Y[i]] = 0

            # Draw again for remaining programs
            self._Screen.blit(self._Background, (0, 0))
            for prog in self._Programs:
                self._DrawLightRibbon(prog._Id, prog._Avatar, \
                                      prog.LightCycle.LightRibbon(), \
                                      prog.LightCycle.RibbonColor)
        
        # Flip! Flip! (i.e. update the display with the latest changes)
        pygame.display.flip()
    
    def IsRunning(self):
        '''
        Returns a value indicating whether the game is still running.
        '''
        
        return len(self._Programs) > 1
    
    def LoadProgram(self, Program):
        '''
        Load a program in to the game grid.
        '''
        
        self._Programs.append(Program)
        pos = Program.LightCycle.LightRibbon()[0]
        self.Sandbox[pos[0]][pos[1]] = Program._Id
    
    def SetFrameRate(self, Rate):
        '''
        Sets the frame rate.
        '''
        
        self._FrameRate = Rate
    
    def _DrawLightRibbon(self, Id, Avatar, Vertices, Color = Color.RED):
        '''
        Draws the light ribbon.
        '''
        #Vertices2 = []
        #for vertex in Vertices:
        #    Vertices2.append((vertex[0]*10,vertex[1]*10))

        #pygame.draw.lines(self._Screen, Color, False, Vertices2, 10)
        for vertex in Vertices:
            pygame.draw.rect(self._Screen, Color, [vertex[0]*10, vertex[1]*10, 10, 10])

        pos = Vertices[-1]
        rect = Avatar.get_rect()
        self._Screen.blit(Avatar, (pos[0]*10-rect[2], pos[1]*10+5))
        vert = Vertices[-1]
        if len(Vertices) > 1:
            prev = Vertices[-2]
        else:
            prev = Vertices[-1]

        if vert[0] < self.Sandbox.shape[0] and vert[1] < self.Sandbox.shape[1]:
            if prev[0] == vert[0]:
                rng = xrange(vert[1], prev[1], -1 if vert[1]>=prev[1] else 1)
                for i in rng:
                    if self.Sandbox[vert[0]][i] > 0:
                        break
                    self.Sandbox[vert[0]][i] = Id
            elif prev[1] == vert[1]:
                rng = xrange(vert[0], prev[0], -1 if vert[0]>=prev[0] else 1)
                for i in rng:
                    if self.Sandbox[i][vert[1]] > 0:
                        break
                    self.Sandbox[i][vert[1]] = self.Sandbox[i][vert[1]] + Id
    
    def _HandleEvents(self, Events):
        '''
        Handles input events from the user(s).
        '''
        
        # TODO: Do not make static!!!!
        # Need to do something cool so there can be more
        # than just two programs playing (possibly use Id).
        
        # TODO: Add pause handling (i.e. K_SPACE).
        # TODO: Add additional exit handling (i.e. K_ESCAPE).
        # TODO: Add speed handling per program.
        
        for e in Events:
            if e.type == QUIT:
                self._Programs = []
                #pygame.quit()
            elif e.type == KEYDOWN:
                for prog in self._Programs:
                    if prog.IsHuman():
                        prog.HandleEvent(e)


    def _HandleAI(self):
        Opponentheadlist=[]
        for prog in self._Programs:
            if not prog.IsHuman():
                # modified to get the list of current opponents head coordinates
                for opponent in self._Opponents(prog):
                    Opponentheadlist.append(opponent.LightCycle.LightRibbon()[-1])
                prog.HandleAI(Opponentheadlist, self.Sandbox)

    
    def _Opponents(self, Program):
        '''
        Finds a programs opponents.
        '''
        
        opponents = self._Programs[:]
        opponents.remove(Program)
        
        return opponents


    def _DumpSandbox(self):
        np.savetxt('dump.txt', self.Sandbox, fmt='%d')
