from Graph import Graph_Simulator
if __name__ == '__main__':
    Graph_Simulator().run()

    # pygame.init()
    #
    # CLOCK = pygame.time.Clock()
    # FPS = 60
    #
    # WIDTH = 1280
    # HEIGHT = 720
    # RESOLUTION = (WIDTH, HEIGHT)
    # SCREEN = pygame.display.set_mode(RESOLUTION)
    #
    # while True:
    #     CLOCK.tick(FPS)
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             exit()
    #
    #     SCREEN.fill(pygame.Color("black"))
    #
    #     center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
    #     end = pygame.Vector2(pygame.mouse.get_pos())
    #     draw_arrow(SCREEN, center, end, pygame.Color("dodgerblue"), 10, 20, 12)
    #
    #     pygame.display.flip()

# import pygame
# import math
# # Initialize Pygame
# pygame.init()
#
# # Set the window dimensions
# window_width = 640
# window_height = 480
#
# # Create a Pygame window
# screen = pygame.display.set_mode((window_width, window_height))
#
# # Set the start and end points for the directed edge
# start_point = (100, 100)
# end_point = (200, 200)
# m = (start_point[1] - end_point[1]) / (start_point[0] - end_point[0])
# n = start_point[1] + (-1)*m*start_point[0]
# m_meshik = (-1)/m
# n_meshik = end_point[1] + (-1)*m_meshik*end_point[0]
#
# print(m,n)
# print(m_meshik,n_meshik)
# # Set the line thickness and color
# line_thickness = 2
# line_color = (255, 255, 255)  # red
#
# pygame.draw.line(screen, line_color, start_point, end_point, line_thickness)
# pygame.draw.polygon(screen, line_color, [(205,205), (205,195), (195,205)])
#
# # Update the Pygame display
# pygame.display.flip()
#
# # Run the Pygame loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
# # Quit Pygame
# pygame.quit()

import pygame

def draw_arrow(
        surface: pygame.Surface,
        start: pygame.Vector2,
        end: pygame.Vector2,
        color: pygame.Color,
        body_width: int = 2,
        head_width: int = 4,
        head_height: int = 2,
    ):
    """Draw an arrow between start and end with the arrow head at the end.

    Args:
        surface (pygame.Surface): The surface to draw on
        start (pygame.Vector2): Start position
        end (pygame.Vector2): End position
        color (pygame.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        head_width (int, optional): Defaults to 4.
        head_height (float, optional): Defaults to 2.
    """
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


pygame.init()

CLOCK = pygame.time.Clock()
FPS = 60

WIDTH = 1280
HEIGHT = 720
RESOLUTION = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(RESOLUTION)

while True:
    CLOCK.tick(FPS)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    SCREEN.fill(pygame.Color("black"))

    center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
    end = pygame.Vector2(pygame.mouse.get_pos())
    draw_arrow(SCREEN, center, end, pygame.Color("dodgerblue"), 10, 20, 12)

    pygame.display.flip()

