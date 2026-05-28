from os.path import exists
import pygame
import random
import debug
from imagelist import ImageList
from mysprite import MySprite

clock = pygame.time.Clock()
FPS = 5
screen_width = 1920/2
screen_height = 1074/2
running = True

pygame.init()

pygame.display.set_caption('SNAK: The Game')
fps = 60

game_map = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
game_bg = pygame.transform.scale(pygame.image.load("images/Background/SnakeMap.png").convert_alpha(), (game_map.get_width(), game_map.get_height()))

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
    main_game()

pygame.quit()