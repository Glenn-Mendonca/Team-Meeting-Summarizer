from tkinter import *
import tkinter.ttk as ttk
import time

def bar():
    l4=Label(root,text='Loading...',fg='white',bg=bg_colour)
    lst4=('Calibri (Body)',10)
    l4.config(font=lst4)
    l4.place(x=18,y=210)
    for i in range(100):
        progress['value']=i
        root.update_idletasks()
        time.sleep(0.03)
    root.destroy()

root = Tk()
wid, hgt = 427, 250
sc_wid, sc_hgt = root.winfo_screenwidth(), root.winfo_screenheight()
Xcor = (sc_wid/2)-(wid/2)
Ycor = (sc_hgt/2)-(hgt/2)
root.geometry(f'{wid}x{hgt}+{int(Xcor)}+{int(Ycor)}')
root.overrideredirect(1)

style = ttk.Style()
style.theme_use('clam')
style.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')

progress= ttk.Progressbar(root,style="red.Horizontal.TProgressbar",orient=HORIZONTAL,length=500,mode='determinate',)
progress.place(x=-10,y=235)

bg_colour = '#249794'

Frame(root,width=427,height=241,bg=bg_colour).place(x=0,y=0)

b1=Button(root,width=10,height=1,text='Get Started',command=bar,border=0,fg=bg_colour,bg='white')
b1.place(x=170,y=200)

l1=Label(root,text='Team',fg='white',bg=bg_colour)
lst1=('Calibri (Body)',18,'bold')
l1.config(font=lst1)
l1.place(x=50,y=72)

l2=Label(root,text='Meeting',fg='white',bg=bg_colour)
lst2=('Calibri (Body)',18)
l2.config(font=lst2)
l2.place(x=135,y=72)

l3=Label(root,text='Summarizer',fg='white',bg=bg_colour)
lst3=('Calibri (Body)',13)
l3.config(font=lst3)
l3.place(x=50,y=110)

root.mainloop()