#인덱스, 타이머 추가
import pygame
import sys
import math
import random
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED =  (255, 0, 0)
YELLOW = (255, 224, 0)
GREEN = (0, 255, 0)

idx = 0
tmr = 0
se_crash = None #차량 충돌시 사용할 효과음 로딩 변수

DATA_LR = [0,0,0,0,0,0,0,0,0,0,
           0,0,1,2,3,2,1,0,2,4,
           2,4,2,0,0,0,-2,-2,-4,-4,
           -2,-1,0,0,0,0,0,0,0] #도로 커브  생성 기본  데이터
DATA_UD = [0,0,1,2,3,2,1,0,-2,-4,
           -2,0,0,0,0,0,-1,-2,-3,-4,
           -3,-2,-1,0,0,0,0,0,0,0,
           0,0,0,-3,3,0,-6,6,0] #도로 기복 생성  기본 데이터
CLEN = len(DATA_LR) 

BOARD = 120 #도로를 그릴 판 수
CMAX = BOARD * CLEN # 코스 길이 지정 상수
curve = [0] * CMAX #도로 커브 방향 관리 리스트
updown = [0] * CMAX #도로 기복을 넣을 리스트
object_left = [0] * CMAX #도로 왼쪽에 물체 넣을 리스트
object_right = [0] * CMAX  #도로 오른쪽에 물체 넣을 리스트

CAR = 30  #차량 수
car_x = [0] * CAR  #차량 가로 방향
car_y = [0] * CAR #차량 위치
car_lr = [0] * CAR #차량 좌우 방향
car_spd = [0] * CAR #차량 속도
PLCAR_Y = 10 #플레이어 차량 표시 위치, 가짱 가까운 도로(화면 아래)가 0

def make_course(): #코스 데이터 생성 함수``
    for i in range(CLEN):
        lr1 = DATA_LR[i] #커브 데이터 대입
        lr2 = DATA_LR[(i + 1) % CLEN] #다음 커브 데이터 대입
        ud1 = DATA_UD[i] #기복 데이터
        ud2 = DATA_UD[(i + 1) % CLEN] #다음 기복 데이터
        for j in range(BOARD):
            pos = j + BOARD * i 
            curve[pos] = lr1 * (BOARD - j) / BOARD + lr2 * j / BOARD #도로 커브 계산
            updown[pos] = ud1 * (BOARD - j) / BOARD + ud2 * j / BOARD #도로 기복 계산
            if j == 60:
                object_right[pos] = 1 #간판
            if i % 8 < 7:
                if j % 12 == 0:
                    object_left[pos] = 2  #야자나무
            else:
                if j % 20 == 0:
                    object_left[pos] = 3 #요트
            if j % 12 == 6:
                object_left[pos] = 9 #바다

def draw_obj(bg, img, x, y,  sc):
    img_rz = pygame.transform.rotozoom(img, 0, sc)  #확대 축소한 이미지  생성
    w = img_rz.get_width() #이미지 폭
    h = img_rz.get_height() #이미지 높이
    bg.blit(img_rz,  [x- w / 2, y - h])  #이미지 그리기

def draw_shadow(bg, x, y, siz): #그림자 표시함수
    shadow = pygame.Surface([siz, siz/4])  #그릴 화면 준비
    shadow.fill(RED) #해당 화면을 빨강색으로 채움
    shadow.set_colorkey(RED) #투과색 지정
    shadow.set_alpha(128)   #투명도 설정
    pygame.draw.ellipse(shadow, BLACK,[0, 0, siz, siz / 4])  #검은색 타원 그림
    bg.blit(shadow,  [x - siz / 2, y - siz / 4])  #타원을 게임 화면에 전송

def init_car(): #차량 관리 리스트 초기화 함수
    for i in range(1, CAR):
        car_x[i] = random.randint(50, 750) #가로 방향 좌표 무작위 결정
        car_y[i] = random.randint(200, CMAX - 200) #코스 상 위치 무작위 결정
        car_lr[i] = 0 #좌우 움직임 0 대입 (정면 향함)
        car_spd[i] = random.randint(100, 200) #속도 무작위 결정
    car_x[0] = 400 #플레이어 차량 가로 방향 화면 중앙
    car_y[0] = 0  #플레이어 자량 코스 상 위치 초기화
    car_lr[0] = 0
    car_spd[0] = 0

def drive_car(key):  # 플레이어 차량 조작 및 제어
    global idx, tmr
    if key[K_LEFT] == 1:  #왼쪽 방향키를 누르면
        if car_lr[0] > -3: 
            car_lr[0] -= 1   #방향 - 1(왼쪽으로 회전)
        car_x[0] = car_x[0]  + (car_lr[0]  - 3) * car_spd[0] / 100 - 5  #차량 가로 방향 좌표 계산
    elif  key[K_RIGHT]  == 1: #오른쪽 방향키를 누르면
        if car_lr[0] < 3:
            car_lr[0] += 1   #방향 + 1(오른쪽으로 회전)
        car_x[0] = car_x[0]  + (car_lr[0]  + 3) * car_spd[0] / 100 + 5 #차량 가로 방향 좌표 계산
    else:
        car_lr[0] = int (car_lr[0] * 0.9) #정면 방향으로 가까이 이동
    
    if key[K_a] == 1:  #악셀레이터
        car_spd[0] += 3
    elif key[K_z] == 1: #브레이크
        car_spd[0] -= 10
    else:  
        car_spd[0] -=  0.25

    if car_spd[0] < 0:  #속도가 0 미만이면
        car_spd[0] = 0  #0
    if car_spd[0] > 320:  #속도가 320 이상이면 
        car_spd[0] = 320  #320  
    
    car_x[0] -= car_spd[0] * curve[int(car_y[0] + PLCAR_Y) % CMAX] / 50 #차량 속도와 도로 커브에서 가로 방향 좌표 계산
    if car_x[0] < 0: #왼쪽 도로 끝에 닿으면
        car_x[0] = 0
        car_spd[0] *= 0.9  #감속
    if car_x[0] > 800:  #오른쪽 도로 끝에  닿으면
        car_x[0] = 800
        car_spd[0] *= 0.9  #감속

    car_y[0] = car_y[0] + car_spd[0] / 100 #차량 속도에서 코스 상 위치  계산
    if car_y[0] > CMAX - 1: #코스 종점을 넘으면
        car_y[0] -= CMAX #코스 시작으로  되돌림
        idx = 3 #idx에 3 대입
        tmr = 0 #tmr에 0 대입

def move_car(cs): #COM 차량 제어
    for i in range(cs, CAR):
        if car_spd[i] < 100: #속도가 100보다 느리면 
            car_spd[i] += 3 #속도 증가
        if i == tmr % 120: #일정 시간별로
            car_lr[i] += random.choice([-1, 0, 1]) #방향 무작위
            if car_lr[i] < -3: car_lr[i] = -3
            if car_lr[i] > 3: car_lr[i] = 3
        car_x[i] = car_x[i] + car_lr[i] * car_spd[i] / 100 #차량 방향, 속도에서 가로 좌표 계산

        if car_x[i] < 50: #왼쪽 길 끝에 가까우면
            car_x[i] = 50 #그 이상 못가도록
            car_lr[i] = int(car_lr[i] * 0.9) #정면쪽으로 이동
        if car_x[i] > 750: #오른쪽 길 끝에 가까우면
            car_x[i] = 750 #그 이상 못가도록
            car_lr[i] = int(car_lr[i] * 0.9) #정면쪽으로 이동
        car_y[i] += car_spd[i] / 100 #차량 속도에서 코스 상 위치 계산
        if car_y[i] > CMAX - 1: #코스 종점을 넘었다면
            car_y[i] -= CMAX #코스 시작으로 이동
        if idx == 2: #레이스 중 히트 체크
            cx = car_x[i] - car_x[0] #플레이어 차량과 가로 방향 거리
            cy = car_y[i] - (car_y[0] + PLCAR_Y) % CMAX #플레이어 차량과 코스상의 거리
            if -100 <= cx and cx <= 100 and -10 <= cy and cy <= 10: #이들 범위 내라면
                car_x[0] -= cx / 4 #플레이어 차량 가로로 이동
                car_x[i] += cx / 4 #COM 차량 가로로 이동
                car_spd[0], car_spd[i] = car_spd[i] * 0.3, car_spd[0] * 0.3 #2개 차량 속도를 서로 바꿔 감속
                se_crash.play() #충돌음 출력

def draw_text(scrn, txt, x, y, col, fnt): #그림자 포함 문자열 표시 함수
    sur = fnt.render(txt, True, BLACK)
    x -= sur.get_width() / 2 #센터링 계산
    y -= sur.get_height() / 2 #센터링 계산
    scrn.blit(sur, [x + 2, y + 2])
    sur = fnt.render(txt, True, col)
    scrn.blit(sur, [x, y])


def main(): 
    global idx, tmr, se_crash
    pygame.init()
    pygame.display.set_caption("Python Racer")
    screen =  pygame.display.set_mode((800, 600)) #화면 초기화
    clock = pygame.time.Clock()  
    fnt_s = pygame.font.Font(None, 40) #작은 크기 문자
    fnt_m = pygame.font.Font(None, 50) #중간 크기 문자
    fnt_l = pygame.font.Font(None, 120) #큰 크기 문자
  
    img_title = pygame.image.load("image_pr/title.png").convert() #타이틀 로고 이미지
    img_bg = pygame.image.load("image_pr/bg.png").convert() #배경 이미지 로딩 
    img_sea = pygame.image.load("image_pr/sea.png").convert_alpha() #배경(하늘과 땅) 이미지 
    img_obj = [
        None,
        pygame.image.load("image_pr/board.png").convert_alpha(),
        pygame.image.load("image_pr/yashi.png").convert_alpha(),
        pygame.image.load("image_pr/yacht.png").convert_alpha()
    ]
    img_car = [
        pygame.image.load("image_pr/car00.png").convert_alpha(),
        pygame.image.load("image_pr/car01.png").convert_alpha(),
        pygame.image.load("image_pr/car02.png").convert_alpha(),
        pygame.image.load("image_pr/car03.png").convert_alpha(),
        pygame.image.load("image_pr/car04.png").convert_alpha(),
        pygame.image.load("image_pr/car05.png").convert_alpha(),
        pygame.image.load("image_pr/car06.png").convert_alpha(),
        pygame.image.load("image_pr/car10.png").convert_alpha(),
        pygame.image.load("image_pr/car11.png").convert_alpha(),
        pygame.image.load("image_pr/car12.png").convert_alpha(),
        pygame.image.load("image_pr/car13.png").convert_alpha(),
        pygame.image.load("image_pr/car14.png").convert_alpha(),
        pygame.image.load("image_pr/car15.png").convert_alpha(),
        pygame.image.load("image_pr/car16.png").convert_alpha(),
        pygame.image.load("image_pr/car20.png").convert_alpha(),
        pygame.image.load("image_pr/car21.png").convert_alpha(),
        pygame.image.load("image_pr/car22.png").convert_alpha(),
        pygame.image.load("image_pr/car23.png").convert_alpha(),
        pygame.image.load("image_pr/car24.png").convert_alpha(),
        pygame.image.load("image_pr/car25.png").convert_alpha(),
        pygame.image.load("image_pr/car26.png").convert_alpha()
    ]

    se_crash = pygame.mixer.Sound("sound_pr/crash.ogg") #충돌음 로딩

    #도로 판 기본 형태 계산
    BOARD_W = [0] * BOARD #판의 폭
    BOARD_H = [0] * BOARD #판의 높이
    BOARD_UD = [0] * BOARD #판의 기복 
    for i in range(BOARD):
        BOARD_W[i] = 10 +  (BOARD - i) * (BOARD - i) / 12
        BOARD_H[i] = 3.4 * (BOARD - i) / BOARD
        BOARD_UD[i] =2 * math.sin(math.radians(i * 1.5))
    
    make_course() #코스 데이터 생성
    init_car() #차량 관리 리스트 초기화

    vertical = 0 #배경 가로 방향 위치

    while True:
        for event in pygame.event.get():
            if event.type == QUIT: #윈도우 x 버튼 클릭시
                pygame.quit() #pygame 모듈 초기화 삭제
                sys.exit()  #프로그램 종료
            if event.type == KEYDOWN:
                if event.key == K_F1: #F1 키
                    screen = pygame.display.set_mode((800, 600), FULLSCREEN) # 풀 스크린
                if event.key == K_F2 or event.key == K_ESCAPE: #F2, esc 키
                    screen = pygame.display.set_mode((800, 600)) #일반 화면 크기
        tmr += 1
        
        #화면에 그릴 도로 x 좌표와 높낮이 계산
        di = 0 #도로 커브 방향 계산 변수
        ud = 0 #판의 높낮이 계산 변수
        board_x = [0] * BOARD #판의 x좌표 계산 리스트
        board_ud = [0] * BOARD #판의 높낮이 계산 리스트 
        for i in range(BOARD):
            di += curve[int(car_y[0] + i) % CMAX] #커브 데이터로 도로 굽기 계산
            ud  += updown[int(car_y[0] + i) % CMAX] #기복 데이터에서 도로 기복 계산
            board_x[i] = 400 - BOARD_W[i] * car_x[0] / 800 + di / 2 #판의 x 좌표를 계산
            board_ud[i] =  ud / 30  #판의 높낮이 계산
        
        horizon = 400 + int(ud /  3) #지평선 좌표 계산
        sy = horizon #도로를 그리기 시작할 위치

        vertical =  vertical - int(car_spd[0] * di / 8000) #배경 수직 위치
        if vertical < 0:
            vertical += 800
        if vertical >= 800:
            vertical -=  800

        #필드 그리기
        screen.fill((0,56, 255)) #하늘 색상
        screen.blit(img_bg, [vertical - 800, horizon - 400])  #하늘과 땅 이미지(왼쪽)
        screen.blit(img_bg, [vertical, horizon  - 400])  #하늘과 땅 이미지(오른쪽)
        screen.blit(img_sea, [board_x[BOARD - 1] -780, sy]) #가장 먼 바다 그림(왼쪽)

        #그리기 데이터를 기초로 도로 그리기
        for i in range(BOARD - 1, 0, -1):
            ux = board_x[i] #사다리꼴 윗변 x좌표
            uy =  sy - BOARD_UD[i] * board_ud[i] #윗변 Y 좌표
            uw =  BOARD_W[i] #윗변 폭 대입
            sy = sy + BOARD_H[i] * (600 - horizon) / 200  #사다리꼴을 그릴 y 좌표 대입
            bx = board_x[i - 1] #아랫변 x좌표 
            by = sy - BOARD_UD[i - 1] * board_ud[i - 1] #아랫변 y좌표
            bw = BOARD_W[i - 1]  #아랫변 폭 대입
            col = (160, 160, 160) #판 색상 대입
            if int(car_y[0] + i) % CMAX == PLCAR_Y + 10: #골 위치라면
                col = (192, 0, 0) #빨간색 선 값 대입
            pygame.draw.polygon(screen, col, [[ux, uy], [ux + uw, uy], [bx + bw, by], [bx, by]])

            if int(car_y[0]  + i) % 10  <= 4: #좌우 노란색  선
                pygame.draw.polygon(screen, YELLOW, [[ux, uy],  [ux + uw * 0.02, uy], [bx + bw * 0.02, by], [bx, by]]) #도로 왼쪽
                pygame.draw.polygon(screen, YELLOW, [[ux + uw  * 0.98, uy],  [ux + uw, uy], [bx  + bw,  by], [bx + bw * 0.98, by]]) #도로 오른쪽
            if int(car_y[0] + i) % 20 <= 10: #흰색선
                pygame.draw.polygon(screen, WHITE, [[ux + uw * 0.24, uy],  [ux + uw * 0.26, uy], [bx + bw * 0.26,  by], [bx + bw * 0.24, by]]) #왼쪽
                pygame.draw.polygon(screen, WHITE, [[ux + uw * 0.49, uy],  [ux + uw * 0.51, uy], [bx + bw * 0.51,  by], [bx + bw * 0.49, by]]) #중앙
                pygame.draw.polygon(screen, WHITE, [[ux + uw * 0.74, uy],  [ux + uw * 0.76, uy], [bx + bw * 0.76,  by], [bx + bw * 0.74, by]]) #오른쪽
            
            scale = 1.5 * BOARD_W[i] / BOARD_W[0]
            obj_l = object_left[int(car_y[0] + i) %  CMAX] #도로 왼쪽  물체
            if obj_l == 2: #야자나무
                draw_obj(screen, img_obj[obj_l], ux - uw * 0.05, uy, scale)
            if obj_l == 3: #요트
                draw_obj(screen, img_obj[obj_l], ux - uw * 0.5, uy, scale)
            if obj_l == 9: #바다
                screen.blit(img_sea, [ux - uw * 0.5 - 780, uy])
            
            obj_r = object_right[int(car_y[0] + i) %  CMAX] #도로 오른쪽  물체
            if obj_r == 1: #간판
                draw_obj(screen, img_obj[obj_r], ux + uw * 1.3, uy, scale)
            
            for c in range(1, CAR): #COM 차량
                if int(car_y[c]) % CMAX == int(car_y[0] + i) % CMAX:
                    lr = int(4 * (car_x[0] - car_x[c]) / 800) #플레이어가 보는 COM 차량 방향
                    if lr < -3: lr = -3
                    if lr > 3: lr = 3
                    draw_obj(screen, img_car[(c % 3) * 7 + 3 + lr], ux + car_x[c] * BOARD_W[i] / 800, uy, 0.05 + BOARD_W[i] / BOARD_W[0]) 
            
            if i == PLCAR_Y: #플레이어 차량
                draw_shadow(screen, ux + car_x[0] * BOARD_W[i] / 800, uy, 200 * BOARD_W[i] / BOARD_W[0])
                draw_obj(screen, img_car[3 + car_lr[0]], ux + car_x[0] * BOARD_W[i] / 800, uy, 0.05 + BOARD_W[i] / BOARD_W[0])
        
        draw_text(screen, str(int(car_spd[0])) + "km/h", 680, 30, RED, fnt_m)

        key = pygame.key.get_pressed() #key에 모든 키 상태 대입

        if idx == 0:
            screen.blit(img_title, [120, 120])
            draw_text(screen, "[A] Start game", 400, 320, WHITE, fnt_m)
            move_car(0)
            if key[K_a] != 0:
                init_car()
                idx = 1
                tmr = 0
        if idx == 1:
            n = 3 - int(tmr/60)
            draw_text(screen, str(n), 400, 240, YELLOW, fnt_l)
            if tmr == 179:
                pygame.mixer.music.load("sound_pr/bgm.ogg")
                pygame.mixer.music.play(-1)
                idx = 2
                tmr = 0
        
        if idx == 2:
            if tmr < 60:
                draw_text(screen, "Go!", 400, 240, RED, fnt_l)
            drive_car(key) #플레이어 차량 조작
            move_car(1) #COM 차량 이동
        
        if idx == 3: #골인
            if tmr == 1:
                pygame.mixer.music.stop() #BGM 중지
            if tmr == 30: 
                pygame.mixer.music.load("sound_pr/goal.ogg") #골
                pygame.mixer.music.play(0)
            draw_text(screen, "GOAL!", 400, 240, GREEN, fnt_l) #GOAL! 표시
            car_spd[0] = car_spd[0] * 0.96 #플레이어 차량 속도 감속
            car_y[0] = car_y[0] + car_spd[0] / 100 #코스 위를 이동
            move_car(1) #COM 차량 이동
            if tmr > 60 * 8: #8초 후
                idx = 0 # 첫 화면으로

        pygame.display.update()
        clock.tick(60) #60 프레임
       
if __name__ == '__main__': #이 프로그램 직접  실행시
    main() #main() 함수 호출
