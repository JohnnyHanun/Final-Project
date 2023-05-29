import pygame
import pygame_gui
import pygame_menu
from constants import *

from typing import Dict, Union, Optional, List

theme = pygame_menu.Theme(
    background_color=(192, 192, 192),
    cursor_color=(255, 255, 255),
    cursor_selection_color=(80, 80, 80, 120),
    scrollbar_color=(39, 41, 42),
    scrollbar_slider_color=(65, 66, 67),
    scrollbar_slider_hover_color=(90, 89, 88),
    selection_color=(255, 255, 255),
    title_background_color=(47, 48, 51),
    title_font_color=(215, 215, 215),
    widget_font_color=(200, 200, 200),
    widget_selection_effect=pygame_menu.widgets.NoneSelection()
)


class StackElement:
    def __init__(self,
                 window_surface: pygame.Surface,
                 text: str,
                 element_color: str,
                 text_color: tuple[int, int, int] = WHITE_COLOR,
                 font_size: int = 23):
        self.element: pygame.Rect = pygame.Rect(ELEMENT_POS)
        self.text_pos: tuple[float, float] = TEXT_POS  # text_pos
        self.element_color = element_color
        self.__text = text
        self.text_view = pygame.font.SysFont("arial", font_size, True, True).render(text, True, text_color)
        self.windows_surface = window_surface

    def show(self):
        pygame.draw.rect(self.windows_surface, self.element_color, self.element)
        self.windows_surface.blit(self.text_view, self.text_pos)

    def update(self, element_tracker: int):
        x, y, w, h = ELEMENT_POS
        y = y - h * (element_tracker % NINE) - NINE
        x1, y1 = TEXT_POS
        y1 = y1 - h * (element_tracker % NINE) - NINE
        x1 = x1 - len(self.__text) * 4
        self.text_pos = (x1, y1)
        self.element = pygame.Rect((x, y, w, h))
        return self

    def pushAnimation(self, element_tracker: int, speed: int = TEN):
        clock = pygame.time.Clock()
        rect = pygame.Rect(STARTING_POS)
        x, y, w, h = ELEMENT_POS
        y = y - h * (element_tracker % NINE) - NINE
        x1, y1 = TEXT_POS
        y1 = y1 - h * (element_tracker % NINE) - NINE
        x1 = x1 - len(self.__text) * 4
        self.text_pos = (x1, y1)
        self.element = pygame.Rect((x, y, w, h))
        while rect.y <= y + h:
            clock.tick(30)
            if rect.y <= y + h:
                rect.y += speed
            pygame.draw.rect(self.windows_surface, self.element_color, rect)
            self.windows_surface.blit(self.text_view, (x1, rect.y))

            # Updating the display surface
            pygame.display.update()
            # to delete the old rect
            self.windows_surface.fill(color=BLACK_COLOR, rect=rect)

        return self

    def popAnimation(self, speed: int = TEN):
        clock = pygame.time.Clock()
        rect = pygame.Rect(self.element)
        prev_rect = pygame.Rect(self.element)

        y = STARTING_POS[1]
        while rect.y > y:
            clock.tick(30)
            if rect.y > y:
                prev_rect.y = rect.y
                rect.y -= speed
            pygame.draw.rect(self.windows_surface, self.element_color, rect)
            self.windows_surface.blit(self.text_view, (self.text_pos[0], rect.y))

            # Updating the display surface
            pygame.display.update()
            # to delete the old rect
            self.windows_surface.fill(color=BLACK_COLOR, rect=prev_rect)

        return self

    def __str__(self):
        return self.__text


class StackVisualizer:
    def __init__(self, menu=None):
        self.stack: list[StackElement] = []
        self.limit = 15
        self.element_tracker = 0
        SCREEN_SIZE1 = (1024, 900)
        self.window_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        self.stack_body = (350, 80, 300, 560)  # x, y, width, height
        self.stack_position = (400, 200, 512, 220)  # x, y, width, height
        self.main_menu = menu
        self.animation_speed = TEN
        self.__setup_menu()


    def __setup_menu(self):

        def button_onmouseover(w: 'pygame_menu.widgets.Widget', _) -> None:
            """
            Set the background color of buttons if entered.
            """
            if w.get_id() == 'pop' or w.get_id() == 'ClearStack':
                w.set_background_color((255, 102, 102))
            else:
                w.set_background_color((153, 255, 153))

        def button_onmouseleave(w: 'pygame_menu.widgets.Widget', _) -> None:
            """
            Set the background color of buttons if leaved.
            """
            if w.get_id() == 'pop' or w.get_id() == 'ClearStack':
                w.set_background_color(RED)
            else:
                w.set_background_color((0, 204, 0))

        self.menu = pygame_menu.Menu("Stack Menu", 300, 847, theme=theme, position=(100, 0))
        text_input = self.menu.add.text_input(
            '',
            maxwidth=10,
            textinput_id='text_input',
            input_underline='_',
            repeat_keys=False,
            font_color=WHITE_COLOR,
            repeat_keys_interval_ms=1000)
        text_input.translate(0, 25 + 50)
        btn = self.menu.add.button("   Push   ", self.push, border_color=ORANGE, font_color=BLACK_COLOR,
                                   font_size=30,
                                   button_id='push',
                                   background_color=(0, 204, 0), cursor=pygame_menu.locals.CURSOR_HAND)
        btn.set_onmouseover(button_onmouseover)
        btn.set_onmouseleave(button_onmouseleave)
        btn1 = self.menu.add.button("   Pop   ", self.pop, border_color=WHITE_COLOR, font_color=BLACK_COLOR,
                                    font_size=30,
                                    button_id='pop',
                                    background_color=RED, cursor=pygame_menu.locals.CURSOR_HAND)
        btn1.set_onmouseover(button_onmouseover)
        btn1.set_onmouseleave(button_onmouseleave)
        btn.translate(-65, 49 + 50)
        btn1.translate(70, 0 + 50)
        btn4 = self.menu.add.button("Clear Stack", self.__clear_stack, border_color=WHITE_COLOR,
                                    font_color=BLACK_COLOR,
                                    font_size=30,
                                    button_id='ClearStack',
                                    background_color=RED, cursor=pygame_menu.locals.CURSOR_HAND)
        btn4.set_onmouseover(button_onmouseover)
        btn4.set_onmouseleave(button_onmouseleave)
        btn4.translate(0, 60 + 50)

        btn6 = self.menu.add.range_slider('', 10, (0, 50), 1,
                                          font_color=BLACK_COLOR,
                                          background_color=WHITE_COLOR,
                                          width=200,
                                          range_text_value_color=BLACK_COLOR,
                                          font_size=25,
                                          padding=10,
                                          rangeslider_id='range_slider',
                                          value_format=lambda x: str(int(x)))

        btn6.set_onchange(self.__set_animation_speed)
        btn7 = self.menu.add.label('Animation Speed: ' + str(2000 - self.animation_speed),
                                   font_size=20, font_color=BLACK_COLOR, label_id='speed_label')
        btn6.translate(0, -400)
        btn7.translate(0, -405)
        ############ Error Menu ############

        self.__submenu = pygame_menu.Menu('Error!', 450, 200, theme=theme,
                                          mouse_motion_selection=True, center_content=False)
        self.__submenu.add.label('Stack is empty', font_size=40, font_color=BLACK_COLOR)

        def error():
            self.__submenu.disable()
            self.menu.enable()

        go_back = self.__submenu.add.button('OK', error, border_color=ORANGE, font_color=BLACK_COLOR,
                                            font_size=30,
                                            button_id='ok',
                                            background_color=(0, 204, 0), cursor=pygame_menu.locals.CURSOR_HAND)
        go_back.set_onmouseover(button_onmouseover)
        go_back.set_onmouseleave(button_onmouseleave)
        ############ Error Menu ############

    def __set_animation_speed(self, *args):
        self.animation_speed = int(args[0])
        text_input: pygame_menu.widgets.widget.label.Label = self.menu.get_widget('speed_label')
        text_input.set_title('Animation Speed: ' + str(self.animation_speed))

    def push(self) -> None:
        text_input: pygame_menu.widgets.widget.textinput.TextInput = self.menu.get_widget('text_input')
        value = text_input.get_value()
        if len(value) <= self.limit and value != "":
            COLOR = ELEMENT_COLOR1 if (self.element_tracker % TEN) % 2 == 0 else ELEMENT_COLOR2
            self.element_tracker += 1
            index = self.element_tracker if (self.element_tracker < NINE) else 8
            self.stack.append(StackElement(window_surface=self.window_surface,
                                           text=value, element_color=COLOR).pushAnimation(index,
                                                                                          speed=self.animation_speed))
            text_input.clear()
            return

    def pop(self):
        if not self.stack:
            self.__submenu.enable()
            while self.__submenu.is_enabled():
                self.__submenu.mainloop(self.window_surface, disable_loop=False)
            return
        self.stack[-1].popAnimation(speed=self.animation_speed)
        self.element_tracker -= 1
        return self.stack.pop()

    def top(self):
        if not self.stack:
            return self.stack[-1]

    def __show(self):
        index: int = 0
        for element in self.stack[-NINE:]:
            element.update(index).show()
            index += 1

    def __refresh_screen(self, events):
        self.menu.update(events)
        self.window_surface.fill(BLACK_COLOR)
        self.menu.draw(self.window_surface)
        pygame.draw.rect(self.window_surface, STACK_COLOR, self.stack_body, 5,
                         border_top_right_radius=0)
        self.__show()
        pygame.display.update()

    def __clear_stack(self):
        if not self.stack:
            self.__submenu.enable()
            while self.__submenu.is_enabled():
                self.__submenu.mainloop(self.window_surface, disable_loop=False)
            return
        while self.stack:
            self.pop()
            self.__refresh_screen([])

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        while True:
            time_delta = clock.tick(60) / 1000
            events = pygame.event.get()
            keyboard = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu.enable()
                        pygame.display.set_mode(SCREEN_SIZE)
                        return
                if event.type == pygame.KEYDOWN and keyboard[pygame.K_RETURN] or event.__dict__.get('key') and \
                        event.__dict__['key'] == RIGHT_ENTER_KEY:
                    self.menu.get_widget('push').apply()
                if event.type == pygame.KEYDOWN and keyboard[pygame.K_DELETE]:
                    self.menu.get_widget('pop').apply()
            self.__refresh_screen(events)
