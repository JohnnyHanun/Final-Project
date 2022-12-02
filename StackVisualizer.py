import pygame
import pygame_gui
import sys
from tkinter import messagebox

SCREEN_SIZE = (1024, 900)  # width ,height

class StackVisualizer:
    def __init__(self):
        self.stack = []
        self.limit = 20
        self.stack_body = (350, 80, 300, 570) # x, y, width, height
        self.stack_position = (400, 200, 512, 220)  # x, y, width, height

    def push(self, element: str) -> None:
        if len(element) <= self.limit and element != "":
            self.stack.append(element)

    def pop(self):
        if not self.stack:
            raise Exception("Stack is Empty , Nothing to Pop!")
        return self.stack.pop()

    def top(self):
        if not self.stack:
            return self.stack[-1]

    def run(self):
        pygame.init()
        pygame.display.set_caption('Stack Visualizer')
        window_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        background = pygame.Surface(SCREEN_SIZE)
        background.fill(pygame.Color('#000000'))
        manager = pygame_gui.UIManager(SCREEN_SIZE, 'theme.json')
        container = pygame_gui.core.ui_container.UIContainer(window_surface.get_rect(), manager=manager)
        push_button_layout_rect = pygame.Rect(0, 0, 200, 80)
        push_button_layout_rect.bottomleft = (30, -50)
        push_button = pygame_gui.elements.UIButton(relative_rect=push_button_layout_rect,
                                                   text='Push', manager=manager, container=container
                                                   , anchors={'left': 'left', 'bottom': 'bottom'}, object_id="#button")
        pop_button_layout_rect = pygame.Rect(0, 0, 200, 80)
        pop_button_layout_rect.bottomright = (-30, -50)
        pop_button = pygame_gui.elements.UIButton(relative_rect=pop_button_layout_rect,
                                                  text='Pop', manager=manager, container=container,
                                                  anchors={'right': 'right', 'bottom': 'bottom'})
        text_input_layout_rect = pygame.Rect(0, 0, 300, 80)
        text_input_layout_rect.bottomright = (-500, -50)
        text_input_layout_rect.bottomleft = (120, -50)
        text_input = pygame_gui.elements.UITextEntryLine(relative_rect=text_input_layout_rect,
                                                         manager=manager, object_id='#text_entry',
                                                         anchors={'bottom': 'bottom', 'left_target': push_button,
                                                                  'left': 'left', 'right': 'right',
                                                                  'right_target': pop_button})
        text_input.set_text_length_limit(self.limit)
        stack_body = pygame.Rect(self.stack_body)
        text_input.hide()
        text_flag = False
        text_input_guide = pygame.font.SysFont("arial", 30, True, True, ).render(
            "Please Enter an input up to 20 characters, Then press "
            "enter to push it:", True, (255, 255, 255))
        clock = pygame.time.Clock()
        while True:
            time_delta = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print("My Vrend")
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#text_entry':
                    text_flag = False
                    text_input.hide()
                    text_input.clear()
                    text_input.unfocus()
                    self.push(event.text)
                    print(self.stack)
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == pop_button:
                    try:
                        print(self.pop())
                    except Exception as e:
                        messagebox.askokcancel("Error",str(e),icon="error")
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == push_button:
                    text_flag = True
                    text_input.show()
                    text_input.focus()
                manager.process_events(event)
                manager.update(time_delta)
                window_surface.blit(background, (0, 0))
                pygame.draw.rect(window_surface, (0, 255, 0), stack_body, 5, border_top_right_radius=0)#dont touch
                pygame.draw.rect(window_surface, (232, 139, 0), pygame.Rect((355,590,290,55)), 5, border_top_right_radius=0)
                pygame.draw.rect(window_surface, (51, 255, 255), pygame.Rect((355, 590-56, 290, 55)), 5,border_top_right_radius=0)
                pygame.draw.rect(window_surface, (232, 139, 0), pygame.Rect((355, 590 - 56*2, 290, 55)), 5,border_top_right_radius=0)
                pygame.draw.rect(window_surface, (51, 255, 255), pygame.Rect((355, 590 - 56*3, 290, 55)), 5,border_top_right_radius=0)
                pygame.draw.rect(window_surface, (232, 139, 0), pygame.Rect((355, 590 - 56*4, 290, 55)), 5,border_top_right_radius=0)
                pygame.draw.rect(window_surface, (197, 39, 189), pygame.Rect((355, 590 - 56*5, 290, 55)), 5,border_top_right_radius=0)
                pygame.draw.rect(window_surface, (51, 255, 255), pygame.Rect((355, 590 - 56*6, 290, 55)), 5,border_top_right_radius=0)
                pygame.draw.rect(window_surface, (197, 39, 189), pygame.Rect((355, 590 - 56*7, 290, 55)), 5,border_top_right_radius=0)
                pygame.draw.rect(window_surface, (51, 255, 255), pygame.Rect((355, 590 - 56*8, 290, 55)), 5,border_top_right_radius=0)
                pygame.draw.rect(window_surface, (197, 39, 189), pygame.Rect((355, 590 - 56*9, 290, 55)), 5,border_top_right_radius=0)
                if text_flag:
                    window_surface.blit(text_input_guide, (0, 0))
                manager.draw_ui(window_surface)
            pygame.display.update()
