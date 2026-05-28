from os.path import exists
import pygame
import debug

class ImageList():
    def __init__(self, filename, width, height):
        self._images = []
        count = 0
        while exists(filename + str(count) + '.jpg'):
            image = pygame.image.load(filename + str(count) + '.jpg')
            scaled = pygame.transform.smoothscale(image, [width, height])
            self._images.append(scaled)
            debug.dprint(2,self._images[-1])
            count += 1

    def get_images(self):
        return self._images
    images = property(get_images, None, None)

# testing
debug.DEBUG_LEVEL = 2
if __name__ == "__main__":
    # starting up pygame
    pygame.init()
    # setting up window
    screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)

    TEST_X = 50
    TEST_Y = 50
    TEST_W = 64
    TEST_H = 64
    image_rect = pygame.Rect(TEST_X, TEST_Y, TEST_W, TEST_H)
    # image list for sprite
    image_obj = ImageList("images\\test\\test", 64, 64)
    
    sprite1 = MySprite(TEST_X, TEST_Y, TEST_W, TEST_H, image_obj, screen)

    quitting = False
    
    while not quitting:
        # check the even queue for messages
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
        #Clear The Screen
        screen.fill(pygame.Color('black'))
        pygame.display.flip()

    pygame.quit()
    quit()