import pygame
import os
from threading import Thread
import time
import random
#pylint: disable=no-member, too-many-function-args

pygame.init() # pygame initialization

FPS = 20
WIDTH, HEIGHT = 1000, 640 # screen sizes
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('THE TOGYZ QUMALAQ')
clock = pygame.time.Clock()
try: # trying to load background file
    background = pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '\\background.png')
except pygame.error: # if we can't find file, we will just use brown background
    print('File not found, default background will be used')
    background = pygame.Surface((1000, 640))
    background.fill((61, 23, 0))

menu_song = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '\\menu.wav') # song file
stop_song = False

BROWN_COLOR = (36, 12, 4)
BUTTON_COLOR = (232, 142, 51)#(205, 133, 63)
font = pygame.font.SysFont('Book Antiqua', 70, bold=True)
language = False # False - eng, True - rus
sound_state = True # True - music on, False - music off
sound_level = 0.5 # song volume

THE_TOGYZ_QUMALAQ = ('THE TOGYZ QUMALAQ', 'ТОГЫЗ КУМАЛАК')
SINGLE_PLAYER = ('SINGLE PLAYER', 'ОДИН ИГРОК')
MULTIPLAYER = ('MULTI PLAYER', 'ДВА МГРОКА')
TRAINING = ('RULES OF THE GAME', 'ПРАВИЛА ИГРЫ')
SETTINGS = ('SETTINGS', 'НАСТРОЙКИ')
RETURN = ('RETURN', 'НАЗАД')
CHANGE_LANGUAGE = ('CHANGE LANGUAGE', 'СМЕНИТЬ ЯЗЫК')
RULES = ('RULES', 'ПРАВИЛА')
MUSIC = ('ON/OFF MUSIC', 'ВКЛ/ВЫКЛ МУЗЫКУ')
MUSIC_LEVEL = ('VOLUME', 'ГРОМКОСТЬ')
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

    font = pygame.font.SysFont('Courier', 45, bold=True)# font for buttons

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

transparent_screen = pygame.Surface((1000, 640))
transparent_screen.set_alpha(50)
transparent_screen.fill((0, 0, 0))
def menu():
    global screen, clock


    big_font = pygame.font.SysFont('Book Antiqua', 300, bold=True)
    logo_text = big_font.render('9', True, BROWN_COLOR)

    size = max(logo_text.get_size())
    logo_background = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(logo_background, BROWN_COLOR + (100,), (size // 2, size // 2), size // 2)

    buttons = []
    x_coordinate = int(screen.get_size()[0] * 0.45)  # x coordinate for all buttons
    y_coordinates = (220, 310, 400, 490)  # y coordinate for buttons
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
        screen.blit(transparent_screen, (0, 0))
        screen.blit(header, (screen.get_size()[0] // 2 - header.get_size()[0] // 2 - 60, 80))
        screen.blit(logo_background, (150 + logo_text.get_size()[0] // 2 - logo_background.get_size()[0] // 2,
                    header.get_size()[1] + 130))
        screen.blit(logo_text, (150, header.get_size()[1] + 140))
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
        screen.blit(transparent_screen, (0, 0))
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
    size = (1000, 640)
    fps = 20  # Frames per second
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    block_size = 35
    YELLOW = (237, 132, 17)
    BLACK = (0, 0, 0)

    # Load images
    background = pygame.image.load('background.png')
    ball = pygame.image.load("Ball.png")
    home1 = pygame.image.load('Home.png')
    refresh1 = pygame.image.load('Refresh.png')
    sound_on1 = pygame.image.load('Sound on.png')
    home = pygame.transform.scale(home1, (block_size, block_size))
    refresh = pygame.transform.scale(refresh1, (block_size - 5, block_size - 5))
    sound_on = pygame.transform.scale(sound_on1, (block_size + 15, block_size + 15))

    # Scales
    # ҰяшыҚ
    uyashiq = 9
    u_width = 89
    u_hight = 150
    distance = 10  # Distance between ҰяшыҚ
    # ҚазандыҚ
    qazandik = 2
    q_width = 880
    q_hight = 89

    # For numbers
    pygame.font.init()#жазу корыну ушын
    myfont = pygame.font.SysFont('Arial', 22)

    # List of Numbers of ҚазандыҚ
    quant = []
    for i in range(1, 10):
        quant.append(myfont.render(f"{i}", False, YELLOW))

    # Transparent ҰяшыҚ
    u = pygame.Surface((u_width, u_hight))
    u.fill(BLACK)
    tuzdyk = pygame.Surface((u_width, u_hight))
    tuzdyk.fill((120,120,120))
    # Transparent ҚазандыҚ
    q = pygame.Surface((q_width, q_hight))
    q.set_alpha(140)
    q.fill(BLACK)

    done = False
    Zoom_refresh = True
    Zoom_home = True
    Zoom_sound_on = True
    # Game loop
    while not done:
        screen.blit(background, (0, 0))
        screen.blit(transparent_screen,(0, 0))
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
                        screen.blit(pygame.transform.scale(sound_on1, (block_size + 21, block_size + 21)), (917, 430))
                        Zoom_sound_on = False

            if i.type == pygame.MOUSEBUTTONUP:
                Zoom_refresh = True
                if not Zoom_home:
                    return menu()
                Zoom_sound_on = True
        # Blitting ҰяшыҚ
        for i in range(uyashiq):
            screen.blit(quant[-1 * (i + 1)], (distance * i + 10 + u_width * i + u_width / 2 - 5, 5))
            screen.blit(u, (distance * i + 10 + u_width * i, 30))
            screen.blit(quant[i], (distance * i + 10 + u_width * i + u_width / 2 - 5, size[1] - 30))
            screen.blit(u, (distance * i + 10 + u_width * i, size[1] - u_hight - 30))

            #алгоритм;
            y0 = 35
            for j in range(5):
                screen.blit(ball, (distance * i + u_width * i + 20, y0))
                y0 += 28
            y0 = 35
            for j in range(4):
                screen.blit(ball, (distance * i + u_width * i + 60, y0))
                y0 += 28
            y0 = 580
            for j in range(5):
                screen.blit(ball, (distance * i + u_width * i + 20, y0))
                y0 -= 28
            y0 = 580
            for j in range(4):
                screen.blit(ball, (distance * i + u_width * i + 60, y0))
                y0 -= 28
        pygame.display.update()
        # Blitting ҚазандыҚ
        for i in range(qazandik):
            screen.blit(q, (10, 73 + u_hight + q_hight * i + (distance+5) * i))
        PL1 = True
        cnt = [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9]
        q1 = 0
        q2 = 0
        tuzdyk1 = 19
        tuzdyk2 = 19
        tuz1 = False
        tuz2 = False
        wh = 0

        error1 = pygame.mixer.Sound("error1.mp3")
        kamni = pygame.mixer.Sound("kamni.mp3")
        while PL1:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()
                if i.type == pygame.MOUSEBUTTONDOWN:
                    if i.button == 1:
                        for p in range(9):
                            if i.pos[0] in range(10 + 99*p, 99 + 99*p) and i.pos[1] in range(430, 580):
                                wh = 1
                                kamni.play()
                                v = cnt[p] 
                                cnt[p] = 1
                                if v == 1:
                                    cnt[p]=0
                                    cnt[p+1]+=1
                                    if p==8 and cnt[9]%2==0:
                                        q1+=cnt[9]
                                        cnt[9]=0
                                if v == 0:
                                    error1.play()
                                    cnt[p] = 0
                                    continue
                                if v> (18-p):
                                    for k in range(p+1, 18):
                                        cnt[k]+=1
                                        m = v - 18+p
                                    for k in range(m):
                                        cnt[k]+=1
                                    if m>8 and cnt[m]%2==0:
                                        q1 += cnt[m]
                                    if m>8 and m!=8 and m!=17 and cnt[m]==3:
                                        tuzdyk1 = m
                                        tuz1 = True
                                else:
                                    m = v+p-1
                                    for k in range(p+1, v+p):
                                        cnt[k]+=1
                                    if cnt[m]%2==0 and (m)>8:
                                        q1+=cnt[m]
                                        cnt[m] = 0
                                    if not tuz1:
                                        if m>8 and m!=8 and m!=17 and cnt[m]==3:
                                            tuzdyk1 = m
                                            tuz1 = True
                                if tuz1: q1+=cnt[tuzdyk1]; cnt[tuzdyk1] = 0
                                print(cnt, q1, q2)
                            else:error1.play()
                        for k in range(len(cnt)):
                            if k<9:
                                if cnt[k]==0:
                                    screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                if cnt[k]==1:
                                    screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                    screen.blit(ball, (distance * k + u_width * k + 20, 580))
                                if cnt[k]>10 and cnt[k]<26:
                                    screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                    y0=580
                                    for z in range(5):
                                        screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                        y0-=28
                                    y0=580
                                    for z in range(5):
                                        screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                        y0-=28
                                    l=int((cnt[k]-10)/3)
                                    y0=580 
                                    for z in range(l):
                                        screen.blit(ball, (distance * k + u_width * k + 12, y0))
                                        screen.blit(ball, (distance * k + u_width * k + 40, y0))
                                        screen.blit(ball, (distance * k + u_width * k + 68, y0))
                                        y0-=28
                                    l=(cnt[k]-10)%3
                                    x0=12
                                    for z in range(l):
                                        screen.blit(ball, (distance * k + u_width * k + x0, y0))
                                        x0+=28
                                if cnt[k]>25:
                                    screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                    y0=580
                                    for z in range(5):
                                        screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                        y0-=28
                                    y0=580
                                    for z in range(5):
                                        screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                        y0-=28
                                    
                                    y0=580 
                                    for z in range(5):
                                        screen.blit(ball, (distance * k + u_width * k + 12, y0))
                                        screen.blit(ball, (distance * k + u_width * k + 40, y0))
                                        screen.blit(ball, (distance * k + u_width * k + 68, y0))
                                        y0-=28
                                    

                                if cnt[k]<=10:
                                    screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                    y0=580
                                    for z in range(cnt[k]-int(cnt[k]/2)):
                                        screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                        y0-=28
                                    y0=580
                                    for z in range(int(cnt[k]/2)):
                                        screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                        y0-=28
                                if k==tuzdyk1:
                                    screen.blit(tuzdyk, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))

                            if k>8:
                                k0=17-k
                                if cnt[k]==0:
                                    screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                if cnt[k]==1:
                                    screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                    screen.blit(ball, (distance * k0 + u_width * k0 + 20, 35))
                                if cnt[k]>10 and cnt[k]<26:
                                    screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                    y0=35
                                    for z in range(5):
                                        screen.blit(ball, (distance * k0 + u_width * k0 + 20, y0))
                                        y0+=28
                                    y0=35
                                    for z in range(5):
                                        screen.blit(ball, (distance * k0 + u_width * k0 + 60, y0))
                                        y0+=28
                                    l=int((cnt[k]-10)/3)
                                    y0=35
                                    for z in range(l):
                                        screen.blit(ball, (distance * k0 + u_width * k0 + 12, y0))
                                        screen.blit(ball, (distance * k0 + u_width * k0 + 40, y0))
                                        screen.blit(ball, (distance * k0 + u_width * k0 + 68, y0))
                                        y0+=28
                                    l=(cnt[k]-10)%3
                                    x0=12
                                    for z in range(l):
                                        screen.blit(ball, (distance * k0 + u_width * k0 + x0, y0))
                                        x0+=28
                                if cnt[k]>25:
                                    screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                    y0=580
                                    for z in range(5):
                                        screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                        y0-=28
                                    y0=580
                                    for z in range(5):
                                        screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                        y0-=28
                                    
                                    y0=580 
                                    for z in range(5):
                                        screen.blit(ball, (distance * k + u_width * k + 12, y0))
                                        screen.blit(ball, (distance * k + u_width * k + 40, y0))
                                        screen.blit(ball, (distance * k + u_width * k + 68, y0))
                                        y0-=28
                                if cnt[k]<=10:
                                    screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                    y0=35
                                    for z in range(cnt[k]-int(cnt[k]/2)):
                                        screen.blit(ball, (distance * k0 + u_width * k0 + 20, y0))
                                        y0+=28
                                    y0=35
                                    for z in range(int(cnt[k]/2)):
                                        screen.blit(ball, (distance * k0 + u_width * k0 + 60, y0))
                                        y0+=28
                                if k==tuzdyk2:
                                    screen.blit(tuzdyk, (distance * k0 + 10 + u_width * k0, 30))
                        x0 = 860
                        if q1<=62:
                            for k in range(int(q1/2)):
                                screen.blit(ball, (x0, 240))
                                x0-=28
                            x0 = 860
                            for k in range(q1-int(q1/2)):
                                screen.blit(ball, (x0, 268))
                                x0-=28
                        else:
                    
                            for k in range(31):
                                screen.blit(ball, (x0, 240))
                                screen.blit(ball, (x0, 268))
                                x0-=28
                            x0=860
                            for k in range(int((q1-62)/3)):
                                screen.blit(ball, (x0, 230))
                                screen.blit(ball, (x0, 258))
                                screen.blit(ball, (x0, 286))
                                x0-=28
                            y0=230
                            for k in range((q1-62)%3):
                                screen.blit(ball, (x0, y0))
                                y0+=28
                        pygame.display.update()
                if wh == 1:
                    p = random.randint(0, 8)
                    kamni.play() 
                    print(p)          
                    p = 17-p #pos of choice of 2-player in our cnt[] 9
                    tas = cnt[p] #p = 9(0), tas = 2
                    cnt[p]=1
                    if tas == 1:
                        if p == 17:
                            cnt[0]+=1
                            if cnt[0]%2==0:
                                q2+=cnt[0]
                                cnt[0]= 0
                        else: cnt[p+1]+=1
                        cnt[p]=0
                    if tas == 0:
                        error1.play()
                        cnt[p] = 0
                        continue
                    if tas > (18-p):#2>0
                        for k in range(p+1, 18): #17-p
                            cnt[k]+=1
                        m = tas-19+p#24-19+5=10
                        for k in range(m+1):
                            cnt[k]+=1
                        if m<9 and cnt[m]%2==0:
                            q2 += cnt[m]
                            cnt[m] = 0
                        if not tuz2:
                            if m<9 and m!=8 and m!=17 and cnt[m]==3:
                                tuzdyk2 = m
                                tuz2 = True
                    else:
                        m = tas+p-1#9+9-1=17
                        for k in range(p+1, p+tas):#1, 14
                            cnt[k]+=1
                        if m<9:
                            if cnt[m]%2==0:
                                q2+=cnt[m]
                                cnt[m] = 0
                            if not tuz2:
                                if m!=8 and m!=17 and cnt[m]==3:
                                    tuzdyk2 = m
                                    tuz2 = True
                    if tuz2: q2+=cnt[tuzdyk2]; cnt[tuzdyk2] = 0
                    for k in range(len(cnt)):
                        if k<9:
                            if cnt[k]==0:
                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                            if cnt[k]==1:
                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                screen.blit(ball, (distance * k + u_width * k + 20, 580))
                            if cnt[k]>10 and cnt[k]<26:
                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                y0=580
                                for z in range(5):
                                    screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                    y0-=28
                                y0=580
                                for z in range(5):
                                    screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                    y0-=28
                                l=int((cnt[k]-10)/3)
                                y0=580 
                                for z in range(l):
                                    screen.blit(ball, (distance * k + u_width * k + 12, y0))
                                    screen.blit(ball, (distance * k + u_width * k + 40, y0))
                                    screen.blit(ball, (distance * k + u_width * k + 68, y0))
                                    y0-=28
                                l=(cnt[k]-10)%3
                                x0=12
                                for z in range(l):
                                    screen.blit(ball, (distance * k + u_width * k + x0, y0))
                                    x0+=28
                            if cnt[k]>25:
                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                y0=580
                                for z in range(5):
                                    screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                    y0-=28
                                y0=580
                                for z in range(5):
                                    screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                    y0-=28
                                
                                y0=580 
                                for z in range(5):
                                    screen.blit(ball, (distance * k + u_width * k + 12, y0))
                                    screen.blit(ball, (distance * k + u_width * k + 40, y0))
                                    screen.blit(ball, (distance * k + u_width * k + 68, y0))
                                    y0-=28
                            if cnt[k]<=10:
                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                y0=580
                                for z in range(cnt[k]-int(cnt[k]/2)):
                                    screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                    y0-=28
                                y0=580
                                for z in range(int(cnt[k]/2)):
                                    screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                    y0-=28
                            if k==tuzdyk2:
                                screen.blit(tuzdyk, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))

                        if k>8:
                            k0=17-k
                            if cnt[k]==0:
                                screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                            if cnt[k]==1:
                                screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                screen.blit(ball, (distance * k0 + u_width * k0 + 20, 35))
                            if cnt[k]>10 and cnt[k]<26:
                                screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                y0=35
                                for z in range(5):
                                    screen.blit(ball, (distance * k0 + u_width * k0 + 20, y0))
                                    y0+=28
                                y0=35
                                for z in range(5):
                                    screen.blit(ball, (distance * k0 + u_width * k0 + 60, y0))
                                    y0+=28
                                l=int((cnt[k]-10)/3)
                                y0=35
                                for z in range(l):
                                    screen.blit(ball, (distance * k0 + u_width * k0 + 12, y0))
                                    screen.blit(ball, (distance * k0 + u_width * k0 + 40, y0))
                                    screen.blit(ball, (distance * k0 + u_width * k0 + 68, y0))
                                    y0+=28
                                l=(cnt[k]-10)%3
                                x0=12
                                for z in range(l):
                                    screen.blit(ball, (distance * k0 + u_width * k0 + x0, y0))
                                    x0+=28
                            if cnt[k]>25:
                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                y0=580
                                for z in range(5):
                                    screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                    y0-=28
                                y0=580
                                for z in range(5):
                                    screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                    y0-=28
                                
                                y0=580 
                                for z in range(5):
                                    screen.blit(ball, (distance * k + u_width * k + 12, y0))
                                    screen.blit(ball, (distance * k + u_width * k + 40, y0))
                                    screen.blit(ball, (distance * k + u_width * k + 68, y0))
                                    y0-=28
                            if cnt[k]<=10:
                                screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                y0=35
                                for z in range(cnt[k]-int(cnt[k]/2)):
                                    screen.blit(ball, (distance * k0 + u_width * k0 + 20, y0))
                                    y0+=28
                                y0=35
                                for z in range(int(cnt[k]/2)):
                                    screen.blit(ball, (distance * k0 + u_width * k0 + 60, y0))
                                    y0+=28
                            if k==tuzdyk1:
                                screen.blit(tuzdyk, (distance * k0 + 10 + u_width * k0, 30))

                    x0 = 20
                    if q2<=62:
                        for k in range(int(q2/2)):
                            screen.blit(ball, (x0, 345))
                            x0+=28
                        x0 = 20
                        for k in range(q2-int(q2/2)):
                            screen.blit(ball, (x0, 373))
                            x0+=28
                    else:
                    
                        for k in range(31):
                            screen.blit(ball, (x0, 345))
                            screen.blit(ball, (x0, 373))
                            x0+=28
                        x0=20
                        for k in range(int((q2-62)/3)):
                            screen.blit(ball, (x0, 330))
                            screen.blit(ball, (x0, 358))
                            screen.blit(ball, (x0, 386))
                            x0+=28
                        y0=330
                        for k in range((q2-62)%3):
                            screen.blit(ball, (x0, y0))
                            y0+=28
                    wh = 0
                    pygame.display.update()
                    print(cnt, q1, q2)                
    
            z1,z2=0,0
            for k in range(9):
                z1+=cnt[k]
            for k in range(9,18):
                z2+=cnt[k]
            if z1==0 or z2 == 0:
                q1+=z1
                q2+=z2
            if q1>=81 and q1>q2:
                print("YOU WIN!")
                PL1 = False
                
            if q2>=81 and q2>q1:
                print("YOU LOSE!")
                PL1 = False
        if Zoom_refresh:
            screen.blit(refresh, (920, 83))
        if Zoom_sound_on:
            screen.blit(sound_on, (920, 433))
        if Zoom_home:
            screen.blit(home, (920, 550))
        # screen.blit(ou, (555, 222)

        pygame.display.flip()
        clock.tick(fps)

    #return empty(SINGLE_PLAYER)
def multi(): # call the test function with current gamemode argument
    size = (1000, 640)
    fps = 20  # Frames per second
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    block_size = 35
    YELLOW = (237, 132, 17)
    BLACK = (0, 0, 0)

    # Load images
    background = pygame.image.load('background.png')
    ball = pygame.image.load("Ball.png")
    home1 = pygame.image.load('Home.png')
    refresh1 = pygame.image.load('Refresh.png')
    sound_on1 = pygame.image.load('Sound on.png')
    home = pygame.transform.scale(home1, (block_size, block_size))
    refresh = pygame.transform.scale(refresh1, (block_size - 5, block_size - 5))
    sound_on = pygame.transform.scale(sound_on1, (block_size + 15, block_size + 15))

    # Scales
    # ҰяшыҚ
    uyashiq = 9
    u_width = 89
    u_hight = 150
    distance = 10  # Distance between ҰяшыҚ
    # ҚазандыҚ
    qazandik = 2
    q_width = 880
    q_hight = 89

    # For numbers
    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 22)

    # List of Numbers of ҚазандыҚ
    quant = []
    for i in range(1, 10):
        quant.append(myfont.render(f"{i}", False, YELLOW))

    # Transparent ҰяшыҚ
    u = pygame.Surface((u_width, u_hight))
    u.fill(BLACK)
    tuzdyk = pygame.Surface((u_width, u_hight))
    tuzdyk.fill((120,120,120))
    # Transparent ҚазандыҚ
    q = pygame.Surface((q_width, q_hight))
    q.set_alpha(140)
    q.fill(BLACK)

    done = False
    Zoom_refresh = True
    Zoom_home = True
    Zoom_sound_on = True
    # Game loop
    while not done:
        screen.blit(background, (0, 0))
        screen.blit(transparent_screen,(0, 0))
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
                        screen.blit(pygame.transform.scale(sound_on1, (block_size + 21, block_size + 21)), (917, 430))
                        Zoom_sound_on = False

            if i.type == pygame.MOUSEBUTTONUP:
                Zoom_refresh = True
                if not Zoom_home:
                    return menu()
                Zoom_sound_on = True
        # Blitting ҰяшыҚ
        for i in range(uyashiq):
            screen.blit(quant[-1 * (i + 1)], (distance * i + 10 + u_width * i + u_width / 2 - 5, 5))
            screen.blit(u, (distance * i + 10 + u_width * i, 30))
            screen.blit(quant[i], (distance * i + 10 + u_width * i + u_width / 2 - 5, size[1] - 30))
            screen.blit(u, (distance * i + 10 + u_width * i, size[1] - u_hight - 30))
            
            #screen.blit(ball, (distance * i + u_width * i + 60, 580))

            #алгоритм;
            y0 = 35
            for j in range(5):
                screen.blit(ball, (distance * i + u_width * i + 20, y0))
                y0 += 28
            y0 = 35
            for j in range(4):
                screen.blit(ball, (distance * i + u_width * i + 60, y0))
                y0 += 28
            y0 = 580
            for j in range(5):
                screen.blit(ball, (distance * i + u_width * i + 20, y0))
                y0 -= 28
            y0 = 580
            for j in range(4):
                screen.blit(ball, (distance * i + u_width * i + 60, y0))
                y0 -= 28
        pygame.display.update()
        # Blitting ҚазандыҚ
        for i in range(qazandik):
            screen.blit(q, (10, 73 + u_hight + q_hight * i + (distance+5) * i))
        PL1 = True
        cnt = [9,9,1,9,9,9,9,9,9,2,9,9,9,9,9,9,9,9]
        q1 = 0
        q2 = 0
        tuzdyk1 = 19
        tuzdyk2 = 19
        tuz1 = False
        tuz2 = False
        x1 = 860
        x2 = 860
        error1 = pygame.mixer.Sound("error1.mp3")
        kamni = pygame.mixer.Sound("kamni.mp3")
        wh = 1
        while PL1:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()
                if i.type == pygame.MOUSEBUTTONDOWN:
                    if i.button == 1:
                        for p in range(9):
                            if wh==1:
                                if i.pos[0] in range(10 + 99*p, 99 + 99*p) and i.pos[1] in range(30, 120):
                                    error1.play()
                                if i.pos[0] in range(10 + 99*p, 99 + 99*p) and i.pos[1] in range(430, 580):
                                    kamni.play()
                                    wh = 2
                                    v = cnt[p] 
                                    cnt[p] = 1
                                    if v == 1:
                                        cnt[p]=0
                                        cnt[p+1]+=1
                                        if cnt[9]%2==0:
                                            q1+=cnt[9]
                                            cnt[9]=0
                                    if v == 0:
                                        error1.play()
                                        cnt[p] = 0
                                        continue
                                    if v> (18-p):
                                        for k in range(p+1, 18):
                                            cnt[k]+=1
                                            m = v - 18+p
                                        for k in range(m):
                                            cnt[k]+=1
                                        if m>8 and cnt[m]%2==0:
                                            q1 += v
                                        if m>8 and m!=8 and m!=17 and cnt[m]==3:
                                            tuzdyk1 = m
                                            tuz1 = True
                                    else:
                                        m = v+p-1
                                        for k in range(p+1, v+p):
                                            cnt[k]+=1
                                        if cnt[m]%2==0 and (m)>8:
                                            q1+=cnt[m]
                                            cnt[m] = 0
                                        if not tuz1:
                                            if m>8 and m!=8 and m!=17 and cnt[m]==3:
                                                tuzdyk1 = m
                                                tuz1 = True
                                    if tuz1: q1+=cnt[tuzdyk1]; cnt[tuzdyk1] = 0
                                    print(cnt, q1, q2)
                                    for k in range(len(cnt)):
                                        if k<9:
                                            
                                            if cnt[k]==0:
                                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                            if cnt[k]==1:
                                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                                screen.blit(ball, (distance * k + u_width * k + 20, 580))
                                            if cnt[k]>10 and cnt[k]<26:
                                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                                y0=580
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                                    y0-=28
                                                y0=580
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                                    y0-=28
                                                l=int((cnt[k]-10)/3)
                                                y0=580 
                                                for z in range(l):
                                                    screen.blit(ball, (distance * k + u_width * k + 12, y0))
                                                    screen.blit(ball, (distance * k + u_width * k + 40, y0))
                                                    screen.blit(ball, (distance * k + u_width * k + 68, y0))
                                                    y0-=28
                                                l=(cnt[k]-10)%3
                                                x0=12
                                                for z in range(l):
                                                    screen.blit(ball, (distance * k + u_width * k + x0, y0))
                                                    x0+=28
                                            if cnt[k]>25:
                                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                                y0=580
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                                    y0-=28
                                                y0=580
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                                    y0-=28
                                                
                                                y0=580 
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 12, y0))
                                                    screen.blit(ball, (distance * k + u_width * k + 40, y0))
                                                    screen.blit(ball, (distance * k + u_width * k + 68, y0))
                                                    y0-=28
                                            if cnt[k]<=10:
                                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                                y0=580
                                                for z in range(cnt[k]-int(cnt[k]/2)):
                                                    screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                                    y0-=28
                                                y0=580
                                                for z in range(int(cnt[k]/2)):
                                                    screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                                    y0-=28
                                            if k == tuzdyk2:
                                                screen.blit(tuzdyk, (distance * k + 10 + u_width * k , size[1] - u_hight - 30))
                                        if k>8:
                                            k0=17-k
                                            
                                            if cnt[k]==0:
                                                screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                            if cnt[k]==1:
                                                screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                                screen.blit(ball, (distance * k0 + u_width * k0 + 20, 35))
                                            if cnt[k]>10 and cnt[k]<26:
                                                screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                                y0=35
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 20, y0))
                                                    y0+=28
                                                y0=35
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 60, y0))
                                                    y0+=28
                                                l=int((cnt[k]-10)/3)
                                                y0=35
                                                for z in range(l):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 12, y0))
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 40, y0))
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 68, y0))
                                                    y0+=28
                                                l=(cnt[k]-10)%3
                                                x0=12
                                                for z in range(l):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + x0, y0))
                                                    x0+=28
                                            if cnt[k]>25:
                                                screen.blit(u, (distance * k0 + 10 + u_width * k0, size[1] - u_hight - 30))
                                                y0=580
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 20, y0))
                                                    y0-=28
                                                y0=580
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 60, y0))
                                                    y0-=28
                                                
                                                y0=580 
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 12, y0))
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 40, y0))
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 68, y0))
                                                    y0-=28
                                            if cnt[k]<=10:
                                                screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                                y0=35
                                                for z in range(cnt[k]-int(cnt[k]/2)):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 20, y0))
                                                    y0+=28
                                                y0=35
                                                for z in range(int(cnt[k]/2)):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 60, y0))
                                                    y0+=28
                                            if k == tuzdyk1:
                                                screen.blit(tuzdyk, (distance * k0 + 10 + u_width * k0, 30))
                                    x0 = 860
                                    if q1<=62:
                                        for k in range(int(q1/2)):
                                            screen.blit(ball, (x0, 240))
                                            x0-=28
                                        x0 = 860
                                        for k in range(q1-int(q1/2)):
                                            screen.blit(ball, (x0, 268))
                                            x0-=28
                                    else:
                                        x0=860
                                        for k in range(31):
                                            screen.blit(ball, (x0, 240))
                                            screen.blit(ball, (x0, 268))
                                            x0-=28
                                        x0=860
                                        for k in range(int((q1-62)/3)):
                                            screen.blit(ball, (x0, 230))
                                            screen.blit(ball, (x0, 258))
                                            screen.blit(ball, (x0, 286))
                                            x0-=28
                                        y0=230
                                        for k in range((q1-62)%3):
                                            screen.blit(ball, (x0, y0))
                                            y0+=28
                                    pygame.display.update()
                                    print(cnt, q1, q2)

                            if wh==2:
                                if i.pos[0] in range(10 + 99*p, 99 + 99*p) and i.pos[1] in range(430, 580):
                                    error1.play()
                                if i.pos[0] in range(10 + 99*p, 99 + 99*p) and i.pos[1] in range(30, 120):
                                    kamni.play()
                                    wh = 1
                                    p = 17-p #pos of choice of 2-player in our cnt[] 
                                    tas = cnt[p] #p = 9(0), tas = 2
                                    cnt[p]=1
                                    if tas == 1:
                                        if p == 17:
                                            cnt[0]+=1
                                            if cnt[0]%2==0:
                                                q2+=cnt[0]
                                                cnt[0]=0
                                        else: cnt[p+1]+=1
                                        cnt[p]=0
                                    if tas == 0:
                                        error1.play()
                                        cnt[p] = 0
                                        continue
                                    if tas > (18-p):#2>0
                                        for k in range(p+1, 18): #17-p
                                            cnt[k]+=1
                                        m = tas-19+p#10-17+13=
                                        for k in range(m+1):
                                            cnt[k]+=1
                                        if m<9 and cnt[m]%2==0:
                                            q2 += cnt[m]
                                            cnt[m] = 0
                                        if not tuz2:
                                            if m<9 and m!=8 and m!=17 and cnt[m]==3:
                                                tuzdyk2 = m
                                                tuz2 = True
                                    else:
                                        m = tas+p-1#9+9-1=17
                                        for k in range(p+1, p+tas):#1, 14
                                            cnt[k]+=1
                                        if m<9:
                                            if cnt[m]%2==0:
                                                q2+=cnt[m]
                                                cnt[m] = 0
                                            if not tuz2:
                                                if m!=8 and m!=17 and cnt[m]==3:
                                                    tuzdyk2 = m
                                                    tuz2 = True
                                    if tuz2: q2+=cnt[tuzdyk2]; cnt[tuzdyk2] = 0                     
                                    for k in range(len(cnt)):
                                        if k<9:
                                            
                                            if cnt[k]==0:
                                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                            if cnt[k]==1:
                                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                                screen.blit(ball, (distance * k + u_width * k + 20, 580))
                                            if cnt[k]>10 and cnt[k]<26:
                                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                                y0=580
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                                    y0-=28
                                                y0=580
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                                    y0-=28
                                                l=int((cnt[k]-10)/3)
                                                y0=580 
                                                for z in range(l):
                                                    screen.blit(ball, (distance * k + u_width * k + 12, y0))
                                                    screen.blit(ball, (distance * k + u_width * k + 40, y0))
                                                    screen.blit(ball, (distance * k + u_width * k + 68, y0))
                                                    y0-=28
                                                l=(cnt[k]-10)%3
                                                x0=12
                                                for z in range(l):
                                                    screen.blit(ball, (distance * k + u_width * k + x0, y0))
                                                    x0+=28
                                            if cnt[k]>25:
                                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                                y0=580
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                                    y0-=28
                                                y0=580
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                                    y0-=28
                                                
                                                y0=580 
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 12, y0))
                                                    screen.blit(ball, (distance * k + u_width * k + 40, y0))
                                                    screen.blit(ball, (distance * k + u_width * k + 68, y0))
                                                    y0-=28
                                            if cnt[k]<=10:
                                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                                y0=580
                                                for z in range(cnt[k]-int(cnt[k]/2)):
                                                    screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                                    y0-=28
                                                y0=580
                                                for z in range(int(cnt[k]/2)):
                                                    screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                                    y0-=28
                                            if k == tuzdyk2:
                                                screen.blit(tuzdyk, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                        if k>8:
                                            k0=17-k
                                           
                                            if cnt[k]==0 and k!=tuzdyk2:
                                                screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                            if cnt[k]==1:
                                                screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                                screen.blit(ball, (distance * k0 + u_width * k0 + 20, 35))
                                            if cnt[k]>10 and cnt[k]<26:
                                                screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                                y0=35
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 20, y0))
                                                    y0+=28
                                                y0=35
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 60, y0))
                                                    y0+=28
                                                l=int((cnt[k]-10)/3)
                                                y0=35
                                                for z in range(l):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 12, y0))
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 40, y0))
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 68, y0))
                                                    y0+=28
                                                l=(cnt[k]-10)%3
                                                x0=12
                                                for z in range(l):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + x0, y0))
                                                    x0+=28
                                            if cnt[k]>25:
                                                screen.blit(u, (distance * k + 10 + u_width * k, size[1] - u_hight - 30))
                                                y0=580
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 20, y0))
                                                    y0-=28
                                                y0=580
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 60, y0))
                                                    y0-=28
                                                
                                                y0=580 
                                                for z in range(5):
                                                    screen.blit(ball, (distance * k + u_width * k + 12, y0))
                                                    screen.blit(ball, (distance * k + u_width * k + 40, y0))
                                                    screen.blit(ball, (distance * k + u_width * k + 68, y0))
                                                    y0-=28
                                            if cnt[k]<=10:
                                                screen.blit(u, (distance * k0 + 10 + u_width * k0, 30))
                                                y0=35
                                                for z in range(cnt[k]-int(cnt[k]/2)):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 20, y0))
                                                    y0+=28
                                                y0=35
                                                for z in range(int(cnt[k]/2)):
                                                    screen.blit(ball, (distance * k0 + u_width * k0 + 60, y0))
                                                    y0+=28
                                            if k == tuzdyk1:
                                                screen.blit(tuzdyk, (distance * k0 + 10 + u_width * k0,30))
                                    x0 = 20
                                    if q2<=62:
                                        for k in range(int(q2/2)):
                                            screen.blit(ball, (x0, 345))
                                            x0+=28
                                        x0 = 20
                                        for k in range(q2-int(q2/2)):
                                            screen.blit(ball, (x0, 373))
                                            x0+=28
                                    else:
                                        x0=20
                                        for k in range(31):
                                            screen.blit(ball, (x0, 345))
                                            screen.blit(ball, (x0, 373))
                                            x0+=28
                                        x0=20
                                        for k in range(int((q2-62)/3)):
                                            screen.blit(ball, (x0, 330))
                                            screen.blit(ball, (x0, 358))
                                            screen.blit(ball, (x0, 386))
                                            x0+=28
                                        y0=330
                                        for k in range((q2-62)%3):
                                            screen.blit(ball, (x0, y0))
                                            y0+=28
                                    pygame.display.update()
                                    print(cnt, q1, q2)    
                                    wh = 1

            
            z1,z2=0,0
            for i in range(9):
                z1+=cnt[i]
            for i in range(9,18):
                z2+=cnt[i]
            if z1==0 or z2 ==0:
                q1+=z1
                q2+=z2
            
            if q1>=81 and q1>q2:
                print("First player WIN" )
                PL1 = False
                done=True
            if q2>=81 and q2>q1:
                print("2-player LOSE!")
                PL1 = False
                done=True
        if Zoom_refresh:
            screen.blit(refresh, (920, 83))
        if Zoom_sound_on:
            screen.blit(sound_on, (920, 433))
        if Zoom_home:
            screen.blit(home, (920, 550))
        # screen.blit(ou, (555, 222)
        pygame.display.flip()
        clock.tick(fps)
def training(): # call the test function with current gamemode argument
    return empty(TRAINING)

song = Thread(target=play_song) # create song thread
song.daemon = True
song.start() # start song thread
gamemode = ''
while menu(): # call menu
     pass
