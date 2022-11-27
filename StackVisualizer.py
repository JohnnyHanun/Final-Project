import pygame
import pygame_gui
from pygame_gui.elements import ui_window

SCREEN_SIZE = (1024, 800)


class StackVisualizer:
    def __init__(self):
        self.stack = []
        self.limit = 20
        self.stack_position = (400, 200, 512, 220)  # x,y,h,w h -> height w->width

    def push(self, element: str) -> None:
        if len(element) <= self.limit:
            self.stack.append(element)
        else:
            raise Exception

    def pop(self):
        if not self.stack:
            raise Exception("Stack Empty, Nothing to pop.")
        return self.stack.pop()

    def top(self):
        if not self.stack:
            return self.stack[-1]

    def run(self):
        pygame.init()
        pygame.display.set_caption('Stack Visualizer')
        window_surface = pygame.display.set_mode(SCREEN_SIZE)
        background = pygame.Surface(SCREEN_SIZE)
        background.fill(pygame.Color('#000000'))
        manager = pygame_gui.UIManager(SCREEN_SIZE,'theme.json')
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
        text_input_layout_rect = pygame.Rect(0, 0, 200, 80)
        text_input_layout_rect.bottomright = (-500, -50)
        text_input_layout_rect.bottomleft = (150, -50)
        text_input = pygame_gui.elements.UITextEntryLine(relative_rect=text_input_layout_rect,
                                                          manager=manager, object_id='#text_entry',
                                                         anchors={'bottom': 'bottom', 'left_target': push_button,
                                                                  'left': 'left', 'right': 'right',
                                                                  'right_target': pop_button})
        container.add_element(pop_button)
        container.add_element(push_button)
        text_input.hide()

        text_flag = False
        text_input_guide = pygame.font.SysFont("arial", 30).render(
            "Please Enter an input up to 20 characters, Then press "
            "enter to push it:", False, (255, 255, 255))
        clock = pygame.time.Clock()
        while True:
            time_delta = clock.tick(60)/100
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#text_entry':
                    print('push button1')
                    text_flag = False
                    if event.text != "":
                        self.push(event.text)
                        text_input.hide()
                        text_input.clear()
                        print(self.stack)
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == pop_button:
                    try:
                        print(self.pop())
                    except Exception as e:
                        print(e)
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == push_button:
                    print('push button')
                    text_flag = True
                    text_input.show()

                manager.process_events(event)
                manager.update(time_delta)
                window_surface.blit(background, (0, 0))
                if text_flag:
                    window_surface.blit(text_input_guide, (0, 0))
                manager.draw_ui(window_surface)
            pygame.display.update()
