import sys, random, pygame
from pygame.locals import *

# Initialize pygame
pygame.init()

FPS = 10 # Frames per second
WINDOWWIDTH = 640 # Width
WINDOWHEIGHT = 480 # Height
CELLSIZE = 20 # Cell width and height size

# Defining colors by RGB value
BGCOLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)

muted = 0 # 0 == Music not muted 1 == Music muted
end_start_screen = 0 # 0 == Starting screen, 1 == Game, 2 == Game Over screen

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
CLOCK = pygame.time.Clock()

# Defining font
BASICFONT = pygame.font.Font('freesansbold.ttf', 20)

def main():
    global end_start_screen

    # Main loop
    while True:
        get_new_snake()
        get_random_location()
        music_play()

        # Loop that contains starting screen and main game
        while end_start_screen == 0 or end_start_screen == 1:

            was_key_pressed()

            if end_start_screen == 0:
                show_start_screen()
                show_mute_button()
            elif end_start_screen == 1:
                DISPLAYSURF.fill(BGCOLOR)
                run_game()

            CLOCK.tick(FPS)

        # Loop that contains game over screen
        while end_start_screen == 2:

            was_key_pressed()

            wait_for_key_pressed()

            DISPLAYSURF.fill(BGCOLOR)
            game_over_font = pygame.font.Font('freesansbold.ttf', 150)
            game_surface = game_over_font.render('Game', True, WHITE)
            over_surface = game_over_font.render('Over', True, WHITE)
            game_rect = game_surface.get_rect()
            over_rect = over_surface.get_rect()
            game_rect.midtop = (WINDOWWIDTH / 2, 10)
            over_rect.midtop = (WINDOWWIDTH / 2, game_rect.height + 10 + 25)

            DISPLAYSURF.blit(game_surface, game_rect)
            DISPLAYSURF.blit(over_surface, over_rect)


            CLOCK.tick(FPS)


# Ends and shutdowns game window
def terminate():
    sys.exit()

def was_key_pressed():
    # Loops throw the events
    for event in pygame.event.get():
        global pressed, direction, muted

        if event.type == pygame.QUIT:
            terminate()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                terminate()

            if event.key == pygame.K_m:
                if muted == 0:
                    music_stop()
                    muted = 1

                else:
                    music_play()
                    muted = 0

            """ 
            Checks if user pressed predefined key and changed direction.
            If user wants to go in the opposite direction then the current
            direction, it doesnt changes the direction
            """

            if event.key == pygame.K_w and direction != 'down':

                direction = 'up'

            if event.key == pygame.K_s and direction != 'up':

                direction = 'down'

            if event.key == pygame.K_a and direction != 'right':

                direction = 'left'

            if event.key == pygame.K_d and direction != 'left':

                direction = 'right'

        # Returns True if user pressed any button and False if he didnt pressed anything

        if event.type == pygame.KEYDOWN:
            pressed = True
            return pressed


        else:
            pressed = False
            return pressed

    return pressed

# Waits for user to press any key, then changes end_start_screen state
def wait_for_key_pressed():
    global end_start_screen # 0 = Starting screen, 1 = Game, 2 = Game Over screen

    if end_start_screen == 0 and was_key_pressed():
        end_start_screen = 1

    if end_start_screen == 1:
        return

    if end_start_screen == 2 and was_key_pressed():
        end_start_screen = 1

    if end_start_screen == 0 or end_start_screen == 2:
        if end_start_screen == 0:
            # Text position for starting screen
            top_position = WINDOWHEIGHT / 2
        
        if end_start_screen == 2:
            # Text position for game over screen
            top_position = WINDOWHEIGHT - 100

        msg_surface = BASICFONT.render('PRESS ANY KEY TO PLAY', True, GRAY)
        msg_rect = msg_surface.get_rect()
        msg_rect.center = (WINDOWWIDTH / 2, top_position)
        DISPLAYSURF.blit(msg_surface, msg_rect)
        pygame.display.update()

# Renders Starting screen
def show_start_screen():
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surface = title_font.render('Snake!', True, WHITE)
    title_rect = title_surface.get_rect()
    title_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 100)

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(title_surface, title_rect)
    wait_for_key_pressed()

# Renders Game Over screen
def show_game_over_screen():
    """Show a game over screen when the player loses. (Do not modify.)"""
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)
    game_surface = game_over_font.render('Game', True, WHITE)
    over_surface = game_over_font.render('Over', True, WHITE)
    game_rect = game_surface.get_rect()
    over_rect = over_surface.get_rect()
    game_rect.midtop = (WINDOWWIDTH / 2, 10)
    over_rect.midtop = (WINDOWWIDTH / 2, game_rect.height + 10 + 25)

    DISPLAYSURF.blit(game_surface, game_rect)
    DISPLAYSURF.blit(over_surface, over_rect)
    wait_for_key_pressed()

# Renders Text 'PRESS M TO MUTE'
def show_mute_button():
    msg_surface = BASICFONT.render('PRESS M TO MUTE', True, GRAY)
    msg_rect = msg_surface.get_rect()
    msg_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT - 100)
    DISPLAYSURF.blit(msg_surface, msg_rect)
    pygame.display.update()

# Stops music
def music_stop():
    pygame.mixer.music.stop()

# Starts music
def music_play():
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1,0.0)
    pygame.mixer.music.set_volume(0.08)

# Generates a new snake that start with 3 heads
def get_new_snake():
    global snake, direction, x_start, y_start
    x_start = random.randint(100, WINDOWWIDTH - 100)
    y_start = random.randint(100, WINDOWHEIGHT - 100) 

    x_start = x_start - (x_start % 20)
    y_start = y_start - (y_start % 20)

    snake = [[x_start, y_start], [x_start - 20, y_start], [x_start - 40, y_start]]
    direction = 'right'

# Generates random location for apple
def get_random_location():
    global apple_x, apple_y

    apple_x = random.randint(10, WINDOWWIDTH - 10)
    apple_y = random.randint(10, WINDOWHEIGHT - 10)

    apple_x = apple_x - (apple_x % 20) + 10
    apple_y = apple_y - (apple_y % 20) + 10

# Adds new head in snake list
def add_new_head():
    global snake, x_start, y_start

    snake.insert(len(snake), [x_start, y_start])

def move():
    global x_start, y_start, direction, snake

    # Pops laast head from snake
    snake.pop()

    if direction == 'up':
        #snake[0][1] -= 20
        y_start -= 20

    if direction == 'down':
        #snake[0][1] += 20
        y_start += 20

    if direction == 'right':
        #snake[0][0] += 20
        x_start += 20

    if direction == 'left':
        #snake[0][0] -= 20
        x_start -= 20
    
    # Inserts new head in snake
    snake.insert(0, [x_start, y_start])

# Displays grid
def grid():

    DISPLAYSURF.fill(BGCOLOR)
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # Draw vertical lines
        pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # Draw horizontal lines
        pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))

# Main game code
def run_game():

    grid()
    move()
    check_head_collision(snake)
    check_wall_collision(snake)
    check_apple_collision(snake)
    draw_score()

    for i in range(len(snake)):

        pygame.draw.rect(DISPLAYSURF, GREEN, (snake[i][0], snake[i][1], CELLSIZE, CELLSIZE))

    pygame.draw.circle(DISPLAYSURF, RED, (apple_x, apple_y), CELLSIZE - 10)

    pygame.display.update()

# Checks if snake collide with apple. If true then adds new head and generates new apple
def check_apple_collision(snake):
    if snake[0][0] == (apple_x - 10) and snake[0][1] == (apple_y - 10):
        add_new_head()
        get_random_location()

# Checks if snake collide with his own body. If true, then end_start_screen state changes
def check_head_collision(snake):
    global end_start_screen

    for i in range(len(snake)):
        if i == 0:
            pass
        elif snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            end_start_screen = 2

# Checks if snake collide with a wall. If true then end_start_screen state changes
def check_wall_collision(snake):
    global end_start_screen

    if snake[0][0] < 0:
        end_start_screen = 2

    if snake[0][1] > WINDOWHEIGHT - 20:
        end_start_screen = 2

    if snake[0][0] > WINDOWWIDTH - 20:
        end_start_screen = 2

    if snake[0][1] < 0:
        end_start_screen = 2

# Renders Score
def draw_score():
    score_surface = BASICFONT.render('Score: ' + str(len(snake) - 3), True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(score_surface, score_rect)

if __name__ == '__main__':
    main()