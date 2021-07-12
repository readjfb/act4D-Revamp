import tkinter as tk
from tkinter import ttk


class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Torque GUI")
        self.notebk = ttk.Notebook(self.master)

        self.frame1 = ttk.Frame(self.notebk, width=400, height=400, relief=tk.SUNKEN)
        self.frame2 = ttk.Frame(self.notebk, width=400, height=400, relief=tk.SUNKEN)
        self.frame3 = ttk.Frame(self.notebk, width=400, height=400, relief=tk.SUNKEN)
        self.frame4 = ttk.Frame(self.notebk, width=400, height=400, relief=tk.SUNKEN)

        self.notebk.add(self.frame1, text="General")
        self.notebk.add(self.frame2, text="Subject Info")
        self.notebk.add(self.frame3, text="Jacobean Constants")
        self.notebk.add(self.frame4, text="Maxes")
        self.notebk.pack(expand=1, fill="both")

        # General Pane
        self.start = ttk.Button(self.frame1, text="Start Trial")
        self.start.grid(column=0, row=1, padx=5, pady=5)
        self.pause = ttk.Button(self.frame1, text="Pause Trial")
        self.pause.grid(column=1, row=1, padx=5, pady=5)
        self.end = ttk.Button(self.frame1, text="End Trial")
        self.end.grid(column=2, row=1, padx=5, pady=5)

        self.quit = ttk.Button(self.frame1, text="Exit")
        self.quit.grid(column=3, row=4, padx=5, pady=5)

        self.defTrial = tk.StringVar(self.master)
        self.trialTypes = ["option1", "option2"]
        self.defTrial.set("Select a Trial Type")
        self.trialType = tk.OptionMenu(self.frame1, self.defTrial, *self.trialTypes)
        self.trialType.grid(column=0, row=2, padx=5, pady=5)

        self.trialTog = ttk.Button(self.frame1, text="Practice", command=self.toggle)
        self.trialTog.grid(column=1, row=0, padx=5, pady=5)

        self.save = ttk.Button(self.frame1, text="Save")
        self.save.grid(column=0, row=4, padx=5, pady=5)
        self.erase = ttk.Button(self.frame1, text="Erase")
        self.erase.grid(column=1, row=4, padx=5, pady=5)

        # Subject Info Pane
        self.age = tk.Label(self.frame2, text="Age")
        self.age.grid(row=0, column=0, padx=5, pady=5)
        self.ageEnt = tk.Entry(self.frame2)
        self.ageEnt.grid(row=0, column=1, padx=5, pady=5)

        self.gen = tk.Label(self.frame2, text="Gender")
        self.gen.grid(row=1, column=0, padx=5, pady=5)
        self.genEnt = tk.Entry(self.frame2)
        self.genEnt.grid(row=1, column=1, padx=5, pady=5)

        self.subjectSub = ttk.Button(self.frame2, text="Submit")
        self.subjectSub.grid(row=2, column=0, padx=5, pady=5)

    def toggle(self):
        if self.trialTog["text"] == "Practice":
            self.trialTog.configure(text="Testing")
        else:
            self.trialTog.configure(text="Practice")


def launchGUI():
    root = tk.Tk()
    GUI(root)
    tk.mainloop()


if __name__ == "__main__":
    launchGUI()
