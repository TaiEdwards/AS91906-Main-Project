#INIT
from os.path import exists
import pygame
import random
import debug
from imagelist import ImageList
from mysprite import MySprite
import sys

# CONSTANTS
screen_width = 1920
screen_height = 1009
WINDOWMODE = pygame.RESIZABLE
qutting = False
FPS = 60
mouse_down = False

screen = pygame.display.set_mode((screen_width, screen_height), WINDOWMODE)

# CLASSES

pygame.init()
COLOR_BLACK = pygame.Color('black')
Color_None = pygame.Color(0, 0, 0, 0)
font = pygame.font.SysFont("arial", 20)
DEFAULT_FONT = 'freesansbold.ttf'
DEFAULT_FONT_SIZE = 32

class Button():
    # class defaults
    MIN_BUTTON_W = 100
    MIN_BUTTON_H = 50
    CLICK_OFFSET = 5
    BORDER_WIDTH = 4

    DEFAULT_FONT = 'freesansbold.ttf'
    DEFAULT_FONT_SIZE = 32

    FONT_COLOR = pygame.Color(54, 56, 14)
    HIGHLIGHT_COLOR = pygame.Color('darkgrey')
    BG_COLOR = pygame.Color(2, 136, 209)
    BORDER_COLOR = pygame.Color(1, 87, 155)

    def __init__(self, x, y, w, h, text, font = None, font_color = FONT_COLOR, highlight_color = HIGHLIGHT_COLOR,
                 bg_color = BG_COLOR, border_color = BORDER_COLOR, border_width = BORDER_WIDTH):
        # init internal variables
        self._mouse_over = False
        self._button_down = False
        self._disabled = False  # need to make property for this.
        self._border = border_width

        if w < Button.MIN_BUTTON_W:
            self._w = Button.MIN_BUTTON_W
        else:
            self._w = w
        if h < Button.MIN_BUTTON_H:
            self._h = Button.MIN_BUTTON_H
        else:
            self._h = h
        self._x = x
        self._y = y
        self._text = text
        # check if a valid pygame font object has been given
        if type(font).__name__ == 'Font':
            self._font = font
        else: # use the default
            if not font is None: # let the user know if it's not a valid font object
                print("Button", self._text, "has no valid font object. Using default.")
            self._font = pygame.font.Font( Button.DEFAULT_FONT, Button.DEFAULT_FONT_SIZE)
        self._font_color = font_color
        self._bg_color = bg_color
        self._border_color = border_color
        self._highlight_color = highlight_color
        self._down = False
        self._action = None


    def click(self):
        if self._action == None:
            print("No action function set for button:", self._text)
        else:
            self._action()

    def contains(self, x, y):
        return self.get_rect().collidepoint(x, y)
    
    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._w, self._h)
    def mouse_move(self, x, y):
        if not self._disabled:
            if self.contains( x, y):
                self._mouse_over = True
            else:
                self._mouse_over = False

    def mouse_click(self, event):
        if not self._disabled:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._mouse_over:
                    self._button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self._button_down and self._mouse_over:
                    if not self._action is None:
                        self._action() # I'm clicked
                    else:
                        print("button", self._text, "has no function set")
                self._button_down = False

    def set_action(self, action_function):
        if type(action_function).__name__ == 'function':
            self._action = action_function
    def get_action(self):
        return self._action
    action = property(get_action, set_action)

    def draw(self, screen):
        # draw rectangle
        pygame.draw.rect(screen, self._border_color, self.get_rect())
        pygame.draw.rect(screen, self._bg_color, pygame.Rect(self._x + self._border, self._y + self._border, self._w - self._border*2, self._h - self._border*2))

        # draw the text
        color = self._font_color
        offset = 0
        if self._mouse_over:
            if self._button_down:
                offset = Button.CLICK_OFFSET
            else:
                color = self._highlight_color
        
        # create the rendered text as a surface
        rendered_text = self._font.render(self._text, True, color, self._bg_color)
        # get the rectangle for this new surface
        rendered_text_rect = rendered_text.get_rect() 
        # set the centre of this rectangle to the centre of this button (self)
        rendered_text_rect.center = (self._x + self._w / 2 + offset, self._y + self._h / 2 + offset)
        screen.blit(rendered_text, rendered_text_rect)

class Snake():
    UP = 1

    def __init__(self, x,y, dir = UP):
        self._x = x
        self._y  = y
        self._dir = dir

    def reset(self):
        self._seg_list = []
        self._seg_list.append()


# FUNCTION DEFINITIONS

def main_game():
    # init

    game_map = pygame.transform.scale(pygame.image.load("images\\background\\snakemap.png").convert_alpha(), (500, 500))
    screen.blit(game_map, (500, 500))

    global run

    # main loop
    local_run = True
    while local_run:
        # get the current mouse position
        mouse_pos = pygame.mouse.get_pos()
        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                local_run = False
                run = False
        # blank the screen
        screen.fill((0, 0, 0))

        # draw
        screen.fill((38, 198, 218))
        # show everything we've just drawn
        pygame.display.flip()


# MAIN PROGRAM
PLAY_BUTTON_FONT = 'arial'
PLAY_BUTTON_FONT_SIZE = 140
game_state = True

if __name__ == "__main__":
    #initialise program - load stuff that we need for everything
    # init pygame
    pygame.init()
    # record the start time
    clock = pygame.time.Clock()

    # open the window
    screen = pygame.display.set_mode([screen_width, screen_height], pygame.RESIZABLE)
    # set the window caption
    pygame.display.set_caption('SNAK: The Game')

    # load fonts
    font = pygame.font.Font(DEFAULT_FONT, 24)

    # initialising controls
    controls_dict = {}
    controls_dict["settings"]   = Button(500, 820, 250, 100, "SETTINGS", font)
    controls_dict['credits']   = Button(1000, 820, 250, 100, "CREDITS")
    controls_dict['quit']   = Button(1500, 820, 250, 100, "EXIT")
    controls_dict['quit'].action = sys.exit
    play_button_font = pygame.font.SysFont(PLAY_BUTTON_FONT, PLAY_BUTTON_FONT_SIZE)
    controls_dict['start_button'] = Button(950, 480, 300, 300, '►', play_button_font)
    controls_dict['start_button'].action = main_game
    menu_snake = pygame.transform.scale(pygame.image.load("images\\menu_images\\menu_snake.png").convert_alpha(), (500, 500))
    snak_title = pygame.transform.scale(pygame.image.load("images\\menu_images\\snak_title.png").convert_alpha(), (1300, 500))
    menu_author = pygame.transform.scale(pygame.image.load("images\\menu_images\\tai_edwards.png").convert_alpha(), (900, 350))
    menu_boom = pygame.transform.scale(pygame.image.load("images\\menu_images\\best_game.png").convert_alpha(), (600, 500))
    awards = pygame.transform.scale(pygame.image.load("images\\menu_images\\awards.png").convert_alpha(), (650, 800))
    playbuttonarrow = pygame.transform.scale(pygame.image.load("images\\menu_images\\button_direction.png").convert_alpha(), (1300, 500))

    # main loop

    run = True
    while run:
        # get the current mouse position
        mouse_pos = pygame.mouse.get_pos()
        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in controls_dict.values():
                    button.mouse_click(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in controls_dict.values():
                    button.mouse_click(event)
            if event.type == pygame.MOUSEMOTION:
                for button in controls_dict.values():
                    button.mouse_move(mouse_pos[0], mouse_pos[1])
            if event.type == pygame.VIDEORESIZE:
                screen_width = event.dict['size'][0]
                screen_height = event.dict['size'][1]
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        
        # process actions - take the events you have captured and make the changes that they imply
        # is the mouse down
        if controls_dict['settings'].contains(mouse_pos[0], mouse_pos[1]):
            if event.type == pygame.MOUSEBUTTONDOWN:
                settings_menu = True
                game_state = False
            else:
                pass

        if controls_dict['credits'].contains(mouse_pos[0], mouse_pos[1]):
            if event.type == pygame.MOUSEBUTTONDOWN:
                credits_menu = True
                game_state = False
            else:
                pass

        if controls_dict['quit'].contains(mouse_pos[0], mouse_pos[1]):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Successfully exited program.")
                    sys.exit()
                else:
                    pass




        # process any actions that need to happen every loop
        # blank the screen
        screen.fill((0, 0, 0))

        # draw
        screen.fill((38, 198, 218))
        # draw miscellaneous images
        screen.blit(menu_snake, (10, 510))
        screen.blit(snak_title, (450, -20))
        screen.blit(menu_author, (650, 250))
        screen.blit(menu_boom, (-50, 0))
        screen.blit(awards, (1320, 0))
        screen.blit(playbuttonarrow, (300, 410))

        # draw all buttons
        for button in controls_dict.values():
            button.draw(screen)

        
        # show everything we've just drawn
        pygame.display.flip()    

pygame.quit()