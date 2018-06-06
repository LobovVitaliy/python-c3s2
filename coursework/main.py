from coursework.db import generate
from coursework.rating import show_rating
from coursework.growth import show_growth
from tkinter import *

window = Tk()
window.title("Coursework")

b1 = Button(text="Згенерувати дані та зберегти в БД", command=generate)
b1.grid(row=0, column=0)

b2 = Button(text="Рейтинги груп", command=show_rating)
b2.grid(row=0, column=1)

b3 = Button(text="Приріст студентів", command=show_growth)
b3.grid(row=0, column=2)

if __name__ == '__main__':
    window.mainloop()
