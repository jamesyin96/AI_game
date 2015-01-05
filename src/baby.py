#!/usr/bin/python

import sys, pygame, random

from menu.Menu import *
from menu.Image import *
from world.Heading import Heading
from world.Program import Program
from world.GameGrid import GameGrid
from ai.AI import *


BLACK = (0,0,0)
FPS = 10

SCREEN_WIDTH  = 500
SCREEN_HEIGHT = 500
GRID_WIDTH = 50
GRID_HEIGHT = 50


def exit():
    pygame.quit()
    sys.exit()


def main():
    # initialize pygame
    pygame.init()

    # create a window of 500x500 pixels
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # set title of the window
    pygame.display.set_caption("Racing Baby!")

    bg = load_image('bg3.png', 'img')
    screen.blit(bg, (0, 0))
    pygame.display.flip()

    # create the main menu
    mainMenu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                     [(1, 'Start New Game', None, None),
                      (2, 'Options',        None, None),
                      (3, 'Exit',           None, None)])
    # put the menu in the center
    #mainMenu.set_center(True, True)
    mainMenu.set_alignment('center', 'center')
    mainMenu.set_position(SCREEN_WIDTH/3, SCREEN_HEIGHT*5/12)

    optionMenu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                       [(11, 'Player 1', 'Human', None),
                        (12, 'Player 2', 'Human', None),
                        (13, 'Player 3', 'None',  None),
                        (14, 'Player 4', 'None',  None),
                        (15, 'Go Back',  None,    None)])
    # put the menu in the center
    optionMenu.set_center(True, True)

    # register AIs implemented
    ai_available = {}
    # TEAM: PLEASE IMPLEMENT YOUR AI IN AI.py AND REGISTER HERE
    human = Human()
    ai_available[human.get_name()] = human
    ai1 = AI1()
    ai_available[ai1.get_name()] = ai1
    ai2 = AI2()
    ai_available[ai2.get_name()] = ai2
    ai6 = AI6()
    ai_available[ai6.get_name()] = ai6
    ai5 = AI5()
    ai_available[ai5.get_name()] = ai5

    choice_menu_items = [(101, 'None',  None, None)]
    for k in ai_available:
        choice_menu_items.append((choice_menu_items[-1][0]+1, k, None, None))

    choiceMenu = cMenu(50, 50, 20, 5, 'vertical', 100, screen, choice_menu_items)
    # put the menu in the center
    choiceMenu.set_center(True, True)


    # ignore mouse events (greatly reduce resources when unnecessary)
    pygame.event.set_blocked(pygame.MOUSEMOTION)


    state = 0
    prev_state = 1
    rect_list = []
    random.seed()


    # menu stack to serve as the memory of menu states
    menuStack = [ mainMenu ]
    menuStack[-1].refresh()

    # the main loop
    while True:
        # wait the user input
        e = pygame.event.wait()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                screen.blit(bg, (0, 0))
                pygame.display.flip()
                if menuStack[-1].get_current_id() == 1: # start new game
                    players = get_players(optionMenu, ai_available)
                    start_game(players)
                    screen.blit(bg, (0, 0))
                    pygame.display.flip()
                    rect_list = menuStack[-1].update(e, True)
                elif menuStack[-1].get_current_id() == 2: # options
                    menuStack.append(optionMenu)
                    rect_list = menuStack[-1].update(e, True)
                elif menuStack[-1].get_current_id() == 3: # exit game
                    exit()
                elif menuStack[-1].get_current_id() >= 11 and \
                     menuStack[-1].get_current_id() <= 14: # config player 1
                    menuStack.append(choiceMenu)
                    rect_list = menuStack[-1].update(e, True)
                elif menuStack[-1].get_current_id() == 15: # return to main menu
                    menuStack.pop()
                    rect_list = menuStack[-1].update(e, True)
                elif menuStack[-1].get_current_id() >= 101 and \
                     menuStack[-1].get_current_id() <= 106:
                    menuStack.pop()
                    menuStack[-1].set_current_value(choiceMenu.get_current_label())
                    rect_list = menuStack[-1].update(e, True)
            elif e.key == pygame.K_ESCAPE:
                exit()
            else:
                rect_list = menuStack[-1].update(e)
        elif e.type == pygame.QUIT:
            exit()

        # update the screen
        pygame.display.update(rect_list)


def start_game(players):
    '''
    Start game play.
    '''
    
    #
    # Build the game grid.
    #
    
    #gameGrid = GameGrid(20, 20)
    gameGrid = GameGrid(GRID_WIDTH, GRID_HEIGHT)
    gameGrid.SetFrameRate(FPS)
    
    headings = [Heading.EAST, Heading.WEST, Heading.SOUTH, Heading.NORTH ]
    start_pos = [(1,                gameGrid.Height/2 ),
                 (gameGrid.Width-2, gameGrid.Height/2 ),
                 (gameGrid.Width/2,                  1),
                 (gameGrid.Width/2, gameGrid.Height-2)]
    #
    # Create the programs (players).
    #
    for i, AI in enumerate(players):
        avatar = load_image('baby'+`(i+1)`+'.png', 'img')
        player = Program(i+1, avatar)
        player.UseBaton(headings[i], start_pos[i])
        player.UseAI(AI)
        #
        # Load programs in to the game grid.
        #
        gameGrid.LoadProgram(player)
    
    
    #
    # Engine.
    #
    
    while gameGrid.IsRunning():
        gameGrid.DoWork()

    #gameGrid._DumpSandbox()
    # wait for enter to return to main menu
    while True:
        e = pygame.event.wait()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
            break


def get_players(optionMenu, ai_available):
    items = optionMenu.get_menu_items()
    players = []
    for item in items:
       if item['value'] and ai_available.has_key(item['value']):
          players.append(ai_available[item['value']])
    return players




if __name__ == "__main__":
    main()
