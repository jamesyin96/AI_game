from world.Color import Color
from world.Heading import Heading

class LightCycle(object):
    '''
    Light cycle vehicle
    '''
    
    def __init__(self, Color, Direction = Heading.NORTH, StartX = 0, StartY = 0):
        '''
        Initializes a new instance of the LightCycle class.
        '''
        
        self.RibbonColor = Color
        self.Direction = Direction
        self.DirectionChanged = False
        self._LightRibbon = [(StartX, StartY)]
        self._Speed = 1
    
    def ChangeDirection(self, NewHeading):
        '''
        Change light cycle direction.
        '''
        
        # Check to make sure the bike is not pulling a 180 degree turn.
        if ((self.Direction == Heading.NORTH and NewHeading == Heading.SOUTH)
            or (self.Direction == Heading.SOUTH and NewHeading == Heading.NORTH)
            or (self.Direction == Heading.EAST and NewHeading == Heading.WEST)
            or (self.Direction == Heading.WEST and NewHeading == Heading.EAST)):
            pass
        else:
            self.Direction = NewHeading
            self.DirectionChanged = True
    
    #def CollisionWithLightRibbon(self, Ribbon):
    #    '''
    #    Check each point of a ribbon if we have a collision.
    #    '''
    #    for coord in Ribbon:
    #        if self._LightRibbon.count(coord) > 0:
    #            return True
    #    return False

    def CollisionWithLightRibbonInSandbox(self, Id, Sandbox):
        '''
        Check each point of the sandbox if we have a collision.
        '''

        curr = self._LightRibbon[-1]
        prev = self._LightRibbon[-2] if len(self._LightRibbon) > 1 else self._lightRibbon[-1]
        if curr[0] == prev[0]:
            for i in xrange(min(curr[1], prev[1]), max(curr[1], prev[1])):
                if Sandbox[curr[0]][i] > 0 and Sandbox[curr[0]][i] != Id:
                    return True
                #if Sandbox[vert[0]-1][i] == Id and Sandbox[vert[0]+1][i] == Id:
                #    return True
        if curr[1] == prev[1]:
            for i in xrange(min(curr[0], prev[0]), max(curr[0], prev[0])):
                if Sandbox[i][curr[1]] > 0 and Sandbox[i][curr[1]] != Id:
                    return True
                #if Sandbox[i][vert[1]-1] == Id and Sandbox[i][vert[1]+1] == Id:
                #    return True

        return False

    # it's a backup for the original CollisionWIthLightRibbonInSandbox function
    def CollisionWithLightRibbonInSandbox2(self, Id, Sandbox):
        '''
        Check each point of the sandbox if we have a collision.
        '''

        vert = self._LightRibbon[-1]
        prev = self._LightRibbon[-2] if len(self._LightRibbon) > 1 else self._lightRibbon[-1]
        if vert[0] == prev[0]:
            for i in xrange(min(vert[1], prev[1]), max(vert[1], prev[1])+1):
                if Sandbox[vert[0]][i] > 0 and Sandbox[vert[0]][i] != Id:
                    return True
                if Sandbox[vert[0]-1][i] == Id and Sandbox[vert[0]+1][i] == Id:
                    return True
        if vert[1] == prev[1]:
            for i in xrange(min(vert[0], prev[0]), max(vert[0], prev[0])+1):
                if Sandbox[i][vert[1]] > 0 and Sandbox[i][vert[1]] != Id:
                    return True
                if Sandbox[i][vert[1]-1] == Id and Sandbox[i][vert[1]+1] == Id:
                    return True

        return False

    
    def CollisionWithWall(self, PosX, PosY):
        '''
        Check all possible wall collision combinations.
        '''
        
        # First find the current position.
        currentPosition = self._LightRibbon[-1]
        
        return ((currentPosition[0] < 1 or currentPosition[0] >= PosX)
                or (currentPosition[1] < 1 or currentPosition[1] >= PosY)
                or (self._LightRibbon.count(currentPosition) > 1))
    
    def LightRibbon(self):
        '''
        Return all vertices of the light ribbon.
        '''
        
        return self._LightRibbon[:]
    
    def Move(self):
        '''
        Move the light cycle one unit in its current direction.
        '''
        
        # First find the current position.
        currentPosition = self._LightRibbon[-1]
        #if not self.DirectionChanged and not len(self._LightRibbon) == 1:
            #del self._LightRibbon[-1]

        # Determine which direction to move.
        if self.Direction == Heading.NORTH:
            self._LightRibbon.append((currentPosition[0], currentPosition[1] - self._Speed))
        elif self.Direction == Heading.EAST:
            self._LightRibbon.append((currentPosition[0] + self._Speed, currentPosition[1]))
        elif self.Direction == Heading.SOUTH:
            self._LightRibbon.append((currentPosition[0], currentPosition[1] + self._Speed))
        else:
            self._LightRibbon.append((currentPosition[0] - self._Speed, currentPosition[1]))

        self.DirectionChanged = False
        
        # Return the light ribbon.
        return self._LightRibbon
    
    def SetSpeed(self, NewSpeed):
        self._Speed = NewSpeed
