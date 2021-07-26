import tkinter as tk
from multiprocessing.connection import Client
from tkinter import ttk

class GUI:
    def __init__(self, master, conn, in_conn):
        # queue for multiprocessing
        self.data_queue = conn
        self.in_queue = in_conn

        self.master = master
        self.master.title("Torque GUI")
        self.notebk = ttk.Notebook(self.master)

        # Tabs for each section
        self.frame1 = ttk.Frame(self.notebk, width = 400, height = 400, relief = tk.SUNKEN)
        self.frame2 = ttk.Frame(self.notebk, width = 400, height = 400, relief = tk.SUNKEN)
        self.frame3 = ttk.Frame(self.notebk, width = 400, height = 400, relief = tk.SUNKEN)
        self.frame4 = ttk.Frame(self.notebk, width = 400, height = 400, relief = tk.SUNKEN)
        self.frame5 = ttk.Frame(self.notebk, width = 400, height = 400, relief = tk.SUNKEN)
        
        self.notebk.add(self.frame1, text = 'General')
        self.notebk.add(self.frame2, text = 'Subject Info')
        self.notebk.add(self.frame3, text = 'Jacobean Constants')
        self.notebk.add(self.frame4, text = 'Maxes')
        self.notebk.add(self.frame5, text = 'Automation')
        self.notebk.pack(expand = 1, fill="both")

        # General Pane
        self.trialTog = ttk.Button(self.frame1, text='Practice', command=self.toggle)
        self.trialTog.grid(column=1, row=0, padx=5, pady=5)

        self.subNum = tk.Label(self.frame1, text="Subject Number")
        self.subNum.grid(column=0, row=1, padx=5, pady=5)
        self.subNumEnt = tk.Entry(self.frame1)
        self.subNumEnt.grid(column=1, row=1, padx=5, pady=5)

        self.testArmLab = tk.Label(self.frame1, text="Testing Arm")
        self.testArmLab.grid(column=0, row=2, padx=5, pady=5)
        self.testArmDef = tk.StringVar(self.master)
        self.testArmDef.set("Left/Right")
        self.ArmTypes = ['Left','Right']
        self.testArmType = tk.OptionMenu(self.frame1, self.testArmDef, *self.ArmTypes)
        self.testArmType.grid(column=1, row=2, padx=5, pady=5)
        
        self.start = ttk.Button(self.frame1, text='Start Trial')
        self.start.grid(column=0, row=3, padx=5, pady=5)
        self.pause = ttk.Button(self.frame1, text='Pause Trial')
        self.pause.grid(column=1, row=3, padx=5, pady=5)
        self.end = ttk.Button(self.frame1, text='End Trial')
        self.end.grid(column=2, row=3, padx=5, pady=5)

        self.trialDef = tk.StringVar(self.master)
        self.trialTypes = ['option1','option2']
        self.trialDef.set('Select a Trial Type')
        self.trialType = tk.OptionMenu(self.frame1, self.trialDef, *self.trialTypes)
        self.trialType.grid(column=0, row=4, padx=5, pady=5)

        self.save = ttk.Button(self.frame1, text='Save')
        self.save.grid(column=0, row=5, padx=5, pady=5)
        self.erase = ttk.Button(self.frame1, text='Erase')
        self.erase.grid(column=1, row=5, padx=5, pady=5)

        self.quit = ttk.Button(self.frame1, text='Exit', command=self.close)
        self.quit.grid(column=3, row=5, padx=5, pady=5)
        
        # Subject Info Pane
        self.subjectInfo = ['Age', 'Gender', 'Subject Type', 'Years since stroke',
                            'rNSA', 'FMA', 'Dominant Arm', 'Recovery Paretic Arm']

        for i in range(len(self.subjectInfo)):
            tk.Label(self.frame2, text=self.subjectInfo[i]).grid(row=i, column=0, padx=5, pady=5)
            if self.subjectInfo[i] not in ['Gender', 'Dominant Arm', 'Recovery Paretic Arm']:
                tk.Entry(self.frame2).grid(row=i, column=1, padx=5, pady=5)

        self.genDef = tk.StringVar(self.master)
        self.genDef.set('Select a gender')
        self.genders = ["Male", "Female", "Other"]
        self.genEnt = tk.OptionMenu(self.frame2, self.genDef, *self.genders)
        self.genEnt.grid(row=1, column=1, padx=5, pady=5)

        self.domArmDef = tk.StringVar(self.master)
        self.domArmDef.set("Left/Right")
        self.domArmEnt = tk.OptionMenu(self.frame2, self.domArmDef, *self.ArmTypes)
        self.domArmEnt.grid(row=6, column=1, padx=5, pady=5)

        self.recArmDef = tk.StringVar(self.master)
        self.recArmDef.set("Left/Right")
        self.recArmEnt = tk.OptionMenu(self.frame2, self.recArmDef, *self.ArmTypes)
        self.recArmEnt.grid(row=7, column=1, padx=5, pady=5)

        self.subjectInfo = ['Age', 'Subject Type', 'Years since stroke','rNSA', 'FMA',
                            'Dominant Arm', 'Recovery Paretic Arm', 'Gender']
                
        self.subjectSub = ttk.Button(self.frame2, text="Submit", command=self.subjectSubmit)
        self.subjectSub.grid(row=len(self.subjectInfo),column=0, padx=5, pady=5)

        # Jacobean Constants Pane
        self.jacobInfo = ["Shoulder Abduction Angle","Elbow Flexion Angle","Arm Length",
                          "Z-offset"]

        for i in range(len(self.jacobInfo)):
            tk.Label(self.frame3, text=self.jacobInfo[i]).grid(row=i, column=0, padx=5, pady=5)
            tk.Entry(self.frame3).grid(row=i, column=1)
        
        self.jacobSub = ttk.Button(self.frame3, text="Submit", command=self.jacobSubmit)
        self.jacobSub.grid(row=len(self.jacobInfo),column=0, padx=5, pady=5)

        # Maxes Info Pane
        self.maxInfo = ["Shoulder Abduction Angle","Max Inv. Elbow Torque","Max Elbow Flexion",
                        "Synergy TFlex Involuntary","Max involuntary extension","Max Elbow Extension",
                        "Synergy Text Involuntary"]
        for i in range(len(self.maxInfo)):
            tk.Label(self.frame4, text=self.maxInfo[i]).grid(row=i, column=0, padx=5, pady=5)
            tk.Entry(self.frame4).grid(row=i, column=1)

        self.maxSub = ttk.Button(self.frame4, text="Submit", command=self.maxSubmit)
        self.maxSub.grid(row=len(self.maxInfo),column=0, padx=5, pady=5)

        # Automation Pane
        self.autoText = tk.Label(self.frame5, text="Automation")
        self.autoText.grid(row=0, column=1, padx=5, pady=5)

        self.autoVal = tk.IntVar()
        self.autoVal.set(1)
        
        self.autoOff = tk.Radiobutton(self.frame5, text="Off", variable=self.autoVal, value=1)
        self.autoOff.grid(row=1, column=0, padx=5, pady=5)

        self.autoOn = tk.Radiobutton(self.frame5, text="On", variable=self.autoVal, value=2)
        self.autoOn.grid(row=1, column=2, padx=5, pady=5)

        self.trialNum = tk.Label(self.frame5, text="Set Trial Number")
        self.trialNum.grid(row=2,column=0, padx=5, pady=5)
        self.trialNumEnt = tk.Entry(self.frame5)
        self.trialNumEnt.grid(row=2, column=1, padx=5, pady=5)

        self.trialNumSave = ttk.Button(self.frame5, text="Save")
        self.trialNumSave.grid(row=2,column=2, padx=5, pady=5)
        
        self.pause = ttk.Button(self.frame5, text="Pause")
        self.pause.grid(row=3, column=0, padx=5, pady=5)


    # Helper functions
    def close(self):
        self.master.destroy()
    
    def toggle(self):
        if self.trialTog['text'] == 'Practice':
            self.trialTog.configure(text='Testing')
        else:
            self.trialTog.configure(text='Practice')

    def subjectSubmit(self):
        self.subjectSaved = []
        for child in self.frame2.winfo_children():
            if child.winfo_class() == 'Entry':
                self.subjectSaved.append(child.get())
        self.subjectSaved.append(self.domArmDef.get())
        self.subjectSaved.append(self.recArmDef.get())
        self.subjectSaved.append(self.genDef.get())
        
        self.subjectFinal = dict(zip(self.subjectInfo,self.subjectSaved))
        self.data_queue.put(self.subjectFinal)
        #print(self.subjectFinal)

    def jacobSubmit(self):
        self.jacobSaved = []
        for child in self.frame3.winfo_children():
            if child.winfo_class() == 'Entry':
                self.jacobSaved.append(child.get())
        
        self.jacobFinal = dict(zip(self.jacobInfo,self.jacobSaved))
        print(self.jacobFinal)

    def maxSubmit(self):
        self.maxSaved = []
        for child in self.frame4.winfo_children():
            if child.winfo_class() == 'Entry':
                self.maxSaved.append(child.get())
        
        self.maxFinal = dict(zip(self.maxInfo,self.maxSaved))
        print(self.maxFinal)

def launchGUI(conn, in_conn):
    # run the GUI
    root = tk.Tk()
    gui = GUI(root, conn, in_conn)
    #gui.data_queue.put([42, None, 'hello'])
    tk.mainloop()
    exit()
    

if __name__=='__main__':
    pass
