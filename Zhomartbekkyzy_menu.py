import pygame
import os
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

class Button:
    
    font = pygame.font.SysFont('Courier', 36, bold=True) # font for buttons

    def __init__(self, text, button_x, button_y, txt_col):
        self.button_x = button_x
        self.button_y = button_y
        self.text = text
        self.color = txt_col
        self.active_color = [i // 2 for i in txt_col] # color used if mouse points on button
        self.is_active = False
        self.init_txt()
        w, h = self.txt.get_size()
        self.button_w = w + 8
        self.button_h = h + 8
        self.txt_x = button_x + self.button_w // 2 - w // 2
        self.txt_y = button_y + self.button_h // 2 - h // 2

    def init_txt(self): # create text surface
        self.txt = Button.font.render(str(self.text), True, self.color if not self.is_active else self.active_color)

    def is_pressed(self, pos, event):
        dist_x = pos[0] - self.button_x
        dist_y = pos[1] - self.button_y
        if 0 <= dist_x <= self.button_w and 0 <= dist_y <= self.button_h:
            self.is_active = True # change state to active if mouse points on button
            if event.type == pygame.MOUSEBUTTONDOWN: return True # if mouse is clicked - return true
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
    '''Returns string of choosen gamemode (QUIT, SINGLEPLAYER, MULTIPLAYER, TRAINING, SETTINGS)'''
    global screen, clock
    BROWN_COLOR = (139, 69, 19)
    font = pygame.font.SysFont('Courier', 60, bold=True)
    header = font.render('THE TOGYZ QUMALAQ', True, BROWN_COLOR)

    big_font = pygame.font.SysFont('Courier', 300, bold=True)
    logo_text = big_font.render('9', True, BROWN_COLOR)

    size = max(logo_text.get_size())
    logo_background = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(logo_background, BROWN_COLOR + (50,), (size // 2, size // 2), size // 2)
    
    buttons = []
    texts = ['SINGLE PLAYER', 'MULTIPLAYER', 'TRAINING', 'SETTINGS'] # text for buttons
    x_coordinate = int(screen.get_size()[0] * 0.55) # x coordinate for all buttons
    y_coordinates = (200, 300, 400, 500) # y coordinate for buttons
    BUTTON_COLOR = (205, 133, 63)
    for data in zip(texts, y_coordinates): # correspond each text with y coordinate
        buttons.append(Button(data[0], x_coordinate, data[1], BUTTON_COLOR))

    menuloop = True
    while menuloop:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menuloop = False
            pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.is_pressed(pos, event): # if button is pressed
                    return button.text # return its content

        screen.blit(background, (0, 0)) # draw background image
        screen.blit(header, (screen.get_size()[0] // 2 - header.get_size()[0] // 2, 80))
        screen.blit(logo_background, (100 + logo_text.get_size()[0] // 2 - logo_background.get_size()[0] // 2,
                    header.get_size()[1] + 150))
        screen.blit(logo_text, (100, header.get_size()[1] + 150))
        # draw header, logo etc.
        for button in buttons: # draw all buttons
            button.draw()

        pygame.display.flip() # update display
    
    return 'QUIT' # return QUIT if we came to here


def empty(msg): # test function for gamemodes
    button = Button('RETURN TO MENU', 600, 500, (50, 50, 50))
    font = pygame.font.SysFont('Courier', 60, bold=True)
    text = font.render(msg, True, (0, 0, 0)) # render gamemode
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            pos = pygame.mouse.get_pos()
            if button.is_pressed(pos, event): # if button is pressed - return true and show the menu again
                return True

        screen.fill((255, 255, 255)) # fill with white color
        screen.blit(text, (screen.get_size()[0] // 2 - text.get_size()[0] // 2, 80)) # draw the gammode
        button.draw() # draw the button

        pygame.display.flip() # update the screen


def single(): # call the test function with current gamemode argument
    return empty('single')
def multi(): # call the test function with current gamemode argument
    return empty('multi')
def training(): # call the test function with current gamemode argument
    return empty('training')
def settings(): # call the test function with current gamemode argument
    return empty('settings')

gamemode = ''
modes = {'SINGLE PLAYER': single, 'MULTIPLAYER': multi,
         'TRAINING': training, 'SETTINGS': settings}
while True:
    gamemode = menu() # call menu
    if gamemode == 'QUIT' or not modes[gamemode](): break # if menu func returned QUIT or gamemode returned False - break the loop
