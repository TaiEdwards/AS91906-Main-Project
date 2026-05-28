from os.path import exists
import pygame
import random
import debug
from imagelist import ImageList
from mysprite import MySprite

# CONSTANTS
screen_width = 1920/2
screen_height = 1074/2
FPS = 60

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
    def push():
        pygame.MOUSEBUTTONDOWN
    def draw(self, surface):
        rect = pygame.Rect(self._x, self._y, self._w, self._h)
        if not self._border_width == 0:
            pygame.draw.rect(surface, self._border_color, rect, 2) # 2 represents border thickness
        text_image = self._font.render(self.text, True, 'black')
        text_rect = text_image.get_rect(center = rect.center)
        surface.blit(text_image, text_rect)

buttonA = Button(200, 450, 100, 50, "Settings", font, COLOR_BLACK, 1,  COLOR_BLACK)
"""
buttonB = Button(420, 450, 100, 50, "Credits", COLOR_BLACK, COLOR_BLACK, font)
buttonC = Button(650, 450, 100, 50, "Exit", COLOR_BLACK, COLOR_BLACK, font)
gametitle = Button(240, 50, 450, 150, "Game Title Placeholder", COLOR_BLACK, COLOR_BLACK, font)
gamesubtitle = Button(240, 220, 450, 50, "BY TAI EDWARDS", Color_None, font)
menusnake = Button(20, 250, 150, 300, "Snake Image Placeholder", COLOR_BLACK, COLOR_BLACK, font)"""

# FUNCTION DEFINITIONS
"""
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

"""
def draw_menu():
    screen.fill('light blue')

    start_button = pygame.draw.rect(screen, 'light gray', [350, 300, 240, 60], 0, 5)
    border = pygame.draw.rect(screen, 'dark gray', [350, 300, 240, 60], 5, 5)
    
    font = pygame.font.SysFont("arial", size=20)
    text_image = font.render('Start Game', True, 'black')
    screen.blit(text_image, (430, 320))
    # Displays buttons on main menu
    buttonA.draw(screen)
    """buttonB.draw(screen)
    buttonC.draw(screen)
    gametitle.draw(screen)
    gamesubtitle.draw(screen)
    menusnake.draw(screen)"""

    # Get the mouse position
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    if start_button.collidepoint(mouse_pos) and mouse_pressed:
        return True
    return False
"""
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

        game_map.fill((0, 0, 0))

        game_map.blit(game_bg, (0, 0))

        pygame.display.flip()

    if main_menu():
        if draw_menu():
            main_menu = False
            main_game()

"""
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

    # main loop
    run = True
    while run:

        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # process actions - take the events you have captured and make the changes that they imply


        # draw
        screen.fill('light blue')
        draw_menu()
        
        #update the screen
        pygame.display.flip()

    pygame.quit()

    
    timer = pygame.time.Clock()

    game_map = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    game_bg = pygame.transform.scale(pygame.image.load("images/Background/SnakeMap.png").convert_alpha(), (game_map.get_width(), game_map.get_height()))

    font = pygame.font.Font('freesansbold.ttf', 24)

pygame.quit()