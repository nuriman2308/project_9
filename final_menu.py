import pygame
import os
import sys
from threading import Thread
import time
import numpy as np
import vlc

pygame.init() # pygame initialization

def intro():
    vidPath = 'intro.mp4'
    movie = os.path.expanduser(vidPath)
    # Check if movie is accessible
    if not os.access(movie, os.R_OK):
        print('Error: %s file not readable' % movie)
        sys.exit(1)
    # Create instance of VLC and create reference to movie.
    vlcInstance = vlc.Instance()
    media = vlcInstance.media_new(movie)
    # Create new instance of vlc player
    player = vlcInstance.media_player_new()
    # Pass pygame window id to vlc player, so it can render its contents there (Set a Win32/Win64 API window handle (HWND))
    # get_wm_info - to get information about the current windowing system
    player.set_hwnd(pygame.display.get_wm_info()['window'])
    # Load movie into vlc player instance
    player.set_media(media)
    # Quit pygame mixer to allow vlc full access to audio device (REINIT AFTER MOVIE PLAYBACK IS FINISHED!)
    pygame.mixer.quit()
    player.video_set_mouse_input(True)
    player.video_set_scale(0.9)
    player.play()

    while player.get_state() != vlc.State.Ended:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    player.release()

FPS = 20
WIDTH, HEIGHT = 1000, 640 # screen sizes
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('THE TOGYZ QUMALAQ')
clock = pygame.time.Clock()

icon = pygame.image.load("Logo.png") # Logo of THE TOGYZ QUMALAQ
pygame.display.set_icon(icon)

#intro()

pygame.init()
background = pygame.image.load('background.png')
home1 = pygame.image.load('Home.png')
refresh1 = pygame.image.load('Refresh.png')
sound_on1 = pygame.image.load('Sound on.png')
sound_off1 = pygame.image.load('Sound off.png')
ball = pygame.image.load("Ball.png")

error_sound_music = pygame.mixer.Sound("error1.wav")
stones_moving_sound = pygame.mixer.Sound("kamni.wav")
pressing_sound = pygame.mixer.Sound("pressing sound.wav")
menu_song = pygame.mixer.Sound('menu.wav') # song file
stop_song = False

BROWN_COLOR = (36, 12, 4)
BUTTON_COLOR = (255, 166, 41)
WHITE_COLOR = (255, 255, 179)
BLUE_COLOR = (11, 68, 87)
LOGO_TEXT_COLOR = (28, 9, 2)

font = pygame.font.SysFont('Book Antiqua', 70, bold=True)
language = False # False - eng, True - rus
sound_state = True # True - music on, False - music off
sound_level = 0.5 # song volume

THE_TOGYZ_QUMALAQ = ('THE TOGYZ QUMALAQ', 'ТОГЫЗ КУМАЛАК')
SINGLE_PLAYER = ('SINGLE PLAYER', 'ОДИН ИГРОК')
MULTIPLAYER = ('MULTI PLAYER', 'ДВА ИГРОКА')
TRAINING = ('RULES OF THE GAME', 'ПРАВИЛА ИГРЫ')
SETTINGS = ('SETTINGS', 'НАСТРОЙКИ')

RETURN = ('RETURN', 'НАЗАД')
CHANGE_LANGUAGE = ('CHANGE LANGUAGE', 'СМЕНИТЬ ЯЗЫК')
RULES = ('RULES', 'ПРАВИЛА')  #удалить
MUSIC = ('ON/OFF MUSIC', 'ВКЛ/ВЫКЛ МУЗЫКУ')
MUSIC_LEVEL = ('VOLUME', 'ГРОМКОСТЬ')
LOADING = ['Loading...', 'Загрузка...']
RULES_TEXT = ([], [])

with open(os.path.dirname(os.path.abspath(__file__)) + '\\rules_rus.txt', encoding='UTF-8') as f:
    for line in f.readlines():
        RULES_TEXT[1].append(line.strip('\n '))
# upload rules in rus
with open(os.path.dirname(os.path.abspath(__file__)) + '\\rules_eng.txt') as f:
    for line in f.readlines():
        RULES_TEXT[0].append(line.strip('\n '))

# upload rules in eng


def play_song(): # func to play song
    global menu_song, sound_state, sound_level, stop_song
    while True:
        menu_song.set_volume(sound_level * sound_state) # set volume
        start = end = time.time() # start - song playing started time
        menu_song.play() # start song
        while end - start < 102 and not stop_song: # while music has not ended and we didn't change the volume
            end = time.time() # take curr time
        stop_song = False
        menu_song.stop() # stop playing song


def change_language():
    global language
    language = not language


def mute():
    global sound_state, stop_song
    sound_state = not sound_state
    stop_song = True


def change_volume():
    global sound_level, stop_song
    sound_level += 0.1
    if sound_level > 0.5: sound_level = 0.1
    stop_song = True


def transparent_screen():
    transparent_screen = pygame.Surface((1000, 640))
    transparent_screen.set_alpha(10)
    return transparent_screen


def transparent_table():
    transparent_table = pygame.Surface((955, 400))
    transparent_table.set_alpha(100)
    return transparent_table


class Button:
    font = pygame.font.SysFont('Courier', 45, bold=True)# font for buttons

    def __init__(self, texts, button_x, button_y, txt_col, func):
        self.texts = texts
        self.button_x = button_x
        self.button_y = button_y
        self.color = txt_col
        self.active_color = [i // 2 for i in txt_col] # color used if mouse's position on the button
        self.is_active = False
        self.init_txt()
        w, h = self.txt.get_size()
        self.button_w = w + 8
        self.button_h = h + 8
        self.txt_x = button_x + 4
        self.txt_y = button_y + 4
        self.run = func

    def init_txt(self): # create text surface
        global language
        self.txt = Button.font.render(self.texts[language], True, self.color if not self.is_active else self.active_color)

    def is_pressed(self, pos, event):
        dist_x = pos[0] - self.button_x
        dist_y = pos[1] - self.button_y
        if 0 <= dist_x <= self.button_w and 0 <= dist_y <= self.button_h:
            self.is_active = True # change state to active if mouse on button
            if event.type == pygame.MOUSEBUTTONDOWN: return True
        else:
            self.is_active = False # change state to not active if mouse does not point on button
        return False # return false - button is not clicked

    def draw(self):
        global screen
        self.init_txt()
        but = pygame.Surface((self.button_w, self.button_h))
        but.set_alpha(0)  # make the button transparent
        screen.blit(but, (self.button_x, self.button_y))  # draw button
        screen.blit(self.txt, (self.txt_x, self.txt_y))  # draw text


single_or_multi = 0


def menu():
    global screen, clock, single_or_multi

    big_font = pygame.font.SysFont('Book Antiqua', 300, bold=True)
    logo_text = big_font.render('9', True, LOGO_TEXT_COLOR)

    size = max(logo_text.get_size())
    logo_background = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(logo_background, BROWN_COLOR + (120,), (size // 2, size // 2), size // 2)

    buttons = []
    x_coordinate = int(screen.get_size()[0] * 0.45)  # x coordinate for all buttons
    y_coordinates = (220, 310, 400, 490)  # y coordinate for buttons
    modes = (loading, loading, training, settings) # func-s for buttons
    texts = (SINGLE_PLAYER, MULTIPLAYER, TRAINING, SETTINGS) # text for buttons

    for data in zip(texts, y_coordinates, modes): # correspond each text with y coordinate and appropriate func-s
        buttons.append(Button(data[0], x_coordinate, data[1], BUTTON_COLOR, data[2]))

    menuloop = True
    while menuloop:

        header = font.render(THE_TOGYZ_QUMALAQ[language], True, BROWN_COLOR)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menuloop = False
            pos = pygame.mouse.get_pos()
            for i in range(len(buttons)):
                button = buttons[i]
                if button.is_pressed(pos, event):  # if button is pressed
                    single_or_multi = i # For 'loading' function
                    pressing_sound.play()
                    return button.run()

        screen.blit(background, (0, 0))# draw background image
        screen.blit(transparent_screen(), (0, 0))
        screen.blit(header, (screen.get_size()[0] // 2 - header.get_size()[0] // 2 - 60, 80))
        screen.blit(logo_background, (150 + logo_text.get_size()[0] // 2 - logo_background.get_size()[0] // 2,
                    header.get_size()[1] + 130))
        screen.blit(logo_text, (150, header.get_size()[1] + 140))
        # draw header, logo etc.

        for button in buttons:  # draw all buttons
            button.draw()

        pygame.display.flip()  # update display

    return False


def settings():
    global screen, clock
    return_button = Button(RETURN, 700, 500, BUTTON_COLOR, lambda: True)

    language_button = Button(CHANGE_LANGUAGE, 520, 200, BUTTON_COLOR, change_language)
    music_control = Button(MUSIC, 100, 200, BUTTON_COLOR, mute)
    music_level = Button(MUSIC_LEVEL, 400, 300, BUTTON_COLOR, change_volume)
    support_buttons = (music_control, language_button, music_level) # support buttons

    while True:
        text = font.render(SETTINGS[language], True, BROWN_COLOR)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            pos = pygame.mouse.get_pos()
            for button in support_buttons:
                if button.is_pressed(pos, event):
                    pressing_sound.play()
                    button.run() # just run support buttons if pressed
            if return_button.is_pressed(pos, event):
                pressing_sound.play()
                return return_button.run() # return pressed button func's value (true or false)


        screen.blit(background, (0, 0))
        screen.blit(transparent_screen(), (0, 0))
        screen.blit(text, (screen.get_size()[0] // 2 - text.get_size()[0] // 2, 80))
        for button in (return_button,) + support_buttons: # draw all buttons
            button.draw()

        pygame.display.flip()


class Run:
    def __init__(self, func):
        self.run = func


def loading():
    font = pygame.font.SysFont('Courier', 30, bold=True)
    loading_font = font.render(LOADING[language], True, BUTTON_COLOR)
    which_one = [Run(single), Run(multi)]

    cnt = 0
    k = 0
    while True:
        cnt += 1
        screen.fill((0,0,0))
        screen.blit(loading_font, (200, 420))

        if cnt % 5 == 0:
            for i in range(k+1):
                pygame.draw.rect(screen, BUTTON_COLOR, (200 + i * 100, 470, 60, 40))  #coordinates and width/height
            k += 1
            pygame.display.flip()

        if k > 6: # seven rectangles
            return which_one[single_or_multi].run()
        clock.tick(FPS)

size = (WIDTH, HEIGHT)
block_size = 35

# Scaling images of buttons
home = pygame.transform.scale(home1, (block_size, block_size))
refresh = pygame.transform.scale(refresh1, (block_size - 5, block_size - 5))
sound_on = pygame.transform.scale(sound_on1, (block_size + 15, block_size + 15))
sound_off = pygame.transform.scale(sound_off1, (block_size + 15, block_size + 15))

# ҰяшыҚ параметры
u_width = 89
u_hight = 150
distance = 10  # Distance between ҰяшыҚ

# ҚазандыҚ параметры
q_width = 880
q_hight = u_width

myfont = pygame.font.SysFont('Courier', 22, bold=True) # For numbers
u = pygame.Surface((u_width, u_hight))  # Transparent ҰяшыҚ
u.set_alpha(250)
q = pygame.Surface((q_width, q_hight))  # Transparent ҚазандыҚ
q.set_alpha(250)

quant = []
for i in range(1, 10): # List of Numbers of ҚазандыҚ
    quant.append(myfont.render(f"{i}", False, BROWN_COLOR))

BALLS = np.array([9]*18) # [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9]
first_player = 0 # points
second_player = 0
PLAYERS_POINTS = [first_player, second_player]
queue = 0 # 0 - 1st player, 1 - second player

tuzdik_1_player = None # position
tuzdik_2_player = None
TUZDIK = [tuzdik_1_player, tuzdik_2_player]
ORDER = [[list(range(0, 9)), False], [list(range(9, 18)), False]] # ORDER[0 or 1][1] == False means there is no tuzdik in range

WHO_WINS = -1 # 0 - 1st, 1 - 2nd players
a = -1 # 0 - ATSIRAU, 1 - WIN
ATSIRAU = [['Atsirau, First player wins!','Атсырау, Первый игрок выграл!'],['Atsirau, Second player wins!', 'Атсырау, Второй игрок выграл!']]
WIN = [['First player wins!', 'Первый игрок выграл!'],['Second player wins!','Второй игрок выграл!']]
ATSIRAU_OR_WIN = [ATSIRAU, WIN]

# Категы жондеу онай код жазу жане бырнеше рет каталанатын кодтарды def-ке жазу

class Algorithm:

    def __init__(self, pos):
        self.pos = pos

    def move(self): # balls moving algorithm
        global BALLS, PLAYERS_POINTS, ORDER, TUZDIK, queue, a, WHO_WINS

        list_of_kazandik = range(9, 18) if queue % 2 == 0 else range(0, 9)  # if 1 player, then (9,18) if 2 player - (0,9)
        ZEROS = np.array([0] * 18)  # [0]*18
        pos = self.pos
        cnt = 0

        if pos in ORDER[queue % 2][0]:  # cell is not tuzdik
            if BALLS[pos] != 0:
                while BALLS[pos] != cnt:  # while there is no zero balls in chosen cell
                    next_pos = pos + cnt
                    if BALLS[pos] == 1:  # if one ball in chosen cell
                        ZEROS[next_pos] = -1
                        ZEROS[(next_pos + 1) % 18] = 1
                    else:  # if more than 1 ball in chosen cell
                        if cnt == 0: # if it cell where take balls from
                            ZEROS[next_pos] = -(BALLS[pos] - 1)  # if 5 balls, then -4
                        else:
                            if next_pos <= len(BALLS) - 1:  # in one loop
                                ZEROS[next_pos] += 1
                            else:
                                next_pos %= len(BALLS)
                                ZEROS[next_pos] += 1
                    cnt += 1
                if TUZDIK[0] != None or TUZDIK[1] != None:  ###########
                    if TUZDIK[0] != None:
                        PLAYERS_POINTS[0] += ZEROS[TUZDIK[0]]
                        ZEROS[TUZDIK[0]] = 0
                    if TUZDIK[1] != None:
                        PLAYERS_POINTS[1] += ZEROS[TUZDIK[1]]
                        ZEROS[TUZDIK[1]] = 0

                BALLS += ZEROS
                if cnt == 1:
                    if (pos + cnt) % 18 in list_of_kazandik and BALLS[(pos + cnt) % 18] % 2 == 0:
                        PLAYERS_POINTS[queue % 2] += BALLS[(pos + cnt) % 18]
                        BALLS[(pos + cnt) % 18] = 0
                    if (pos + cnt) % 18 in ORDER[(queue + 1) % 2][0] and ORDER[queue % 2][1] == False \
                            and BALLS[(pos + cnt) % 18] == 3 and (pos + cnt) % 18 != (8 or 17):
                        if TUZDIK[queue % 2 + 1] != None:
                            if TUZDIK[(queue + 1) % 2] != (pos + cnt) % 9:
                                ORDER[queue % 2][1] = True
                                TUZDIK[queue % 2] = (pos + cnt) % 18
                                PLAYERS_POINTS[queue % 2] += 3
                                BALLS[(pos + cnt) % 18] = 0
                            else:
                                pass
                        else:
                            ORDER[queue % 2][1] = True
                            TUZDIK[queue % 2] = (pos + cnt) % 18
                            PLAYERS_POINTS[queue % 2] += 3
                            BALLS[(pos + cnt) % 18] = 0
                else:
                    if (pos + cnt - 1) % 18 in list_of_kazandik and BALLS[(pos + cnt - 1) % 18] % 2 == 0:
                        PLAYERS_POINTS[queue % 2] += BALLS[(pos + cnt - 1) % 18]
                        BALLS[(pos + cnt - 1) % 18] = 0
                    if (pos + cnt - 1) % 18 in ORDER[(queue + 1) % 2][0] and ORDER[queue % 2][1] == False \
                            and BALLS[(pos + cnt - 1) % 18] == 3 and (pos + cnt - 1) % 18 != (8 or 17):
                        if TUZDIK[(queue + 1) % 2] != None:
                            if TUZDIK[(queue + 1) % 2] != (pos + cnt - 1) % 9:
                                ORDER[queue % 2][1] = True
                                TUZDIK[queue % 2] = (pos + cnt - 1) % 18
                                PLAYERS_POINTS[queue % 2] += 3
                                BALLS[(pos + cnt - 1) % 18] = 0
                            else:
                                pass
                        else:
                            ORDER[queue % 2][1] = True
                            TUZDIK[queue % 2] = (pos + cnt - 1) % 18
                            PLAYERS_POINTS[queue % 2] += 3
                            BALLS[(pos + cnt - 1) % 18] = 0
                queue += 1
                stones_moving_sound.play()
            else:
                error_sound_music.play()
        else:
            error_sound_music.play()

        if PLAYERS_POINTS[0] >= 81:
            a = 1
            WHO_WINS = 0
        if PLAYERS_POINTS[1] >= 81:
            a = 1
            WHO_WINS = 1
        if sum(BALLS[0:9]) == 0:
            a = 0  #atsirau
            WHO_WINS = 1
        if sum(BALLS[9:18]) == 0:
            a = 0
            WHO_WINS = 0

    def draw_balls_uyashik(self):
        pos = self.pos
        balls_copy = BALLS.copy()

        if pos < 9: # lower uyashik
            if BALLS[pos] <= 10:
                if BALLS[pos]%2 == 0:
                    for j in range(BALLS[pos] // 2):
                        screen.blit(ball, (15 + (pos+1)*distance + pos*u_width, 585 - 29*j))
                        screen.blit(ball, (45 + (pos+1)*distance + pos*u_width, 585 - 29*j))
                else:
                    if BALLS[pos] > 1:
                        for j in range(BALLS[pos] // 2):
                            screen.blit(ball, (15 + (pos + 1) * distance + pos * u_width, 585 - 29 * j))
                            screen.blit(ball, (45 + (pos+1)*distance + pos*u_width, 585 - 29*j))
                            if j == BALLS[pos]//2 - 1:  # odd ball
                                screen.blit(ball, (15 + (pos+1)*distance + pos*u_width, 585 - 29 * (j+1)))
                    else:
                        screen.blit(ball, (15 + (pos + 1) * distance + pos * u_width, 585))
            elif 10 < BALLS[pos] <= 25:
                for j in range(5):
                    screen.blit(ball, (15 + (pos + 1) * distance + pos * u_width, 585 - 29 * j))
                    screen.blit(ball, (45 + (pos + 1) * distance + pos * u_width, 585 - 29 * j))
                balls_copy -= 10
                for j in range(balls_copy[pos]):
                    if j in range(5):
                        screen.blit(ball, (distance*(pos+1) + 30 + pos*u_width, 580 - 29*j))
                    if j in range(5, 10):
                        screen.blit(ball, (distance*(pos+1) + pos*u_width, 580 - 29*(j-5)))
                    if j in range(10, 15):
                        screen.blit(ball, (distance*(pos+1) + 60 + pos*u_width, 580 - 29*(j-10)))
            else: ######################################################################################################
                for j in range(5):
                    screen.blit(ball, (15 + (pos + 1) * distance + pos * u_width, 585 - 29 * j))
                    screen.blit(ball, (45 + (pos + 1) * distance + pos * u_width, 585 - 29 * j))
                for j in range(15):
                    if j in range(5):
                        screen.blit(ball, (distance * (pos + 1) + 30 + pos * u_width, 580 - 29 * j))
                    if j in range(5, 10):
                        screen.blit(ball, (distance * (pos + 1) + pos * u_width, 580 - 29 * (j - 5)))
                    if j in range(10, 15):
                        screen.blit(ball, (distance * (pos + 1) + 60 + pos * u_width, 580 - 29 * (j - 10)))

        else: # upper uyashik
            if BALLS[pos] <= 10:
                if BALLS[pos]%2 == 0:
                    for j in range(BALLS[pos] // 2):
                        screen.blit(ball, (859 - (pos%9+1)*distance - pos%9*u_width, 30 + 29*j))
                        screen.blit(ball, (829 - (pos%9+1)*distance - pos%9*u_width, 30 + 29*j))
                else:
                    if BALLS[pos] > 1:
                        for j in range(BALLS[pos] // 2):
                            screen.blit(ball, (859 - (pos % 9 + 1) * distance - pos % 9 * u_width, 30 + 29 * j))
                            screen.blit(ball, (829 - (pos % 9 + 1) * distance - pos % 9 * u_width, 30 + 29 * j))
                            if j == BALLS[pos]//2 - 1:
                                screen.blit(ball, (829 - (pos % 9 + 1) * distance - pos % 9 * u_width, 30 + 29 * (j+1)))
                    else:
                        screen.blit(ball, (829 - (pos%9+1)*distance - pos%9*u_width, 30))
            elif 10 < BALLS[pos] <= 25:
                for j in range(5):
                    screen.blit(ball, (859 - (pos % 9 + 1) * distance - pos % 9 * u_width, 30 + 29 * j))
                    screen.blit(ball, (829 - (pos % 9 + 1) * distance - pos % 9 * u_width, 30 + 29 * j))
                balls_copy -= 10
                for j in range(balls_copy[pos]):
                    if j in range(5):
                        screen.blit(ball, (859 - (pos % 9 + 1) * distance - pos % 9 * u_width - 15, 35 + 29 * j))
                    if j in range(5, 10):
                        screen.blit(ball, (859 - (pos % 9 + 1) * distance - pos % 9 * u_width - 45, 35 + 29 *(j-5)))
                    if j in range(10, 15):
                        screen.blit(ball, (859 - (pos % 9 + 1) * distance - pos % 9 * u_width + 15, 35 + 29 *(j-10)))
            else: ######################################################################################################
                for j in range(5):
                    screen.blit(ball, (859 - (pos % 9 + 1) * distance - pos % 9 * u_width, 30 + 29 * j))
                    screen.blit(ball, (829 - (pos % 9 + 1) * distance - pos % 9 * u_width, 30 + 29 * j))
                for j in range(15):
                    if j in range(5):
                        screen.blit(ball, (859 - (pos % 9 + 1) * distance - pos % 9 * u_width - 15, 35 + 29 * j))
                    if j in range(5, 10):
                        screen.blit(ball, (859 - (pos % 9 + 1) * distance - pos % 9 * u_width - 45, 35 + 29 * (j - 5)))
                    if j in range(10, 15):
                        screen.blit(ball, (859 - (pos % 9 + 1) * distance - pos % 9 * u_width + 15, 35 + 29 * (j - 10)))


    def draw_balls_kazandik(self, quantity):
        if quantity > 58:
            quantity = 58
        if quantity%2 == 0:
            for i in range(quantity//2):
                screen.blit(ball, (15 + i*30, 240 + (u_width+distance)*self.pos))
                screen.blit(ball, (15 + i*30, 270 + (u_width+distance)*self.pos))
        else:
            quantity -= 1
            for i in range(quantity//2):
                screen.blit(ball, (15 + i*30, 240 + (u_width+distance)*self.pos))
                screen.blit(ball, (15 + i*30, 270 + (u_width+distance)*self.pos))
                if i == quantity//2 -1:
                    screen.blit(ball, (15 + (i+1) * 30, 240 + (u_width+distance)*self.pos))


# checking which uyashik is pressed
def pressed_uyashik(pos):
    global computer
    error_sound = True
    for j in range(9): # for upper 9 uyashiks
        x_lower = distance * j + 10 + u_width * j
        y_lower = size[1] - u_hight - 30
        if pos[0] in range(x_lower, x_lower + u_width) and pos[1] in range(y_lower, y_lower + u_hight):
            algorithm = Algorithm(j)
            algorithm.move()
            error_sound = False
            computer = True
            pygame.draw.rect(screen, WHITE_COLOR, (x_lower-3, y_lower-3, u_width+6, u_hight+6), 3)

    for j in range(9): # for lower 9 uyashiks
        x_upper = distance * j + 10 + u_width * j
        y_upper = 30
        if pos[0] in range(x_upper, x_upper + u_width) and pos[1] in range(y_upper, y_upper + u_hight):
            algorithm = Algorithm(17 - j)
            algorithm.move()
            error_sound = False
            computer = False
            pygame.draw.rect(screen, WHITE_COLOR, (x_upper-3, y_upper-3, u_width+6, u_hight+6), 3)

    if error_sound == True:
        if not pressed:
            error_sound_music.play()
        else:
            pressing_sound.play()


def refresh_position():
    global BALLS, PLAYERS_POINTS, TUZDIK, ORDER, queue
    BALLS = np.array([9]*18)  # [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9]
    first_player = 0
    second_player = 0
    PLAYERS_POINTS = [first_player, second_player]
    queue = 0
    tuzdik_1_player = None
    tuzdik_2_player = None
    TUZDIK = [tuzdik_1_player, tuzdik_2_player]
    ORDER = [[list(range(0, 9)), False], [list(range(9, 18)), False]]


def winning_page(text): # page shows who wins
    global BALLS, PLAYERS_POINTS, ORDER, TUZDIK, WHO_WINS, queue, a

    font = pygame.font.SysFont('Book Antiqua', 50, bold=True)
    win = font.render(text, True, BROWN_COLOR)
    length = win.get_size()
    which_one = [Run(single), Run(multi)]

    refresh_position()
    WHO_WINS = -1
    a = -1
    while True:
        screen.blit(background, (0, 0))
        screen.blit(transparent_screen(),(0, 0))
        screen.blit(win, (size[0]//2 - length[0]//2, size[1]//2 - length[1]//2))

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    pressing_sound.play()
                    return which_one[single_or_multi].run()
        pygame.display.flip()
        clock.tick(FPS)


def multi():
    global sound_state, zoom_refresh, zoom_home, BALLS, PLAYERS_POINTS, ORDER, TUZDIK, queue, pressed, balls_quantity_font

    done = False
    zoom_refresh = True
    zoom_home = True
    font = pygame.font.SysFont('Courier', 22, bold=True) # font for buttons

    # Game loop
    while not done:
        pressed = False # True - one of 3 buttons pressed(refresh, home, sound)
        screen.blit(background, (0, 0))
        screen.blit(transparent_screen(),(0, 0))

        # Blit ҰяшыҚ
        for i in range(18):
            if i < 9:
                screen.blit(quant[i], (distance * i + 10 + u_width * i + u_width / 2 - 5, size[1] - 30))
                if i != TUZDIK[1]:
                    screen.blit(u, (distance * i + 10 + u_width * i, size[1] - u_hight - 30))
                else:
                    u_tuzdik = pygame.Surface((u_width, u_hight))  # Transparent ҰяшыҚ
                    u_tuzdik.set_alpha(300)
                    u_tuzdik.fill(BLUE_COLOR)
                    screen.blit(u_tuzdik, (distance * i + 10 + u_width * i, size[1] - u_hight - 30))
            if i >= 9:
                screen.blit(quant[-1 * (i%9 + 1)], (distance * (i%9) + 10 + u_width * (i%9) + u_width / 2 - 5, 5))
                if i != TUZDIK[0]:
                    screen.blit(u, (distance * ((17-i)%9) + 10 + u_width * ((17-i)%9), 30)) ############################
                else:
                    u_tuzdik = pygame.Surface((u_width, u_hight))  # Transparent ҰяшыҚ
                    u_tuzdik.set_alpha(300)
                    u_tuzdik.fill(BLUE_COLOR)
                    screen.blit(u_tuzdik, (distance * ((17-i)%9) + 10 + u_width * ((17-i)%9), 30)) #####################

        # Blit ҚазандыҚ
        for i in range(2):
            screen.blit(q, (10, 73 + u_hight + q_hight * i + (distance + 5) * i))

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                done = True
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:

                    pos = i.pos
                    if pos[0] in range(917, 967) and pos[1] in range(83, 111):
                        screen.blit(pygame.transform.scale(refresh1, (block_size + 1, block_size + 1)), (922, 80))
                        zoom_refresh = False
                        pressed = True
                    if pos[0] in range(917, 953) and pos[1] in range(547, 583):
                        screen.blit(pygame.transform.scale(home1, (block_size + 6, block_size + 6)), (917, 547))
                        zoom_home = False
                        pressed = True
                    if pos[0] in range(917, 968) and pos[1] in range(430, 481):
                        if sound_state == True:
                            screen.blit(pygame.transform.scale(sound_on1, (block_size + 21, block_size + 21)),(917, 430))
                        else:
                            screen.blit(pygame.transform.scale(sound_off1, (block_size + 21, block_size + 21)),(917, 430))
                        pressed = True
                        mute()
                    pressed_uyashik(pos)

            if i.type == pygame.MOUSEBUTTONUP:
                if not zoom_refresh:
                    refresh_position()
                    zoom_refresh = not zoom_refresh
                if not zoom_home:
                    refresh_position()
                    return True

        # blit balls to screen
        for i in range(18):
            draw = Algorithm(i)
            draw.draw_balls_uyashik()
        for i in range(2):
            if PLAYERS_POINTS[i] != 0:
                draw = Algorithm(i)
                draw.draw_balls_kazandik(PLAYERS_POINTS[i])

        # Who wins
        if WHO_WINS != -1:
            return winning_page(ATSIRAU_OR_WIN[a][WHO_WINS][language])

        # blit numbers of balls in kazandik and uyashik
        balls_quantity_font = []
        for i in BALLS:  # List of Numbers of BALLS in uiashik
            balls_quantity_font.append([font.render(f"{i}", True, WHITE_COLOR), font.render(f"{i}", True, WHITE_COLOR).get_size()[0]])
        kazandik_quantity_font = []
        for i in PLAYERS_POINTS:
            kazandik_quantity_font.append(font.render(f"{i}", True, WHITE_COLOR))

        for i in range(2):
            screen.blit(kazandik_quantity_font[i], (distance + q_width + 5, 105 + u_hight + q_hight * i + (distance + 5) * i))
        for i in range(9):
            screen.blit(balls_quantity_font[-1 * (i + 1)][0], (distance * i + 10 + u_width * i + u_width // 2
                                                               - balls_quantity_font[-1 * (i + 1)][1]//2 - 5, u_hight + 30))
            screen.blit(balls_quantity_font[i][0], (distance * i + 10 + u_width * i + u_width // 2
                                                    - balls_quantity_font[i][1]//2 - 5, size[1] - u_hight - 55))

        # blit buttons
        if zoom_refresh:
            screen.blit(refresh, (925, 83))
        if zoom_home:
            screen.blit(home, (920, 550))
        if sound_state:
            screen.blit(sound_on, (920, 433))
        else:
            screen.blit(sound_off, (920, 433))

        pygame.display.flip()
        clock.tick(FPS)


def single():
    global sound_state, zoom_refresh, zoom_home, BALLS, PLAYERS_POINTS, ORDER, TUZDIK, queue, pressed, balls_quantity_font, computer

    computer = False # True - computer's turn
    done = False
    zoom_refresh = True
    zoom_home = True
    font = pygame.font.SysFont('Courier', 22, bold=True)# font for buttons
    cnt = 0
    # Game loop
    while not done:
        pressed = False # True - one of 3 buttons pressed(refresh...)
        screen.blit(background, (0, 0))
        screen.blit(transparent_screen(),(0, 0))

        # Blit ҰяшыҚ
        for i in range(18):
            if i < 9:
                screen.blit(quant[i], (distance * i + 10 + u_width * i + u_width / 2 - 5, size[1] - 30))
                if i != TUZDIK[1]:
                    screen.blit(u, (distance * i + 10 + u_width * i, size[1] - u_hight - 30))
                else:
                    u_tuzdik = pygame.Surface((u_width, u_hight))  # Transparent ҰяшыҚ
                    u_tuzdik.set_alpha(300)
                    u_tuzdik.fill(BLUE_COLOR)
                    screen.blit(u_tuzdik, (distance * i + 10 + u_width * i, size[1] - u_hight - 30))
            if i >= 9:
                screen.blit(quant[-1 * (i%9 + 1)], (distance * (i%9) + 10 + u_width * (i%9) + u_width / 2 - 5, 5))
                if i != TUZDIK[0]:
                    screen.blit(u, (distance * ((17-i)%9) + 10 + u_width * ((17-i)%9), 30))   ##########################
                else:
                    u_tuzdik = pygame.Surface((u_width, u_hight))  # Transparent ҰяшыҚ
                    u_tuzdik.set_alpha(300)
                    u_tuzdik.fill(BLUE_COLOR)
                    screen.blit(u_tuzdik, (distance * ((17-i)%9) + 10 + u_width * ((17-i)%9), 30)) #####################

        # Blit ҚазандыҚ
        for i in range(2):
            screen.blit(q, (10, 73 + u_hight + q_hight * i + (distance + 5) * i))

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                done = True
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:

                    pos = i.pos
                    if pos[0] in range(917, 967) and pos[1] in range(83, 111):
                        screen.blit(pygame.transform.scale(refresh1, (block_size + 1, block_size + 1)), (922, 80))
                        zoom_refresh = False
                        pressed = True
                    if pos[0] in range(917, 953) and pos[1] in range(547, 583):
                        screen.blit(pygame.transform.scale(home1, (block_size + 6, block_size + 6)), (917, 547))
                        zoom_home = False
                        pressed = True
                    if pos[0] in range(917, 968) and pos[1] in range(430, 481):
                        if sound_state == True:
                            screen.blit(pygame.transform.scale(sound_on1, (block_size + 21, block_size + 21)),(917, 430))
                        else:
                            screen.blit(pygame.transform.scale(sound_off1, (block_size + 21, block_size + 21)),(917, 430))
                        pressed = True
                        mute()

                    if computer == False:
                        pressed_uyashik(pos)
                    else:
                        error_sound_music.play()

            if i.type == pygame.MOUSEBUTTONUP:
                if not zoom_refresh:
                    refresh_position()
                    zoom_refresh = not zoom_refresh
                if not zoom_home:
                    refresh_position()
                    return True # menu()

        cnt += 1
        if cnt%30 == 0: # computer thinking pause
            positions = [] # list of possible uyashiks
            b = []
            for i in range(9):
                x_upper = distance * ((17-i)%9) + 10 + u_width * ((17-i)%9) + u_width // 2
                y_upper = 30 + u_hight // 2
                if BALLS[9 + i] != 0:
                    positions.append((x_upper, y_upper))
                else:
                    b.append(9+i)
            # computer's turn if True
            if computer == True:
                print(len(b))
                random = np.random.randint(0, len(positions))
                pressed_uyashik(positions[random])

        # blit balls kazandik and uyashik
        for i in range(18):
            draw = Algorithm(i)
            draw.draw_balls_uyashik()
        for i in range(2):
            if PLAYERS_POINTS[i] != 0:
                draw = Algorithm(i)
                draw.draw_balls_kazandik(PLAYERS_POINTS[i])

        # Who wins
        if WHO_WINS != -1:
            return winning_page(ATSIRAU_OR_WIN[a][WHO_WINS][language])

        # blit numbers of balls in kazandik and uyashik
        balls_quantity_font = []
        for i in BALLS:  # List of Numbers of BALLS in kazandik
            balls_quantity_font.append(
                [font.render(f"{i}", True, WHITE_COLOR), font.render(f"{i}", True, WHITE_COLOR).get_size()[0]])
        kazandik_quantity_font = []
        for i in PLAYERS_POINTS:
            kazandik_quantity_font.append(font.render(f"{i}", True, WHITE_COLOR))

        for i in range(2):
            screen.blit(kazandik_quantity_font[i],
                        (distance + q_width + 5, 105 + u_hight + q_hight * i + (distance + 5) * i))
        for i in range(9):
            screen.blit(balls_quantity_font[-1 * (i + 1)][0], (distance * i + 10 + u_width * i + u_width // 2
                                                               - balls_quantity_font[-1 * (i + 1)][1] // 2 - 5,
                                                               u_hight + 30))
            screen.blit(balls_quantity_font[i][0], (distance * i + 10 + u_width * i + u_width // 2
                                                    - balls_quantity_font[i][1] // 2 - 5, size[1] - u_hight - 55))

        # blit buttons
        if zoom_refresh:
            screen.blit(refresh, (925, 83))
        if zoom_home:
            screen.blit(home, (920, 550))
        if sound_state:
            screen.blit(sound_on, (920, 433))
        else:
            screen.blit(sound_off, (920, 433))

        pygame.display.flip()
        clock.tick(FPS)


def training(): # call the test function with current gamemode argument
    global screen, clock
    button = Button(RETURN, 700, 560, BUTTON_COLOR, lambda: True)  # return button
    small_font = pygame.font.SysFont('Courier', 15, bold=True)
    while True:
        text = font.render(RULES[language], True, BROWN_COLOR)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            pos = pygame.mouse.get_pos()
            if button.is_pressed(pos, event):
                pressing_sound.play()
                return button.run()  # return True if return button is pressed

        screen.blit(background, (0, 0))  # draw background
        screen.blit(transparent_screen(), (0, 0))
        screen.blit(transparent_table(), (25, 165))
        screen.blit(text, (screen.get_size()[0] // 2 - text.get_size()[0] // 2, 80))
        for i, line in enumerate(RULES_TEXT[language]):
            line = small_font.render(line, True, WHITE_COLOR)  # render rules texts
            screen.blit(line, (30, 165 + i * 20))  # draw rules texts

        button.draw()  # draw return button
        pygame.display.flip()


song = Thread(target=play_song) # create song thread
song.daemon = True
song.start() # start song thread

# Game loop
while menu(): # call menu
    pass
