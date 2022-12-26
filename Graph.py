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
                 all_nodes  # OBJECT
                 ):
        super(Node, self).__init__()
        self.center = center
        self.surf = pygame.Surface((2 * NODE_R, 2 * NODE_R))
        self.text_view = pygame.font.SysFont("arial", 25, True, True).render(next(NODE_NAME), True, (255, 255, 255))
        pygame.draw.circle(self.surf, 'Green', (NODE_R, NODE_R), NODE_R)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=self.center)
        self.all_nodes = all_nodes

    def update2(self):
        # print(self.rect.x,self.rect.y,self.rect.width,self.rect.height)
        self.surf.blit(self.text_view, (NODE_R // 2 + 15, NODE_R // 2 + 10))


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
            self.__draw_arrow()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(1024/2,900/2))

    def __draw_arrow(self,
            color: pygame.Color = WHITE_COLOR,
            body_width: int = 4,
            head_width: int = 15,
            head_height: int = 15,
    ):
        start , end ,surface = pygame.Vector2(self.start_point) , pygame.Vector2(self.end_point), self.surf
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
        self.graph: dict[Node, list[Node]] = {}
        self.window_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)

    def run(self):
        pygame.init()
        pygame.display.set_caption('Graph Visualizer')
        background = pygame.Surface(SCREEN_SIZE)
        background.fill(pygame.Color(BLACK_COLOR))
        clock = pygame.time.Clock()
        all_nodes = pygame.sprite.Group()
        all_graph = pygame.sprite.Group()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE:
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[pygame.K_LSHIFT]:
                        # pygame.draw.polygon(self.window_surface, ,
                        # ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0),
                        # (200, 100)))
                        all_graph.add(Edge(None,None,(1024, 900),pygame.mouse.get_pos()))
                    else:
                        node = Node(pygame.mouse.get_pos(), all_nodes)
                        all_nodes.add(node)
                        all_graph.add(node)
                # if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                # self.window_surface.blit(background, (0, 0))
            # pygame.display.update()
            # self.window_surface.fill('black')
            for e in all_graph:
                self.window_surface.blit(e.surf, e.rect)
                #e.update2()
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
            clock.tick(60)
