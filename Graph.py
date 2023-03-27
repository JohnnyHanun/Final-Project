import math
import random
import os
import heapq
from typing import TypeVar, Union, Iterable
from constants import *
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time
import pygame
import tkinter as tk
from tkinter import simpledialog
from pygame.locals import (
    RLEACCEL,
)

ROOT = tk.Tk()
ROOT.withdraw()
# ROOT.

def edit_edge_while_add(queue):
    USER_INP = simpledialog.askinteger(title="Edit Weight",
                                       prompt="Please Enter Weight then press Enter")
    # queue.put(USER_INP)
    queue.append(USER_INP)


class Node(pygame.sprite.Sprite):
    def __init__(self,
                 center: tuple[int, int],
                 all_nodes,  # OBJECT
                 draw: bool = True,
                 name: str = ""
                 ):
        super(Node, self).__init__()
        self.color = pygame.Color('Green')
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
        self.algo_node, self.algo_edge, self.self_weight = None, None, math.inf
        self.deg_in, self.deg_out = 0, 0

    def __lt__(self, other):
        return self.self_weight < other.self_weight

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

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
        self.color = color
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
                 edge_color: tuple[int, int, int] = WHITE_COLOR,
                 drawble: bool = True
                 ):
        super(Edge, self).__init__()
        self.activate_comparison = False
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
        self.drawble = drawble
        self.draw()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2))

    def draw(self):
        if self.drawble:
            if self.is_directed:
                self.__draw_arrow()
            else:
                self.__draw_line()

    def __str__(self):
        return f'{self.source} -> {self.destination}'

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        if self.activate_comparison:
            S = self.source
            D = self.destination
            OS = other.source
            OD = other.destination
            return (S == OS and D == OD) or (S == OD and D == OS)
        else:
            return id(self) == id(other)

    def __hash__(self):
        S = self.source
        D = self.destination
        return hash((id(S) ^ id(D))) + hash(S.name) + hash(D.name)

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
        # print(start,head_verts)
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
            self.__draw_weight()

    def __draw_weight(self, angle=0):
        # start, end, surface = pygame.Vector2(self.start_point), pygame.Vector2(self.end_point), self.surf
        #
        # w = pygame.font.SysFont("arial", 25, True, True).render("1" if self.weight == -1 else str(self.weight), True,
        #                                                         (0, 255, 0))
        # middleX = (start.x + end.x) / 2
        # middleY = (start.y + end.y) / 2
        # text_rect = w.get_rect()
        # calc_angle = math.degrees(math.atan2(end.y - start.y, end.x - start.x))
        # # print(f'{self} {self.start_point} {self.end_point}')
        # angle = 25 if calc_angle <= 0 else -25
        # text_rect.center = (middleX, middleY + angle)
        #
        # # text_rect = pygame.transform.rotate(self.)
        #
        # if abs(start.x - end.x) <= 100:
        #     text_rect.center = (middleX + angle, middleY)
        #
        # surface.blit(w, text_rect)
        start, end, surface = pygame.Vector2(self.start_point), pygame.Vector2(self.end_point), self.surf
        str_weight = str(self.weight)
        w = pygame.font.SysFont("arial", 22, True, True).render("1" if self.weight == -1 else str_weight, True,
                                                                (127,255,212))
        angle = math.atan2(end.x - start.x, end.y - start.y)
        middleX = (start.x + end.x) / 2
        middleY = (start.y + end.y) / 2
        # hline_x1 = middleX - 25 * math.cos(angle)
        # hline_y1 = middleY + 25 * math.sin(angle)
        hline_x2 = middleX + 35 * math.cos(angle)
        hline_y2 = middleY - 35 * math.sin(angle)
        w_rect = w.get_rect()
        w_rect.center = (hline_x2, hline_y2)
        self.surf.blit(w,w_rect)
        #pygame.draw.line(self.surf, self.color, (hline_x1,hline_y1), (hline_x2, hline_y2), width=4)

    def set_weight(self, new_weight: int):
        self.weight = new_weight


class Graph_Simulator:
    def __init__(self, file_name: str = ""):
        pygame.init()
        pygame.display.set_caption('Graph Visualizer')
        self.graph: dict[Node, dict[Node, Edge]] = {}
        self.easy_access_graph: dict[str, Node] = {}
        self.window_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        self.all_nodes = pygame.sprite.Group()
        self.all_graph = pygame.sprite.Group()
        self.all_edges = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.is_directed = True
        self.is_weighted = True
        self.ROOT = tk.Tk()
        self.ROOT.withdraw()
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
                self.graph[node] = {}
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
                        edge = self.__is_an_edge(self.graph[dst], src)
                        if edge:
                            self.__two_way_edge(edge, src, dst, 25, weight)
                            flag = True
                            src.deg_out += 1
                            dst.deg_in += 1
                    if flag:
                        continue
                    start, end = self.__calc_position(dst.center, src.center)
                    end1, start1 = self.__calc_position(src.center, dst.center)
                    draw_edge = True if not self.is_directed and not self.__is_an_edge(self.graph[dst], src) else False
                    if self.is_directed:
                        draw_edge = True
                    edge = Edge(src, dst, start, end1, weight, self.is_directed, self.is_weighted, drawble=draw_edge)
                    self.all_graph.add(edge)
                    self.graph[src][dst] = edge
                    src.deg_out += 1
                    dst.deg_in += 1
                    # if not self.is_directed:
                    #     edge = Edge(dst, src, end1, start, weight, self.is_directed, self.is_weighted)
                    #     self.graph[dst].append(edge)
            # for key in self.graph.keys():
            #     print(f"{key} = {' '.join([str(i) for i in self.graph[key]])}")
            #     print()
        except FileNotFoundError:
            print("File not Found/Wrong format , Initalizing Empty Graph.")

    def __is_an_edge(self, edge_dict: dict[Node, Edge], destination: Node):
        return edge_dict.get(destination)

    def __edit_weight(self):
        src: Node = None
        dst: Node = None
        sec = 1000
        while True:
            self.clock.tick(60)
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
        flag = True
        edge = self.__is_an_edge(self.graph[src], dst)
        if not edge:
            src.clicked_off()
            dst.clicked_off()
            return
        weight = 0
        while flag:
            if self.is_weighted:
                q = []
                edit_edge_while_add(q)
                weight = q.pop(0)
                if weight is None:
                    src.clicked_off()
                    dst.clicked_off()
                    return
                if not self.is_directed:
                    edge2 = self.edge = self.__is_an_edge(self.graph[dst], src)
                    edge2.set_weight(weight)
                    edge2.surf.fill(BLACK_COLOR)
                edge.set_weight(weight)
                edge.surf.fill(BLACK_COLOR)
                edge.draw()
                src.clicked_off()
                dst.clicked_off()
                self.__refresh_screen()
                return

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
        self.graph[src][dst] = newEdge
        self.all_graph.add(newEdge)

    def __add_edge(self, position: tuple[int, int]):
        mid: Node = self.__is_in_node(position)
        q = []
        if not mid:
            return
        start, end, weight = 0, 0, 0
        while True:
            self.clock.tick(360)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE:
                    # mouse_pos = pygame.mouse.get_pos()
                    tmp: Node = self.__is_in_node(pygame.mouse.get_pos())
                    if tmp and tmp != mid:
                        for edge in self.graph[mid]:
                            if edge == tmp:
                                self.window_surface.fill(pygame.Color("black"))
                                return
                        self.window_surface.fill(pygame.Color("black"))
                        for edge in self.graph[tmp]:
                            if edge == mid:
                                edit_edge_while_add(q)
                                weight = q.pop(0)
                                if weight is None:
                                    return
                                self.__two_way_edge(self.graph[tmp][mid], mid, tmp, 25,weight=weight)
                                mid.deg_out += 1
                                tmp.deg_in += 1
                                return
                        if self.is_weighted:
                            # q = Queue()
                            # p = Process(target=edit_edge_while_add, args=(q,))
                            # p.run()
                            edit_edge_while_add(q)
                            weight = q.pop(0)
                            if weight is None:
                                return
                        end1, end2 = self.__calc_position(mid.center, tmp.center)
                        edge = Edge(mid, tmp, start, end1, is_directed=self.is_directed, is_weighted=self.is_weighted,
                                    weight=weight)
                        self.graph[mid][tmp] = edge
                        self.all_graph.add(edge)
                        mid.deg_out += 1
                        tmp.deg_in += 1
                        if not self.is_directed:
                            edge = Edge(tmp, mid, end1, start, is_directed=self.is_directed,
                                        is_weighted=self.is_weighted, weight=weight, drawble=False)
                            self.graph[tmp][mid] = edge
                            self.all_graph.add(edge)
                            tmp.deg_out += 1
                            mid.deg_in += 1
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
        for edge in self.graph[global_node].values():
            flag = True if self.__is_an_edge(self.graph[edge.destination], global_node) else False
            angle = 0 if (flag and not self.is_directed) or not flag else -25

            start, end = self.__calc_position(edge.destination.center, global_node.center, angle)
            end1, end2 = self.__calc_position(global_node.center, edge.destination.center, -angle)
            edge.start_point = start
            edge.end_point = end1
            edge.surf.fill(BLACK_COLOR)
            if self.is_directed:
                edge.draw()
            else:
                edge.draw()

        for node, val in self.graph.items():
            if node != global_node:
                node1 = val.get(global_node)
                if node1:
                    edge = self.graph[node][global_node]
                    flag = True if self.__is_an_edge(self.graph[global_node], node) else False
                    angle = 0 if (flag and not self.is_directed) or not flag else -25
                    start, end = self.__calc_position(node.center, edge.destination.center, -angle)
                    end1, end2 = self.__calc_position(edge.destination.center, node.center, angle)
                    edge.start_point = end1
                    edge.end_point = start
                    edge.surf.fill(BLACK_COLOR)
                    edge.draw()

        # for node in self.graph.keys():
        #     # self.__refresh_screen()
        #     for node1 in self.graph[node]:
        #         edge = self.graph[node][node1]
        #         if node == global_node:
        #             flag = True if self.__is_an_edge(self.graph[node1], node) else False
        #             angle = 0 if (flag and not self.is_directed) or not flag else -25
        #
        #             start, end = self.__calc_position(edge.destination.center, node.center, angle)
        #             end1, end2 = self.__calc_position(node.center, edge.destination.center, -angle)
        #             edge.start_point = start
        #             edge.end_point = end1
        #             edge.surf.fill(BLACK_COLOR)
        #             if self.is_directed:
        #                 edge.draw(double_edge=flag)
        #             else:
        #                 edge.draw()
        #         elif node1 == global_node:
        #             flag = True if self.__is_an_edge(self.graph[global_node], node) else False
        #             angle = 0 if (flag and not self.is_directed) or not flag else -25
        #             start, end = self.__calc_position(node.center, edge.destination.center, -angle)
        #             end1, end2 = self.__calc_position(edge.destination.center, node.center, angle)
        #             edge.start_point = end1
        #             edge.end_point = start
        #             edge.surf.fill(BLACK_COLOR)
        #             edge.draw()

    def __delete_node(self):
        nd = self.__is_in_node(pygame.mouse.get_pos())
        if nd:
            for e in self.graph[nd].values():
                e.destination.deg_in -= 1
                self.all_graph.remove(e)
            self.graph.pop(nd)
            self.all_graph.remove(nd)
            self.all_nodes.remove(nd)
            for v in self.graph.values():
                edge = self.__is_an_edge(v, nd)
                if edge:
                    edge.source.deg_out -= 1
                    v.pop(edge.destination)
                    self.all_graph.remove(edge)

    def __refresh_screen(self):
        # fnt = pygame.font.SysFont("Arial", 25)
        # fps_string = "%.0f" % self.clock.get_fps()
        # txt_surface = fnt.render(fps_string, True, WHITE_COLOR)
        # self.stabling_graph()
        # self.window_surface.blit(txt_surface, (0,0))
        self.clock.tick(144)
        self.all_graph.clear(self.window_surface, self.window_surface.copy())
        self.__stabling_graph()
        self.window_surface.fill(BLACK_COLOR)
        self.all_graph.draw(self.window_surface)
        pygame.display.update()

    def __delete_edge(self, queue):
        src, dst = queue
        if self.is_directed:
            edge = self.__is_an_edge(self.graph[src], dst)
            if edge:
                self.all_graph.remove(edge)
                self.graph[src].pop(dst)
        else:
            edge = self.__is_an_edge(self.graph[src], dst)
            if edge:
                self.all_graph.remove(edge)
                self.graph[src].pop(dst)
                edge = self.__is_an_edge(self.graph[dst], src)
                self.all_graph.remove(edge)
                self.graph[dst].pop(src)

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
        self.graph[node] = {}

    def __algo_choose_nodes(self, flag=False):
        src: Node = None
        dst: Node = None
        while True:
            self.clock.tick(144)
            if src and dst:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_CLICK:
                    return None, None
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE:
                    node_pressed = self.__is_in_node(pygame.mouse.get_pos())
                    if not src and node_pressed:
                        src = node_pressed
                        src.clicked_on()
                        if flag:
                            return src
                    elif not dst and node_pressed and node_pressed != src:
                        dst = node_pressed
                        dst.clicked_on()
                self.__refresh_screen()
        return src, dst

    def __clean_data_for_algos(self):
        for v in self.graph.keys():
            v.algo_node, v.algo_edge, v.self_weight = None, None, math.inf
            v.clicked_off()
            for edge in self.graph[v].values():
                edge.activate_comparison, edge.color = False, WHITE_COLOR
                edge.surf.fill(BLACK_COLOR)
                edge.draw()
        self.__refresh_screen()

    def __fill_list_with_edges(self, print_queue, edges_to_print):
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
    def __avoiding_pygame_crush(self):
        pygame.event.pump()
        self.clock.tick(144)

    def __perform_animation(self, edges_to_print, sec, src, dst):
        pygame.display.update()
        if not self.is_directed:
            for edge1, edge2 in edges_to_print:
                edge1.color = ORANGE
                edge2.color = ORANGE
                edge1.draw()
                edge2.draw()
                self.__refresh_screen()
                pygame.time.delay(sec)

            pygame.time.delay(sec)
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
                pygame.time.delay(sec)
            pygame.time.delay(sec)
            src.clicked_off()
            dst.clicked_off()
            for edge in edges_to_print:
                edge.color = WHITE_COLOR
                edge.draw()
        self.__refresh_screen()

    def __DFS_Helper(self, nd: Node, visited: dict[Node, bool], sec: int, stack: list = None):
        if stack is None:
            stack = []
        visited[nd] = True
        for nde in self.graph[nd]:
            if not visited.get(nde):
                pygame.time.delay(sec // 2)
                self.__avoiding_pygame_crush()
                nde.paint_node(YELLOW)
                self.__refresh_screen()
                self.__DFS_Helper(nde, visited, sec, stack)
        pygame.time.delay(sec // 2)
        self.__avoiding_pygame_crush()
        nd.paint_node(SPECIAL_BLUE)
        stack.append(nd)
        self.__refresh_screen()

    def __DFS(self):
        pygame.event.pump()
        sec = 1000
        src = self.__algo_choose_nodes(flag=True)
        if not src:
            return
        self.__clean_data_for_algos()
        src.clicked_off()
        visited = {}
        src.paint_node(YELLOW)
        self.__refresh_screen()
        self.__DFS_Helper(src, visited, sec)
        for node in self.graph:
            if not visited.get(node):
                node.paint_node(YELLOW)
                self.__refresh_screen()
                self.__DFS_Helper(node, visited, sec)

        src.paint_node(SPECIAL_BLUE)
        pygame.time.delay(sec // 2)
        self.__refresh_screen()
        pygame.time.delay(sec)
        self.__clean_data_for_algos()

    def __Dijkstra(self):
        pygame.event.pump()
        sec = 1000
        src, dst = self.__algo_choose_nodes()
        if not src or not dst:
            return
        self.__clean_data_for_algos()
        src.clicked_off()
        dst.clicked_off()
        heap = list(self.graph.keys())
        src.self_weight = 0
        heapq.heapify(heap)
        while heap:
            self.__refresh_screen()
            time.sleep(1 / 2)
            pygame.time.delay(sec // 2)
            curr = heap.pop(0)
            curr.paint_node(RED)
            for node, edge in self.graph[curr].items():
                pygame.time.delay(sec // 2)
                node.paint_node(YELLOW)
                self.__refresh_screen()
                if curr.self_weight + edge.weight < node.self_weight:
                    node.algo_node = curr
                    node.self_weight = curr.self_weight + edge.weight
            heapq.heapify(heap)
        if not dst.algo_node:
            self.__clean_data_for_algos()
            return
        for node in self.graph:
            node.clicked_off()
        pygame.time.delay(sec)
        src.paint_node(TARGET)
        dst.paint_node(TARGET)
        self.__refresh_screen()
        print_queue = [dst]
        nd = dst.algo_node
        print_queue.append(nd)
        while nd != src:
            nd = nd.algo_node
            print_queue.append(nd)
        print_queue.reverse()
        edges_to_print = []
        self.__fill_list_with_edges(print_queue, edges_to_print)
        self.__perform_animation(edges_to_print, sec, src, dst)

    def __MST_KRUSKAL(self):
        pygame.event.pump()
        sec = 1000

        num_of_nodes = len(self.graph.keys())
        all_colors = [(0, 0, 0), (255, 255, 255), (0, 255, 0)]
        all_sets = []
        mst_edges = []
        duplicate_edges = []
        all_edges = set()

        def find(given_node):
            for index, Set in enumerate(all_sets):
                if given_node in Set:
                    return index

        def union(S1, S2):
            set1 = all_sets[S1]
            set2 = all_sets[S2]
            all_sets.remove(set1)
            all_sets.remove(set2)
            set1 |= set2
            clr = None
            for nd in set1:
                if not clr:
                    clr = nd.color
                else:
                    nd.paint_node(clr)
            all_sets.append(set1)

        for node, edges in self.graph.items():
            all_sets.append({node})
            color = (tuple([random.randint(0, 255) for i in range(3)]))
            while color in all_colors:
                color = (tuple([random.randint(0, 255) for i in range(3)]))
            all_colors.append(color)
            node.paint_node(color)
            for edge in edges.values():
                if not self.is_directed:
                    edge.activate_comparison = True
                    all_edges.add(edge)
                else:
                    all_edges.add(edge)
        self.__refresh_screen()
        all_edges = list(all_edges)
        all_edges.sort()
        while len(mst_edges) != num_of_nodes - 1 and all_edges:
            curr_edge = all_edges.pop(0)
            s1 = find(curr_edge.source)
            s2 = find(curr_edge.destination)
            if s1 != s2:
                curr_edge.color = BROWN
                curr_edge.draw()
                if not self.is_directed:
                    second_edge = self.__is_an_edge(self.graph[curr_edge.destination], curr_edge.source)
                    second_edge.color = BROWN
                    second_edge.draw()
                    duplicate_edges.append(second_edge)
                self.__refresh_screen()
                pygame.time.delay(sec + sec // 2)
                mst_edges.append(curr_edge)
                union(s1, s2)
        self.__clean_data_for_algos()
        self.window_surface.fill(pygame.Color(BLACK_COLOR))

        for edge in mst_edges + duplicate_edges:
            src, dst = edge.source, edge.destination
            src.paint_node(SPECIAL_BLUE)
            dst.paint_node(SPECIAL_BLUE)
            edge.draw()
            self.window_surface.blit(src.surf, src.rect)
            self.window_surface.blit(dst.surf, dst.rect)
            self.window_surface.blit(edge.surf, edge.rect)
        pygame.display.update()
        pygame.time.delay(3 * sec)
        self.__clean_data_for_algos()
        for edge in mst_edges + all_edges + duplicate_edges:
            edge.color = WHITE_COLOR
            edge.draw()
        self.__refresh_screen()

    def __reverse_graph(self):
        reversed_graph: dict[Node, dict[Node, Edge]] = {}
        all_graph_reversed = pygame.sprite.Group()
        for node in self.graph.keys():
            reversed_graph[node] = {}
            all_graph_reversed.add(node)
        for key in self.graph.keys():
            for node, edge in self.graph[key].items():
                new_edge = Edge(edge.destination, edge.source, edge.end_point, edge.start_point, edge.weight
                                , edge.is_directed, edge.is_weighted)
                reversed_graph[node][key] = new_edge
                all_graph_reversed.add(new_edge)
        return reversed_graph, all_graph_reversed

    def __Kosaraju_Sharir(self):
        pygame.event.pump()
        sec = 1000
        # lst_to_shuffle = [(key, key.deg_in + key.deg_out) for key in self.graph.keys()]
        # random.shuffle(lst_to_shuffle)
        # random_node, _ = max(lst_to_shuffle, key=lambda x: x[1])
        random_node = random.choice(list(self.graph.keys()))
        self.__clean_data_for_algos()
        visited = {}
        stack: list[Node] = []
        random_node.paint_node(YELLOW)
        self.__refresh_screen()
        self.__DFS_Helper(random_node, visited, sec, stack)
        for node in self.graph:
            if not visited.get(node):
                node.paint_node(YELLOW)
                self.__refresh_screen()
                self.__DFS_Helper(node, visited, sec, stack)
        saving_real_graph = self.graph
        saving_real_group = self.all_graph
        pygame.time.delay(3 * sec)
        self.__avoiding_pygame_crush()
        self.__clean_data_for_algos()
        self.graph, self.all_graph = self.__reverse_graph()
        self.__refresh_screen()
        visited = {}
        strongly_connected_components = []
        while stack:
            component = []
            src = stack.pop(-1)
            if not visited.get(src):
                src.paint_node(YELLOW)
                pygame.time.delay(sec)
                self.__refresh_screen()
                self.__DFS_Helper(src, visited, sec, component)
                strongly_connected_components.append(component)
        self.graph, self.all_graph = saving_real_graph, saving_real_group
        for component in strongly_connected_components:
            elements_to_print = pygame.sprite.Group()
            self.window_surface.fill(BLACK_COLOR)
            for strong in component:
                strong.paint_node(ORANGE)
                elements_to_print.add(strong)
                for node, edge in self.graph[strong].items():
                    if node in component:
                        elements_to_print.add(edge)
            elements_to_print.draw(self.window_surface)
            pygame.display.update()
            pygame.time.delay(3*sec)
            self.__avoiding_pygame_crush()
        all_colors = [(0, 0, 0), (255, 255, 255), (0, 255, 0)]
        counter = 0
        while counter != len(strongly_connected_components):
            color = tuple([random.randint(0, 255) for _ in range(3)])
            if color not in all_colors:
                all_colors.append(color)
                for node in strongly_connected_components[counter]:
                    node.paint_node(color)
                counter += 1
        self.__refresh_screen()
        pygame.time.delay(5 * sec)
        self.__clean_data_for_algos()
    def __BFS(self):
        pygame.event.pump()
        queue = []
        sec = 1000
        visited_nodes = {}
        src, dst = self.__algo_choose_nodes()
        if not src or not dst:
            return
        src.clicked_off()
        dst.clicked_off()
        queue.append(src)
        print_queue = []
        self.__clean_data_for_algos()
        visited_nodes[src] = True
        src.paint_node(YELLOW)
        while queue:
            self.__refresh_screen()
            pygame.time.delay(sec // 2)
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
            for node in self.graph[curr]:
                if not visited_nodes.get(node):
                    visited_nodes[node] = True
                    queue.append(node)
                    pygame.time.delay(sec // 2)
                    node.paint_node(YELLOW)
                    self.__refresh_screen()
                    if not node.algo_node:
                        node.algo_node = curr
        for node in list(visited_nodes.keys()) + queue:
            node.clicked_off()
        pygame.time.delay(sec)
        src.paint_node(TARGET)
        dst.paint_node(TARGET)
        self.__refresh_screen()
        print_queue.reverse()
        edges_to_print = []
        self.__fill_list_with_edges(print_queue, edges_to_print)
        self.__perform_animation(edges_to_print, sec, src, dst)

    def __clicked_off(self, delete_edge_queue):
        for nd in delete_edge_queue:
            nd.clicked_off()
        return []

    def run(self):
        drag = False
        global_node: Node = None
        delete_edge_queue = []
        while True:
            self.clock.tick(360) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                key_pressed = pygame.key.get_pressed()

                if event.type == pygame.KEYDOWN and key_pressed[pygame.K_b]:
                    self.__BFS()
                if event.type == pygame.KEYDOWN and key_pressed[pygame.K_m]:
                    if self.is_weighted:
                        self.__MST_KRUSKAL()
                    # else:
                    #     self.__SPT()
                if event.type == pygame.KEYDOWN and key_pressed[pygame.K_k]:
                    if self.is_directed:
                        self.__Kosaraju_Sharir()
                if event.type == pygame.KEYDOWN and key_pressed[pygame.K_d]:
                    if self.is_weighted:
                        self.__Dijkstra()
                if event.type == pygame.KEYDOWN and key_pressed[pygame.K_f]:
                    self.__DFS()
                if event.type == pygame.KEYDOWN and key_pressed[pygame.K_e]:
                    self.__edit_weight()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_CLICK:
                    delete_edge_queue = self.__clicked_off(delete_edge_queue)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE:
                    pressed_node = self.__is_in_node(pygame.mouse.get_pos())
                    if pressed_node:
                        global_node, drag = self.__pressed_on_node(pressed_node, True, delete_edge_queue)
                        if len(delete_edge_queue) == 2:
                            delete_edge_queue = self.__delete_edge(delete_edge_queue)
                    else:
                        delete_edge_queue = self.__clicked_off(delete_edge_queue)
                        global_node = None
                        drag = False

                    if key_pressed[pygame.K_LSHIFT] or key_pressed[pygame.K_RSHIFT]:
                        self.__add_edge(pygame.mouse.get_pos())
                        delete_edge_queue = []
                        drag = False
                        if global_node:
                            global_node.clicked_off()
                            global_node = None

                    elif key_pressed[pygame.K_BACKSPACE] or key_pressed[pygame.K_LCTRL]:
                        self.__delete_node()
                        delete_edge_queue = []
                        global_node = None
                        drag = False
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
