
__all__ = ['main']

import pygame
import pygame_menu
import pygame_gui
from pygame_menu.examples import create_example_window
from Graph import Graph_Simulator
from typing import Optional
from StackVisualizer import StackVisualizer
from BinarySearchTree import BSTVisualizer
from constants import *
import subprocess
import sys
import os
pygame.init()
# infoObject = pygame.display.Info()
# pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
# SCREEN_SIZE = (infoObject.current_w, infoObject.current_h)
# Constants and global variables
FPS = 60
is_weighted_graph = [True]
clock: Optional['pygame.time.Clock'] = None
main_menu: Optional['pygame_menu.Menu'] = None
surface: Optional['pygame.Surface'] = None
if sys.platform == "win32":
    command = r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" ' \
              r'/v "Desktop" '
    result = subprocess.run(command, stdout=subprocess.PIPE, text = True)
    desktop = result.stdout.splitlines()[2].split()[2]
else:
    desktop = os.path.expanduser("~/Desktop")


def get_input(value):
    file_name.insert(0, value)


def weighted_graph(value):
    is_weighted_graph[0] = value


def file_name_init(is_weighted_graph: list, font: 'pygame.font.Font') -> None:
    # Define globals
    global main_menu
    manager = pygame_gui.UIManager((SCREEN_SIZE[0], SCREEN_SIZE[1]))
    rect = pygame.Rect(((SCREEN_SIZE[0] - (SCREEN_SIZE[0] * 0.6)) // 2, (SCREEN_SIZE[1] - (SCREEN_SIZE[1] * 0.6))//2),
                       (SCREEN_SIZE[0] * 0.6, SCREEN_SIZE[1] * 0.6))
    file_dialog = pygame_gui.windows.ui_file_dialog.UIFileDialog(rect=rect, manager=manager, initial_file_path=desktop)
    while True:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu.enable()
                    return
            if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                if event.ui_element == file_dialog:
                    Graph_Simulator(file_name=event.text, menu=main_menu).run()
                    main_menu.disable()
                    main_menu.full_reset()
                    main_menu.enable()
                    return

            if event.type == pygame_gui.UI_WINDOW_CLOSE:
                if event.ui_element == file_dialog:
                    main_menu.disable()
                    main_menu.full_reset()
                    main_menu.enable()
                    return
            manager.process_events(event)
        manager.update(time_delta)
        surface.fill((128, 0, 128))
        manager.draw_ui(surface)
        pygame.display.update()


def directed_graph_init(is_weighted_graph: list, font: 'pygame.font.Font') -> None:
    # Define globals
    global main_menu
    Graph_Simulator(menu=main_menu,is_directed=True, is_weighted=is_weighted_graph[-1]).run()
    main_menu.disable()
    main_menu.full_reset()
    main_menu.enable()


def undirected_graph_init(is_weighted_graph: list, font: 'pygame.font.Font',) -> None:
    # Define globals
    global main_menu
    Graph_Simulator(menu=main_menu, is_directed=False, is_weighted=is_weighted_graph[-1]).run()
    main_menu.disable()
    main_menu.full_reset()
    main_menu.enable()


def stack_init():
    global main_menu
    StackVisualizer(menu=main_menu).run()
    main_menu.disable()
    main_menu.full_reset()
    main_menu.enable()

def BST_init():
    global main_menu
    BSTVisualizer(main_menu=main_menu).run()
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
    surface = create_example_window('DATA STRUCTURES', SCREEN_SIZE)
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus: Graph Menu
    # -------------------------------------------------------------------------
    graph_menu = pygame_menu.Menu(
        height=SCREEN_SIZE[1] * 0.6,
        title='Graph Menu',
        width=SCREEN_SIZE[0] * 0.6
    )

    graph_menu.add.button('Import graph from file', file_name_init,is_weighted_graph,
                          pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))

    graph_menu.add.toggle_switch('Weighted Graph', True, toggleswitch_id='first_switch', onchange=weighted_graph)

    graph_menu.add.button('Directed Graph', directed_graph_init, is_weighted_graph,
                          pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))

    graph_menu.add.button('Undirected Graph', undirected_graph_init, is_weighted_graph,
                          pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))

    graph_menu.add.button('Return to main menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Main
    # -------------------------------------------------------------------------
    main_theme = pygame_menu.themes.THEME_DEFAULT.copy()

    main_menu = pygame_menu.Menu(
        height=SCREEN_SIZE[1] * 0.6,
        theme=main_theme,
        title='Main Menu',
        width=SCREEN_SIZE[0] * 0.6
    )

    main_menu.add.button('Graph', graph_menu)
    main_menu.add.button('Stack', stack_init)
    main_menu.add.button('Binary Search Tree', BST_init)
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


if __name__ == '__main__':
    main()
