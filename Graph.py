import math
import random
import time
import pygame
import pygame_gui

from Utils import Utils
from pygame.locals import (
    RLEACCEL,
)

"""CONSTANTS"""
NODE_R: int = 30
LEFT_MOUSE: int = 1
RIGHT_CLICK: int = 3
Utils: Utils = Utils()
NODE_NAME = Utils.gen_letters()
SCREEN_SIZE = (1024, 900)  # width ,height
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)


class Node(pygame.sprite.Sprite):
    def __init__(self,
                 center: tuple[int, int],
                 all_nodes,  # OBJECT
                 draw: bool = True,
                 name: str = ""
                 ):
        super(Node, self).__init__()
        self.center = center
        self.surf = pygame.Surface((2 * NODE_R, 2 * NODE_R))
        self.image = self.surf
        self.name = "" if not draw else name
        self.text_view = pygame.font.SysFont("arial", 25, True, False).render("" if not draw else self.name, True,
                                                                              (255, 255, 255))
        self.is_clicked = False
        if draw:
            pygame.draw.circle(self.surf, 'Green', (NODE_R, NODE_R), NODE_R)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=self.center)
        self.all_nodes = all_nodes
        self.surf.blit(self.text_view, (20, 20))
        self.algo_node, self.algo_edge = None, None

    def __str__(self):
        return self.name

    def clicked_on(self):
        self.surf.fill(pygame.Color('Black'))
        pygame.draw.circle(self.surf, 'Blue', (NODE_R, NODE_R), NODE_R)
        pygame.draw.circle(self.surf, 'Green', (NODE_R, NODE_R), NODE_R - 4)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=self.center)
        self.surf.blit(self.text_view, (20, 20))
        self.is_clicked = True

    def clicked_off(self):
        pygame.draw.circle(self.surf, 'Green', (NODE_R, NODE_R), NODE_R)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=self.center)
        self.surf.blit(self.text_view, (20, 20))
        self.is_clicked = False

    def move(self, mouse_pos: tuple[int, int]):
        self.center = mouse_pos
        self.clicked_on()

    def paint_node(self, color: pygame.Color):
        self.surf.fill(pygame.Color('Black'))
        pygame.draw.circle(self.surf, color, (NODE_R, NODE_R), NODE_R)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=self.center)
        self.surf.blit(self.text_view, (20, 20))


class Edge(pygame.sprite.Sprite):
    def __init__(self,
                 node1: Node,
                 node2: Node,
                 start_point: tuple[int, int],
                 end_point: tuple[int, int],
                 weight: int = 0,
                 is_directed: bool = True,
                 is_weighted: bool = True,
                 edge_color: tuple[int, int, int] = WHITE_COLOR
                 ):
        super(Edge, self).__init__()
        self.color = edge_color
        self.source = node1
        self.destination = node2
        self.start_point = start_point
        self.end_point = end_point
        self.weight = weight
        self.is_directed = is_directed
        self.is_weighted = is_weighted
        self.surf = pygame.Surface(SCREEN_SIZE)
        self.image = self.surf
        self.draw()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2))

    def draw(self):
        if self.is_directed:
            self.__draw_arrow()
        else:
            self.__draw_line()

    def __str__(self):
        return f'{self.source} -> {self.destination}'

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

    def __draw_line(self,
                    body_width: int = 4):
        # start, end = pygame.Vector2(self.start_point), pygame.Vector2(self.end_point)
        # middleX = (start.x + end.x) / 2
        # middleY = (start.y + end.y) / 2
        # surface = pygame.Surface((NODE_R*2,NODE_R*2))
        # rect = surface.get_rect(center=(middleX,middleY))
        # pygame.draw.rect(self.surf,self.color,rect)
        pygame.draw.line(self.surf, self.color, self.start_point, self.end_point, width=body_width)
        if self.is_weighted:
            self.__draw_weight()

    def __draw_arrow(self,
                     body_width: int = 4,
                     head_width: int = 15,
                     head_height: int = 15
                     ):
        start, end, surface = pygame.Vector2(self.start_point), pygame.Vector2(self.end_point), self.surf
        arrow = start - end
        angle = arrow.angle_to(pygame.Vector2(0, -1))
        body_length = arrow.length() - head_height

        # Create the triangle head around the origin
        head_verts = [
            pygame.Vector2(0, head_height / 2),  # Center
            pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
            pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
        ]
        # Rotate and translate the head into place
        translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
        for i in range(len(head_verts)):
            head_verts[i].rotate_ip(-angle)
            head_verts[i] += translation
            head_verts[i] += start

        pygame.draw.polygon(surface, self.color, head_verts)

        # Stop weird shapes when the arrow is shorter than arrow head
        if arrow.length() >= head_height:
            # Calculate the body rect, rotate and translate into place
            body_verts = [
                pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
                pygame.Vector2(body_width / 2, body_length / 2),  # Topright
                pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
                pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
            ]
            translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
            for i in range(len(body_verts)):
                body_verts[i].rotate_ip(-angle)
                body_verts[i] += translation
                body_verts[i] += start
            pygame.draw.polygon(surface, self.color, body_verts)
            if self.is_weighted:
                self.__draw_weight(angle)

    def __draw_weight(self, angle=0):
        start, end, surface = pygame.Vector2(self.start_point), pygame.Vector2(self.end_point), self.surf

        w = pygame.font.SysFont("arial", 25, True, True).render("1" if self.weight == -1 else str(self.weight), True,
                                                                (0, 255, 0))
        middleX = (start.x + end.x) / 2
        middleY = (start.y + end.y) / 2
        text_rect = w.get_rect()
        text_rect.center = (middleX, middleY - 25)
        # text_rect = pygame.transform.rotate(self.)

        if abs(start.x - end.x) <= 100:
            text_rect.center = (middleX + 15, middleY)

        surface.blit(w, text_rect)


class Graph_Simulator:
    def __init__(self, file_name: str = ""):
        pygame.init()
        pygame.display.set_caption('Graph Visualizer')
        self.graph: dict[Node, list[Edge]] = {}
        self.easy_access_graph: dict[str, Node] = {}
        self.window_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        self.all_nodes = pygame.sprite.Group()
        self.all_graph = pygame.sprite.Group()
        self.all_edges = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.is_directed = True
        self.is_weighted = True
        if file_name:
            self.__create_graph_from_file(file_name)

    def __create_graph_from_file(self, file_name: str):
        try:
            G, self.is_directed, self.is_weighted = Utils.graph_parser(file_name)
            coordinates = []
            while len(coordinates) != len(G.keys()):
                X, Y = random.randint(50, SCREEN_SIZE[0] - 50), random.randint(50, SCREEN_SIZE[1] - 50)
                if (X, Y) in coordinates:
                    continue
                coordinates.append((X, Y))
            for name, center in zip(G.keys(), coordinates):
                node = Node(center=center, all_nodes=self.all_nodes, draw=True, name=name)
                self.all_nodes.add(node)
                self.all_graph.add(node)
                self.graph[node] = []
                self.easy_access_graph[name] = node
            for nd in G.keys():
                for eg in G[nd]:
                    dst_name, weight = "", 0
                    if len(eg) == 2:
                        dst_name, weight = eg
                    else:
                        dst_name = eg[0]
                    src, dst = self.easy_access_graph[nd], self.easy_access_graph[dst_name]
                    flag = False
                    if self.is_directed:
                        for dg in self.graph[dst]:
                            if dg.destination == src:
                                self.__two_way_edge(dg, src, dst, 25, weight)
                                flag = True
                                break
                    if flag:
                        continue
                    start, end = self.__calc_position(dst.center, src.center)
                    end1, start1 = self.__calc_position(src.center, dst.center)
                    edge = Edge(src, dst, start, end1, weight, self.is_directed, self.is_weighted)
                    self.all_graph.add(edge)
                    self.graph[src].append(edge)
                    # if not self.is_directed:
                    #     edge = Edge(dst, src, end1, start, weight, self.is_directed, self.is_weighted)
                    #     self.graph[dst].append(edge)
            # for key in self.graph.keys():
            #     print(f"{key} = {' '.join([str(i) for i in self.graph[key]])}")
            #     print()
        except FileNotFoundError:
            print("File not Found/Wrong format , Initalizing Empty Graph.")

    def __is_an_edge(self, edge_lst: list[Edge], destination: Node):
        for edge in edge_lst:
            if edge.destination == destination:
                return edge
        return False

    def __stabling_graph(self):
        return
        L0 = 250  # nominal distance in pixles
        K1, K2 = 10, 1  # force/distance
        V = 3  # pixel/frem
        TOL = 5
        for v in self.all_nodes:
            fx, fy = 0, 0
            for u in self.all_nodes:
                if v == u:
                    continue
                dx = u.center[0] - v.center[0]
                dy = u.center[1] - v.center[1]
                dist = math.sqrt((dx ** 2) + (dy ** 2)) + 1e-10
                my_k = K1 if self.__is_an_edge(self.graph[u], v) else K2
                if dist > L0 + TOL:
                    fx += my_k * (dx / dist)
                    fy += my_k * (dy / dist)
                elif dist < L0 - TOL:
                    fx -= my_k * (dx / dist)
                    fy -= my_k * (dy / dist)
            norm_f = math.sqrt((fx ** 2) + (fy ** 2)) + 1e-10
            fx /= norm_f
            fy /= norm_f
            new_x = v.center[0] + (fx * V)
            new_y = v.center[1] + (fy * V)
            new_x = max(50, min(1024 - 50, new_x))
            new_y = max(50, min(900 - 50, new_y))
            v.center = (new_x, new_y)
            v.rect = v.surf.get_rect(center=v.center)

    def __is_in_node(self, position: tuple[int, int]):
        tmp_node = Node(position, None, False)
        node = pygame.sprite.spritecollideany(tmp_node, self.all_nodes)
        return None if not node else node

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

    def __two_way_edge(self, edge, src, dst, angle=25, weight=0):
        start, end = self.__calc_position(src.center, dst.center, -angle)
        end1, end2 = self.__calc_position(dst.center, src.center, angle)
        edge.start_point = start
        edge.end_point = end1
        edge.surf.fill(BLACK_COLOR)
        edge.draw()
        start, end = self.__calc_position(src.center, dst.center, angle)
        end1, end2 = self.__calc_position(dst.center, src.center, -angle)
        newEdge = Edge(src, dst, end1, start, is_directed=self.is_directed, is_weighted=self.is_weighted, weight=weight)
        self.graph[src].append(newEdge)
        self.all_graph.add(newEdge)

    def __add_edge(self, position: tuple[int, int]):
        mid: Node = self.__is_in_node(position)
        if not mid:
            return
        start, end, weight = 0, 0, 0
        while True:
            time_delta = self.clock.tick(144) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE:
                    # mouse_pos = pygame.mouse.get_pos()
                    tmp: Node = self.__is_in_node(pygame.mouse.get_pos())
                    if tmp and tmp != mid:
                        for edge in self.graph[mid]:
                            if edge.destination == tmp:
                                self.window_surface.fill(pygame.Color("black"))
                                return
                        self.window_surface.fill(pygame.Color("black"))
                        for edge in self.graph[tmp]:
                            if edge.destination == mid:
                                self.__two_way_edge(edge, mid, tmp, 25)
                                return

                        end1, end2 = self.__calc_position(mid.center, tmp.center)
                        edge = Edge(mid, tmp, start, end1, is_directed=self.is_directed, is_weighted=self.is_weighted,
                                    weight=weight)
                        self.graph[mid].append(edge)
                        self.all_graph.add(edge)
                        if not self.is_directed:
                            edge = Edge(tmp, mid, end1, start, is_directed=self.is_directed,
                                        is_weighted=self.is_weighted, weight=weight)
                            self.graph[tmp].append(edge)
                            self.all_graph.add(edge)
                        return

                    else:
                        self.window_surface.fill(pygame.Color("black"))
                        return

            self.window_surface.fill(pygame.Color("black"))
            for e in self.all_graph:
                self.window_surface.blit(e.surf, e.rect)
            start, end = self.__calc_position(pygame.mouse.get_pos(), mid.center)

            tmp_edge = Edge(None, None, start, end, is_directed=self.is_directed, is_weighted=self.is_weighted)
            self.window_surface.blit(tmp_edge.surf, tmp_edge.rect)
            pygame.display.flip()

    def __move_node(self, global_node):
        for node in self.graph.keys():
            for edge in self.graph[node]:
                if node == global_node:
                    flag = False
                    for edge1 in self.graph[edge.destination]:
                        if edge1.destination == node:
                            flag = True
                            break
                    angle = 0 if (flag and not self.is_directed) or not flag else -25

                    start, end = self.__calc_position(edge.destination.center, node.center, angle)
                    end1, end2 = self.__calc_position(node.center, edge.destination.center, -angle)
                    edge.start_point = start
                    edge.end_point = end1
                    edge.surf.fill(BLACK_COLOR)
                    edge.draw()
                elif edge.destination == global_node:
                    flag = False
                    for edge1 in self.graph[global_node]:
                        if edge1.destination == node:
                            flag = True
                            break
                    angle = 0 if (flag and not self.is_directed) or not flag else -25
                    start, end = self.__calc_position(node.center, edge.destination.center, -angle)
                    end1, end2 = self.__calc_position(edge.destination.center, node.center, angle)
                    edge.start_point = end1
                    edge.end_point = start
                    edge.surf.fill(BLACK_COLOR)
                    edge.draw()

    def __delete_node(self):
        nd = self.__is_in_node(pygame.mouse.get_pos())
        if nd:
            for v in self.graph[nd]:
                self.all_graph.remove(v)
            self.graph.pop(nd)
            self.all_graph.remove(nd)
            self.all_nodes.remove(nd)
            for node, edges in self.graph.items():
                new_lst: list[Edge] = []
                for edge in edges:
                    if edge.destination != nd:
                        new_lst.append(edge)
                    else:
                        self.all_graph.remove(edge)
                if len(new_lst) != len(self.graph[node]):
                    self.graph[node] = new_lst

    def __refresh_screen(self):
        # fnt = pygame.font.SysFont("Arial", 25)
        # fps_string = "%.0f" % self.clock.get_fps()
        # txt_surface = fnt.render(fps_string, True, WHITE_COLOR)
        # self.stabling_graph()
        # self.window_surface.blit(txt_surface, (0,0))
        self.__stabling_graph()
        self.window_surface.fill(BLACK_COLOR)
        self.all_graph.draw(self.window_surface)
        pygame.display.flip()

    def __delete_edge(self, queue):
        src, dst = queue
        if self.is_directed:
            for edge in self.graph[src]:
                if edge.destination == dst:
                    self.all_graph.remove(edge)
                    self.graph[src].remove(edge)
                    break
        else:
            for edge in self.graph[src]:
                if edge.destination == dst:
                    self.all_graph.remove(edge)
                    self.graph[src].remove(edge)
                    break
            for edge in self.graph[dst]:
                if edge.destination == src:
                    self.all_graph.remove(edge)
                    self.graph[dst].remove(edge)
                    break
        src.clicked_off()
        dst.clicked_off()
        return []

    def __pressed_on_node(self, pressed_node, drag: bool, delete_edge_queue: list):
        delete_edge_queue.append(pressed_node)
        pressed_node.clicked_on()
        d = drag
        global_node = pressed_node
        return global_node, d

    def __add_node(self, mouse_pos):
        node_name = next(NODE_NAME)
        while self.easy_access_graph.get(node_name):
            node_name = next(NODE_NAME)
        node = Node(mouse_pos, self.all_nodes, name=node_name)
        self.all_nodes.add(node)
        self.all_graph.add(node)
        self.graph[node] = []

    def __BFS(self):
        queue = []
        sec = 1000
        visited_edges = {}
        visited_nodes = {}
        src: Node = None
        dst: Node = None
        while True:
            self.clock.tick(60) / sec
            if src and dst:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_CLICK:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE:
                    node_pressed = self.__is_in_node(pygame.mouse.get_pos())
                    if not src and node_pressed:
                        src = node_pressed
                        src.clicked_on()
                    elif not dst and node_pressed and node_pressed != src:
                        dst = node_pressed
                        dst.clicked_on()
                self.__refresh_screen()
        src.clicked_off()
        dst.clicked_off()
        queue.append(src)
        print_queue = []
        YELLOW = (255, 255, 0)
        ORANGE = (220, 137, 12)
        RED = (255, 0, 0)
        TARGET = (204, 0, 102)
        for v in self.graph.keys():
            v.algo_node, v.algo_edge = None, None
        visited_nodes[src] = True
        src.paint_node(YELLOW)
        while queue:
            self.__refresh_screen()
            pygame.time.wait(sec//2)
            curr = queue.pop(0)
            visited_nodes[curr] = True
            curr.paint_node(RED)
            if curr == dst:
                print_queue.append(curr)
                nd = curr.algo_node
                print_queue.append(nd)
                while nd != src:
                    nd = nd.algo_node
                    print_queue.append(nd)
                break
            for edge in self.graph[curr]:
                if not visited_edges.get(edge):
                    queue.append(edge.destination)
                    if not visited_nodes.get(edge.destination):
                        pygame.time.wait(sec//2)
                        edge.destination.paint_node(YELLOW)
                        self.__refresh_screen()
                    if not edge.destination.algo_node:
                        edge.destination.algo_node = curr
                    visited_edges[edge] = True
        for node in list(visited_nodes.keys()) + queue:
            node.clicked_off()
        pygame.time.wait(sec)
        src.paint_node(TARGET)
        dst.paint_node(TARGET)
        self.__refresh_screen()
        print_queue.reverse()
        edges_to_print = []
        for i in range(len(print_queue)):
            if i + 1 == len(print_queue):
                break
            SRC = print_queue[i]
            DST = print_queue[i + 1]
            if not self.is_directed:
                edges_to_print.append(
                    (self.__is_an_edge(self.graph[SRC], DST), self.__is_an_edge(self.graph[DST], SRC)))
            else:
                edges_to_print.append(self.__is_an_edge(self.graph[SRC], DST))
        if not self.is_directed:
            for edge1, edge2 in edges_to_print:
                edge1.color = ORANGE
                edge2.color = ORANGE
                edge1.draw()
                edge2.draw()
                self.__refresh_screen()
                pygame.time.wait(sec)
            pygame.time.wait(sec)
            src.clicked_off()
            dst.clicked_off()
            for edge1, edge2 in edges_to_print:
                edge1.color = WHITE_COLOR
                edge2.color = WHITE_COLOR
                edge1.draw()
                edge2.draw()
        else:
            for edge in edges_to_print:
                edge.color = ORANGE
                edge.draw()
                self.__refresh_screen()
                pygame.time.wait(sec)
            pygame.time.wait(sec)
            src.clicked_off()
            dst.clicked_off()
            for edge in edges_to_print:
                edge.color = WHITE_COLOR
                edge.draw()
        self.__refresh_screen()

    def __clicked_off(self, delete_edge_queue):
        for nd in delete_edge_queue:
            nd.clicked_off()
        return []

    def run(self):
        drag = False
        global_node: Node = None
        delete_edge_queue = []
        while True:
            time_delta = self.clock.tick(144) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                key_pressed = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN and key_pressed[pygame.K_b]:
                    self.__BFS()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_CLICK:
                    delete_edge_queue = self.__clicked_off(delete_edge_queue)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE:
                    pressed_node = self.__is_in_node(pygame.mouse.get_pos())
                    if pressed_node:
                        # delete_edge_queue.append(pressed_node)
                        # pressed_node.clicked_on()
                        # drag = True
                        # global_node = pressed_node
                        global_node, drag = self.__pressed_on_node(pressed_node, True, delete_edge_queue)
                        if len(delete_edge_queue) == 2:
                            delete_edge_queue = self.__delete_edge(delete_edge_queue)
                    else:
                        delete_edge_queue = self.__clicked_off(delete_edge_queue)
                        global_node = None
                        drag = False
                    if key_pressed[pygame.K_LSHIFT]:
                        self.__add_edge(pygame.mouse.get_pos())
                        delete_edge_queue = []
                        # self.all_graph.add(Edge(None, None, (1024, 900), pygame.mouse.get_pos()))
                    elif key_pressed[pygame.K_BACKSPACE] or key_pressed[pygame.K_LCTRL]:
                        self.__delete_node()
                        delete_edge_queue = []

                    else:
                        mouse_pos = pygame.mouse.get_pos()
                        nd: Node = self.__is_in_node(mouse_pos)
                        if not nd and not delete_edge_queue:
                            self.__add_node(mouse_pos)
                        else:
                            if not nd.is_clicked:
                                drag = True
                                global_node = nd
                                global_node.clicked_on()

                elif event.type == pygame.MOUSEMOTION:
                    if drag:
                        global_node.move(event.pos)
                        self.__move_node(global_node)
                        delete_edge_queue = []

                elif event.type == pygame.MOUSEBUTTONUP:
                    if drag:
                        drag = False
                        if global_node not in delete_edge_queue:
                            global_node.clicked_off()
                            global_node = None
            self.__refresh_screen()
