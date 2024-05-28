import tkinter

root = tkinter.Tk()
root.title("도로 그리기 v3")
canvas = tkinter.Canvas(width=800, height=600, bg="blue")
canvas.pack()

canvas.create_rectangle(0, 300, 800, 600, fill="green") #캔버스 아래쪽 절반에 녹색 사각형 그리기

BORD_COL = ["white", "silver", "gray"] #판 색 정의 리스트
h = 2 #첫 번째 판 높이
y = 300 #첫 번째 판의 y 좌표

for i in range(1, 24):
    uw = i * i * 1.5 #판의 폭
    ux = 400 - uw / 2  
    bw = (i + 1) * (i + 1) * 1.5
    bx = 400 - bw / 2
    col = BORD_COL[i % 3]
    canvas.create_polygon(ux, y, ux + uw, y, bx + bw, y + h, bx, y + h, fill=col) #판을 다각형(사다리꼴)로 그림
    y = y + h
    h = h + 1

root.mainloop()