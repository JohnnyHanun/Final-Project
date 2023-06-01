import copy
import math
import sys
from Graph import Edge
from Graph import Node
from Utils import Utils
import random
import pygame
from constants import *
import pygame_gui
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


class BSTNode(Node):
    def __init__(self, center: tuple[int, int], value: int, left: Node = None, right: Node = None, parent: Node = None,
                 all_nodes=None):
        self.value = value
        super(BSTNode, self).__init__(center, all_nodes, name=str(value))
        self.height = 1
        self.left: BSTNode = left
        self.right: BSTNode = right
        self.parent: BSTNode = parent
        self.is_right_son = False

    def __lt__(self, other):
        return self.value < other if isinstance(other, int) else self.value < other.value

    def __gt__(self, other):
        return self.value > other if isinstance(other, int) else self.value > other.value

    def __eq__(self, other):
        return self.value == other if isinstance(other, int) else self.value == other.value

    def __deepcopy__(self, memodict):
        return self

    def __hash__(self):
        return hash(self.value)


class BSTVisualizer:
    def __init__(self, main_menu):
        pygame.init()
        pygame.display.set_caption('BST Visualizer')
        self.main_menu = main_menu
        self.window_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        self.all_nodes = pygame.sprite.Group()
        self.all_edges = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.root = None
        self.all_values: dict[int, BSTNode] = {}
        self.is_AVL = True
        self.animation_speed = 150
        self.__error_message = None
        self.__traversal_shower = None
        self.__error_traversal = None
        self.__setup_menu()

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

        self.menu = pygame_menu.Menu("BST Menu", 300, 847, theme=theme, position=(100, 0))
        btn4 = self.menu.add.text_input(
            '',
            maxwidth=10,
            textinput_id='text_input',
            input_underline='_',
            repeat_keys=False,
            font_color=WHITE_COLOR,
            repeat_keys_interval_ms=1000)
        btn4.translate(0, 25 + 50)
        btn = self.menu.add.button("   Add   ", self.__add_node, border_color=ORANGE, font_color=BLACK_COLOR,
                                   font_size=30,
                                   button_id='add',
                                   background_color=(0, 204, 0), cursor=pygame_menu.locals.CURSOR_HAND)
        btn.set_onmouseover(button_onmouseover)
        btn.set_onmouseleave(button_onmouseleave)
        # btn._font_color = (255,255,255)
        btn1 = self.menu.add.button("Delete", self.__delete_node, border_color=WHITE_COLOR, font_color=BLACK_COLOR,
                                    font_size=30,
                                    button_id='delete',
                                    background_color=RED, cursor=pygame_menu.locals.CURSOR_HAND)
        btn1.set_onmouseover(button_onmouseover)
        btn1.set_onmouseleave(button_onmouseleave)
        btn.translate(-65, 49 + 50)
        btn1.translate(70, 0 + 50)

        # print(btn.get_position(), btn1.get_position())

        def onchange_dropselect(*args) -> None:
            print(args[0])

        btn2 = self.menu.add.dropselect(
            title='',
            items=[('Inorder', 0),
                   ('PreOrder', 1),
                   ('PostOrder', 2),
                   ('', 3)],
            dropselect_id='dropselect',
            font_size=16,
            padding=0,
            selection_box_height=5,
            selection_box_inflate=(0, 20),
            selection_box_margin=0,
            selection_box_text_margin=10,
            selection_box_width=250,
            selection_option_font_size=20,
            shadow_width=20
        )
        btn2.translate(0, 25 + 50)
        btn3 = self.menu.add.button("Activate Traversal", self.__traversal_activation, border_color=WHITE_COLOR,
                                    font_color=BLACK_COLOR,
                                    font_size=30,
                                    button_id='Traversal',
                                    background_color=SPECIAL_BLUE, cursor=pygame_menu.locals.CURSOR_HAND)
        btn3.translate(0, 50 + 50)
        btn3.set_onmouseover(button_onmouseover)
        btn3.set_onmouseleave(button_onmouseleave)
        btn4 = self.menu.add.button("Clear Tree", self.__clear_tree, border_color=WHITE_COLOR,
                                    font_color=BLACK_COLOR,
                                    font_size=30,
                                    button_id='ClearTree',
                                    background_color=RED, cursor=pygame_menu.locals.CURSOR_HAND)
        btn4.set_onmouseover(button_onmouseover)
        btn4.set_onmouseleave(button_onmouseleave)
        btn4.translate(0, 60 + 50)

        btn5 = self.menu.add.toggle_switch("AVL Tree?", self.is_AVL, font_size=30, font_color=BLACK_COLOR,
                                           toggleswitch_id='AVL',
                                           onchange=self.__set_is_AVL, width=100)
        btn5.translate(-8, -440)
        btn6 = self.menu.add.range_slider('', 200 - 15, (0, 200), 1,
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
        self.__error_message = pygame_menu.Menu('Error!', 550, 200, theme=theme,
                                                mouse_motion_selection=True, center_content=False)
        self.__error_message.add.label('The Tree Is Empty', font_size=25, font_color=BLACK_COLOR,label_id='error_message')

        self.__traversal_shower = pygame_menu.Menu('', 550, 200, theme=theme,
                                                   mouse_motion_selection=True, center_content=False)
        self.__traversal_shower.add.label('', font_size=25, font_color=BLACK_COLOR, label_id='traversal_shower')
        self.__error_traversal = pygame_menu.Menu('Error!', 550, 200, theme=theme,
                                                  mouse_motion_selection=True, center_content=False)
        self.__error_traversal.add.label('You Must Select An Option', font_size=25, font_color=BLACK_COLOR)

        def error():
            self.__error_message.disable()
            self.menu.enable()

        def traversal_shower_manu():
            self.__traversal_shower.disable()
            self.menu.enable()

        def traversal_shower_error():
            self.__error_traversal.disable()
            self.menu.enable()

        go_back = self.__error_message.add.button('OK', error, border_color=ORANGE, font_color=BLACK_COLOR,
                                                  font_size=30,
                                                  button_id='ok',
                                                  background_color=(0, 204, 0), cursor=pygame_menu.locals.CURSOR_HAND)
        go_back.set_onmouseover(button_onmouseover)
        go_back.set_onmouseleave(button_onmouseleave)

        go_back1 = self.__traversal_shower.add.button('OK', traversal_shower_manu, border_color=ORANGE, font_color=BLACK_COLOR,
                                                      font_size=30,
                                                      button_id='ok',
                                                      background_color=(0, 204, 0),
                                                      cursor=pygame_menu.locals.CURSOR_HAND)
        go_back1.set_onmouseover(button_onmouseover)
        go_back1.set_onmouseleave(button_onmouseleave)

        go_back2 = self.__error_traversal.add.button('OK', traversal_shower_error, border_color=ORANGE, font_color=BLACK_COLOR,
                                                     font_size=30,
                                                     button_id='ok',
                                                     background_color=(0, 204, 0),
                                                     cursor=pygame_menu.locals.CURSOR_HAND)
        go_back2.set_onmouseover(button_onmouseover)
        go_back2.set_onmouseleave(button_onmouseleave)

    def __set_animation_speed(self, *args):

        self.animation_speed = 2000 - int(args[0]) * 10  # int(args[0] / 100 * 1000)
        text_input: pygame_menu.widgets.widget.label.Label = self.menu.get_widget('speed_label')
        text_input.set_title('Animation Speed: ' + str(2000 - self.animation_speed))

    def __set_is_AVL(self, *args):
        self.is_AVL = args[0]
        self.menu.get_widget('ClearTree').apply(False)

    def __clear_tree(self, show_error=True):
        if self.root is None and show_error:
            self.__error_message.enable()
            self.__error_message.get_widget('error_message').set_title('The Tree Is Empty')
            while self.__error_message.is_enabled():
                self.__error_message.mainloop(self.window_surface, disable_loop=False)
            return
        self.all_values = {}
        self.all_nodes.empty()
        self.all_edges.empty()
        self.__deleteTree(self.root)
        self.root = None

    def __move_all_nodes_right(self, root: BSTNode):
        if root is None:
            return
        X, Y = root.center
        X += 3 * NODE_R + 10
        root.center = (X, Y)
        root.clicked_off()
        self.__move_all_nodes_right(root.left)
        self.__move_all_nodes_right(root.right)

    def __move_all_nodes_left(self, root: BSTNode):
        if root is None:
            return
        X, Y = root.center
        X -= 3 * NODE_R - 10
        root.center = (X, Y)
        root.clicked_off()
        self.__move_all_nodes_left(root.left)
        self.__move_all_nodes_left(root.right)

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

    def __getHeight(self, root: BSTNode):
        if not root:
            return 0
        return root.height

    def getBalance(self, root: BSTNode):
        if not root:
            return 0
        return self.__getHeight(root.left) - self.__getHeight(root.right)

    def __rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.__getHeight(z.left),
                           self.__getHeight(z.right))
        y.height = 1 + max(self.__getHeight(y.left),
                           self.__getHeight(y.right))
        return y

    def __leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.__getHeight(z.left),
                           self.__getHeight(z.right))
        y.height = 1 + max(self.__getHeight(y.left),
                           self.__getHeight(y.right))
        return y

    def __delete_node_avl_helper(self, root: BSTNode, value: int, bro: list[BSTNode]):
        # Find the node to be deleted and remove it
        if root is None:
            return root
        elif value < root.value:
            bro.append(copy.deepcopy(root))
            root.left = self.__delete_node_avl_helper(root.left, value, bro)
        elif value > root.value:
            bro.append(root)
            root.right = self.__delete_node_avl_helper(root.right, value, bro)
        else:
            if root.left is None:
                bro.append(copy.deepcopy(root))
                temp = root.right
                return temp
            elif root.right is None:
                bro.append(copy.deepcopy(root))
                temp = root.left
                return temp
            temp = root.right
            while temp.left:
                temp = temp.left
            bro.append(copy.deepcopy(root))
            new_node = BSTNode(root.center, temp.value, root.left, root.right, root.parent)
            new_node.right = self.__delete_node_avl_helper(root.right,
                                                           temp.value, bro)
            del root
            root = new_node

        if root is None:
            return root

        # Update the balance factor of nodes
        root.height = 1 + max(self.__getHeight(root.left),
                              self.__getHeight(root.right))

        balanceFactor = self.getBalance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.__rightRotate(root)
            else:
                root.left = self.__leftRotate(root.left)
                return self.__rightRotate(root)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.__leftRotate(root)
            else:
                root.right = self.__rightRotate(root.right)
                return self.__leftRotate(root)
        return root

    def __add_node_avl_helper(self, root: BSTNode, value: int, parent=None):
        # Find the correct location and insert the node
        if not root:
            X, Y = 0, 0
            new_node = BSTNode((X, Y), value, parent=parent)
            self.all_values[value] = new_node
            self.all_nodes.add(new_node)
            return new_node
        elif value < root.value:
            root.left = self.__add_node_avl_helper(root.left, value, root)
        else:
            root.right = self.__add_node_avl_helper(root.right, value, root)

        root.height = 1 + max(self.__getHeight(root.left),
                              self.__getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor > 1:
            if value < root.left.value:
                return self.__rightRotate(root)
            else:
                root.left = self.__leftRotate(root.left)
                return self.__rightRotate(root)

        if balanceFactor < -1:
            if value > root.right.value:
                return self.__leftRotate(root)
            else:
                root.right = self.__rightRotate(root.right)
                return self.__leftRotate(root)
        return root

    def __add_node_helper(self, node: BSTNode, value: int, bro: list[BSTNode], parent=None, ):
        if node is not None and node.value == value:
            bro.append(node)
            return node
        if node is None:
            right = 0
            if parent is None:
                X, Y = MID_POS_TREE
            else:
                if parent.value > value:
                    ##LEFT##
                    X = parent.center[0] - 2 * NODE_R
                    Y = parent.center[1] + 2 * NODE_R
                    right = 1
                else:
                    ##RIGHT##
                    X = parent.center[0] + 2 * NODE_R
                    Y = parent.center[1] + 2 * NODE_R
                    right = 2
            new_node = BSTNode((X, Y), value, parent=parent)
            new_node.is_right_son = right
            self.all_values[value] = new_node
            self.all_nodes.add(new_node)
            bro.append(new_node)
            return new_node
        if value < node.value:
            bro.append(node)
            node.left = self.__add_node_helper(node.left, value, bro, node)
        else:
            bro.append(node)
            node.right = self.__add_node_helper(node.right, value, bro, node)
        return node

    def __check_collision(self):
        lst: list[BSTNode] = []
        for node1 in self.all_nodes:
            temp_group = pygame.sprite.Group()
            for node2 in self.all_nodes:
                if node1 is node2:
                    continue
                else:
                    temp_group.add(node2)
            collide = pygame.sprite.spritecollideany(node1, temp_group)
            if collide:
                lst.append(collide)
        return lst

    def __check_collision2(self):
        for node1 in self.all_nodes:
            temp_group = pygame.sprite.Group()
            for node2 in self.all_nodes:
                if node1 is node2:
                    continue
                else:
                    temp_group.add(node2)
            collide = pygame.sprite.spritecollideany(node1, temp_group)
            if collide:
                return collide
        return False

    def __is_in_subtree(self, root: BSTNode, node: BSTNode):
        if root is None:
            return False
        if root.value == node:
            return True
        return self.__is_in_subtree(root.left, node) or self.__is_in_subtree(root.right, node)

    def __avoid_collision(self, root: BSTNode):
        self.__move_all_nodes_right(root.right)
        self.__move_all_nodes_left(root.left)
        for edge in self.all_edges:
            # start, _ = self.__calc_position(new_node.center, parent.center)
            # end, _ = self.__calc_position(parent.center, new_node.center)
            start, _ = self.__calc_position(edge.destination.center, edge.source.center)
            end, _ = self.__calc_position(edge.source.center, edge.destination.center)
            edge.start_point = start
            edge.end_point = end
            edge.surf.fill(BLACK_COLOR)
            edge.draw()

    def __add_animation(self, bro: list[BSTNode]):
        last_node: BSTNode = bro.pop(-1)
        if last_node not in self.all_nodes:
            return
        if last_node is self.root:
            return
        sec = self.animation_speed
        edge_last_node: Edge = self.__find_edge(last_node.parent, last_node)
        if last_node.draw:
            self.all_nodes.remove(last_node)
            self.all_edges.remove(edge_last_node)
        self.__refresh_screen(pygame.event.get())
        for node in bro:
            if not node.draw:
                continue
            node.clicked_on(TARGET)
            self.__refresh_screen(pygame.event.get())
            pygame.time.delay(sec)
        if edge_last_node and edge_last_node.draw:
            self.all_edges.add(edge_last_node)
        if last_node.draw:
            last_node.paint_node(TARGET)
        self.__refresh_screen(pygame.event.get())
        pygame.time.delay(sec)
        self.all_nodes.add(last_node)
        self.__refresh_screen(pygame.event.get())
        pygame.time.delay(sec)
        bro.append(last_node)
        for node in bro:
            if not node.draw:
                continue
            node.clicked_off()

    def __find_node(self, root: BSTNode, value: int):
        if root is None:
            return
        if root.value == value:
            return root
        if value < root.value:
            return self.__find_node(root.left, value)
        return self.__find_node(root.right, value)

    def __diff_parent(self, root: BSTNode):
        if root is None:
            return
        if root.parent is None:
            return
        parent: BSTNode = root.parent
        if parent.is_right_son != root.is_right_son:
            return parent
        return self.__diff_parent(parent)

    def __fix_position(self, root: BSTNode, move: int):
        if root is None:
            return
        X, Y = root.center
        X += move
        Y += NODE_R
        root.center = (X, Y)
        self.__fix_position(root.left, move)
        self.__fix_position(root.right, move)

    def __deleteTree(self, root: BSTNode):
        if root:
            self.__deleteTree(root.left)
            self.__deleteTree(root.right)
            self.all_nodes.remove(root)
            del root

    def __fix_heights(self, root: BSTNode):
        if root is None:
            return
        root.height = 1 + max(self.__getHeight(root.left), self.__getHeight(root.right))
        self.__fix_heights(root.left)
        self.__fix_heights(root.right)

    def __fix_positions_avl_tree(self, root: BSTNode):
        if root is None:
            return
        self.root = self.__add_node_helper(self.root, root.value, [])
        self.__fix_parents(self.root)
        Inserted_node: BSTNode = self.__find_node(self.root, root.value)
        diff_parent = self.__diff_parent(Inserted_node)
        while diff_parent:
            if diff_parent is not None and diff_parent is not self.root:
                if diff_parent.is_right_son == 1:
                    self.__fix_position(diff_parent, 2 * -NODE_R)
                else:
                    self.__fix_position(diff_parent, 2 * NODE_R)
            diff_parent = self.__diff_parent(diff_parent)
        self.__fix_positions_avl_tree(root.left)
        self.__fix_positions_avl_tree(root.right)

    def __add_node(self):
        text_input: pygame_menu.widgets.widget.textinput.TextInput = self.menu.get_widget('text_input')
        value = text_input.get_value()
        if len(value) == 0:
            return
        if not text_input.get_value().isnumeric():
            self.__error_message.enable()
            e: pygame_menu.widgets.widget.label.Label = self.__error_message.get_widget('error_message')
            e.set_title('Value must be an integer')
            while self.__error_message.is_enabled():
                self.__error_message.mainloop(self.window_surface, disable_loop=False)
            text_input.clear()
            return
        try:
            value = int(value)
        except ValueError:
            text_input.clear()
            return
        if value > 9999 or value < -9999:
            self.__error_message.enable()
            e: pygame_menu.widgets.widget.label.Label = self.__error_message.get_widget('error_message')
            e.set_title('Value must be between -9999 to 9999')
            while self.__error_message.is_enabled():
                self.__error_message.mainloop(self.window_surface, disable_loop=False)
            text_input.clear()
            return
        text_input.clear()
        if not self.all_values.get(value):
            bro: list[BSTNode] = []
            if not self.is_AVL:
                self.root = self.__add_node_helper(self.root, value, bro)
            else:
                self.root = self.__add_node_avl_helper(self.root, value)
                temp = self.root
                self.root = None
                self.__fix_positions_avl_tree(temp)
                self.__deleteTree(temp)
                self.root = self.__add_node_helper(self.root, value, bro)
                self.__fix_heights(self.root)
            if not self.is_AVL:
                Inserted_node: BSTNode = self.__find_node(self.root, value)
                self.__fix_parents(self.root)
                diff_parent = self.__diff_parent(Inserted_node)
                while diff_parent:
                    if diff_parent is not None and diff_parent is not self.root:
                        if diff_parent.is_right_son == 1:
                            self.__fix_position(diff_parent, 2 * -NODE_R)
                        else:
                            self.__fix_position(diff_parent, 2 * NODE_R)
                    diff_parent = self.__diff_parent(diff_parent)
            self.all_nodes = pygame.sprite.Group()
            self.__draw_new_nodes(self.root)
            self.all_edges.empty()
            self.__draw_new_edges(self.root)
            self.__add_animation(bro)

            # print("*******************")
            # for i in answer:
            #     print(f'{str(i)} = {i.center}')
            # print("*************************")
            # self.__add_animation(bro)
        # for i in [8, 3, 10, 1, 6, 4, 7, 14]:
        #     if not self.all_values.get(i):
        #         self.root = self.__add_node_helper(self.root, i)

    def __swap_node(self, src: BSTNode, dst: BSTNode):
        pass

        ################################
        # don't forget to delete edges #
        ################################

    def __find_edge(self, src: BSTNode, dst: BSTNode):
        if src is None or dst is None:
            return None
        e = None
        for edge in self.all_edges:
            if edge.source == src and edge.destination == dst:
                e = edge
                break
        return e

    def __fix_position_subtree(self, root: BSTNode):
        if root is None:
            return
        if root.parent is not None:
            if root.parent.value > root.value:
                ##LEFT##
                X = root.parent.center[0] - NODE_R
                Y = root.parent.center[1] + NODE_R
            else:
                ##RIGHT##
                X = root.parent.center[0] + NODE_R
                Y = root.parent.center[1] + NODE_R
            root.center = (X, Y)
            root.clicked_off()
            e = self.__find_edge(root.parent, root)
            self.all_edges.remove(e)
            start, _ = self.__calc_position(root.center, root.parent.center)
            end, _ = self.__calc_position(root.parent.center, root.center)
            e = Edge(root.parent, root, start_point=start, end_point=end, is_weighted=False,
                     is_directed=True)
            self.all_edges.add(e)
        self.__fix_position_subtree(root.left)
        self.__fix_position_subtree(root.right)

    def __delete_node_helper(self, root: BSTNode, value: int, bro: list[BSTNode]):
        if root is None:
            return None
        if value < root.value:
            bro.append(copy.deepcopy(root))
            root.left = self.__delete_node_helper(root.left, value, bro)
            if root.left is not None:
                root.left.parent = root
        elif value > root.value:
            bro.append(copy.deepcopy(root))
            root.right = self.__delete_node_helper(root.right, value, bro)
            if root.right is not None:
                root.right.parent = root
        else:
            if root.left is None:
                bro.append(copy.deepcopy(root))
                return root.right
            elif root.right is None:
                bro.append(copy.deepcopy(root))
                return root.left
            temp = root.right
            while temp.left:
                temp = temp.left
            new_node = BSTNode(root.center, temp.value, root.left, root.right, root.parent)
            new_node.right = self.__delete_node_avl_helper(root.right,
                                                           temp.value, bro)
            del root
            root = new_node
        return root

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
        if not (self.menu.get_position()[0] - NODE_R > X > 0 + NODE_R and Y < SCREEN_SIZE[1]):  # or root.parent is not None and not root.parent.draw:
            root.hide_node()
        self.__draw_new_nodes(root.left)
        self.__draw_new_nodes(root.right)

    def __fix_parents(self, root: BSTNode):
        if root is None:
            return
        if root is self.root:
            root.parent = None
            root.center = MID_POS_TREE
        if root.left is not None:
            root.left.parent = root
        if root.right is not None:
            root.right.parent = root
        root.clicked_off()
        self.__fix_parents(root.left)
        self.__fix_parents(root.right)

    def __delete_animation(self, bro: list[BSTNode]):
        last_node: BSTNode = bro.pop(-1)
        if not last_node.draw:
            return
        sec = self.animation_speed
        if last_node.parent is None:
            last_node.paint_node(RED)
            self.__refresh_screen(pygame.event.get())
            self.__refresh_screen(pygame.event.get())
            pygame.time.delay(sec)
            return
        last_node_edge: Edge = self.__find_edge(last_node.parent, last_node)
        for node in bro:
            node.clicked_on(TARGET)
            self.__refresh_screen(pygame.event.get())
            pygame.time.delay(sec)
        self.all_edges.remove(last_node_edge)
        self.__refresh_screen(pygame.event.get())
        pygame.time.delay(sec)
        last_node.paint_node(RED)
        self.__refresh_screen(pygame.event.get())
        pygame.time.delay(sec)

    def __delete_node(self):
        text_input: pygame_menu.widgets.widget.textinput.TextInput = self.menu.get_widget('text_input')
        if len(text_input.get_value()) == 0:
            return
        if self.root is None:
            self.__error_message.enable()
            self.__error_message.get_widget('error_message').set_title('The Tree Is Empty')
            while self.__error_message.is_enabled():
                self.__error_message.mainloop(self.window_surface, disable_loop=False)
            text_input.clear()
            return
        if not text_input.get_value().isnumeric():
            self.__error_message.enable()
            e: pygame_menu.widgets.widget.label.Label = self.__error_message.get_widget('error_message')
            e.set_title('Value must be an integer')
            while self.__error_message.is_enabled():
                self.__error_message.mainloop(self.window_surface, disable_loop=False)
            text_input.clear()
            return
        value = int(text_input.get_value())
        if value > 9999 or value < -9999:
            self.__error_message.enable()
            e: pygame_menu.widgets.widget.label.Label = self.__error_message.get_widget('error_message')
            e.set_title('Value must be between -9999 to 9999')
            while self.__error_message.is_enabled():
                self.__error_message.mainloop(self.window_surface, disable_loop=False)
            text_input.clear()
            return
        text_input.clear()
        if self.all_values.get(value):
            bro: list[BSTNode] = []
            self.all_values.pop(value)
            if not self.is_AVL:
                self.root = self.__delete_node_helper(self.root, value, bro)
            else:
                self.root = self.__delete_node_avl_helper(self.root, value, bro)
            self.__delete_animation(bro)
            self.__fix_parents(self.root)
            temp = self.root
            self.root = None
            self.__fix_positions_avl_tree(temp)
            self.all_nodes.empty()
            self.all_edges.empty()
            self.__draw_new_nodes(self.root)
            self.__draw_new_edges(self.root)
            # if self.root is not None:
            #     self.__fix_position_subtree(self.root.left)
            #     self.__fix_position_subtree(self.root.right)
            # answer: BSTNode | bool = self.__check_collision()
            # if answer:
            #     self.__avoid_collision(self.root)
        else:
            self.__error_message.enable()
            self.__error_message.get_widget('error_message').set_title(f'{value} Is Not In The Tree')
            while self.__error_message.is_enabled():
                self.__error_message.mainloop(self.window_surface, disable_loop=False)

    def __Inorder(self, root: BSTNode, result: list[str]):
        if root is None:
            return result
        self.__Inorder(root.left, result)
        result.append(str(root))
        root.paint_node(ORANGE)
        self.__refresh_screen([])
        pygame.time.delay(self.animation_speed)
        self.__Inorder(root.right, result)
        return result

    def __Preorder(self, root: BSTNode, result: list[str]):
        if root is None:
            return result
        result.append(str(root))
        root.paint_node(ORANGE)
        self.__refresh_screen([])
        pygame.time.delay(self.animation_speed)
        self.__Preorder(root.left, result)
        self.__Preorder(root.right, result)
        return result

    def __Postorder(self, root: BSTNode, result: list[str]):
        if root is None:
            return result
        self.__Postorder(root.left, result)
        self.__Postorder(root.right, result)
        result.append(str(root))
        root.paint_node(ORANGE)
        self.__refresh_screen([])
        pygame.time.delay(self.animation_speed)
        return result

    def __refresh_screen(self, events):
        self.menu.update(events)
        self.window_surface.fill(BLACK_COLOR)
        self.menu.draw(self.window_surface)
        self.all_nodes.draw(self.window_surface)
        self.all_edges.draw(self.window_surface)
        pygame.display.update()

    def __traversal_activation(self):
        w: pygame_menu.widgets.widget.dropselect.DropSelect = self.menu.get_widget('dropselect')
        if self.root is None:
            self.__error_message.enable()
            while self.__error_message.is_enabled():
                self.__error_message.mainloop(self.window_surface, disable_loop=False)
            return

        def traversal_shower(which_traversal, result):
            self.__traversal_shower.set_title(which_traversal)
            self.__traversal_shower.get_widget('traversal_shower').set_title(', '.join(result))
            self.__traversal_shower.enable()
            while self.__traversal_shower.is_enabled():
                self.__traversal_shower.mainloop(self.window_surface, disable_loop=False)

        try:
            val = w.get_value()
            traversal, result = None, None
            if val[0][0] == 'Inorder':
                traversal, result = 'Inorder', self.__Inorder(root=self.root, result=[])
            elif val[0][0] == 'PreOrder':
                traversal, result = 'PreOrder', self.__Preorder(root=self.root, result=[])
            elif val[0][0] == 'PostOrder':
                traversal, result = 'PostOrder', self.__Postorder(root=self.root, result=[])
            if traversal and result:
                traversal_shower(traversal, result)

            for node in self.all_nodes:
                node.clicked_off()

        except Exception:
            self.__error_message.enable()
            w: pygame_menu.widgets.widget.label.Label = self.__error_message.get_widget('error_message')
            w.set_title('You Must Select An Option')
            while self.__error_message.is_enabled():
                self.__error_message.mainloop(self.window_surface, disable_loop=False)
            return
            # pass

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
