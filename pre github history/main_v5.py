from os.path import exists
import pygame
import random
import debug
from imagelist import ImageList
from mysprite import MySprite




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
    pass

run = True
while run:
    screen.fill('light blue')
    timer.tick(fps)
    if main_menu:
        draw_menu()
    else:
        draw_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()

def main_menu()

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

if __name__ == "__main__":
    #initialise program - load stuff that we need for everything

    # create the screen

    main_menu()

pygame.quit()