import pygame
import sys
from pygame.locals import *
from database import Database
from load import load_image #load_sound, load_music
from menu import *
from mode_single import *
from mode_time import  *
from mode_pvp import *

if not pygame.mixer:
    print('Warning, sound disablead')
if not pygame.font:
    print('Warning, fonts disabled')

BACK = 0

# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# WHITE = (255, 255, 255)

direction = {None: (0, 0), pygame.K_UP: (0, -2), pygame.K_DOWN: (0, 2),
             pygame.K_LEFT: (-2, 0), pygame.K_RIGHT: (2, 0)}

# Initialize everything
pygame.mixer.pre_init(11025, -16, 2, 512)
pygame.init()
screen_size = 500 # 스크린 가로, 스크린 세로
screen = pygame.display.set_mode((screen_size, screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption("Let's Kirin!")
pygame.mouse.set_visible(0)

# 데베 함수 메뉴 구현
hiScores=Database().getScores()
soundFX = Database.getSound()
music = Database.getSound(music=True)
if music and pygame.mixer:
    pygame.mixer.music.play(loops=-1)

# selection = 1
showSelectModes=False
showHiScores = False

#--------------------------------------------------------------------#

#########################
#    Init Menu Loop     #
#########################

# inInitMenu loop = Init_page & login_page & signup_page
# Init_page = 1. log in 2. sign up 3. Quit 
# login_page = enter ID, enter PWD, BACK
# signup_page = enter ID, enter PWD, BACK
inInitMenu=True
while inInitMenu:
    userSelection, screen_size=Menu(screen_size).init_page()
    flag=True
    while flag:   
        if userSelection==1 or userSelection==2: #로그인/회원가입
            pageResult, screen_size=Menu(screen_size).login_sign_page(userSelection)
            if pageResult==BACK: #back
                flag=False  
            else: 
                # print(pageResult)
                flag=False
                inInitMenu=False          
        elif userSelection==3: #끝내기
            pygame.quit()
            sys.exit()


# After login - infinite loop
windowShow = True
while windowShow:

#########################
#    Start Menu Loop    #
#########################

    inMainMenu=True
    while inMainMenu:
        userSelection, screen_size=Menu(screen_size).inMenu_page()
        flag=True
        while flag:
            if userSelection == 1:
                pageResult, screen_size=Menu(screen_size).select_game_page()
                if pageResult == BACK: #back
                    flag = False
                elif (pageResult == 'SingleMode' or 
                    pageResult == 'TimeMode' or
                    pageResult == 'PvpMode'):
                    flag = False
                    inMainMenu = False 
            elif userSelection == 2:
                pageResult, screen_size = Menu(screen_size).score_page()
                if pageResult == BACK:
                    flag = False
            elif userSelection == 6:
                pygame.quit()
                sys.exit()


#########################
#    Start Game Loop    #
#########################

    if pageResult == 'SingleMode':
        print('Play Single mode')
        Single.playGame(screen_size)    # 메뉴에서 설정한 윈도우 창크기 받아오기
    elif pageResult == 'TimeMode':
        print('Play Time mode')
        Time.playGame(screen_size)
    elif pageResult == 'PvpMode':
        print('Play Pvp mode')
        Pvp.playGame(screen_size)
    #screen_size = Pvp.playGame(screen_size) 형태로 screen_size를 받아오는게 안됨    
    
    print("Game End")   