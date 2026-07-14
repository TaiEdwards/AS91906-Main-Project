#INIT
from os.path import exists
import pygame
import random
import sys
import time

# CONSTANTS SECTION

TILE_SIZE = 32
TILES_ACROSS = 35
TILES_DOWN = 20

# window size for the menu
MENU_LOGICAL_W = 1920
MENU_LOGICAL_H = 1009

# The game's logical screen size before scaling
GAME_LOGICAL_W = TILES_ACROSS * TILE_SIZE
GAME_LOGICAL_H = TILES_DOWN * TILE_SIZE

# set the initial real screen size to the same
screen_width = GAME_LOGICAL_W
screen_height = GAME_LOGICAL_H 

# window mode and max FPS
WINDOWMODE = pygame.RESIZABLE
FPS = 60


# CLASSES

pygame.init()
COLOR_BLACK = pygame.Color('black')
COLOR_RED = pygame.Color('red')
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

    # Call the action function.
    def click(self):
        if self._action == None:
            print("No action function set for button:", self._text)
        else:
            self._action()

    # Checking if the mouse is inside the button rectangle.
    def contains(self, x, y):
        return self.get_rect().collidepoint(x, y)
    
    # Returns the button's rectangle.
    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._w, self._h)

    # Inform the button about mouse movements.
    # Decides whether the mouse is inside or not.
    def mouse_move(self, x, y):
        if not self._disabled:
            if self.contains( x, y):
                self._mouse_over = True
            else:
                self._mouse_over = False

    # Check if the mouse is inside and call the action function.
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

    # Get/Set property methods for the action function.
    def set_action(self, action_function):
        if type(action_function).__name__ == 'function':
            self._action = action_function
    def get_action(self):
        return self._action
    action = property(get_action, set_action)

    # self draw function - requires a screen object to draw to
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

# The Snake itself. Contains a list of 
# segments as tuples of position and direction.
class Snake():
    # Indexes into the directional vector list.
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    
    # Image index for Snake segments.
    IMG_HEAD = 0
    IMG_BODY = 1
    IMG_TAIL = 2

    POS_HEAD = 0
    POS_TAIL = -1

    # Snake updates every half a second
    INITIAL_SPEED = 0.1

    DIR = [(0, -1), (0, 1), (-1, 0), ( 1, 0 )]

    # Init function, sets up the Snake
    # load the images, define the intial three segments, etc
    def __init__(self, x, y):
        self._x = x
        self._y = y

        # Set initial direction.
        self._direction = Snake.RIGHT
        # make the segments
        self._segments = [(x, y, self._direction), (x - TILE_SIZE, y, self._direction), (x - TILE_SIZE * 2, y, self._direction)] # List of segment positions

        self._die = False
        self._growing = False
        # load the images
        self._images = []
        self._images.append(pygame.transform.scale(pygame.image.load("images\\snake\\blockhead.png").convert_alpha(), (50, 50)))
        self._images.append(pygame.transform.scale(pygame.image.load("images\\snake\\blockbody.png").convert_alpha(), (50, 50)))
        self._images.append(pygame.transform.scale(pygame.image.load("images\\snake\\blockbutt.png").convert_alpha(), (50, 50)))

        # setting the time for the next frame
        self._next_frame = time.time()
        self._move_delay = Snake.INITIAL_SPEED

    # Set new direction for Snake but don't allow reversing.
    def change_direction(self, new_direction):
        # prevent reversing
        if (self._direction == Snake.UP and new_direction == Snake.DOWN) or \
            (self._direction == Snake.DOWN and new_direction == Snake.UP) or \
            (self._direction == Snake.LEFT and new_direction == Snake.RIGHT) or \
            (self._direction == Snake.RIGHT and new_direction == Snake.LEFT):
            return
        self._direction = new_direction

    # Moves the Snake by adding a new head and deleting the tail
    def move(self):
        # If it's time to move 
        if time.time() > self._next_frame:
            # New head
            new_head = (self._x + Snake.DIR[self._direction][0] * TILE_SIZE, self._y + Snake.DIR[self._direction][1] * TILE_SIZE, self._direction)
            self._segments.insert(Snake.POS_HEAD, new_head)
            if not self._growing: # remove tail unless growing
                self._segments.pop()
            else:
                self._growing = False
            # Update position using directional vectors.
            self._x += Snake.DIR[self._direction][0] * TILE_SIZE
            self._y += Snake.DIR[self._direction][1] * TILE_SIZE
            # Setting the next time to move.
            self._next_frame = self._next_frame + self._move_delay

    # tell the snake to grow next move/frame
    def grow(self):
        self._growing = True

    # Draw the Snake.
    def draw(self, screen):
        # Drawing the head and tail.
        screen.blit(self._images[Snake.IMG_HEAD], (self._segments[Snake.POS_HEAD][0], self._segments[Snake.POS_HEAD][1]))
        screen.blit(self._images[Snake.IMG_TAIL], (self._segments[Snake.POS_TAIL][0], self._segments[Snake.POS_TAIL][1]))
        # Drawing the segments.
        for segment in self._segments[1:-1]: # List slice giving only the middle elements.
            screen.blit(self._images[Snake.IMG_BODY], (segment[0], segment[1]))

    # Get own rectangle.
    def get_rect(self):
        return pygame.Rect(self._x, self._y, TILE_SIZE, TILE_SIZE)

    def collide(self, other_rect):
        # return True if we are touching something else
        return self.get_rect().colliderect(other_rect)

    # Check if the Snake needs to die.
    def death_detect(self, arena_w, arena_h):
        # Check if the Snake is within the arena.
        arena_rect = pygame.Rect(0, 0, arena_w, arena_h)
        if not self.collide(arena_rect):
            self._die = True
        # Check if the Snake is touching itself.
        for segment in self._segments[1:]:
            if self.collide(pygame.Rect(segment[0], segment[1], TILE_SIZE, TILE_SIZE)):
                self._die = True
        return self._die

class Food():
    #food_coordinates = randint()
    def __init__(self, image):
        self._image = image
        self._h = TILE_SIZE
        self._w = TILE_SIZE
        self.reset()

    # Respawning the food.
    def reset(self):
        self._x = random.randint(0, TILES_ACROSS - 1) * TILE_SIZE
        self._y = random.randint(0, TILES_DOWN - 1) * TILE_SIZE

    # Draw self.
    def draw(self, screen):
        screen.blit(self._image, (self._x, self._y))

    # Return own rectangle.
    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._w, self._h)



# FUNCTION DEFINITIONS

def game_over(canvas, screen, screen_width, screen_height):
    # Global to allow a cascading exit from
    # both this loop and the menu's loop.
    global run

    # init
    canvas = pygame.Surface((GAME_LOGICAL_W, GAME_LOGICAL_H))

    font = pygame.font.Font(DEFAULT_FONT, DEFAULT_FONT_SIZE)
    game_over_text = font.render("GAME OVER!!", COLOR_BLACK, COLOR_RED)
    game_over_rect = game_over_text.get_rect()
    # set co-ordinates for the text
    game_over_rect.center = (screen_width // 2, screen_height // 2)
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
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                local_run = False

        # draw
        canvas.blit(game_over_text, game_over_rect)
        
        # scale the canvas and blit
        scaled_canvas = pygame.transform.scale(canvas,(screen_width, screen_height))
        screen.blit(scaled_canvas, (0,0))

        # show everything drawn
        pygame.display.flip()
        # end of main game loop.


def main_game(screen):
    global screen_width
    global screen_height
    # Global to allow a cascading exit from
    # both this loop and the menu's loop.
    global run
    # init
    canvas = pygame.Surface((GAME_LOGICAL_W, GAME_LOGICAL_H))
    # creating map
    game_map = pygame.transform.scale(pygame.image.load("images\\background\\snakemap.png").convert_alpha(), (1920, 1010))

    # intialising snake images

    # initialising snake default co-ordinates
    snake_x = random.randint(3, TILES_ACROSS - 3) * TILE_SIZE
    snake_y = random.randint(3, TILES_DOWN - 3) * TILE_SIZE

    # initialising snake
    snake = Snake(snake_x, snake_y) # starting position
    direction = snake.DOWN

    frame_count = 0
    move_internal = 10


    # initialising food images
    apple = pygame.transform.scale(pygame.image.load("images\\food\\snak_apple.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
    food = Food(apple)

    # main loop
    local_run = True
    while local_run:
        clock.tick(FPS)
        frame_count += 1
        # get the current mouse position
        mouse_pos = pygame.mouse.get_pos()
        # process events
        for event in pygame.event.get():
            # Process window resize
            if event.type == pygame.VIDEORESIZE:
                screen_width = event.dict['size'][0]
                screen_height = event.dict['size'][1]
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            # Are we quitting
            if event.type == pygame.QUIT:
                local_run = False
                run = False
            # Direction keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_direction(Snake.LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(Snake.RIGHT)
                elif event.key == pygame.K_UP:
                    snake.change_direction(Snake.UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(Snake.DOWN)

        # move the snake
        snake.move()

        # check for a food collision
        if snake.collide(food.get_rect()):
            food.reset()
            snake.grow()
        # check if snake hits self or exits arena
        if snake.death_detect(GAME_LOGICAL_W, GAME_LOGICAL_H):
            local_run = False

        # blank the screen
        canvas.fill((0, 0, 0))

        # draw
        canvas.fill((38, 198, 218))
        # show everything we've just drawn
        canvas.blit(game_map, (0, 0))
        # blitting food before snake to ensure it is behind the snake
        food.draw(canvas)
        snake.draw(canvas)
        # scale the canvas and blit
        scaled_canvas = pygame.transform.scale(canvas,(screen_width, screen_height))
        screen.blit(scaled_canvas, (0,0))

        # show everything drawn
        pygame.display.flip()
        # end of main game loop.

    # game over screen goes here.
    game_over(canvas, screen, screen_width, screen_height)



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

    quitting = False
    mouse_down = False
    # create the main screen
    screen = pygame.display.set_mode((screen_width, screen_height), WINDOWMODE)
    # set the window caption
    pygame.display.set_caption('SNAK: The Game')

    # create the drawing / scaled canvas
    canvas = pygame.Surface((MENU_LOGICAL_W, MENU_LOGICAL_H))




    # load fonts
    font = pygame.font.Font(DEFAULT_FONT, 24)

    # initialising controls
    controls_dict = {} # menu controls in a dictionary for flexibility and efficiency
    controls_dict["settings"]   = Button(500, 820, 250, 100, "SETTINGS", font)
    controls_dict['credits']   = Button(1000, 820, 250, 100, "CREDITS")
    controls_dict['quit']   = Button(1500, 820, 250, 100, "EXIT")
    controls_dict['quit'].action = sys.exit
    play_button_font = pygame.font.SysFont(PLAY_BUTTON_FONT, PLAY_BUTTON_FONT_SIZE)
    controls_dict['start_button'] = Button(950, 480, 300, 300, ' ►', play_button_font, bg_color=pygame.Color(55, 231, 0), border_color=pygame.Color(0, 130, 7))
    controls_dict['start_button'].action = lambda x=screen: main_game(x)

    # Load the images
    menu_snake = pygame.transform.scale(pygame.image.load("images\\menu_images\\menu_snake.png").convert_alpha(), (500, 500))
    snak_title = pygame.transform.scale(pygame.image.load("images\\menu_images\\snak_title.png").convert_alpha(), (1300, 500))
    menu_author = pygame.transform.scale(pygame.image.load("images\\menu_images\\tai_edwards.png").convert_alpha(), (900, 350))
    menu_boom = pygame.transform.scale(pygame.image.load("images\\menu_images\\best_game.png").convert_alpha(), (600, 500))
    awards = pygame.transform.scale(pygame.image.load("images\\menu_images\\awards.png").convert_alpha(), (650, 800))
    playbuttonarrow = pygame.transform.scale(pygame.image.load("images\\menu_images\\button_direction.png").convert_alpha(), (1300, 500))

    # main loop

    run = True
    while run:
        # get the mouse current position
        coords=pygame.mouse.get_pos()
	    # scale the mouse coordinates
        scaled_coords = ( coords[0] * MENU_LOGICAL_W //screen_width , coords[1] * MENU_LOGICAL_H //screen_height )
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
                    button.mouse_move(scaled_coords[0], scaled_coords[1])
            if event.type == pygame.VIDEORESIZE:
                screen_width = event.dict['size'][0]
                screen_height = event.dict['size'][1]
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        
        # process actions - take the events you have captured and make the changes that they imply
        # is the mouse down
        if controls_dict['settings'].contains(scaled_coords[0], scaled_coords[1]):
            if event.type == pygame.MOUSEBUTTONDOWN:
                settings_menu = True
                game_state = False

        if controls_dict['credits'].contains(scaled_coords[0], scaled_coords[1]):
            if event.type == pygame.MOUSEBUTTONDOWN:
                credits_menu = True
                game_state = False

        if controls_dict['quit'].contains(scaled_coords[0], scaled_coords[1]):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Successfully exited program.")
                    sys.exit()

        # process any actions that need to happen every loop
        # blank the screen
        canvas.fill((0, 0, 0))

        # draw
        canvas.fill((38, 198, 218))
        # draw miscellaneous images
        canvas.blit(menu_snake, (10, 510))
        canvas.blit(snak_title, (450, -20))
        canvas.blit(menu_author, (650, 250))
        canvas.blit(menu_boom, (-50, 0))
        canvas.blit(awards, (1320, 0))
        canvas.blit(playbuttonarrow, (300, 410))

        # draw all buttons
        for button in controls_dict.values():
            button.draw(canvas)

        # scale the canvas and blit
        scaled_canvas = pygame.transform.scale(canvas,(screen_width, screen_height))
        screen.blit(scaled_canvas, (0,0))

        # show everything we've just drawn
        pygame.display.flip()    

pygame.quit()