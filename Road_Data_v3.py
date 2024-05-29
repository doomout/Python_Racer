#물체 데이터 추가
import pygame
import sys
import math
from pygame.locals import *

WHITE = (255, 255, 255)
YELLOW = (255, 224, 0)

DATA_LR = [0,0,0,0,0,0,0,0] #도로 커브  생성 기본  데이터
DATA_UD = [0,-2,-4,-6,-4,-2,2,4,2] #도로 기복 생성  기본 데이터
CLEN = len(DATA_LR) 

BOARD = 120 #도로를 그릴 판 수
CMAX = BOARD * CLEN # 코스 길이 지정 상수
curve = [0] * CMAX #도로 커브 방향 관리 리스트
updown = [0] * CMAX #도로 기복을 넣을 리스트
object_left = [0] * CMAX #도로 왼쪽에 물체 넣을 리스트
object_right = [0] * CMAX  #도로 오른쪽에 물체 넣을 리스트

def make_course(): #코스 데이터 생성 함수
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
            if j % 12 == 0:
                object_left[pos] = 2  #야자나무
            if j % 20 == 0:
                object_left[pos] = 3 #요트
            if  j % 12 == 6:
                object_left[pos] = 9 #바다

def draw_obj(bg, img, x, y,  sc):
    img_rz = pygame.transform.rotozoom(img, 0, sc)  #확대 축소한 이미지  생성
    w = img_rz.get_width() #이미지 폭
    h = img_rz.get_height() #이미지 높이
    bg.blit(img_rz,  [x- w / 2, y - h])  #이미지 그리기

def main(): 
    pygame.init()
    pygame.display.set_caption("Python Racer")
    screen =  pygame.display.set_mode((800, 600)) #화면 초기화
    clock = pygame.time.Clock()  
  
    img_bg = pygame.image.load("image_pr/bg.png").convert() #배경 이미지 로딩
    img_sea = pygame.image.load("image_pr/sea.png").convert_alpha()
    img_obj = [
        None,
        pygame.image.load("image_pr/board.png").convert_alpha(),
        pygame.image.load("image_pr/yashi.png").convert_alpha(),
        pygame.image.load("image_pr/yacht.png").convert_alpha()
    ]

    #도로 판 기본 형태 계산
    BOARD_W = [0] * BOARD #판의 폭
    BOARD_H = [0] * BOARD #판의 높이
    BOARD_UD = [0] * BOARD #판의 기복 
    for i in range(BOARD):
        BOARD_W[i] = 10 +  (BOARD - i) * (BOARD - i) / 12
        BOARD_H[i] = 3.4 * (BOARD - i) / BOARD
        BOARD_UD[i] =2 * math.sin(math.radians(i * 1.5))
    
    make_course() #코스 데이터 생성

    car_y = 0 #코스 상 위치
    vertical = 0 #배경 가로 방향 위치

    while True:
        for event in pygame.event.get():
            if event.type == QUIT: #윈도우 x 버튼 클릭시
                pygame.quit() #pygame 모듈 초기화 삭제
                sys.exit()  #프로그램 종료
        
        key = pygame.key.get_pressed() 
        if key[K_UP] == 1:  #위쪽 방향키를 누르면
            car_y = (car_y + 1) % CMAX #코스 상 위치 이동
        
        #화면에 그릴 도로 x 좌표와 높낮이 계산
        di = 0 #도로 커브 방향 계산 변수
        ud = 0 #판의 높낮이 계산 변수
        board_x = [0] * BOARD #판의 x좌표 계산 리스트
        board_ud = [0] * BOARD #판의 높낮이 계산 리스트 
        for i in range(BOARD):
            di += curve[(car_y + i) % CMAX] #커브 데이터로 도로 굽기 계산
            ud  += updown[(car_y + i) % CMAX] #기복 데이터에서 도로 기복 계산
            board_x[i] = 400 - BOARD_W[i] / 2 +  di /2 #판의 x 좌표를 계산
            board_ud[i] =  ud / 30  #판의 높낮이 계산
        
        horizon = 400 + int(ud /  3) #지평선 좌표 계산
        sy = horizon #도로를 그리기 시작할 위치

        vertical =  vertical - di * key[K_UP] / 30 #배경 수직 위치
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
            pygame.draw.polygon(screen, col, [[ux, uy], [ux + uw, uy], [bx + bw, by], [bx, by]])

            if int(car_y  + i) % 10  <= 4: #좌우 노란색  선
                pygame.draw.polygon(screen, YELLOW, [[ux, uy],  [ux + uw * 0.02, uy], [bx + bw * 0.02, by], [bx, by]]) #도로 왼쪽
                pygame.draw.polygon(screen, YELLOW, [[ux + uw  * 0.98, uy],  [ux + uw, uy], [bx  + bw,  by], [bx + bw * 0.98, by]]) #도로 오른쪽
            if int(car_y + i) % 20 <= 10: #흰색선
                pygame.draw.polygon(screen, WHITE, [[ux + uw * 0.24, uy],  [ux + uw * 0.26, uy], [bx + bw * 0.26,  by], [bx + bw * 0.24, by]]) #왼쪽
                pygame.draw.polygon(screen, WHITE, [[ux + uw * 0.49, uy],  [ux + uw * 0.51, uy], [bx + bw * 0.51,  by], [bx + bw * 0.49, by]]) #중앙
                pygame.draw.polygon(screen, WHITE, [[ux + uw * 0.74, uy],  [ux + uw * 0.76, uy], [bx + bw * 0.76,  by], [bx + bw * 0.74, by]]) #오른쪽
            
            scale = 1.5 * BOARD_W[i] / BOARD_W[0]
            obj_l = object_left[int(car_y + i) %  CMAX] #도로 왼쪽  물체
            if obj_l == 2: #야자나무
                draw_obj(screen, img_obj[obj_l], ux - uw * 0.05, uy, scale)
            if obj_l == 3: #요트
                draw_obj(screen, img_obj[obj_l], ux - uw * 0.5, uy, scale)
            if obj_l == 9: #바다
                screen.blit(img_sea, [ux - uw * 0.5 - 780, uy])
            
            obj_r = object_right[int(car_y + i) %  CMAX] #도로 오른쪽  물체
            if obj_r == 1: #간판
                draw_obj(screen, img_obj[obj_r], ux + uw * 1.3, uy, scale)

        pygame.display.update()
        clock.tick(60) #60 프레임
  
if __name__ == '__main__': #이 프로그램 직접  실행시
    main() #main() 함수 호출
