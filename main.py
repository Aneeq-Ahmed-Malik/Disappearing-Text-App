import math
import customtkinter

WIDTH = 800
HEIGHT = 450

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


class MainWindow(customtkinter.CTk):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.maxsize(WIDTH, HEIGHT)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - WIDTH) // 2
        y = (screen_height - HEIGHT) // 2

        self.title("Dangerous Text App")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
        self.heading = customtkinter.CTkLabel(self, text="Dangerous Text App", font=customtkinter.CTkFont(family="Helvetica", size=30, weight="bold"))
        self.heading.grid(row=0, column=1, sticky="nsew", pady=50)

        self.diff = customtkinter.CTkLabel(self, text="Choose Difficulty", font=customtkinter.CTkFont(family="calibiri", size=20, weight="bold"))
        self.diff.grid(row=1, column=1, sticky="n", pady=(20, 70))

        self.easy = customtkinter.CTkButton(self, text="Easy", font=customtkinter.CTkFont(family="Trebuchet MS", size=20, weight="bold"), hover_color="orange", command=lambda: self.play(5, 7))
        self.easy.grid(row=2, column=0, sticky="ne")

        self.medium = customtkinter.CTkButton(self, text="Medium", font=customtkinter.CTkFont(family="Trebuchet MS", size=20, weight="bold"), hover_color="orange", command=lambda: self.play(3, 5))
        self.medium.grid(row=2, column=1)

        self.hard = customtkinter.CTkButton(self, text="Hard", font=customtkinter.CTkFont(family="Trebuchet MS", size=20, weight="bold"), hover_color="orange", command=lambda: self.play(1.5, 3))
        self.hard.grid(row=2, column=2, sticky="w")

    def play(self, warning, counter):

        self.heading.grid_forget()
        self.diff.grid_forget()
        self.easy.grid_forget()
        self.medium.grid_forget()
        self.hard.grid_forget()

        self.frame = Game(self, warning, counter)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.tkraise()

    def main_window(self):
        self.heading.grid(row=0, column=1, sticky="nsew", pady=50)
        self.diff.grid(row=1, column=1, sticky="n", pady=(20, 70))
        self.easy.grid(row=2, column=0, sticky="ne")
        self.medium.grid(row=2, column=1)
        self.hard.grid(row=2, column=2, sticky="w")


def format_time(seconds):

    count_min = math.floor(seconds / 60)
    count_sec = seconds % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    if count_min < 10:
        count_min = f"0{count_min}"

    return f"{count_min}:{count_sec}"


class Game(customtkinter.CTkFrame):
    def __init__(self, master: MainWindow, warning, counter,  **kwargs):
        super().__init__(master, **kwargs)

        self.start_timer = warning
        self.timer_upto = counter

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.count = 0
        self.timer = None
        self.time_to_count = self.timer_upto
        self.warning = None

        self.lbl = customtkinter.CTkLabel(self, text="Magic Writing\nYour text will disappear if you stop writing", font=("Helvetica", 20, "bold"), text_color="orchid")
        self.lbl.grid(row=0, column=1, sticky="nsew")

        self.time = customtkinter.CTkLabel(self, text="Time\n00:00", font=("Courier", 20, "bold"),  text_color="plum3")
        self.time.grid(row=0, column=0)

        self.best_time = customtkinter.CTkLabel(self, text="Record\n00:00", font=("Courier", 20, "bold"), text_color="plum3")
        self.best_time.grid(row=0, column=2)

        self.box = customtkinter.CTkTextbox(self, width=600, height=300, font=("arial", 20), text_color="plum1", wrap=customtkinter.WORD)
        self.box.grid(row=1, column=1, sticky="sw", pady=(10, 0))

        self.counter = customtkinter.CTkLabel(self, text="", font=("Courier", 40, "bold"), text_color="red")
        self.counter.grid(row=2, column=1, sticky="ew")

        self.restart = customtkinter.CTkButton(self, text="Restart", font=customtkinter.CTkFont(family="Trebuchet MS", size=20, weight="bold"), hover_color="orange", width=200, command=lambda: self.reset())
        self.restart.grid(row=2, column=1, sticky="w")

        self.back = customtkinter.CTkButton(self, text="Back", font=customtkinter.CTkFont(family="Trebuchet MS", size=20, weight="bold"), hover_color="orange", width=200, command=lambda: [self.destroy(), master.main_window()])
        self.back.grid(row=2, column=1, sticky="e")
        self.warning = self.after(int(self.start_timer * 1000), self.time_up)
        self.box.bind("<KeyRelease>", self.count_down)
        self.box.bind("<KeyPress>", self.check_typing)
        self.get_highscore()
        self.box.focus_set()

    def count_down(self, event):

        self.time.configure(text=f"Time\n{format_time(self.count)}")
        self.count += 1
        self.timer = self.after(1000, self.count_down, event)
        self.box.unbind("<KeyRelease>")

    def get_highscore(self):
        try:
            with open("highscore.txt", mode="r") as file:
                scores = [int(score.strip()) for score in file.readlines()]
                self.best_time.configure(text=f"Record\n{format_time(max(scores))}")
        except FileNotFoundError:
            return

    def check_typing(self, event):
        if event.char != '':
            char = list(event.char)[0]
            if 32 <= ord(char) <= 126:  # Only printable ASCII values
                self.after_cancel(self.warning)
                self.warning = self.after(self.start_timer * 1000, self.time_up)
                self.counter.configure(text="")
                self.time_to_count = self.timer_upto

    def time_up(self):
        if self.count == 0:
            return
        self.counter.configure(text=self.time_to_count)
        self.time_to_count -= 1

        if self.time_to_count >= 0:
            self.warning = self.after(1000, self.time_up)
        else:
            self.after_cancel(self.timer)
            self.box.delete("0.0", "end")
            with open(file="highscore.txt", mode="a") as file:
                file.write(str(self.count) + "\n")
            self.count = 0
            self.box.bind("<KeyRelease>", self.count_down)

    def reset(self):
        if self.count == 0:
            return
        self.box.delete("0.0", "end")
        self.counter.configure(text="")
        self.after_cancel(self.warning)
        self.after_cancel(self.timer)
        self.box.bind("<KeyRelease>", self.count_down)
        self.time_to_count = self.timer_upto
        self.warning = self.after(int(self.start_timer * 1000), self.time_up)
        self.time.configure(text="Time\n00:00")
        self.count = 0


app = MainWindow()

app.mainloop()
