from Graph import Graph_Simulator
from Utils import Utils
from threading import Thread
# import pygame
#
# # Initialize Pygame
# pygame.init()
#
# # Set the screen size
# screen_width, screen_height = 800, 600
# screen = pygame.display.set_mode((screen_width, screen_height))
#
# # Set the line parameters
# line_start = (250, 10)
# line_end = (10, 250)
# line_width = 5
#
# # Draw the line
# pygame.draw.line(screen, (255, 255, 255), line_start, line_end, line_width)
#
# # Set the font and size
# font = pygame.font.SysFont('Arial',25)
#
# # Calculate the midpoint of the line
# midpoint = ((line_start[0] + line_end[0]) // 2, (line_start[1] + line_end[1]) // 2)
#
# # Render the text surface
# text_surface = font.render('10', True, (255, 255, 255))
#
# # Get the dimensions of the text surface
# text_width, text_height = text_surface.get_size()
# print(text_surface.get_size())
# # Blit the text surface onto the screen
# screen.blit(text_surface, (midpoint[0] + text_width , midpoint[1] ))
#
# # Update the display
# pygame.display.update()
#
# # Run the game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
# # Quit Pygame
# pygame.quit()
#



if __name__ == '__main__':
    #s = Utils().graph_parser(r'C:\Users\yoyom\Desktop\gonen_graph2.txt')
    #print(s)
    #Graph_Simulator(r'C:\Users\yoyom\Desktop\gonen_graph3.txt').run()
    Graph_Simulator(r'C:\Users\yoyom\Desktop\gonen_graph2.txt').run()
import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Cross from Line Example")

# Define the color of the cross
color = (255, 0, 0)

# Define the endpoints of the given line
x1, y1 = 100, 200
x2, y2 = 300, 200

# Find the midpoint of the given line
midpoint = ((x1 + x2) // 2, (y1 + y2) // 2)

# Find the angle of the given line in radians
angle = math.atan2(y2 - y1, x2 - x1)

# Calculate the endpoints of the vertical line of the cross
vline_x1 = midpoint[0] - 50 * math.sin(angle)
vline_y1 = midpoint[1] - 50 * math.cos(angle)
vline_x2 = midpoint[0] + 50 * math.sin(angle)
vline_y2 = midpoint[1] + 50 * math.cos(angle)

# Calculate the endpoints of the horizontal line of the cross
hline_x1 = midpoint[0] - 50 * math.cos(angle)
hline_y1 = midpoint[1] + 50 * math.sin(angle)
hline_x2 = midpoint[0] + 50 * math.cos(angle)
hline_y2 = midpoint[1] - 50 * math.sin(angle)

# Draw the vertical line of the cross
pygame.draw.line(screen, color, (vline_x1, vline_y1), (vline_x2, vline_y2), 5)

# Draw the horizontal line of the cross
pygame.draw.line(screen, color, (hline_x1, hline_y1), (hline_x2, hline_y2), 5)

# Update the screen
pygame.display.flip()

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()







