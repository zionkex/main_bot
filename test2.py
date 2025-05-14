from tkinter import *
import random
import tkinter.messagebox
can = Tk()
can.title("Полотно для малювання")
can.geometry()
can.resizable (False, False)
cant = Canvas(width=800, height=700, bg='white')
cant.pack()


adder = []
x = 5
y = 3
bolt_y = 380
bolt_x = 130
hp=3
text1=hp*"❤️️"
size_x1 = 320
size_y1 = 350
size_x2 = 100
size_y2 = 70

text = cant.create_text(150,20,text = text1 ,font = 50)
ball1 = cant.create_oval(bolt_x,bolt_y,bolt_x+30,bolt_y+30)
plat = cant.create_rectangle(300,670,400,675,fill="black")

for i in range(1,11):
    if i < 2:
        size_x1 = 325
        size_y1 = 350
    elif i < 4:
        size_x1 = 250 + (i-2)*150
        size_y1 = 250
    elif i < 7:
        size_x1 = 170 + (i-4)*150
        size_y1 = 150
    elif i < 11:
        size_x1 = 100 + (i-7)*150
        size_y1 = 50
    # cant.create_rectangle(size_x1, size_y1, size_x1 + size_x2, size_y1 + size_y2)
    block = cant.create_rectangle(size_x1, size_y1, size_x1 + size_x2, size_y1 + size_y2)
    print("my new block",block)
    adder.append(block)
    print(adder)
block_check = []

for k in range(len(adder)):
    block_check.append(1)

def delete():
    global bolt_x,bolt_y,y
    if y<0:
        for i in range(len(adder)):
            if block_check[i]== 1:
                cant.itemconfigure(adder[i], state='normal')
                x1,y1,x2,y2=cant.coords(adder[i])
                if (bolt_x + 15 >= x1 and bolt_x + 15 <= x2
                        and bolt_y + 15 >= y1 and bolt_y + 15 <= y2):
                    cant.delete(adder[i])
                    block_check[i] = 0
                    y = -y
                    break
    elif y>0:
        for i in range (len(adder)):
            if block_check[i]== 1:
                cant.itemconfigure(adder[i], state='hidden')

def move(event):
    if cant.coords(plat)[0] - 20 > 0 and event.keysym == "a":
        cant.move(plat, -20, 0)
    elif cant.coords(plat)[2] + 20 < 800 and event.keysym == "d":
        cant.move(plat, 20, 0)

def ball():

    global ball1,bolt_y,bolt_x,x,y,text,text1,hp
    cant.move(ball1,x,y)
    cant.after(10, ball)
    bolt_x+=x
    bolt_y+=y
    if (cant.coords(ball1)[0] < cant.coords(plat)[2] and
             cant.coords(ball1)[2] > cant.coords(plat)[0] and
             cant.coords(ball1)[3] > cant.coords(plat)[1] and
             cant.coords(ball1)[1] < cant.coords(plat)[3]):
         x = x
         y = -y
    if cant.coords(ball1)[0] < 10:
        x = -x
        y =y
    elif cant.coords(ball1)[2] > 800:
        x =-x
        y = y
    elif cant.coords(ball1)[1] < 0:
        x=x
        y=-y
    elif cant.coords(ball1)[3] > 700:
        x=x
        y=-y
        cant.delete(text)
        hp-=1
        text1=hp*"❤️"
        if hp==0:
            can.destroy()
            tkinter.messagebox.showinfo("lose", 'Game over')

        else:
            text = cant.create_text(150, 20, text=text1, font=50)
    if not any(block_check):

        can.destroy()
        tkinter.messagebox.showinfo("win", 'You won')

    delete()

ball()

cant.focus_set()
cant.bind('<a>', move)
cant.bind('<d>', move)


cant.mainloop()
