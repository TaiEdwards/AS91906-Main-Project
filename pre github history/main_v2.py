from os.path import exists
import pygame
import imagelist
import debug
import time

SCREEN_WIDTH = 610
SCREEN_HEIGHT = 480

# Creating the enemy
class MySprite():
    def __init__(self, x, y, w, h, images, screen):
        valid = True

        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._w = w
        self._h = h
        self._xd = 0
        self._yd = 0
        self._images = images
        self._screen = screen

        # set default frame
        self._current_frame = 0
        self._start_frame = 0
        self._end_frame = 0
        self._next_frame = time.time()
        self._delay = -1 # default to not animating
        self._repeat = False
        self._next_move = time.time()
        self._move_delay = 0

        if not valid:
            print("Something invalid happened. I am going to quit.")
            exit(0)

    def get_x(self):
        return self._x
    def set_x(self, x):
        if x >= 0 and x <= SCREEN_WIDTH:
            self._x = x
        elif x < 0:
            self._x = 0
        else:
            self._x = SCREEN_WIDTH - 1

    def get_y(self):
        return self._y
    def set_y(self, y):
        if y >= 0 and y <= SCREEN_WIDTH:
            self._y = y
        elif y < 0:
            self._y = 0
        else:
            self._y = SCREEN_WIDTH - 1

    x = property(get_x, set_x)
    y = property(get_y, set_y)

    def set_pos(self, x, y):
        self.set_x(x)
        self.set_y(y)

    
    def move(self, x_delta, y_delta = None):
        # changing the vector if required
        if not x_delta is None:
            self._xd = x_delta
        if not y_delta is None:
            self._yd = y_delta

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._w, self._h)
    def collide(self):
        pass

    def move(self, x_delta = None, y_delta = None, delay = None):
        # changing the vector if required
        if not x_delta is None:
            self._xd = x_delta
        if not y_delta is None:
            self._yd = y_delta
        if not delay is None:
            self._move_delay = delay
            if not delay == self._move_delay:
                self._next_move = time.time()

        if time.time() > self._next_move:
            self.set_x(self.x + self._xd)
            self.set_y(self.y + self._yd)
            self._next_move = self._next_move + self._move_delay

    def draw(self):
        self._screen.blit(self._images.images[self._current_frame], self.get_rect())

    def collide(self, other_rect):
        if isinstance(other_rect, pygame.Rect):
            if not (self._y > other_rect.y + other_rect.h or \
                self._x > other_rect.x + other_rect.w or \
                    self._x + self._w < other_rect.x or \
                        self._y + self._h < other_rect.y ):
                return True
            else:
                return False
        else:
            pass # need to decide what to do here

    def set_animation(self, start_frame = 0, end_frame = 0, delay = 0, repeat = -1):
        if start_frame >= 0 and start_frame < len(self._images.images):
            self._start_frame = start_frame
        if end_frame >= 0 and end_frame < len(self._images.images) and start_frame <= end_frame:
            self._end_frame = end_frame
        if delay > 0:
            self._delay = delay
        if repeat:
            self._repeat = True
        else:
            self._repeat = False

            self._next_frame = time.time() + delay

    def animate(self, reset_animation = False):
        # If we're animating
        if not self._delay == -1:
            # If we're resetting
            if reset_animation == True:
                self._current_frame = self._start_frame
            else:
                if time.time() > self._next_frame:
                    # Go to our next frame
                    if self._current_frame == self._end_frame:
                        if self._repeat:
                            self._current_frame = self._start_frame
                    else:
                        self._current_frame += 1

            self._next_frame = self._next_frame + self._delay

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._w, self._h)

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

    spritelist = []
    spritelist.append(MySprite(TEST_X, TEST_Y, TEST_W, TEST_H, image_obj, screen))
    spritelist[-1].set_animation(0, 3, 0.1, True)
    spritelist.append(MySprite(TEST_X+TEST_W, TEST_Y, TEST_W, TEST_H, image_obj, screen))

    quitting = False
    while not quitting:
        # check the even queue for messages
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
        #Clear The Screen
        screen.fill(pygame.Color('black'))

        # draw, animate and move sprites in the list
        for sprite in spritelist:
            sprite.draw()
            sprite.animate()
            sprite.move(1, 0, 1)

        # show the updated display
        pygame.display.flip()

    pygame.quit()
    quit()