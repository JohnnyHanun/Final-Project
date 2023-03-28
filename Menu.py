"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - GAME SELECTOR
Game with 3 difficulty options.
"""

__all__ = ['main']

import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from Graph import Graph_Simulator
from random import randrange
from typing import Tuple, Any, Optional, List
from StackVisualizer import StackVisualizer

# Constants and global variables
ABOUT = [f'pygame-menu {pygame_menu.__version__}',
         f'Author: {pygame_menu.__author__}',
         f'Email: {pygame_menu.__email__}']
DIFFICULTY = ['EASY']
FPS = 60
WINDOW_SIZE = (1024, 900)
is_weighted_graph = [True]
file_name = [r'/Users/gonenselner/Desktop/gonen_graph.txt', r'/Users/gonenselner/Desktop/gonen_graph 2.txt']
# file_name = [r'C:\Users\yoyom\Desktop\gonen_graph.txt', r'C:\Users\yoyom\Desktop\gonen_graph2.txt']
clock: Optional['pygame.time.Clock'] = None
main_menu: Optional['pygame_menu.Menu'] = None
surface: Optional['pygame.Surface'] = None


def get_input(value):
    file_name.insert(0, value)


def weighted_graph(value):
    is_weighted_graph[0] = value


def directed_graph_init(file_name: list, is_weighted_graph: list, font: 'pygame.font.Font', test: bool = False) -> None:
    """
    Main game function.

    :param is_weighted_graph:
    :param file_name:
    :param difficulty: Difficulty of the game
    :param font: Pygame font
    :param test: Test method, if ``True`` only one loop is allowed
    """

    # Define globals
    global main_menu
    global clock
    if len(file_name) == 0:
        Graph_Simulator(menu=main_menu, is_weighted=is_weighted_graph[-1]).run()
    else:
        Graph_Simulator(file_name=file_name[0], menu=main_menu).run()

    main_menu.disable()
    main_menu.full_reset()
    main_menu.enable()


def undirected_graph_init(file_name: list, is_weighted_graph: list, font: 'pygame.font.Font',
                          test: bool = False) -> None:
    """
    Main game function.

    :param is_weighted_graph:
    :param file_name:
    :param difficulty: Difficulty of the game
    :param font: Pygame font
    :param test: Test method, if ``True`` only one loop is allowed
    """

    # Define globals
    global main_menu
    global clock
    if len(file_name) == 0:
        Graph_Simulator(menu=main_menu, is_directed=False, is_weighted=is_weighted_graph[-1]).run()
    else:
        Graph_Simulator(file_name=file_name[1], menu=main_menu, is_directed=False).run()

    main_menu.disable()
    main_menu.full_reset()
    main_menu.enable()

def stack_init():
    global main_menu
    StackVisualizer(menu=main_menu).run()
    main_menu.disable()
    main_menu.full_reset()
    main_menu.enable()


def main_background() -> None:
    """
    Function used by menus, draw on background while menu is active.
    """
    global surface
    surface.fill((128, 0, 128))


def main(test: bool = False) -> None:
    """
    Main program.

    :param test: Indicate function is being tested
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global clock
    global main_menu
    global surface
    global is_weighted_graph
    global file_name

    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    surface = create_example_window('Example - Game Selector', WINDOW_SIZE)
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus: Play Menu
    # -------------------------------------------------------------------------
    graph_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        title='Graph Menu',
        width=WINDOW_SIZE[0] * 0.85
    )

    submenu_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    submenu_theme.widget_font_size = 15
    play_submenu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.5,
        theme=submenu_theme,
        title='Submenu',
        width=WINDOW_SIZE[0] * 0.7
    )
    for i in range(30):
        play_submenu.add.button(f'Back {i}', pygame_menu.events.BACK)
    play_submenu.add.button('Return to main menu', pygame_menu.events.RESET)

    graph_menu.add.text_input('File Path: ', input_type=pygame_menu.locals.INPUT_TEXT,
                              default='', input_underline='_',
                              onchange=get_input)
    graph_menu.add.toggle_switch('Weighted Graph', True, toggleswitch_id='first_switch', onchange=weighted_graph)
    graph_menu.add.button('Directed Graph',  # When pressing return -> play(DIFFICULTY[0], font)
                          directed_graph_init,
                          file_name, is_weighted_graph,
                          pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
    graph_menu.add.button('Undirected Graph',  # When pressing return -> play(DIFFICULTY[0], font)
                          undirected_graph_init,
                          file_name, is_weighted_graph,
                          pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
    graph_menu.add.button('Return to main menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus:About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    about_theme.widget_margin = (0, 0)

    # -------------------------------------------------------------------------
    # Create menus: Main
    # -------------------------------------------------------------------------
    main_theme = pygame_menu.themes.THEME_DEFAULT.copy()

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        theme=main_theme,
        title='Main Menu',
        width=WINDOW_SIZE[0] * 0.6
    )

    main_menu.add.button('Graph', graph_menu)
    main_menu.add.button('Stack', stack_init)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
