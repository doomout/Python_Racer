#방향키로 경사로 만들기
import tkinter

def key_down(e):
    key = e.keysym
    if key == "Up":
        draw_road(0, -5)
    if key == "Down":
        draw_road(0, 5)


BORD_COL = ["white", "silver", "gray"] #판 색 정의 리스트
def draw_road(di, updown):
    canvas.delete("ROAD") #먼저 도로 삭제
    h = 24 #첫 번째 판 높이
    y = 600 - h #첫 번째 판의 y 좌표
    for i in range(23, 0, -1):
        uw = (i - 1) * (i - 1) * 1.5 #판의 폭
        ux = 400 - uw / 2  + di * (23 - (i - 1))
        bw = i * i * 1.5
        bx = 400 - bw / 2 + di * (23 - i)
        col = BORD_COL[i % 3]
        canvas.create_polygon(ux, y, ux + uw, y, bx + bw, y + h, bx, y + h, fill=col, tag="ROAD") #판을 다각형(사다리꼴)로 그림
        h = h - 1
        y = y - h + updown

root = tkinter.Tk()
root.title("키보드로 경사로 만들기")
root.bind("<Key>", key_down)
canvas = tkinter.Canvas(width=800, height=600, bg="blue")
canvas.pack() #캔버스 배치
canvas.create_rectangle(0, 300, 800, 600, fill="green") #캔버스 아래쪽 절반에 녹색 사각형 그리기
canvas.create_text(400, 100, text="위쪽, 아래쪽 방향키를 눌러주세요.", fill="white")

root.mainloop()