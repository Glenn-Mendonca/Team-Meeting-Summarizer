import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import HORIZONTAL
import time

class Splash(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wid, self.hgt = 427, 250
        self.sc_wid, self.sc_hgt = self.winfo_screenwidth(), self.winfo_screenheight()
        self.Xcor = (self.sc_wid/2)-(self.wid/2)
        self.Ycor = (self.sc_hgt/2)-(self.hgt/2)
        self.geometry(f'{self.wid}x{self.hgt}+{int(self.Xcor)}+{int(self.Ycor)}')
        self.overrideredirect(1)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')

        self.bg_colour = '#249794'

        self.main()

    def main(self):
        self.progress = ttk.Progressbar(self, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=500, mode='determinate',)
        self.progress.place(x=-10,y=235)

        tk.Frame(self, width=427, height=241, bg=self.bg_colour).place(x=0, y=0)
        self.progress.after(100, self.bar)

        l1 = tk.Label(self, text='Team', fg='white', bg=self.bg_colour)
        font1=('Calibri (Body)',18,'bold')
        l1.config(font=font1)
        l1.place(x=50, y=72)

        l2 = tk.Label(self, text='Meeting', fg='white', bg=self.bg_colour)
        font2 = ('Calibri (Body)',18)
        l2.config(font=font2)
        l2.place(x=135, y=72)

        l3 = tk.Label(self, text='Summarizer', fg='white', bg=self.bg_colour)
        font3=('Calibri (Body)',13)
        l3.config(font=font3)
        l3.place(x=50,y=110)

    def bar(self):
        l4 = tk.Label(self, text='Loading...', fg='white', bg=self.bg_colour)
        font = ('Calibri (Body)',10)
        l4.config(font=font)
        l4.place(x=18,y=210)
        for i in range(100):
            self.progress['value'] = i
            self.update_idletasks()
            time.sleep(0.03)
        self.destroy()