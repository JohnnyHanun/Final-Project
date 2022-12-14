import pygame
import pygame_gui
from tkinter import messagebox
import tkinter
root = tkinter.Tk()
root.withdraw()

""" CONSTANTS """
SCREEN_SIZE = (1024, 900)  # width ,height
WHITE_COLOR = (255, 255, 255)
GREY_COLOR = (128, 128, 128)
TEXT_COLOR = (127, 0, 255)
ELEMENT_POS = (355, 590, 290, 55)  # x , y , width , height
TEXT_POS = (482.5, 590)
TEN = 10


class StackElement:
    def __init__(self,
                 window_surface: pygame.Surface,
                 text: str,
                 element_color: tuple[int, int, int],
                 text_color: tuple[int, int, int] = TEXT_COLOR,
                 font_size: int = 20):
        self.element: pygame.Rect = pygame.Rect(ELEMENT_POS)
        self.text_pos: tuple[float, float] = TEXT_POS  # text_pos
        self.element_color = element_color
        self.__text = text
        self.text_view = pygame.font.SysFont("arial", font_size, True, True).render(text, True, text_color)
        self.windows_surface = window_surface

    # def set_pos(self,text_pos: tuple[int, int], ):
    def show(self):
        pygame.draw.rect(self.windows_surface, self.element_color, self.element)
        self.windows_surface.blit(self.text_view, self.text_pos)

    def update(self, element_tracker: int):
        x, y, w, h = ELEMENT_POS
        y = y - h * (element_tracker % TEN) - TEN
        x1, y1 = TEXT_POS
        y1 = y1 - h * (element_tracker % TEN) - TEN
        x1 = x1 - len(self.__text) * 4
        self.text_pos = (x1, y1)
        self.element = pygame.Rect((x, y, w, h))
        return self

    def __str__(self):
        return self.__text


class StackVisualizer:
    def __init__(self):
        self.stack: list[StackElement] = []
        self.limit = 20
        self.element_tracker = 0
        self.window_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        self.stack_body = (350, 80, 300, 560)  # x, y, width, height
        self.stack_position = (400, 200, 512, 220)  # x, y, width, height

    def push(self, element: str) -> None:
        if len(element) <= self.limit and element != "":
            COLOR = WHITE_COLOR if (self.element_tracker % TEN) % 2 == 0 else GREY_COLOR
            self.element_tracker += 1
            self.stack.append(StackElement(window_surface=self.window_surface,
                                           text=element, element_color=COLOR).update(self.element_tracker))

    def pop(self):
        if not self.stack:
            raise Exception("Stack is Empty , Nothing to Pop!")
        self.element_tracker -= 1
        return self.stack.pop()

    def top(self):
        if not self.stack:
            return self.stack[-1]

    def __show(self):
        index: int = 0
        for element in self.stack[-TEN:]:
            element.update(index).show()
            index += 1

    def run(self):
        pygame.init()
        pygame.display.set_caption('Stack Visualizer')
        background = pygame.Surface(SCREEN_SIZE)
        background.fill(pygame.Color('#000000'))
        manager = pygame_gui.UIManager(SCREEN_SIZE, 'theme.json')
        container = pygame_gui.core.ui_container.UIContainer(self.window_surface.get_rect(), manager=manager)
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
        text_input_guide = pygame.font.SysFont("arial", 30, True, True).render(
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
                        messagebox.askokcancel("Error", str(e), icon="error")
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == push_button:
                    text_flag = True
                    text_input.show()
                    text_input.focus()
                manager.process_events(event)
                manager.update(time_delta)
                self.window_surface.blit(background, (0, 0))
                pygame.draw.rect(self.window_surface, (0, 255, 0), stack_body, 5,
                                 border_top_right_radius=0)  # dont touch
                # pygame.draw.rect(self.window_surface, (255, 255, 255), pygame.Rect((355, 590-10, 290, 55)))
                # pygame.draw.rect(self.window_surface, (128, 128, 128), pygame.Rect((355, 590 - 55-10, 290, 55)))
                # pygame.draw.rect(self.window_surface, (255, 255, 255), pygame.Rect((355, 590 - 55 * 2-10, 290, 55)))
                # pygame.draw.rect(self.window_surface, (128, 128, 128), pygame.Rect((355, 590 - 55 * 3-10, 290, 55)))
                # pygame.draw.rect(self.window_surface, (255, 255, 255), pygame.Rect((355, 590 - 55 * 4-10, 290, 55)))
                # pygame.draw.rect(self.window_surface, (128, 128, 128), pygame.Rect((355, 590 - 55 * 5-10, 290, 55)))
                # pygame.draw.rect(self.window_surface, (255, 255, 255), pygame.Rect((355, 590 - 55 * 6-10, 290, 55)))
                # pygame.draw.rect(self.window_surface, (128, 128, 128), pygame.Rect((355, 590 - 55 * 7-10, 290, 55)))
                # pygame.draw.rect(self.window_surface, (255, 255, 255), pygame.Rect((355, 590 - 55 * 8-10, 290, 55)))
                # pygame.draw.rect(self.window_surface, (128, 128, 128), pygame.Rect((355, 590 - 55 * 9-10, 290, 55)))
                self.__show()
                if text_flag:
                    self.window_surface.blit(text_input_guide, (0, 0))
                manager.draw_ui(self.window_surface)
            pygame.display.update()
