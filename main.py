# import pygame
# import pygame_gui
# import time
# pygame.init()
#
# pygame.display.set_caption('Quick Start')
# window_surface = pygame.display.set_mode((800, 600))
#
# background = pygame.Surface((800, 600))
# background.fill(pygame.Color('#456321'))
# s=pygame.font.SysFont("arial",50).render("Bruh",False,(255,255,255))
# manager = pygame_gui.UIManager((800, 600))
# hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),manager=manager,
#                                             text='Say Hello',
#                                             )
#
# clock = pygame.time.Clock()
# is_running = True
# flag = False
# while is_running:
#     time_delta = clock.tick(60) / 1000.0
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             is_running = False
#         if event.type == pygame_gui.UI_BUTTON_PRESSED:
#             if event.ui_element == hello_button:
#                 flag = not flag
#
#         manager.process_events(event)
#         manager.update(time_delta)
#         window_surface.blit(background, (0, 0))
#         if flag:
#             window_surface.blit(s, (360, 340))
#         manager.draw_ui(window_surface)
#     pygame.display.update()
# # import the pygame module, so you can use it
# # import pygame
# # import pygame_gui
#
# # define a main function
# # def main():
# #     # initialize the pygame module
# #     pygame.init()
# #     # load and set the logo
# #     pygame.display.set_caption("minimal program")
# #     user_text = ''
# #     input_rect = pygame.Rect(200, 200, 140, 32)
# #     active = False
# #     # create a surface on screen that has the size of 240 x 180
# #     screen = pygame.display.set_mode((1024, 800),pygame.RESIZABLE)
# #     color_active = pygame.Color('lightskyblue3')
# #     # define a variable to control the main loop
# #     running = True
# #     color_passive = pygame.Color('chartreuse4')
# #     color = color_passive
# #     # main loop
# #     mousePos = (0, 0)
# #     while running:
# #         # event handling, gets all event from the event queue
# #         for event in pygame.event.get():
# #             # only do something if the event is of type QUIT
# #             if event.type == pygame.QUIT:
# #                 # change the value to False, to exit the main loop
# #                 running = False
# #
# #             if event.type == pygame.MOUSEBUTTONDOWN:
# #                 mousePos = pygame.mouse.get_pos()
# #                 if input_rect.collidepoint(event.pos):
# #                     active = True
# #                 else:
# #                     active = False
# #
# #             if event.type == pygame.KEYDOWN:
# #
# #                 # Check for backspace
# #                 if event.key == pygame.K_BACKSPACE:
# #
# #                     print(user_text)
# #                     # get text input from 0 to -1 i.e. end.
# #                     user_text = user_text[:-1]
# #
# #                 # Unicode standard is used for string
# #                 # formation
# #                 else:
# #                     user_text += event.unicode
# #         # Drawing Rectangle
# #         x = 400
# #         y = 200
# #         h = 512
# #         w = 220
# #         green = (0, 255, 0)
# #         blue = (255, 255, 255)
# #
# #         font = pygame.font.Font('freesansbold.ttf', 20)
# #
# #         text = font.render(user_text, True, green, blue)
# #         pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x, y, w, h), 2, border_top_right_radius=0)
# #         screen.blit(text, mousePos)
# #         # pygame.draw.circle(screen, green, mousePos, 50)
# #         pygame.draw.line(screen, (255, 255, 255), (x, y + 30), (x + w, y + 30), 4)
# #         pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x + w, y + 60), 4)
# #         pygame.draw.line(screen, (255, 255, 255), (x, y + 90), (x + w, y + 90), 4)
# #         pygame.display.flip()
# #
# #
# # # run the main function only if this module is executed as the main script
# # # (if you import this as a module then nothing is executed)
# # if __name__ == "__main__":
# #     main()
import StackVisualizer



from Utils import  Utils
if __name__ == "__main__":
    #StackVisualizer.StackVisualizer().run()
    for i in gen:
        print(i)

