import pygame
import os
import sys
import vlc #new
from threading import Thread
import time

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


WIDTH, HEIGHT = 1000, 640 # screen sizes
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('THE TOGYZ QUMALAQ')
icon = pygame.image.load("Logo.png")
pygame.display.set_icon(icon)
intro()

pygame.init()
clock = pygame.time.Clock()
FPS = 20
pygame. display. set_icon(icon)

background = pygame.image.load('background.png')
home1 = pygame.image.load('Home.png')
refresh1 = pygame.image.load('Refresh.png')
sound_on1 = pygame.image.load('Sound on.png')
sound_off1 = pygame.image.load('Sound off.png')

menu_song = pygame.mixer.Sound('menu.wav') # song file
stop_song = False

BROWN_COLOR = (36, 12, 4)
BUTTON_COLOR = (255, 166, 41)
WHITE_COLOR = (255, 255, 179)
single_or_multi = 0

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


def transparent_table(): # RULES
    transparent_table = pygame.Surface((955, 365))
    transparent_table.set_alpha(100)
    return transparent_table


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


def transparent_screen():# menu and single, multi player
    transparent_screen = pygame.Surface((1000, 640))
    transparent_screen.set_alpha(10)
    return transparent_screen


class Button:
    font = pygame.font.SysFont('Courier', 45, bold=True)# font for buttons

    def __init__(self, texts, button_x, button_y, txt_col, func):
        self.texts = texts
        self.button_x = button_x
        self.button_y = button_y
        self.color = txt_col
        self.active_color = [i // 2 for i in txt_col] # color used if mouse's position on the button
        self.is_active = False # if cursor is on the button
        self.init_txt()
        w, h = self.txt.get_size() # size of the text
        self.button_w = w + 8
        self.button_h = h + 8
        self.txt_x = button_x + 4 #self.button_w // 2 - w // 2
        self.txt_y = button_y + 4 #self.button_h // 2 - h // 2
        self.run = func

    def init_txt(self): # create text surface
        global language
        self.txt = Button.font.render(self.texts[language], True, self.color if not self.is_active else self.active_color)

    def is_pressed(self, pos, event):
        dist_x = pos[0] - self.button_x
        dist_y = pos[1] - self.button_y
        if 0 <= dist_x <= self.button_w and 0 <= dist_y <= self.button_h:
            self.is_active = True # change state to active if cursor on button
            if event.type == pygame.MOUSEBUTTONDOWN: return True
        else:
            self.is_active = False # change state to not active if cursor does not point on button
        return False # return false - button is not clicked

    def draw(self):
        global screen
        self.init_txt()
        but = pygame.Surface((self.button_w, self.button_h))
        but.set_alpha(0) # make the button transparent
        screen.blit(but, (self.button_x, self.button_y)) # draw button
        screen.blit(self.txt, (self.txt_x, self.txt_y)) # draw text


def menu():
    global screen, clock, single_or_multi

    big_font = pygame.font.SysFont('Book Antiqua', 300, bold=True)
    logo_text = big_font.render('9', True, BROWN_COLOR)

    size = max(logo_text.get_size())
    logo_background = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(logo_background, BROWN_COLOR + (100,), (size // 2, size // 2), size // 2)

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
                    return button.run()

        screen.blit(background, (0, 0))# draw background image
        screen.blit(transparent_screen(), (0, 0))
        screen.blit(header, (screen.get_size()[0] // 2 - header.get_size()[0] // 2 - 60, 80))
        screen.blit(logo_background, (150 + logo_text.get_size()[0] // 2 - logo_background.get_size()[0] // 2,
                    header.get_size()[1] + 130))
        screen.blit(logo_text, (150, header.get_size()[1] + 140))
        # draw header, logo etc.

        for button in buttons: # draw all buttons
            button.draw()

        pygame.display.flip() # update display

    return False
#end of menu section


def settings():
    global screen, clock
    return_button = Button(RETURN, 700, 500, BUTTON_COLOR, lambda: True)
    language_button = Button(CHANGE_LANGUAGE, 520, 200, BUTTON_COLOR, change_language)
    music_control = Button(MUSIC, 100, 200, BUTTON_COLOR, mute)
    music_level = Button(MUSIC_LEVEL, 400, 300, BUTTON_COLOR, change_volume)
    support_buttons = (music_control, language_button, music_level, return_button) # support buttons

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
                    button.run() # just run support buttons if pressed
            if return_button.is_pressed(pos, event):
                return return_button.run() # return pressed button func's value (true or false)


        screen.blit(background, (0, 0))
        screen.blit(transparent_screen(), (0, 0))
        screen.blit(text, (screen.get_size()[0] // 2 - text.get_size()[0] // 2, 80))
        for button in support_buttons: # draw all buttons
            button.draw()

        pygame.display.flip()


def training(): # call the test function with current gamemode argument
    global screen, clock
    button = Button(RETURN, 700, 530, BUTTON_COLOR, lambda: True)  # return button
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


class Run:
    def __init__(self, func):
        self.run = func


def loading():
    font = pygame.font.SysFont('Courier', 30, bold=True)
    loading_font = font.render(LOADING[language], True, BUTTON_COLOR)

    which_one = [] # multi or single
    for i in single, multi:
        which_one.append(Run(i))

    cnt = 0
    k = 0
    while True:
        cnt += 1
        screen.fill((0,0,0))
        screen.blit(loading_font, (200, 420))

        if cnt % 5 == 0:
            for i in range(k+1):
                pygame.draw.rect(screen, BUTTON_COLOR, (200 + i * 100, 470, 60, 40))
            k += 1
            pygame.display.flip()

        if k > 6:
            return which_one[single_or_multi].run() # to run function of buttons
        clock.tick(FPS)


def single(): # call the test function with current gamemode argument
    global screen, clock, sound_state
    size = (WIDTH, HEIGHT)

    block_size = 35
    YELLOW = (255, 166, 41)

    # Scaling images
    home = pygame.transform.scale(home1, (block_size, block_size))
    refresh = pygame.transform.scale(refresh1, (block_size - 5, block_size - 5))
    sound_on = pygame.transform.scale(sound_on1, (block_size + 15, block_size + 15))
    sound_off = pygame.transform.scale(sound_off1, (block_size + 15, block_size + 15))

    # Scales
    # ҰяшыҚ
    uyashiq = 9
    u_width = 89
    u_hight = 150
    distance = 10  # Distance between ҰяшыҚ
    # ҚазандыҚ
    qazandik = 2
    q_width = 880
    q_hight = u_width

    # For numbers
    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 22)

    # List of Numbers of ҚазандыҚ
    quant = []
    for i in range(1, 10):
        quant.append(myfont.render(f"{i}", False, YELLOW))

    # Transparent ҰяшыҚ
    u = pygame.Surface((u_width, u_hight))
    u.set_alpha(140)

    # Transparent ҚазандыҚ
    q = pygame.Surface((q_width, q_hight))
    q.set_alpha(140)

    done = False
    Zoom_refresh = True
    Zoom_home = True
    # Game loop
    while not done:
        screen.blit(background, (0, 0))
        screen.blit(transparent_screen(),(0, 0))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                done = True
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    if i.pos[0] in range(917, 967) and i.pos[1] in range(83, 111):
                        screen.blit(pygame.transform.scale(refresh1, (block_size + 1, block_size + 1)), (917, 80))
                        Zoom_refresh = False
                    if i.pos[0] in range(917, 953) and i.pos[1] in range(547, 583):
                        screen.blit(pygame.transform.scale(home1, (block_size + 6, block_size + 6)), (917, 547))
                        Zoom_home = False
                    if i.pos[0] in range(917, 968) and i.pos[1] in range(430, 481):
                        if sound_state == True:
                            screen.blit(pygame.transform.scale(sound_on1, (block_size + 21, block_size + 21)),(917, 430))
                        else:
                            screen.blit(pygame.transform.scale(sound_off1, (block_size + 21, block_size + 21)),(917, 430))
                        mute()

            if i.type == pygame.MOUSEBUTTONUP:
                if not Zoom_refresh:
                    return single()
                if not Zoom_home:
                    return menu()


        # Blitting ҰяшыҚ
        for i in range(uyashiq):
            screen.blit(quant[-1 * (i + 1)], (distance * i + 10 + u_width * i + u_width / 2 - 5, 5))
            screen.blit(u, (distance * i + 10 + u_width * i, 30))
            screen.blit(quant[i], (distance * i + 10 + u_width * i + u_width / 2 - 5, size[1] - 30))
            screen.blit(u, (distance * i + 10 + u_width * i, size[1] - u_hight - 30))

        # Blitting ҚазандыҚ
        for i in range(qazandik):
            screen.blit(q, (10, 73 + u_hight + q_hight * i + (distance+5) * i))

        if Zoom_refresh:
            screen.blit(refresh, (920, 83))
        if Zoom_home:
            screen.blit(home, (920, 550))
        if sound_state:
            screen.blit(sound_on, (920, 433))
        else:
            screen.blit(sound_off, (920, 433))


        pygame.display.flip()
        clock.tick(FPS)


def multi(): # call the test function with current gamemode argument
    global screen, clock, sound_state
    size = (WIDTH, HEIGHT)

    block_size = 35
    YELLOW = (255, 166, 41)

    # Scaling images
    home = pygame.transform.scale(home1, (block_size, block_size))
    refresh = pygame.transform.scale(refresh1, (block_size - 5, block_size - 5))
    sound_on = pygame.transform.scale(sound_on1, (block_size + 15, block_size + 15))
    sound_off = pygame.transform.scale(sound_off1, (block_size + 15, block_size + 15))

    # Scales
    # ҰяшыҚ
    uyashiq = 9
    u_width = 89
    u_hight = 150
    distance = 10  # Distance between ҰяшыҚ
    # ҚазандыҚ
    qazandik = 2
    q_width = 880
    q_hight = u_width

    # For numbers
    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 22)

    # List of Numbers of ҚазандыҚ
    quant = []
    for i in range(1, 10):
        quant.append(myfont.render(f"{i}", False, YELLOW))

    # Transparent ҰяшыҚ
    u = pygame.Surface((u_width, u_hight))
    u.set_alpha(140)

    # Transparent ҚазандыҚ
    q = pygame.Surface((q_width, q_hight))
    q.set_alpha(140)

    done = False
    Zoom_refresh = True
    Zoom_home = True
    # Game loop
    while not done:
        screen.blit(background, (0, 0))
        screen.blit(transparent_screen(), (0, 0))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                done = True
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    if i.pos[0] in range(917, 967) and i.pos[1] in range(83, 111):
                        screen.blit(pygame.transform.scale(refresh1, (block_size + 1, block_size + 1)), (917, 80))
                        Zoom_refresh = False
                    if i.pos[0] in range(917, 953) and i.pos[1] in range(547, 583):
                        screen.blit(pygame.transform.scale(home1, (block_size + 6, block_size + 6)), (917, 547))
                        Zoom_home = False
                    if i.pos[0] in range(917, 968) and i.pos[1] in range(430, 481):
                        if sound_state:
                            screen.blit(pygame.transform.scale(sound_on1, (block_size + 21, block_size + 21)), (917, 430))
                        else:
                            screen.blit(pygame.transform.scale(sound_off1, (block_size + 21, block_size + 21)), (917, 430))
                        mute()

            if i.type == pygame.MOUSEBUTTONUP:
                if not Zoom_refresh:
                    return multi()
                if not Zoom_home:
                    return menu()

        # Blitting ҰяшыҚ
        for i in range(uyashiq):
            screen.blit(quant[-1 * (i + 1)], (distance * i + 10 + u_width * i + u_width / 2 - 5, 5))
            screen.blit(u, (distance * i + 10 + u_width * i, 30))
            screen.blit(quant[i], (distance * i + 10 + u_width * i + u_width / 2 - 5, size[1] - 30))
            screen.blit(u, (distance * i + 10 + u_width * i, size[1] - u_hight - 30))

        # Blitting ҚазандыҚ
        for i in range(qazandik):
            screen.blit(q, (10, 73 + u_hight + q_hight * i + (distance + 5) * i))

        if Zoom_refresh:
            screen.blit(refresh, (920, 83))
        if Zoom_home:
            screen.blit(home, (920, 550))
        if sound_state:
            screen.blit(sound_on, (920, 433))
        else:
            screen.blit(sound_off, (920, 433))

        pygame.display.flip()
        clock.tick(FPS)

song = Thread(target=play_song) # create song thread
song.daemon = True
song.start() # start song thread
gamemode = ''
while menu(): # call menu
    pass
