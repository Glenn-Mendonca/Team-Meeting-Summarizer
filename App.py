from Include.Dependencies.Initial import *
from Include.Dependencies.Splash import Splash
from Include.Dependencies.Scrapper import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
from tkinter.constants import (
    LEFT,
    NORMAL,
    WORD,
    END
)
from tkinter import filedialog as fd
import ctypes
import requests
from datetime import datetime
ctypes.windll.shcore.SetProcessDpiAwareness(1)
themes = ["light", "dark"]
style.use("ggplot")

# App Definition
class App(tk.Tk):
    # App Constructor
    def __init__(self):
        super().__init__()
        self.title("Team Meetings Summarizer")
        self.geometry("900x800")
        self.resizable(False, False)
        self.iconbitmap("./Include/Images/icon.ico")
        self.tk.call("source", "sun-valley.tcl")
        self.theme = 0
        self.interval = 0
        self.participantsdata = {"x":[0],"y":[0]}
        self.wpsdata = {"x":[0],"y":[0]}
        self.wpsstr = ""
        self.participantcount = 0
        self.play_state = False
        self.final_transcript, self.meet_code, self.generated_transcript, self.speaker, self.prev_speaker = "", "", "", "", ""
        self.scrapper = Scrapper()
        self.initial()
        self.Start()
        self.main()

    # Initial Screen
    def initial(self):
        window = Initial(self, self.getcode)
        window.grab_set()

    # Main Screen
    def main(self):
        # Title Frame
        self.title_frame = tk.LabelFrame(
            self, text="Title", font=12, borderwidth=3, highlightthickness=0
        )
        # Title Textbox
        self.title = tk.Text(self.title_frame, wrap=WORD, bd=0, height=2, width=35)
        self.title.pack(pady=10, padx=10)
        self.title_frame.pack(pady=10)

        # self.date = tk.Label(self.menu_frame, text = (datetime.today()).strftime('%d-%m-%Y'))

        # Group Frame to hold Agenda and Transcript Textbox
        self.group_trag = tk.Frame(self, borderwidth=0, highlightthickness=0)

        # Transcript Frame
        self.transcript_frame = tk.LabelFrame(
            self.group_trag,
            text="Transcript",
            font=12,
            borderwidth=3,
            highlightthickness=0,
        )
        # Transcript Textbox
        self.transcript = tk.Text(
            self.transcript_frame, wrap=WORD, bd=0, height=25, width=35
        )
        self.transcript.pack(pady=10, padx=10)
        self.transcript.config(state=NORMAL)
        self.transcript_frame.pack(side=LEFT, padx=20)

        # Agenda Frame
        self.agenda_frame = tk.LabelFrame(
            self.group_trag, text="Agenda", font=12, borderwidth=3, highlightthickness=0
        )
        # Agenda Textbox
        self.agenda = tk.Text(self.agenda_frame, wrap=WORD, bd=0, height=10, width=35)
        self.agenda.pack(pady=10, padx=10)
        self.agenda_frame.pack(side=LEFT, padx=20)

        graphs = plt.Figure(figsize=(5,4), dpi=60)
        #WPS Graph
        self.wpsplot = graphs.add_subplot(211)
        #Participant Graph
        self.participantsplot = graphs.add_subplot(212)

        self.canvas = FigureCanvasTkAgg(graphs, self.agenda_frame)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        

        self.group_trag.pack()

        # ttk.Separator(self, orient=HORIZONTAL, ).pack(side=BOTTOM)#place(relx=0, rely=0.95, relwidth=0.2, relheight=1)

        # Menu Frame
        self.menu_frame = tk.LabelFrame(
            self, text="Menu", font=12, borderwidth=3, highlightthickness=0
        )
        # Play/Pause Button
        self.play_icon = tk.PhotoImage(
            file=f"./Include/Images/{themes[(self.theme+1)%2]}/play.png"
        )
        
        self.play = tk.Button(
            self.menu_frame,
            bd=0,
            width=40,
            height=40,
            image=self.play_icon,
            command=self.pause_play,
        )
        self.play.pack(side=LEFT, padx=10, pady=10)

        # Stop Button
        self.stop_icon = tk.PhotoImage(
            file=f"./Include/Images/{themes[(self.theme+1)%2]}/stop.png"
        )
        self.stop = tk.Button(
            self.menu_frame,
            bd=0,
            width=40,
            height=40,
            image=self.stop_icon,
            command=self.Stop,
        )
        self.stop.pack(side=LEFT, padx=10, pady=10)

        # Theme Button
        self.mode_icon = tk.PhotoImage(
            file=f"./Include/Images/{themes[(self.theme+1)%2]}/theme.png"
        )
        self.mode = tk.Button(
            self.menu_frame,
            bd=0,
            width=40,
            height=40,
            image=self.mode_icon,
            command=self.updatetheme,
        )
        self.mode.pack(side=LEFT, padx=10, pady=10)

        # Summarize Button
        self.summarize_icon = tk.PhotoImage(
            file=f"./Include/Images/{themes[(self.theme+1)%2]}/summarize.png"
        )
        self.summarize = tk.Button(
            self.menu_frame,
            bd=0,
            width=40,
            height=40,
            image=self.summarize_icon,
            command=self.summarize_text,
        )
        self.summarize.pack(side=LEFT, padx=10, pady=10)

        # Time Label
        self.time = ttk.Label(self.menu_frame, text="", width=10, font="Segoe-Ui 15")
        self.time.pack(side=LEFT, padx=10, pady=10)
        self.time.after(1000, self.update_time)

        self.menu_frame.pack(pady=10)

    # Switching Play/Pause Button
    def pause_play(self):
        try:
            self.play_icon = tk.PhotoImage(
                file=f"./Include/Images/{themes[(self.theme+1)%2]}/play.png"
            )
            self.pause_icon = tk.PhotoImage(
                file=f"./Include/Images/{themes[(self.theme+1)%2]}/pause.png"
            )
            self.play_state = not self.play_state
            if self.play_state:
                print("Playing")
                self.play.configure(image=self.pause_icon)
            else:
                print("Pausing")
                self.play.configure(image=self.play_icon)
        except:
            pass

    # Switching Themes
    def updatetheme(self):
        self.theme += 1
        self.tk.call("set_theme", themes[self.theme % 2])
        try:
            self.play_icon = tk.PhotoImage(
                file=f"./Include/Images/{themes[(self.theme+1)%2]}/play.png"
            )
            self.pause_icon = tk.PhotoImage(
                file=f"./Include/Images/{themes[(self.theme+1)%2]}/pause.png"
            )
            self.stop_icon = tk.PhotoImage(
                file=f"./Include/Images/{themes[(self.theme+1)%2]}/stop.png"
            )
            self.mode_icon = tk.PhotoImage(
                file=f"./Include/Images/{themes[(self.theme+1)%2]}/theme.png"
            )
            self.summarize_icon = tk.PhotoImage(
                file=f"./Include/Images/{themes[(self.theme+1)%2]}/summarize.png"
            )
            if self.play_state:
                self.play.configure(image=self.pause_icon)
            else:
                self.play.configure(image=self.play_icon)
            self.stop.configure(image=self.stop_icon)
            self.mode.configure(image=self.mode_icon)
            self.summarize.configure(image=self.summarize_icon)
            self.summarize
        except:
            pass

    # Update Time
    def update_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.time.configure(text=str(current_time))
        self.time.after(1000, self.update_time)

    # Summarize Text
    def summarize_text(self):
        filetypes = (
            ('text files', '*.txt')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )
        data = filename.read().replace('\n', '')
        response = requests.post('http://backendIP/upload', data=data, timeout = 30)
        location = f'./Transcripts/summary.txt'
        with open(location, 'w') as file:
            file.write(response)


    # Update Transcript Text
    def update_transcript(self):
        self.scrapper.extractcaptions(self.getdata)
        if(self.play_state and self.generated_transcript!=""):
            self.transcript.delete(1.0, END)
            if(self.prev_speaker != self.speaker):
                self.final_transcript += "\n" + self.speaker + "\n"
                self.prev_speaker = self.speaker
            self.final_transcript += self.generated_transcript
            self.wpsstr += " " + self.generated_transcript + " "
            self.generated_transcript = ""
            self.transcript.insert(END, self.final_transcript)
        self.after(5000, self.update_transcript)

    # Start Meet Bot
    def Start(self):
        if(self.meet_code.isalnum()):
            if(self.scrapper.login(self.meet_code)):
                print("All processes went smoothly")
                self.after(1, self.update_transcript)
                self.after(1, self.update_graphs)
            else:
                print("Some Error occured !")
        else:
            self.after(1000, self.Start)

    #Stop Meet Bot
    def Stop(self):
        self.scrapper.driver.quit()
        Title = self.title.get(1.0, "end-1c")
        Agenda = self.agenda.get(1.0, "end-1c") 
        location = f'./Transcripts/{Title}.txt'
        with open(location, 'w') as file:
            file.write("Title:\n" + Title + "\n" + "Agenda:\n" + Agenda + "\n" + self.final_transcript)
            messagebox.showinfo('Transcript Info',f'Generated Transcript is saved at {os.path.abspath(location)}')
            time.sleep(5)
            print("Stopping")

    # Get Meet Code
    def getcode(self, code):
        self.meet_code = code

    # Get Transcript Data
    def getdata(self, data):
        if(data['Speaker']!="" and data['Transcript']!=""):
            self.speaker = data['Speaker']
            self.generated_transcript = data['Transcript']
            self.participantcount = data['Users']

    # Update Graphs
    def update_graphs(self):
        print("Graph Updated")
        print(self.wpsdata, self.participantsdata)
        self.interval += 5
        self.wpsdata['x'].append(len(self.wpsstr.split()))
        self.participantsdata['x'].append(self.participantcount)
        self.wpsdata['y'].append(self.interval)
        self.participantsdata['y'].append(self.interval)
        self.wpsstr = ""
        # WPS
        self.wpsplot.plot(self.wpsdata['y'], self.wpsdata['x'], "k--")
        self.wpsplot.fill_between(self.wpsdata['y'], self.wpsdata['x'], color="#539ecd")
        # Participants
        self.participantsplot.clear()
        self.participantsplot.plot(self.participantsdata['y'], self.participantsdata['x'], "k--")
        self.participantsplot.fill_between(self.participantsdata['y'], self.participantsdata['x'], color="#539ecd")
        self.canvas.draw_idle() 
        self.after(60000, self.update_graphs)
        

# Splash Screen
def splash():
    splash = Splash()
    splash.mainloop()


if __name__ == "__main__":
    splash()
    app = App()
    app.mainloop()
