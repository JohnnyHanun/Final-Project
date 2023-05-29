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


class HeapNode(BSTNode):
    def __init__(self, center: tuple[int, int], value: int):
        super(HeapNode, self).__init__(center, value)


class Heap:
    def __init__(self, maxsize, is_min=True):
        self.min = None
        self.FRONT = None
        self.Copy_Heap = None
        self.Heap = None
        self.size = None
        self.maxsize = None
        self.initalize_heap(maxsize, is_min)

    def initalize_heap(self, maxsize, is_min):
        self.maxsize = maxsize
        self.size = 0
        self.Heap = [None] * (self.maxsize + 1)
        self.Copy_Heap = None
        self.Heap[0] = -1 * sys.maxsize
        self.FRONT = 1
        self.min = is_min
        self.Heap[0] = -1 * sys.maxsize if is_min else sys.maxsize

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

    def swap_heaps_for_algorithm(self):
        self.Copy_Heap, self.Heap = self.Heap, self.Copy_Heap

    # Function to insert a node into the heap
    def insert(self, element):
        if self.size >= self.maxsize:
            return
        self.size += 1
        self.Heap[self.size] = element

        current = self.size
        sift = []
        self.Copy_Heap = copy.deepcopy(self.Heap)
        if self.min:
            while self.Heap[current] < self.Heap[self.parent(current)]:
                sift.append((self.Heap[current], self.Heap[self.parent(current)]))
                self.swap(current, self.parent(current))
                current = self.parent(current)
        else:
            while self.Heap[current] > self.Heap[self.parent(current)]:
                sift.append((self.Heap[current], self.Heap[self.parent(current)]))
                self.swap(current, self.parent(current))
                current = self.parent(current)
        return sift

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
            self.Heap[self.size + 1] = None
            return popped
        else:
            popped = self.Heap[self.FRONT]
            self.Heap[self.FRONT] = self.Heap[self.size]
            self.size -= 1
            self.max_heapify(self.FRONT)
            self.Heap[self.size + 1] = None
            return popped

    def find_pos(self, value):
        for i in range(1, self.size):
            if self.Heap[i] == value:
                return i
        return -1


class HeapVisualizer:
    def __init__(self, main_menu):
        self.num_of_elements = 0
        pygame.init()
        pygame.display.set_caption('Heap Visualizer')
        self.main_menu = main_menu
        self.window_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        self.all_nodes = pygame.sprite.Group()
        self.all_edges = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.root = None
        self.heap = Heap(100)
        self.all_values: set[int] = set()
        self.is_MIN = True
        self.animation_speed = 1850
        self.__error_message = None
        self.__setup_menu()


    def __deleteTree(self, root: HeapNode):
        if root:
            self.__deleteTree(root.left)
            self.__deleteTree(root.right)
            self.all_nodes.remove(root)
            del root

    def __fix_position(self, root: BSTNode, move: int):
        if root is None:
            return
        X, Y = root.center
        X += move
        Y += NODE_R
        root.center = (X, Y)
        self.__fix_position(root.left, move)
        self.__fix_position(root.right, move)

    def __diff_parent(self, root: BSTNode):
        if root is None:
            return
        if root.parent is None:
            return
        parent: BSTNode = root.parent
        if parent.is_right_son != root.is_right_son:
            return parent
        return self.__diff_parent(parent)

    def __calc_position(self, mouse_pos: tuple[int, int], center: tuple[int, int], angle_to_add: float = 0):
        theta = math.atan2(mouse_pos[1] - center[1], mouse_pos[0] - center[0]) + angle_to_add
        radius = NODE_R
        centerX = center[0]
        centerY = center[1]
        centerX = centerX + (radius * math.cos(theta))
        centerY = centerY + (radius * math.sin(theta))
        start = pygame.Vector2((centerX, centerY))
        end = pygame.Vector2(mouse_pos)
        return start, end

    def __draw_new_edges(self, root: BSTNode):
        if root is None:
            return
        if root.parent is not None and root in self.all_nodes and root.draw:
            start, _ = self.__calc_position(root.center, root.parent.center)
            end, _ = self.__calc_position(root.parent.center, root.center)
            e = Edge(root.parent, root, start_point=start, end_point=end, is_weighted=False,
                     is_directed=True)
            self.all_edges.add(e)
        self.__draw_new_edges(root.left)
        self.__draw_new_edges(root.right)

    def __draw_new_nodes(self, root: BSTNode):
        if root is None:
            return
        root.clicked_off()
        X, Y = root.center
        self.all_nodes.add(root)
        if not (self.menu.get_position()[0] - NODE_R > X > 0 + NODE_R and Y < SCREEN_SIZE[
            1]):  # or root.parent is not None and not root.parent.draw:
            root.hide_node()
        self.__draw_new_nodes(root.left)
        self.__draw_new_nodes(root.right)

    def __stabling_heap(self, diff_parent):
        while diff_parent:
            if diff_parent is not None and diff_parent != self.root:
                if diff_parent.is_right_son == 1:
                    self.__fix_position(diff_parent, 2 * -NODE_R)
                else:
                    self.__fix_position(diff_parent, 2 * NODE_R)
            diff_parent = self.__diff_parent(diff_parent)

    def __heap_tree_creator(self):
        heap_order = self.__get_heap_order(self.heap.FRONT, [], "")
        nodes = []
        for (_, val, _, _) in heap_order:
            heap_node = HeapNode(MID_POS_TREE, val)
            nodes.append(heap_node)
            # self.all_nodes.add(heap_node)

        for (index, (heap_index, val, parent, left_or_right)) in enumerate(heap_order):
            if index == 0:
                continue
            node: HeapNode = nodes[nodes.index(val)]
            node_parent: HeapNode = nodes[nodes.index(parent)]
            node.parent = node_parent
            node.is_right_son = 2 if left_or_right == 'right' else 1
            if node.is_right_son == 1:
                X = node_parent.center[0] - 2 * NODE_R
                Y = node_parent.center[1] + 2 * NODE_R
                node.center = (X, Y)
                node_parent.left = node
            else:
                X = node_parent.center[0] + 2 * NODE_R
                Y = node_parent.center[1] + 2 * NODE_R
                node.center = (X, Y)
                node_parent.right = node
        return nodes

    def __perform_heap_animation(self, sift):
        self.heap.swap_heaps_for_algorithm()
        nodes = self.__heap_tree_creator()
        self.root = nodes[0]
        for index, node in enumerate(nodes):
            if index == 0:
                continue
            self.__stabling_heap(self.__diff_parent(node))
        self.all_nodes = pygame.sprite.Group()
        self.__draw_new_nodes(self.root)
        self.all_edges.empty()
        self.__draw_new_edges(self.root)
        self.__refresh_screen(pygame.event.get())

        def get_nodes(val1, val2):
            node1, node2 = None, None
            for node in self.all_nodes:
                if node == val1:
                    node1 = node
                if node == val2:
                    node2 = node
            return node1, node2

        for val1, val2 in sift:
            node1, node2 = get_nodes(val1, val2)
            node1.paint_node(SPECIAL_BLUE)
            node2.paint_node(ORANGE)
            self.__refresh_screen(pygame.event.get())
            pygame.time.delay(self.animation_speed)
            node1.center, node2.center = node2.center, node1.center
            node1.rect = node1.surf.get_rect(center=node1.center)
            node2.rect = node2.surf.get_rect(center=node2.center)
            self.__refresh_screen(pygame.event.get())
            pygame.time.delay(self.animation_speed)
            node1.clicked_off()
            node2.clicked_off()
        self.heap.swap_heaps_for_algorithm()
    def __add_helper(self,value : int):
        if value > 9999 or value < -9999:
            return

        if value in self.all_values:
            return
        self.__deleteTree(self.root)
        sift = self.heap.insert(value)
        if sift:
            self.__perform_heap_animation(sift)
        self.all_values.add(value)
        self.num_of_elements += 1
        nodes = self.__heap_tree_creator()
        self.root = nodes[0]
        for index, node in enumerate(nodes):
            if index == 0:
                continue
            self.__stabling_heap(self.__diff_parent(node))
        self.all_nodes = pygame.sprite.Group()
        self.__draw_new_nodes(self.root)
        self.all_edges.empty()
        self.__draw_new_edges(self.root)
    def __add(self):
        text_input: pygame_menu.widgets.widget.textinput.TextInput = self.menu.get_widget('text_input')
        value = text_input.get_value()
        try:
            value = eval(value) if value else ""
            if isinstance(value,list) and all(isinstance(i,int) for i in value):
                for val in value:
                    self.__add_helper(val)
            if not isinstance(value,int):
                raise ValueError("Gonen")
        except Exception:
            text_input.clear()
            return
        text_input.clear()
        self.__add_helper(value)

        def get_path_insertion(root, lst):
            if root.parent is None:
                return lst
            lst.append(root.parent)
            return get_path_insertion(root.parent, lst)

    def __get_heap_order(self, index, lst, son_of):
        if self.heap.Heap[index] is None:
            return lst
        lst.append((index, self.heap.Heap[index], self.heap.Heap[self.heap.parent(index)], son_of))
        self.__get_heap_order(self.heap.right_child(index), lst, "right")
        self.__get_heap_order(self.heap.left_child(index), lst, "left")
        return lst

    def __delete_node(self):
        if self.num_of_elements == 0:
            self.__error_message.enable()
            self.__error_message.set_title("The Heap is Empty")
            while self.__error_message.is_enabled():
                self.__error_message.mainloop(self.window_surface, disable_loop=False)
        if self.num_of_elements > 0:
            top = self.heap.remove()
            self.all_values.remove(top)
            self.num_of_elements -= 1
            self.root.paint_node(RED)
            self.__refresh_screen(pygame.event.get())
        if self.num_of_elements == 0:
            self.heap.initalize_heap(100, self.heap.min)
        else:
            self.__deleteTree(self.root)
        nodes = self.__heap_tree_creator()
        self.root = None if not nodes else nodes[0]
        for index, node in enumerate(nodes):
            if index == 0:
                continue
            self.__stabling_heap(self.__diff_parent(node))
        self.all_nodes = pygame.sprite.Group()
        self.__draw_new_nodes(self.root)
        self.all_edges.empty()
        self.__draw_new_edges(self.root)
        pygame.time.delay(self.animation_speed)

    def __set_is_min(self, *args):
        self.is_MIN = args[0]
        if self.is_MIN:
            self.menu.get_widget('delete').set_title('Pop Min')
        else:
            self.menu.get_widget('delete').set_title('Pop Max')
        self.__clear_heap()

    def __clear_heap(self):
        self.heap = Heap(100,is_min=self.is_MIN)
        self.num_of_elements = 0
        self.all_values = set()
        self.__deleteTree(self.root)
        self.all_nodes.empty()
        self.all_edges.empty()

    def __set_animation_speed(self, *args):
        self.animation_speed = 2000 - int(args[0] / 100 * 1000)
        text_input: pygame_menu.widgets.widget.label.Label = self.menu.get_widget('speed_label')
        text_input.set_title('Animation Speed: ' + str(2000 - self.animation_speed))

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
        btn1 = self.menu.add.button("Pop Min", self.__delete_node, border_color=WHITE_COLOR, font_color=BLACK_COLOR,
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
        btn7 = self.menu.add.label('Animation Speed: ' + str(2000 - self.animation_speed),
                                   font_size=20, font_color=BLACK_COLOR, label_id='speed_label')
        btn6.translate(0, -400)
        btn7.translate(0, -405)
        self.__error_message = pygame_menu.Menu('', 450, 200, theme=theme,
                                          mouse_motion_selection=True, center_content=False)
        self.__error_message.add.label('', font_size=25, font_color=BLACK_COLOR,label_id='traversal_shower')

        def error():
            self.__error_message.disable()
            self.menu.enable()

        go_back = self.__error_message.add.button('OK', error, border_color=ORANGE, font_color=BLACK_COLOR,
                                            font_size=30,
                                            button_id='ok',
                                            background_color=(0, 204, 0), cursor=pygame_menu.locals.CURSOR_HAND)
        go_back.set_onmouseover(button_onmouseover)
        go_back.set_onmouseleave(button_onmouseleave)


    def __refresh_screen(self, events):
        self.menu.update(events)
        self.window_surface.fill(BLACK_COLOR)
        self.menu.draw(self.window_surface)
        self.all_nodes.draw(self.window_surface)
        self.all_edges.draw(self.window_surface)
        pygame.display.update()

    def run(self):
        pygame.init()
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
