import math
import time
import numpy as np
import pygame
import pygame_gui
from Utils import Utils
from pygame.locals import (
    RLEACCEL,
)

"""CONSTANTS"""
NODE_R: int = 40
LEFT_MOUSE: int = 1
Utils: Utils = Utils()
NODE_NAME = Utils.gen_letters()
SCREEN_SIZE = (1024, 900)  # width ,height
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)


class Node(pygame.sprite.Sprite):
    def __init__(self,
                 center: tuple[int, int],
                 all_nodes,  # OBJECT
                 draw: bool = True
                 ):
        super(Node, self).__init__()
        self.center = center
        self.surf = pygame.Surface((2 * NODE_R, 2 * NODE_R))
        self.text_view = pygame.font.SysFont("arial", 25, True, True).render("" if not draw else next(NODE_NAME), True,
                                                                             (255, 255, 255))
        self.is_clicked = False
        if draw:
            pygame.draw.circle(self.surf, 'Green', (NODE_R, NODE_R), NODE_R)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=self.center)
        self.all_nodes = all_nodes
        self.surf.blit(self.text_view, (NODE_R // 2 + 15, NODE_R // 2 + 10))
    def clicked_on(self):
        self.surf.fill(pygame.Color('Black'))
        pygame.draw.circle(self.surf, 'Red', (NODE_R, NODE_R), NODE_R)
        pygame.draw.circle(self.surf, 'Green',(NODE_R,NODE_R),NODE_R-2)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=self.center)
        self.surf.blit(self.text_view, (NODE_R // 2 + 15, NODE_R // 2 + 10))
        self.is_clicked = True
    def clicked_off(self):
        pygame.draw.circle(self.surf, 'Green', (NODE_R, NODE_R), NODE_R)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=self.center)
        self.surf.blit(self.text_view, (NODE_R // 2 + 15, NODE_R // 2 + 10))
        self.is_clicked = False
    def move(self, mouse_pos: tuple[int, int]):
        self.center = mouse_pos
        self.clicked_on()





class Edge(pygame.sprite.Sprite):
    def __init__(self,
                 node1: Node,
                 node2: Node,
                 start_point: tuple[int, int],
                 end_point: tuple[int, int],
                 weight: int = 0,
                 is_directed: bool = True,
                 edge_color: tuple[int, int, int] = WHITE_COLOR
                 ):
        super(Edge, self).__init__()
        self.source = node1
        self.destination = node2
        self.start_point = start_point
        self.end_point = end_point
        self.weight = weight
        self.is_directed = is_directed
        self.surf = pygame.Surface(SCREEN_SIZE)
        if self.is_directed:
            self.draw_arrow()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(1024 / 2, 900 / 2))

    def draw_arrow(self,
                   color: pygame.Color = WHITE_COLOR,
                   body_width: int = 4,
                   head_width: int = 15,
                   head_height: int = 15,
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

        pygame.draw.polygon(surface, color, head_verts)

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
            pygame.draw.polygon(surface, color, body_verts)


class Graph_Simulator:
    def __init__(self):
        self.graph: dict[Node, list[Edge]] = {}
        self.window_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        self.all_nodes = pygame.sprite.Group()
        self.all_graph = pygame.sprite.Group()
        self.all_edges = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

    def __is_an_edge(self, edge_lst: list[Edge], destination: Node):
        for edge in edge_lst:
            if edge.destination == destination:
                return True
        return False

    def __stabling_graph(self):
        pass
        # stable = [False for i in range(len(self.all_nodes))]  # |V| Trues
        # EPS = 0.1
        # K1, K2, l0 = 0.2, 0.3, 1000
        # validation = True
        # counter = 20
        # while counter != 0:
        #     counter -= 1
        #     index = 0
        #     for v in self.all_nodes:
        #         F = np.array([0, 0], dtype='float64')
        #         for u in self.all_nodes:
        #             if v != u:
        #                 direction = np.array(list(u.center)) - np.array(list(v.center), dtype='float64')
        #                 length = np.linalg.norm(direction)
        #                 direction /= length
        #                 my_k = K1 if self.__is_an_edge(self.graph[u], v) else K2
        #                 if length > l0:
        #                     F += direction * (length - l0) * my_k
        #                 else:
        #                     F -= direction * (length - l0) * my_k
        #                 vx, vy = v.center
        #                 if (vx + EPS * direction[0]) > 0 and (v.center[0] + EPS * direction[0]) < 1000:
        #                     vx += EPS * F[0]
        #                 if (vy + EPS * direction[1]) > 0 and (v.center[1] + EPS * direction[1]) < 900:
        #                     vy += EPS * F[1]
        #                 v.center = (vx, vy)
        #                 v.rect = v.surf.get_rect(center=v.center)
        #         if validation:
        #             stable[index] = True
        #         index += 1
        # import random
        # for u in self.all_graph:
        #
        #
        #
        # self.window_surface.fill(pygame.Color("black"))

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

    def __add_edge(self, position: tuple[int, int]):
        mid: Node = self.__is_in_node(position)
        if not mid:
            return
        start, end = 0, 0
        while True:
            self.clock.tick(60)
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
                                angle = 25
                                start, end = self.__calc_position(mid.center, tmp.center, -angle)
                                end1, end2 = self.__calc_position(tmp.center, mid.center, angle)
                                edge.start_point = start
                                edge.end_point = end1
                                edge.surf.fill(BLACK_COLOR)
                                edge.draw_arrow()
                                start, end = self.__calc_position(mid.center, tmp.center, angle)
                                end1, end2 = self.__calc_position(tmp.center, mid.center, -angle)
                                newEdge = Edge(mid, tmp, end1, start)
                                self.graph[mid].append(newEdge)
                                self.all_graph.add(newEdge)


                                # end1, end2 = self.__calc_position(mid.center, tmp.center, angle)
                                # start, end = self.__calc_position(pygame.mouse.get_pos(), mid.center, -angle)
                                # newEdge = Edge(mid, tmp, start, end1)
                                # self.graph[mid].append(newEdge)
                                # self.all_graph.add(newEdge)
                                # self.all_graph.remove(edge)
                                # self.graph[tmp].remove(edge)
                                # end1, end2 = self.__calc_position(tmp.center, mid.center, -angle)
                                # start, end = self.__calc_position(mid.center, tmp.center, angle)
                                # edge = Edge(tmp, mid, start, end1)
                                # self.all_graph.add(edge)
                                # self.graph[tmp].append(edge)

                                return
                        end1, end2 = self.__calc_position(mid.center, tmp.center)
                        edge = Edge(mid, tmp, start, end1)
                        self.graph[mid].append(edge)
                        self.all_graph.add(edge)
                        return
                    else:
                        self.window_surface.fill(pygame.Color("black"))
                        return

            self.window_surface.fill(pygame.Color("black"))
            for e in self.all_graph:
                self.window_surface.blit(e.surf, e.rect)
            start, end = self.__calc_position(pygame.mouse.get_pos(), mid.center)

            tmp_edge = Edge(None, None, start, end)
            self.window_surface.blit(tmp_edge.surf, tmp_edge.rect)
            pygame.display.flip()

    def run(self):
        pygame.init()
        pygame.display.set_caption('Graph Visualizer')
        background = pygame.Surface(SCREEN_SIZE)
        background.fill(pygame.Color(BLACK_COLOR))
        drag = False
        global_node : Node = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE:
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[pygame.K_LSHIFT]:
                        self.__add_edge(pygame.mouse.get_pos())
                        # self.all_graph.add(Edge(None, None, (1024, 900), pygame.mouse.get_pos()))
                    elif key_pressed[pygame.K_BACKSPACE]:
                        nd = self.__is_in_node(pygame.mouse.get_pos())
                        if nd:
                            for v in self.graph[nd]:
                                self.all_graph.remove(v)
                            self.graph.pop(nd)
                            self.all_graph.remove(nd)
                            self.all_nodes.remove(nd)
                            for node,edges in self.graph.items():
                                new_lst : list[Edge] = []
                                for edge in edges:
                                    if edge.destination != nd:
                                        new_lst.append(edge)
                                    else:
                                        self.all_graph.remove(edge)
                                if len(new_lst) != len(self.graph[node]):
                                    self.graph[node] = new_lst


                    else:
                        mouse_pos = pygame.mouse.get_pos()
                        nd = self.__is_in_node(mouse_pos)
                        if not nd:
                            node = Node(mouse_pos, self.all_nodes)
                            self.all_nodes.add(node)
                            self.all_graph.add(node)
                            self.graph[node] = []
                        else:
                            if not nd.is_clicked:
                                drag = True
                                global_node = nd
                                global_node.clicked_on()

                elif event.type == pygame.MOUSEMOTION:
                    if drag:
                        global_node.move(event.pos)
                        for node in self.graph.keys():
                            for edge in self.graph[node]:
                                if node == global_node:
                                    flag = False
                                    for edge1 in self.graph[edge.destination]:
                                        if edge1.destination == node:
                                            flag = True
                                            break
                                    angle = 0 if not flag else -25
                                    start, end = self.__calc_position(edge.destination.center, node.center, angle)
                                    end1, end2 = self.__calc_position(node.center, edge.destination.center, -angle)
                                    edge.start_point = start
                                    edge.end_point = end1
                                    edge.surf.fill(BLACK_COLOR)
                                    edge.draw_arrow()
                                elif edge.destination == global_node:
                                    flag = False
                                    for edge1 in self.graph[global_node]:
                                        if edge1.destination == node:
                                            flag = True
                                            break
                                    angle = 0 if not flag else -25
                                    start, end = self.__calc_position(node.center, edge.destination.center, -angle)
                                    end1, end2 = self.__calc_position( edge.destination.center, node.center, angle)
                                    edge.start_point = end1
                                    edge.end_point = start
                                    edge.surf.fill(BLACK_COLOR)
                                    edge.draw_arrow()

                        # for edge in self.graph[global_node]:
                        #     print('here')
                        #     for e in self.graph[edge.destination]:
                        #         if e.destination == global_node:
                        #
                        #             start, end = self.__calc_position(edge.destination.center, global_node.center,45)
                        #             end1, end2 = self.__calc_position(global_node.center, edge.destination.center,-45)
                        #         else:
                        #             start, end = self.__calc_position(edge.destination.center, global_node.center)
                        #             end1, end2 = self.__calc_position(global_node.center, edge.destination.center)
                        #
                        #     edge.start_point = start
                        #     edge.end_point = end1
                        #     edge.surf.fill(BLACK_COLOR)
                        #     edge.draw_arrow()
                        # for node in self.graph:
                        #     if node != global_node:
                        #         for edge in self.graph[node]:
                        #             if edge.destination == global_node:
                        #                 start, end = self.__calc_position(global_node.center, node.center)
                        #                 end1, end2 = self.__calc_position(node.center, global_node.center)
                        #
                        #                 edge.start_point = start
                        #                 edge.end_point = end1
                        #                 edge.surf.fill(BLACK_COLOR)
                        #                 edge.draw_arrow()


                elif event.type == pygame.MOUSEBUTTONUP:
                    if drag:
                        drag = False
                        global_node.clicked_off()
                        global_node = None








            self.window_surface.fill(pygame.Color('Black'))
            for e in self.all_graph:
                self.window_surface.blit(e.surf, e.rect)
                # e.update2()
            # for e in all_graph:
            #     while True:
            #         tmp_group = pygame.sprite.Group()
            #         tmp_group.add(e)
            #         collision = pygame.sprite.groupcollide(tmp_group,all_graph,False ,False)
            #         for our , collided in collision:
            #             collided.remove(our)
            #
            #
            #         if pygame.sprite.spritecollideany(e, all_graph) != e:
            #             while pygame.sprite.spritecollide()
            pygame.display.flip()
            self.clock.tick(60)
