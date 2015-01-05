
from math import sqrt, fabs
from world.Heading import Heading
import random
import numpy
from sys import maxsize

class Human():
    def __init__(self):
        pass

    def get_name(self):
        return 'Human'



# add your AI implementation class below
class AI1():
    def __init__(self):
        pass

    def get_name(self):
        return 'AI - Tian Zhang'

    # given the grid height, width, all opponents ribbons and self,
    # make decision now
    def react(self, me, opponentshead, sandbox):
        pos = me.LightRibbon()[-1]

        minDists = { 'E'  : 0,
                     'W'  : 0,
                     'S'  : 0,
                     'N'  : 0 }

        for i in xrange(pos[0]+1, sandbox.shape[0]):
            if sandbox[i][pos[1]] > 0:
                break
            minDists['E'] += 1
        for i in xrange(pos[0]-1, 0, -1):
            if sandbox[i][pos[1]] > 0:
                break
            minDists['W'] += 1
        for i in xrange(pos[1]+1, sandbox.shape[1]):
            if sandbox[pos[0]][i] > 0:
                break
            minDists['S'] += 1
        for i in xrange(pos[1]-1, 0, -1):
            if sandbox[pos[0]][i] > 0:
                break
            minDists['N'] += 1

        if me.Direction == Heading.EAST:
            if minDists['E'] <= me._Speed*2:
                me.ChangeDirection(Heading.NORTH if minDists['N']>minDists['S'] else Heading.SOUTH);
        elif me.Direction == Heading.WEST:
            if minDists['W'] <= me._Speed*2:
                me.ChangeDirection(Heading.NORTH if minDists['N']>minDists['S'] else Heading.SOUTH);
        elif me.Direction == Heading.SOUTH:
            if minDists['S'] <= me._Speed*2:
                me.ChangeDirection(Heading.EAST if minDists['E']>minDists['W'] else Heading.WEST);
        elif me.Direction == Heading.NORTH:
            if minDists['N'] <= me._Speed*2:
                me.ChangeDirection(Heading.EAST if minDists['E']>minDists['W'] else Heading.WEST);




class AI2():
    # A wall-hugger AI: try to move close to the most closest two walls but not too close to hit the wall

    def __init__(self):
        pass

    def get_name(self):
        return 'AI - Zijiao Chen'

    # given the grid height, width, all opponents ribbons and self,
    # make decision now
    def react(self, me, opponentshead, sandbox):
        pos = me.LightRibbon()[-1]

        minDists = { 'E'  : 0,
                     'W'  : 0,
                     'S'  : 0,
                     'N'  : 0 }

        for i in xrange(pos[0]+1, sandbox.shape[0]):
            if sandbox[i][pos[1]] > 0:
                break
            minDists['E'] += 1
        for i in xrange(pos[0]-1, 0, -1):
            if sandbox[i][pos[1]] > 0:
                break
            minDists['W'] += 1



        for i in xrange(pos[1]+1, sandbox.shape[1]):
            if sandbox[pos[0]][i] > 0:
                break
            minDists['S'] += 1
        for i in xrange(pos[1]-1, 0, -1):
            if sandbox[pos[0]][i] > 0:
                break
            minDists['N'] += 1

        inverse_dir = { Heading.EAST: 'W', 
                        Heading.NORTH: 'S', 
                        Heading.SOUTH: 'N', 
                        Heading.WEST: 'E' }

         # inverse the key-value pair in minDists
        minDists_inv = {val: key for key, val in minDists.items()} 
        possible_dir = {}
        for key in minDists_inv: 
         # remove the 1 impossible direction; avoid walls that are too close
            if key >= 1 * me._Speed and minDists_inv[key] != inverse_dir[me.Direction]:
                # key >= 1 can be replaced by key > 1, resulting in a slightly different behavior
                possible_dir[key] = minDists_inv[key]

        convert_dict = {'W': Heading.WEST, 
                        'S': Heading.SOUTH, 
                        'N': Heading.NORTH, 
                        'E': Heading.EAST}
                        
        if len(possible_dir) == 0:
            pass  # hopeless, wait for death
        else:
            me.ChangeDirection(convert_dict[possible_dir[min(possible_dir)]])


class AI3():
    # A open-space seeker trying to move towards to most open space


    def __init__(self):
        pass

    def get_name(self):
        return 'AI - OpenSpace-Seeker by Zijiao Chen'

    # given the grid height, width, all opponents ribbons and self,
    # make decision now
    def react(self, me, sandbox):
        pos = me.LightRibbon()[-1]

        minDists = { 'E'  : 0,
                     'W'  : 0,
                     'S'  : 0,
                     'N'  : 0 }

        for i in xrange(pos[0]+1, sandbox.shape[0]):
            if sandbox[i][pos[1]] > 0:
                break
            minDists['E'] += 1
        for i in xrange(pos[0]-1, 0, -1):
            if sandbox[i][pos[1]] > 0:
                break
            minDists['W'] += 1
        for i in xrange(pos[1]+1, sandbox.shape[1]):
            if sandbox[pos[0]][i] > 0:
                break
            minDists['S'] += 1
        for i in xrange(pos[1]-1, 0, -1):
            if sandbox[pos[0]][i] > 0:
                break
            minDists['N'] += 1

        # cannot make a 180 degree turn
        inverse_dir = {Heading.EAST: 'W',
                       Heading.NORTH: 'S',
                       Heading.SOUTH: 'N',
                       Heading.WEST: 'E'}

        minDists_inv = {val: key for key, val in minDists.items()}  # inverse the key-value pair in minDists

        possible_dir = {}

        for key in minDists_inv:  # remove the 1 impossible direction; avoid walls that are too close
            if key > 1 * me._Speed and minDists_inv[key] != inverse_dir[me.Direction]:
                possible_dir[key] = minDists_inv[key]

        # 

        convert_dict = {'W': Heading.WEST,
                        'S': Heading.SOUTH,
                        'N': Heading.NORTH,
                        'E': Heading.EAST}

        if len(possible_dir) == 0:
            pass  # hopeless, wait for death
        else:
            me.ChangeDirection(convert_dict[possible_dir[max(possible_dir)]])


class Elapsed(Exception):
        pass
class AI4():
    '''
    Using minmax method to implement this AI
    '''
    SEPARATED = False
    START_TIME = None
    infinity = maxsize
    NORTH = 11
    EAST = 12
    SOUTH = 13
    WEST = 14
    DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
    MIRROR = {NORTH:SOUTH, EAST:WEST, SOUTH:NORTH, WEST:EAST}
    def __init__(self):
        SEPARATED = False
        START_TIME = None
        infinity = maxsize
        NORTH =11
        EAST =12
        SOUTH =13
        WEST = 14
        DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
        MIRROR = {NORTH:SOUTH, EAST:WEST, SOUTH:NORTH, WEST:EAST}
        pass

    def get_name(self):
        return 'AI - Minimax'
#==================================================

    def moves(self,player=1):
        '''Calculate which moves are safe to make'''
        origin = self.origin(player)
        possible = dict((dir,self.rel(dir,origin)) for dir in DIRECTIONS)
        possible1 = [dir for dir in possible if not (possible[dir]==99)]
        passable = [dir for dir in possible1 if (self._sandbox[possible[dir]]== 0 and possible[dir]!=origin)]
        return passable

    # modified to fix bug in this function that the boundary condition is not fully considered
    def rel(self,direction,origin = None):
        ''' return the position after one step for specific direction'''
        if not origin:
            origin = self.Me()
        x, y = origin
        if (x<self._sandbox.shape[0]) and (y<self._sandbox.shape[1]):
            if direction == NORTH and y+1 < self._sandbox.shape[1]:
                return x, y+1
            elif direction == SOUTH and y-1 >= 0:
                return x, y-1
            elif direction == EAST and x+1 < self._sandbox.shape[0]:
                return x+1, y
            elif direction == WEST and x-1 >= 0:
                return x-1, y
            else:
                return origin
        else:
            return 99
    def adjacent(self,origin):
        ''' return the adjacent tile of this position'''
        #print origin, [self.rel(dir,origin) for dir in DIRECTIONS if (self.rel(dir,origin) != origin)]
        result = [self.rel(dir,origin) for dir in DIRECTIONS if (self.rel(dir,origin) != origin)]
        return [eachresult for eachresult in result if (self._sandbox[eachresult[0]][eachresult[1]] == 0)]

    def Me(self):
        return self._me

    def them(self):
        return self._them

    def origin(self,player=1):
        if player == 1:
            return self.Me()
        else:
            return self.them()

##=======================================================
    def react(self, me, opponentshead, sandbox):
        a = numpy.empty_like (sandbox)
        a[:] = sandbox
        self._sandbox = a
        def move_forth(move,player=1):
            origin = self.origin(player)
            to = self.rel(move,origin)
            self._sandbox[origin] = player
            if player == 1:
                self._sandbox[to] = 1
                self._me = to
            else:
                self._sandbox[to] = 2
                self._them = to

        def move_back(move,player=1):
            origin = self.origin(player)
            to = self.rel(MIRROR[move],origin)
            self._sandbox[origin] = 0
            if player == 1:
                self._sandbox[to] = 1
                self._me = to
            else:
                self._sandbox[to] = 2
                self._them = to

        def Elapsed():
            pass
#===================================================
        def check_elapsed_time():
            t = time.time()
            #print t
            if (t - START_TIME) > 0.09:
                return Elapsed()
        def dis(ori,des):
            ''' return the manhattan distance'''
            a,b = ori
            c,d = des
            return (abs(a-c)+abs(b-d))
#=============================================================
        ''' check if 'st' and 'en' are separated by ribbons, A* '''

        def are_connected(st,en):
            closedset = set()
            openset = [st]
            g_score = {st : 0 }
            h_score = {st : dis(st,en)}
            f_score = {st : h_score[st]}

            def lowestf(x,y):
                if f_score[x] > f_score[y]:
                    return -1
                elif f_score[x] == f_score[y]:
                    return 0
                else: return 1

            def neighbor_nodes(pos):
                for i in self.adjacent(pos):
                    a,b = i
                    if (a<self._sandbox.shape[0]) and (b<self._sandbox.shape[1]):
                        if self._sandbox[i] == 0 :
                            yield i
                    else: continue


            while len(openset) > 0:
                openset.sort(lowestf)
                x = openset.pop()
                if x == en:
                    return True
                closedset.add(x)
                for y in neighbor_nodes(x):
                    if y in closedset: continue
                    tentative_g_score = g_score[x] + 1
                    if y not in openset:
                        openset.append(y)
                        tentative_is_better = True
                    elif tentative_g_score < g_score[y]:
                        tentative_is_better = True
                    else:
                        tentative_is_better = False

                    if tentative_is_better == True:
                        g_score[y] = tentative_g_score
                        h_score[y] = dis(y,en)
                        f_score[y] = g_score[y] + h_score[y]
            return False

        def fill_from(pos,maxi=50):
            '''  return the reachable possition from the 'me' position.
            maxi is the max position it return
            pos = me.LightRibbon()[-1]
            '''
            old = set()
            new = set()
            new.add(pos)
            while len(new)>0 and len(old) < maxi:
                t = new.pop()
                old.add(t)
                for a in self.adjacent(t):
                    x,y = a
                    if (abs(x)<self._sandbox.shape[0]) and (abs(y)<self._sandbox.shape[1]):
                        if (self._sandbox[a] != 0) or (a in old):
                            continue
                        else:
                            new.add(a)
                    else:
                        continue
            return old

        def evaluate(player):
            '''' minimax evaluation function based on free space'''
            me_valid = len(self.moves(1))
            them_valid = len(self.moves(-1))
            players_adjacent = self.them() in self.adjacent(self.Me())

            if (them_valid == 0 or me_valid == 0): ## end game position
                if me_valid > 0:
                    if players_adjacent:
                        result = 11
                    else:
                        result = 100
                elif them_valid > 0:
                    if players_adjacent:
                        result = -11
                    else:
                        result = -100
                else:
                    result = -11
            else: ## Not the end game situiation
                if not are_connected(self.Me(),self.them()):
                    ''' when this AI and it opponent are separated, favor position
                        where this AI have more free space'''
                    mine = fill_from(self.Me())
                    theirs = fill_from(self.them())
                    m = len(mine)
                    t = len(theirs)
                    result = 12+float(abs(m-t))/float(max(m,t))*86
                    if t > m:
                        result = -result
                      ### 12 to 99 positive number means i have more space
                        ### -12 to -99 negative number means opponent has more space
                else:
                    result = 0
            return result*player

        def order_by_closeness(to,moves):
            ''' order the move by closeness to our opponent'''
            x,y = self.Me()
            ox,oy = to
            dx = x-ox
            dy = y-oy
            def order(a,b):
                if dy > 0:
                    if a == SOUTH : return 1
                    if b == SOUTH : return -1
                    if a == NORTH : return -1
                    if b == NORTH : return 1
                if dy <0:
                    if a == SOUTH : return -1
                    if b == SOUTH : return 1
                    if a == NORTH : return 1
                    if b == NORTH : return -1
                if dx >0:
                    if a == EAST : return 1
                    if b == EAST : return -1
                    if a == WEST : return -1
                    if b == WEST : return 1
                if dx <0:
                    if a == EAST : return 1
                    if b == EAST : return -1
                    if a == WEST : return -1
                    if b == WEST : return 1
                return 0
            moves.sort(order)
#================================================
        def alphabeta(depth,alpha,beta,player,best_first_move=None):
            # reasonable moves
            moves = list(self.moves(player))
            print moves

        # if there are no possible moves, evaluate the position
            if (depth == 0) or (len(moves) == 0):
                alpha = evaluate(player)
                return alpha, None

        # order the moves by closeness to the enemy
            order_by_closeness((self._sandbox.shape[0]/2,self._sandbox.shape[1]/2),moves)

            order_by_closeness(self.them(),moves)


        ## if a best_first_move is provided put it first to the list in hope of
        ##getting more alpha-beta cuts
            if best_first_move != None:
                moves.remove(best_first_move)
                moves = [best_first_move] + moves

        ## prepare a default best_move
            best_move = moves[0] if len(moves) > 0 else None
            #print len(moves)
        ##explore each move
            for move in moves:

                move_forth(move,player)
                #print "Hello 1"
                val = -alphabeta(depth-1,-beta,-alpha,-player)[0]
                print val
                move_back(move,player)
                #print "Hello 3"
                #print " "*(10-depth)+"(%d) %d %d"%(player,val,move)
                #check_elapsed_time()
                if val > alpha:
                    best_move = move
                    alpha = val
                    if alpha >= beta:
                        return alpha, best_move

        ### suicide case.......
            val = -11*player
            if val > alpha:
                for d in DIRECTIONS:
                    if self._sandbox[self.rel(d,self.origin(player))] == 1 \
                    or self._sandbox[self.rel(d,self.origin(player))] == 2 :
                        return val, d

            return alpha, best_move

        SEPARATED = False
        #START_TIME = None
        infinity = maxsize
        global NORTH
        global EAST
        global SOUTH
        global WEST
        NORTH =11
        EAST =12
        SOUTH =13
        WEST = 14
        global DIRECTIONS
        DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
        global MIRROR
        MIRROR = {NORTH:SOUTH, EAST:WEST, SOUTH:NORTH, WEST:EAST}
        self._me = me.LightRibbon()[-1]
        self._them = opponentshead[0]
        #self._sandbox = sandbox
        #global START_TIME
        #START_TIME = time.time()
        move = None
        depth = 1
        #try:

        if SEPARATED == False:
            while(depth < 5):
                alpha, move = alphabeta(depth,-infinity,+infinity,1,best_first_move = move)
                #print move
                depth = depth+1
        else:
            pass
            #except Elapsed:

        if move != None:
            #print move
            if move == NORTH:
                me.ChangeDirection(Heading.NORTH)
            elif move == SOUTH:
                me.ChangeDirection(Heading.SOUTH)
            elif move == WEST:
                me.ChangeDirection(Heading.WEST)
            else:
                me.ChangeDirection(Heading.EAST)
        #else:
        #    me.ChangeDirection(Heading.NORTH)



class AI5():
    global NORTH
    global EAST
    global SOUTH
    global WEST
    NORTH =11
    EAST =12
    SOUTH =13
    WEST = 14
    global DIRECTIONS
    DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
    def __init__(self):
        pass

    def get_name(self):
        return 'AI - surround & survive'

    def dis(self,ori,des):
            ''' return the manhattan distance'''
            a,b = ori
            c,d = des
            return (abs(a-c)+abs(b-d))

    # modified to fix bug in this function that the boundary condition is not fully considered
    def rel(self,direction,origin = None):
        ''' return the position after one step for specific direction'''
        if not origin:
            origin = self.Me()
        x, y = origin
        if (abs(x)<self._sandbox.shape[0]) and (abs(y)<self._sandbox.shape[1]):
            if direction == NORTH and abs(y+1) < self._sandbox.shape[1]:
                return x, y+1
            elif direction == SOUTH and abs(y-1) >= 0:
                return x, y-1
            elif direction == EAST and abs(x+1) < self._sandbox.shape[0]:
                return x+1, y
            elif direction == WEST and abs(x-1) >= 0:
                return x-1, y
            else:
                return origin
        else:
            return 99
    def adjacent(self,origin):
        ''' return the adjacent tile of this position'''
        #print origin, [self.rel(dir,origin) for dir in DIRECTIONS if (self.rel(dir,origin) != origin)]
        result = [self.rel(dir,origin) for dir in DIRECTIONS if (self.rel(dir,origin) != origin)]
        return [eachr for eachr in result if (self._sandbox[eachr[0]][eachr[1]] == 0)]

    def Me(self):
        return self._me

    def react(self, me, opponents, sandbox):
        pos = me.LightRibbon()[-1]
        self._sandbox = sandbox
        self._me = me.LightRibbon()[-1]
        self._them = opponents[0]


        def fill_from(pos,maxi=50):
            '''  return the reachable possition from the 'me' position.
            maxi is the max position it return
            pos = me.LightRibbon()[-1]
            '''
            old = set()
            new = set()
            new.add(pos)
            while len(new)>0 and len(old) < maxi:
                t = new.pop()
                old.add(t)
                for a in self.adjacent(t):
                    x,y = a
                    if (abs(x)<self._sandbox.shape[0]) and (abs(y)<self._sandbox.shape[1]):
                        if (self._sandbox[a] > 0) or (a in old):
                            continue
                        else:
                            new.add(a)
                    else:
                        continue
            return len(old)

        toWall = 0
        if me.Direction == Heading.EAST:
            for i in xrange(pos[0]+1, sandbox.shape[0]):
                if sandbox[i][pos[1]] > 0:
                    break
                toWall += 1
        elif me.Direction == Heading.WEST:
            for i in xrange(pos[0]-1, 0, -1):
                if sandbox[i][pos[1]] > 0:
                    break
                toWall += 1
        elif me.Direction == Heading.SOUTH:
            for i in xrange(pos[1]+1, sandbox.shape[1]):
                if sandbox[pos[0]][i] > 0:
                    break
                toWall += 1
        else:
            for i in xrange(pos[1]-1, 0, -1):
                if sandbox[pos[0]][i] > 0:
                    break
                toWall += 1

        distance = self.dis(pos,opponents[0])
        adjnode = self.adjacent(pos)

        #print distance
        if distance > me._Speed*2 and len(adjnode)>0 and toWall > me._Speed:
            disvector = [self.dis(node,opponents[0]) for node in adjnode]
            #print disvector
            #print 'current node:', pos
            #print 'adjacent node: ',adjnode
            loc = numpy.where(disvector==numpy.amin(disvector))
            locx,locy = adjnode[loc[0][0]]
            #print locx, locy
            directionx = locx - pos[0]
            directiony = locy - pos[1]
        elif len(adjnode)>0:
            freeSpace = [fill_from(node,50) for node in adjnode if sandbox[node[0]][node[1]]==0]
            loc = numpy.where(freeSpace==numpy.amax(freeSpace))
            locx,locy = adjnode[loc[0][0]]
            directionx = locx - pos[0]
            directiony = locy - pos[1]
        else:
            directionx, directiony = 0, 0
        #print directionx, directiony
        if me.Direction == Heading.EAST or me.Direction == Heading.WEST:
            if directiony == -1:
                me.ChangeDirection(Heading.NORTH)
            elif directiony == 1:
                me.ChangeDirection(Heading.SOUTH)
        elif me.Direction == Heading.NORTH or me.Direction == Heading.SOUTH:
            if directionx == -1:
                me.ChangeDirection(Heading.WEST)
            elif directionx == 1:
                me.ChangeDirection(Heading.EAST)


class AI6():
    def __init__(self):
        pass
    
    def get_name(self):
        return 'AI - Bo Qu'
    
    # given the grid height, width, all opponents ribbons and self,
    # make decision now
    def react(self, me, opponentshead, sandbox):
        pos = me.LightRibbon()[-1]
        oppo_pos = opponentshead[-1]
        BestDist = 0
        BestDir = 'N'
        
        minDists = { 'E'  : 0,
                     'W'  : 0,
                     'S'  : 0,
                     'N'  : 0 }
        NextStep = { 'E':[pos[0]+1,pos[1]],
                     'W':[pos[0]-1,pos[1]],
                     'S':[pos[0],pos[1]-1],
                     'N':[pos[0],pos[1]+1]
                              }
        
        DIR ={'E':Heading.EAST,
              'W':Heading.WEST,
              'S':Heading.SOUTH,
              'N':Heading.NORTH
            }



        for i in xrange(pos[0]+1, sandbox.shape[0]):
            if sandbox[i][pos[1]] > 0:
                break
            minDists['E'] += 1
        for i in xrange(pos[0]-1, 0, -1):
            if sandbox[i][pos[1]] > 0:
                break
            minDists['W'] += 1



        for i in xrange(pos[1]+1, sandbox.shape[1]):
            if sandbox[pos[0]][i] > 0:
                break
            minDists['S'] += 1
        for i in xrange(pos[1]-1, 0, -1):
            if sandbox[pos[0]][i] > 0:
                break
            minDists['N'] += 1

        REV_DIR ={
                Heading.EAST:'E',
                Heading.WEST:'W',
                Heading.SOUTH:'S',
                Heading.NORTH:'N'
                }
        possible_dir = []

        for i in minDists:
            print i
            print minDists[i]
            if minDists[i] > 1 * me._Speed and i!= REV_DIR[me.Direction]:
                print minDists[i]
                possible_dir.append(i)
#                print possible_dir

#        if minDists[REV_DIR[me.Direction]] <= me._Speed*2:
        if len(possible_dir)==0:
                    print "len = 0"
                    pass
        else:
            for dir in possible_dir:
                dest =NextStep[dir]
                print dest
                distance = (dest[0]- oppo_pos[0])**2+(dest[1]- oppo_pos[1])**2
                        #distance = minDists[dir]
                if distance >= BestDist:
                    BestDist = distance
                    BestDir = dir
            me.ChangeDirection(DIR[BestDir])
