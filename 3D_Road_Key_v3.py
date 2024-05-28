#키보드로 자유롭게 도로 상태 바꾸기
import tkinter
import math

curve = 0 #커브 크기
undulation = 0 #기복 크기
tmr = 0 #타이머 변수

def key_down(e):
    global curve,  undulation #전역 변수 선언
    key = e.keysym
    if key == "Up":
        undulation = undulation - 20
    if key == "Down":
        undulation = undulation + 20
    if key == "Left":
        curve = curve - 5
    if key == "Right":
        curve = curve + 5
    draw_road(curve,  undulation)

updown = [0] * 24 #판의 Y 좌표를 미끄러뜨린 값을 넣을 리스트
for i in range(23, -1, -1):
    updown[i] = math.sin(math.radians(180 * i / 23))

BORD_COL = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"] #판 색 정의 리스트
def draw_road(di, ud):
    canvas.delete("ROAD") #먼저 도로 삭제
    h = 24 #첫 번째 판 높이
    y = 600 - h #첫 번째 판의 y 좌표
    for i in range(23, 0, -1):
        uw = (i - 1) * (i - 1) * 1.5 #판의 윗변 폭
        ux = 400 - uw / 2  + di * (23 - (i - 1)) #판의 윗변 x좌표
        uy = y + int(updown[i - 1] * ud) #판의 윗변 y 좌표
        bw = i * i * 1.5 #판의 아랫변 폭
        bx = 400 - bw / 2 + di * (23 - i) #판의 아랫변 x좌표
        by = y + h + int(updown[i] * ud)  #판의 아랫변 y좌표
        col = BORD_COL[(6 - tmr % 7 + i) % 7] #판의 색 변수
        canvas.create_polygon(ux, uy, ux + uw, uy, bx + bw, by, bx, by, fill=col, tag="ROAD") #판을 다각형(사다리꼴)로 그림
        h = h - 1
        y = y - h
    
def main():
    global tmr 
    tmr = tmr + 1
    draw_road(curve, undulation)
    root.after(200, main) #0.2초 후 다시 main() 함수 실행

root = tkinter.Tk()
root.title("도로 그리기")
root.bind("<Key>", key_down)
canvas = tkinter.Canvas(width=800, height=600, bg="black")
canvas.pack() #캔버스 배치
canvas.create_rectangle(0, 300, 800, 600, fill="gray") 
canvas.create_text(400, 100, text="방향키로 도로를 바꿀 수 있습니다.", fill="white")
main()
root.mainloop()