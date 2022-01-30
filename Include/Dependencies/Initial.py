import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox
from tkinter.constants import CENTER

class Initial(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.geometry('300x100')
        self.title('GMeet Code')
        self.app = app

        gmeet = PhotoImage(file = './Include/Images/meeticon.png')
        self.iconphoto(False, gmeet)

        self.code = tk.StringVar()

        tk.Label(self,
            text='Meet Code'
        ).pack()

        tk.Entry(self,
            textvariable = self.code,
            justify=CENTER
        ).pack()

        ttk.Button(self,
                text='Submit',
                command=self.exit).pack(expand=True)

    def exit(self):
        if(len(self.code.get()) == 10 and (self.code.get()).isalpha()):
            self.app(self.code.get())
            self.destroy()
        else:
            messagebox.showerror('Incorrect Code','GMeet Code consists of 10 alphabet characters.')