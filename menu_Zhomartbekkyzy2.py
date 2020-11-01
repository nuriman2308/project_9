import pygame
import os
from threading import Thread
import time
#pylint: disable=no-member, too-many-function-args

pygame.init() # pygame initialization

FPS = 60
WIDTH, HEIGHT = 1000, 640 # screen sizes
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('THE TOGYZ QUMALAQ')
clock = pygame.time.Clock()
try: # trying to load background file
    background = pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '\\background.jpg')
except pygame.error: # if we can't find file, we will just use brown background
    print('File not found, default background will be used')
    background = pygame.Surface((1000, 640))
    background.fill((61, 23, 0))

menu_song = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '\\menu.wav') # song file
stop_song = False

BROWN_COLOR = (139, 69, 19)
BUTTON_COLOR = (205, 133, 63)
font = pygame.font.SysFont('Courier', 60, bold=True)
language = False # False - eng, True - rus
sound_state = True # True - music on, False - music off
sound_level = 0.5 # song volume

THE_TOGYZ_QUMALAQ = ('THE TOGYZ QUMALAQ', 'ТОҒЫЗ ҚҰМАЛАҚ')
SINGLE_PLAYER = ('SINGLE PLAYER', 'ОДИНОЧНАЯ ИГРА')
MULTIPLAYER = ('MULTIPLAYER', 'МУЛЬТИПЛЕЕР')
TRAINING = ('TRAINING', 'ТРЕНИРОВКА')
SETTINGS = ('SETTINGS', 'НАСТРОЙКИ')
RETURN = ('RETURN', 'НАЗАД')
CHANGE_LANGUAGE = ('CHANGE LANGUAGE', 'СМЕНИТЬ ЯЗЫК')
RULES = ('RULES', 'ПРАВИЛА')
MUSIC = ('ON/OFF MUSIC', 'ВКЛ/ВЫКЛ МУЗЫКУ')
MUSIC_LEVEL = ('CHANGE VOLUME', 'ИЗМЕНИТЬ ГРОМКОСТЬ')
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

class Button:

    font = pygame.font.SysFont('Courier', 36, bold=True)# font for buttons

    def __init__(self, texts, button_x, button_y, txt_col, func):
        self.texts = texts
        self.button_x = button_x
        self.button_y = button_y
        self.color = txt_col
        self.active_color = [i // 2 for i in txt_col] # color used if mouse points on button
        self.is_active = False
        self.init_txt()
        w, h = self.txt.get_size()
        self.button_w = w + 8
        self.button_h = h + 8
        self.txt_x = button_x + self.button_w // 2 - w // 2
        self.txt_y = button_y + self.button_h // 2 - h // 2
        self.run = func

    def init_txt(self): # create text surface
        global language
        self.txt = Button.font.render(self.texts[language], True, self.color if not self.is_active else self.active_color)

    def is_pressed(self, pos, event):
        dist_x = pos[0] - self.button_x
        dist_y = pos[1] - self.button_y
        if 0 <= dist_x <= self.button_w and 0 <= dist_y <= self.button_h:
            self.is_active = True # change state to active if mouse points on button
            if event.type == pygame.MOUSEBUTTONDOWN: return True
        else:
            self.is_active = False # change state to not active if mouse does not point on button
        return False # return false - button is not clicked

    def draw(self):
        global screen
        self.init_txt()
        but = pygame.Surface((self.button_w, self.button_h))
        but.set_alpha(0) # make the button transparent
        screen.blit(but, (self.button_x, self.button_y)) # draw button
        screen.blit(self.txt, (self.txt_x, self.txt_y)) # draw text


def menu():
    global screen, clock

    big_font = pygame.font.SysFont('Courier', 300, bold=True)
    logo_text = big_font.render('9', True, BROWN_COLOR)

    size = max(logo_text.get_size())
    logo_background = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(logo_background, BROWN_COLOR + (50,), (size // 2, size // 2), size // 2)

    buttons = []
    x_coordinate = int(screen.get_size()[0] * 0.55)  # x coordinate for all buttons
    y_coordinates = (200, 300, 400, 500)  # y coordinate for buttons
    modes = (single, multi, training, settings) # func-s for buttons
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
            for button in buttons:
                if button.is_pressed(pos, event):  # if button is pressed
                    return button.run() # run its func

        screen.blit(background, (0, 0))# draw background image
        screen.blit(header, (screen.get_size()[0] // 2 - header.get_size()[0] // 2, 80))
        screen.blit(logo_background, (100 + logo_text.get_size()[0] // 2 - logo_background.get_size()[0] // 2,
                    header.get_size()[1] + 150))
        screen.blit(logo_text, (100, header.get_size()[1] + 150))
        # draw header, logo etc.
        for button in buttons: # draw all buttons
            button.draw()

        pygame.display.flip() # update display

    return False

def rules():
    global screen, clock
    button = Button(RETURN, 700, 500, BUTTON_COLOR, lambda: True) #return button
    small_font = pygame.font.SysFont('Courier', 18, bold=True)
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
                return button.run() # return True if return buttom is pressed

        screen.blit(background, (0, 0)) # draw background
        screen.blit(text, (screen.get_size()[0] // 2 - text.get_size()[0] // 2, 80))
        for i, line in enumerate(RULES_TEXT[language]):
            line = small_font.render(line, True, BUTTON_COLOR) # render rules texts
            screen.blit(line, (screen.get_size()[0] // 2 - line.get_size()[0] // 2, 150 + i*20)) # draw rules texts

        button.draw() # draw return button
        pygame.display.flip()

def settings():
    global screen, clock
    return_button = Button(RETURN, 700, 500, BUTTON_COLOR, lambda: True)
    rules_button = Button(RULES, 500, 300, BUTTON_COLOR, rules)
    buttons = (rules_button, return_button) # "callable" buttons

    language_button = Button(CHANGE_LANGUAGE, 500, 200, BUTTON_COLOR, change_language)
    music_control = Button(MUSIC, 100, 200, BUTTON_COLOR, mute)
    music_level = Button(MUSIC_LEVEL, 100, 300, BUTTON_COLOR, change_volume)
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
                    button.run() # just run support buttons if pressed
            for button in buttons:
                if button.is_pressed(pos, event):
                    return button.run() # return pressed button func's value (true or false)

        screen.blit(background, (0, 0))
        screen.blit(text, (screen.get_size()[0] // 2 - text.get_size()[0] // 2, 80))
        for button in buttons + support_buttons: # draw all buttons
            button.draw()

        pygame.display.flip()


def empty(texts): # test function for gamemodes
    global screen, clock
    button = Button(RETURN, 700, 500, (50, 50, 50), lambda: True)
    while True:
        text = font.render(texts[language], True, (0, 0, 0))  # render gamemode
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            pos = pygame.mouse.get_pos()
            if button.is_pressed(pos, event): 
                return button.run() # return True if return bitton is pressed

        screen.fill((255, 255, 255)) # fill with white color
        screen.blit(text, (screen.get_size()[0] // 2 - text.get_size()[0] // 2, 80))
        button.draw() # draw the button

        pygame.display.flip()  # update the screen

def single(): # call the test function with current gamemode argument
    return empty(SINGLE_PLAYER)
def multi(): # call the test function with current gamemode argument
    return empty(MULTIPLAYER)
def training(): # call the test function with current gamemode argument
    return empty(TRAINING)

song = Thread(target=play_song) # create song thread
song.daemon = True
song.start() # start song thread
gamemode = ''
while menu(): # call menu
    pass
