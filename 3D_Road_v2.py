import tkinter

root = tkinter.Tk()
root.title("도로 그리기 v2")
canvas = tkinter.Canvas(width=800, height=600, bg="blue")
canvas.pack()

canvas.create_rectangle(0, 300, 800, 600, fill="green") #캔버스 아래쪽 절반에 녹색 사각형 그리기

BORD_COL = ["white", "silver", "gray"] #판 색 정의 리스트
h = 2 #첫 번째 판 높이
y = 300 #첫 번째 판의 y 좌표

for i in range(1, 24):
    w = i * i * 1.5 #판의 폭을 계산해서 w에 대입
    x = 400 - w / 2  #판을 그릴 x 좌표에 변수 x에 대입
    col = BORD_COL[i % 3]
    canvas.create_rectangle(x, y, x + w, y + h, fill=col) #(x,y) 위치에 폭 w, 높이 h 판 그림
    y = y + h
    h = h + 1

root.mainloop()