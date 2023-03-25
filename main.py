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







