#도로의 기복 표현하기
import pygame
import sys
import math
from pygame.locals import *

BOARD = 120 #도로를 그릴 판 수
CMAX = BOARD * 4 # 코스 길이 지정 상수
curve = [0] * CMAX #도로 커브 방향 관리 리스트
updown = [0] * CMAX #도로 기복을 넣을 리스트

def make_course(): #코스 데이터 생성 함수
    for i in range(CMAX):
        updown[i] = int(5 * math.sin(math.radians(i)))

def main(): 
    pygame.init()
    pygame.display.set_caption("Python Racer")
    screen =  pygame.display.set_mode((800, 600)) #화면 초기화
    clock = pygame.time.Clock()  
  
    img_bg = pygame.image.load("image_pr/bg.png").convert() #배경 이미지 로딩

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
            if (car_y + i) % 12 == 0:  #일정 간격으로 12장 중 1장
                col = (255, 255, 255) #흰색 대입
            pygame.draw.polygon(screen, col, [[ux, uy], [ux + uw, uy], [bx + bw, by], [bx, by]])

        pygame.display.update()
        clock.tick(60) #60 프레임
  
if __name__ == '__main__': #이 프로그램 직접  실행시
    main() #main() 함수 호출
