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

class Button():
    def __init__(self, x, y, w, h, text, font, bgcolor, border_width = 0, border_color = COLOR_BLACK):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self.text = text
        self._bgcolor = bgcolor
        self._border_width = border_width
        self._border_color = border_color
        self._font = font
    def mouse_in(self, x, y):
        self._x = x
        self._y = y
        return True or False

    def contains(self, x, y):
        if x >= self._x and x <= self._x + self._w and y >= self._y and y <= self._y + self._h:
            return True
        else:
            return False

    def push(self):
        pass
        #pygame.MOUSEBUTTONDOWN

    def draw(self, surface):
        rect = pygame.Rect(self._x, self._y, self._w, self._h)
        if not self._border_width == 0:
            pygame.draw.rect(surface, self._border_color, rect, 2) # 2 represents border thickness
        text_image = self._font.render(self.text, True, 'black')
        text_rect = text_image.get_rect(center = rect.center)
        surface.blit(text_image, text_rect)

    def mouse_click(self, event):
        if not self._disabled:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._mouse_over:
                    self._button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self._button_down and self._mouse_over:
                    # clicked
                    self._button_down = False


# FUNCTION DEFINITIONS

def draw_game():
    menu_btn = pygame.draw.rect(screen, 'light gray', [230, 450, 260, 40], 0, 5)
    pygame.draw.rect(screen, 'dark gray', [230, 450, 260, 40], 5, 5)
    text = font.render('Main Menu', True, 'black')
    screen.blit(text, (245, 457))
    if menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        menu = True
    else:
        menu = False
    return menu


def draw_menu():
    screen.fill('light green')

    start_button = pygame.draw.rect(screen, 'green', [820, 400, 300, 300], 0, 5)
    border = pygame.draw.rect(screen, 'dark green', [820, 400, 300, 300], 5, 5)
    
    font = pygame.font.SysFont("arial", size=140)
    text_image = font.render('►', True, (0, 0, 0))
    screen.blit(text_image, (935, 470))
    # Displays buttons on main menu
    button_a.draw(screen)
    button_b.draw(screen)
    button_c.draw(screen)
    gametitle.draw(screen)
    gamesubtitle.draw(screen)
    menusnake.draw(screen)

    # Get the mouse position
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    if start_button.collidepoint(mouse_pos) and mouse_pressed:
        return True
    return False

def main_menu():
        pass



def main_game():
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((0, 0, 0))

        screen.blit(game_bg, (0, 0))

        pygame.display.flip()

    if main_menu():
        if draw_menu():
            main_menu = False
            main_game()


# MAIN PROGRAM

if __name__ == "__main__":
    #initialise program - load stuff that we need for everything
    clock = pygame.time.Clock()

    # init pygame
    pygame.init()
    # open the window
    screen = pygame.display.set_mode([screen_width, screen_height])
    # set the window caption
    pygame.display.set_caption('SNAK: The Game')

    # load fonts
    font = pygame.font.Font('freesansbold.ttf', 24)
    # loading images
    game_bg = pygame.transform.scale(pygame.image.load("images/Background/SnakeMap.png").convert_alpha(), (screen.get_width(), screen.get_height()))

    # initialising controls
    button_a = Button(250, 820, 250, 100, "Settings", font, COLOR_BLACK, 1, COLOR_BLACK)
    button_b = Button(850, 820, 250, 100, "Credits", font, COLOR_BLACK, 1, COLOR_BLACK)
    button_c = Button(1500, 820, 250, 100, "Exit", font, COLOR_BLACK, 1, COLOR_BLACK)
    gametitle = Button(660, 50, 600, 250, "Game Title Placeholder", font, COLOR_BLACK, 1, COLOR_BLACK)
    gamesubtitle = Button(740, 320, 450, 50, "BY TAI EDWARDS", font, Color_None, 0, Color_None)
    menusnake = Button(20, 700, 150, 300, "Snake Image Placeholder", font, COLOR_BLACK, 1, COLOR_BLACK)

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
                button_a.mouse_click(event)
            if event.type == pygame.MOUSEBUTTONUP:
                button_a.mouse_click(event)
            if event.type == pygame.MOUSEMOTION:
                button_a.mouse_in(mouse_pos[0], mouse_pos[1])


            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

        # process actions - take the events you have captured and make the changes that they imply
        # is the mouse down
        """
            mouse_pos = pygame.mouse.get_pos()
            if button_a.contains(mouse_pos[0], mouse_pos[1]):
                if pygame.mouse.get_pressed:
                    mouse_down = True

            if button_b.contains(mouse_pos[0], mouse_pos[1]):
                mouse_down = True

            if button_c.contains(mouse_pos[0], mouse_pos[1]):
                if pygame.mouse.get_pressed():
                    pygame.quit()
                    sys.exit()
        """

        if mouse_down == True:
            pass

        # process any actions that need to happen every loop


        # draw
        screen.fill('light blue')
        button_a.draw()
        button_b.draw()
        button_c.draw()
        
        # show everything we've just drawn
        pygame.display.flip()
    

pygame.quit()