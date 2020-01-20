from tkinter import *
app = Tk()
app.title("Hand Draw")
app.geometry("500x400")
drawBoard = Canvas(app, width=500, height=200)
pen = Button(app, text="insert Pen image", width="20", height="3")
clearCanvas = Button(app, text="insert clearcanvas image", width="20", height="3")
erase = Button(app, text="insert erase image", width="20", height="3")
drawBoard.pack()
def mmove(event):
    x, y = event.x, event.y
    x1 = (x+1)
    y1 = (y+1)
    drawBoard.create_line(x, y, x1, y1)
    print(event.x, event.y)
app.bind('<B1-Motion>', mmove)
#Change app bind when color is different
#Make movement on opencv into movement on canvas
pen.pack()
clearCanvas.pack()
erase.pack()
app.mainloop()
