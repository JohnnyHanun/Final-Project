import copy
import math
import sys
import pygame
from constants import *
from BinarySearchTree import *
import pygame_gui
import pygame_menu
import pygame_menu

sys.setrecursionlimit(10000)
theme = pygame_menu.Theme(
    background_color=(192, 192, 192),
    cursor_color=(255, 255, 255),
    cursor_selection_color=(80, 80, 80, 120),
    scrollbar_color=(39, 41, 42),
    scrollbar_slider_color=(65, 66, 67),
    scrollbar_slider_hover_color=(90, 89, 88),
    selection_color=(255, 255, 255),
    title_background_color=(47, 48, 51),
    title_font_color=(215, 215, 215),
    widget_font_color=(200, 200, 200),
    widget_selection_effect=pygame_menu.widgets.NoneSelection()
)


class Heap:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.size = 0
        self.Heap = [0] * (self.maxsize + 1)
        self.Heap[0] = -1 * sys.maxsize
        self.FRONT = 1
        self.min = True

    # Function to return the position of
    # parent for the node currently
    # at pos
    def parent(self, pos):
        return pos // 2

    # Function to return the position of
    # the left child for the node currently
    # at pos
    def left_child(self, pos):
        return 2 * pos

    # Function to return the position of
    # the right child for the node currently
    # at pos
    def right_child(self, pos):
        return (2 * pos) + 1

    def is_leaf(self, pos):
        return pos * 2 > self.size

    def swap(self, fpos, spos):
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]

    def min_heapify(self, pos):
        if not self.is_leaf(pos):
            if (self.Heap[pos] > self.Heap[self.left_child(pos)] or
                    self.Heap[pos] > self.Heap[self.right_child(pos)]):

                # Swap with the left child and heapify
                # the left child
                if self.Heap[self.left_child(pos)] < self.Heap[self.right_child(pos)]:
                    self.swap(pos, self.left_child(pos))
                    self.min_heapify(self.left_child(pos))

                # Swap with the right child and heapify
                # the right child
                else:
                    self.swap(pos, self.right_child(pos))
                    self.min_heapify(self.right_child(pos))

    def max_heapify(self, pos):

        # If the node is a non-leaf node and greater
        # than any of its child
        if not self.is_leaf(pos):
            if (self.Heap[pos] < self.Heap[self.left_child(pos)] or
                    self.Heap[pos] < self.Heap[self.right_child(pos)]):

                # Swap with the left child and heapify
                # the left child
                if self.Heap[self.left_child(pos)] > self.Heap[self.right_child(pos)]:
                    self.swap(pos, self.left_child(pos))
                    self.max_heapify(self.left_child(pos))

                # Swap with the right child and heapify
                # the right child
                else:
                    self.swap(pos, self.right_child(pos))
                    self.max_heapify(self.right_child(pos))

    # Function to insert a node into the heap
    def insert(self, element):
        if self.size >= self.maxsize:
            return
        self.size += 1
        self.Heap[self.size] = element

        current = self.size
        if self.min:
            while self.Heap[current] < self.Heap[self.parent(current)]:
                self.swap(current, self.parent(current))
                current = self.parent(current)
        else:
            while self.Heap[current] > self.Heap[self.parent(current)]:
                self.swap(current, self.parent(current))
                current = self.parent(current)


    # Function to print the contents of the heap
    def Print(self):
        for i in range(1, (self.size // 2) + 1):
            print(" PARENT : " + str(self.Heap[i]) + " LEFT CHILD : " +
                  str(self.Heap[2 * i]) + " RIGHT CHILD : " +
                  str(self.Heap[2 * i + 1]))

    # Function to build the min heap using
    # the minHeapify function
    def minHeap(self):

        for pos in range(self.size // 2, 0, -1):
            self.min_heapify(pos)

    def max_heap(self):

        for pos in range(self.size // 2, 0, -1):
            self.max_heapify(pos)
    # Function to remove and return the minimum
    # element from the heap
    def remove(self):
        if self.min:
            popped = self.Heap[self.FRONT]
            self.Heap[self.FRONT] = self.Heap[self.size]
            self.size -= 1
            self.min_heapify(self.FRONT)
            return popped
        else:
            popped = self.Heap[self.FRONT]
            self.Heap[self.FRONT] = self.Heap[self.size]
            self.size -= 1
            self.max_heapify(self.FRONT)
            return popped


class HeapVisualizer:
    def __init__(self, main_menu):
        pygame.init()
        pygame.display.set_caption('Heap Visualizer')
        self.main_menu = main_menu
        self.window_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        self.all_nodes = pygame.sprite.Group()
        self.all_edges = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.root = None
        self.heap = Heap(100)
        self.all_values: dict[int, BSTNode] = {}
        self.is_MIN = True
        self.animation_speed = 150
        self.__setup_menu()

    def __add(self):
        pass

    def __delete_node(self):
        pass

    def __set_is_min(self, *args):
        pass

    def __clear_heap(self):
        pass

    def __set_animation_speed(self, *args):
        self.animation_speed = int(args[0] / 100 * 1000)
        text_input: pygame_menu.widgets.widget.label.Label = self.menu.get_widget('speed_label')
        text_input.set_title('Animation Speed: ' + str(self.animation_speed))

    def __setup_menu(self):

        def button_onmouseover(w: 'pygame_menu.widgets.Widget', _) -> None:
            """
            Set the background color of buttons if entered.
            """
            if w.get_id() == 'delete' or w.get_id() == 'ClearTree':
                w.set_background_color((255, 102, 102))
            elif w.get_id() == 'Traversal':
                # w.set_background_color((204, 229, 255))
                w.set_background_color((25, 155, 255))
            else:
                w.set_background_color((153, 255, 153))

        def button_onmouseleave(w: 'pygame_menu.widgets.Widget', _) -> None:
            """
            Set the background color of buttons if leaved.
            """
            if w.get_id() == 'delete' or w.get_id() == 'ClearTree':
                w.set_background_color(RED)
            elif w.get_id() == 'Traversal':
                w.set_background_color(SPECIAL_BLUE)
            else:
                w.set_background_color((0, 204, 0))

        self.menu = pygame_menu.Menu("Heap Menu", 300, 847, theme=theme, position=(100, 0))
        self.menu.add.vertical_fill()
        btn4 = self.menu.add.text_input(
            '',
            maxwidth=10,
            textinput_id='text_input',
            input_underline='_',
            repeat_keys=False,
            font_color=WHITE_COLOR,
            repeat_keys_interval_ms=1000)
        btn4.translate(0, 25 + 50)
        btn = self.menu.add.button("   Add   ", self.__add, border_color=ORANGE, font_color=BLACK_COLOR,
                                   font_size=30,
                                   button_id='add',
                                   background_color=(0, 204, 0), cursor=pygame_menu.locals.CURSOR_HAND)
        btn.set_onmouseover(button_onmouseover)
        btn.set_onmouseleave(button_onmouseleave)
        btn1 = self.menu.add.button("Remove", self.__delete_node, border_color=WHITE_COLOR, font_color=BLACK_COLOR,
                                    font_size=30,
                                    button_id='delete',
                                    background_color=RED, cursor=pygame_menu.locals.CURSOR_HAND)
        btn1.set_onmouseover(button_onmouseover)
        btn1.set_onmouseleave(button_onmouseleave)
        btn.translate(-65, 49 + 50)
        btn1.translate(70, 0 + 50)

        btn4 = self.menu.add.button("Clear Heap", self.__clear_heap, border_color=WHITE_COLOR,
                                    font_color=BLACK_COLOR,
                                    font_size=30,
                                    button_id='ClearTree',
                                    background_color=RED, cursor=pygame_menu.locals.CURSOR_HAND)
        btn4.set_onmouseover(button_onmouseover)
        btn4.set_onmouseleave(button_onmouseleave)
        btn4.translate(0, 60 + 50)

        btn5 = self.menu.add.toggle_switch("MIN?", self.is_MIN, font_size=30, font_color=BLACK_COLOR,
                                           toggleswitch_id='MIN',
                                           onchange=self.__set_is_min, width=100)
        btn5.translate(-8, -440)
        btn6 = self.menu.add.range_slider('', 15, (0, 200), 1,
                                          font_color=BLACK_COLOR,
                                          background_color=WHITE_COLOR,
                                          width=200,
                                          range_text_value_color=BLACK_COLOR,
                                          font_size=25,
                                          padding=10,
                                          rangeslider_id='range_slider',
                                          value_format=lambda x: str(int(x)))

        btn6.set_onchange(self.__set_animation_speed)
        btn7 = self.menu.add.label('Animation Speed: ' + str(self.animation_speed),
                                   font_size=20, font_color=BLACK_COLOR, label_id='speed_label')
        btn6.translate(0, -400)
        btn7.translate(0, -405)

    def __refresh_screen(self, events):
        self.menu.update(events)
        self.window_surface.fill(BLACK_COLOR)
        self.menu.draw(self.window_surface)
        self.all_nodes.draw(self.window_surface)
        self.all_edges.draw(self.window_surface)
        pygame.display.update()

    def run(self):
        while True:
            time_delta = self.clock.tick(60) / 1000.0
            events = pygame.event.get()
            keyboard = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu.enable()
                        return
                if event.type == pygame.KEYDOWN and keyboard[pygame.K_RETURN] or event.__dict__.get('key') and \
                        event.__dict__['key'] == RIGHT_ENTER_KEY:
                    self.menu.get_widget('add').apply()
                if event.type == pygame.KEYDOWN and keyboard[pygame.K_DELETE]:
                    self.menu.get_widget('delete').apply()
            self.__refresh_screen(events)
