from os.path import exists
import pygame
import random
import debug
from imagelist import ImageList
from mysprite import MySprite

# CONSTANTS
FPS = 60

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

    start_button = pygame.draw.rect(screen, 'light gray', [200, 150, 240, 60], 0, 5)
    border = pygame.draw.rect(screen, 'dark gray', [200, 150, 240, 60], 5, 5)
    font = pygame.font.SysFont("arial", size=20)
    text_image = font.render('Start Game', True, 'black')
    screen.blit(text_image, (220, 165))

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
    screen_width = 1920/2
    screen_height = 1074/2
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

    
    fps = 60
    timer = pygame.time.Clock()

    game_map = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    game_bg = pygame.transform.scale(pygame.image.load("images/Background/SnakeMap.png").convert_alpha(), (game_map.get_width(), game_map.get_height()))

    font = pygame.font.Font('freesansbold.ttf', 24)

pygame.quit()