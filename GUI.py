import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Torque GUI")
        self.notebk = ttk.Notebook(self.master)

        
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

        self.subArmLab = tk.Label(self.frame1, text="Subject's Dominant Arm")
        self.subArmLab.grid(column=0, row=2, padx=5, pady=5)
        self.subArm = tk.StringVar(self.master)
        self.subArmTypes = ['Left','Right']
        self.subArm.set("Left/Right")
        self.subArmType = tk.OptionMenu(self.frame1, self.subArm, *self.subArmTypes)
        self.subArmType.grid(column=1, row=2, padx=5, pady=5)

        self.testArmLab = tk.Label(self.frame1, text="Testing Arm")
        self.testArmLab.grid(column=0, row=3, padx=5, pady=5)
        self.testArm = tk.StringVar(self.master)
        self.testArmTypes = ['Left','Right']
        self.testArm.set("Left/Right")
        self.testArmType = tk.OptionMenu(self.frame1, self.testArm, *self.testArmTypes)
        self.testArmType.grid(column=1, row=3, padx=5, pady=5)
        
        self.start = ttk.Button(self.frame1, text='Start Trial')
        self.start.grid(column=0, row=4, padx=5, pady=5)
        self.pause = ttk.Button(self.frame1, text='Pause Trial')
        self.pause.grid(column=1, row=4, padx=5, pady=5)
        self.end = ttk.Button(self.frame1, text='End Trial')
        self.end.grid(column=2, row=4, padx=5, pady=5)

        self.defTrial = tk.StringVar(self.master)
        self.trialTypes = ['option1','option2']
        self.defTrial.set('Select a Trial Type')
        self.trialType = tk.OptionMenu(self.frame1, self.defTrial, *self.trialTypes)
        self.trialType.grid(column=0, row=5, padx=5, pady=5)

        self.save = ttk.Button(self.frame1, text='Save')
        self.save.grid(column=0, row=6, padx=5, pady=5)
        self.erase = ttk.Button(self.frame1, text='Erase')
        self.erase.grid(column=1, row=6, padx=5, pady=5)

        self.quit = ttk.Button(self.frame1, text='Exit')
        self.quit.grid(column=3, row=6, padx=5, pady=5)
        
        # Subject Info Pane
        self.age = tk.Label(self.frame2, text="Age")
        self.age.grid(row=0,column=0, padx=5, pady=5)
        self.ageEnt = tk.Entry(self.frame2)
        self.ageEnt.grid(row=0, column=1, padx=5, pady=5)

        self.gen = tk.Label(self.frame2, text="Gender")
        self.gen.grid(row=1,column=0, padx=5, pady=5)
        self.genEnt = tk.Entry(self.frame2)
        self.genEnt.grid(row=1, column=1, padx=5, pady=5)

        self.subType = tk.Label(self.frame2, text="Subject Type")
        self.subType.grid(row=2,column=0, padx=5, pady=5)
        self.subTypeEnt = tk.Entry(self.frame2)
        self.subTypeEnt.grid(row=2, column=1, padx=5, pady=5)

        self.years = tk.Label(self.frame2, text="Years since stroke")
        self.years.grid(row=3,column=0, padx=5, pady=5)
        self.yearsEnt = tk.Entry(self.frame2)
        self.yearsEnt.grid(row=3, column=1, padx=5, pady=5)

        self.rnsa = tk.Label(self.frame2, text="rNSA")
        self.rnsa.grid(row=4,column=0, padx=5, pady=5)
        self.rnsaEnt = tk.Entry(self.frame2)
        self.rnsaEnt.grid(row=4, column=1, padx=5, pady=5)

        self.fma = tk.Label(self.frame2, text="FMA")
        self.fma.grid(row=5,column=0, padx=5, pady=5)
        self.fmaEnt = tk.Entry(self.frame2)
        self.fmaEnt.grid(row=5, column=1, padx=5, pady=5)

        self.domArm = tk.Label(self.frame2, text="Dominant arm selection")
        self.domArm.grid(row=6,column=0, padx=5, pady=5)
        self.domArmEnt = tk.Entry(self.frame2)
        self.domArmEnt.grid(row=6, column=1, padx=5, pady=5)

        self.recArm = tk.Label(self.frame2, text="Recovery Paretic Arm")
        self.recArm.grid(row=7,column=0, padx=5, pady=5)
        self.recArmEnt = tk.Entry(self.frame2)
        self.recArmEnt.grid(row=7, column=1, padx=5, pady=5)

        
        self.subjectSub = ttk.Button(self.frame2, text="Submit")
        self.subjectSub.grid(row=8,column=0, padx=5, pady=5)

        # Jacobean Constants Pane
        self.shoulder = tk.Label(self.frame3, text="Shoulder Abduction Angle")
        self.shoulder.grid(row=0,column=0, padx=5, pady=5)
        self.shoulderEnt = tk.Entry(self.frame3)
        self.shoulderEnt.grid(row=0, column=1, padx=5, pady=5)

        self.elbow = tk.Label(self.frame3, text="Elbow Flexion Angle")
        self.elbow.grid(row=1,column=0, padx=5, pady=5)
        self.elbowEnt = tk.Entry(self.frame3)
        self.elbowEnt.grid(row=1, column=1, padx=5, pady=5)

        self.armLength = tk.Label(self.frame3, text="Arm Length")
        self.armLength.grid(row=2,column=0, padx=5, pady=5)
        self.armLengthEnt = tk.Entry(self.frame3)
        self.armLengthEnt.grid(row=2, column=1, padx=5, pady=5)

        self.zoff = tk.Label(self.frame3, text="Z-offset")
        self.zoff.grid(row=3,column=0, padx=5, pady=5)
        self.zoffEnt = tk.Entry(self.frame3)
        self.zoffEnt.grid(row=3, column=1, padx=5, pady=5)

        self.jacobSub = ttk.Button(self.frame3, text="Submit")
        self.jacobSub.grid(row=4,column=0, padx=5, pady=5)

        # Maxes Info Pane
        self.maxShoulder = tk.Label(self.frame4, text="Shoulder Abduction Angle")
        self.maxShoulder.grid(row=0,column=0, padx=5, pady=5)
        self.maxShoulderEnt = tk.Entry(self.frame4)
        self.maxShoulderEnt.grid(row=0, column=1, padx=5, pady=5)

        self.maxInvElbow = tk.Label(self.frame4, text="Max Inv. Elbow Torque")
        self.maxInvElbow.grid(row=1,column=0, padx=5, pady=5)
        self.maxInvElbowEnt = tk.Entry(self.frame4)
        self.maxInvElbowEnt.grid(row=1, column=1, padx=5, pady=5)

        self.maxElbowFlex = tk.Label(self.frame4, text="Max Elbow Flexion")
        self.maxElbowFlex.grid(row=2,column=0, padx=5, pady=5)
        self.maxElbowFlexEnt = tk.Entry(self.frame4)
        self.maxElbowFlexEnt.grid(row=2, column=1, padx=5, pady=5)

        self.synTflex = tk.Label(self.frame4, text="Synergy TFlex Involuntary")
        self.synTflex.grid(row=3,column=0, padx=5, pady=5)
        self.synTflexEnt = tk.Entry(self.frame4)
        self.synTflexEnt.grid(row=3, column=1, padx=5, pady=5)

        self.maxInvExt = tk.Label(self.frame4, text="Max involuntary extension")
        self.maxInvExt.grid(row=4,column=0, padx=5, pady=5)
        self.maxInvExtEnt = tk.Entry(self.frame4)
        self.maxInvExtEnt.grid(row=4, column=1, padx=5, pady=5)

        self.maxElbowExt = tk.Label(self.frame4, text="Max Elbow Extension")
        self.maxElbowExt.grid(row=5,column=0, padx=5, pady=5)
        self.maxElbowExtEnt = tk.Entry(self.frame4)
        self.maxElbowExtEnt.grid(row=5, column=1, padx=5, pady=5)

        self.synText = tk.Label(self.frame4, text="Synergy Text Involuntary")
        self.synText.grid(row=6,column=0, padx=5, pady=5)
        self.synTextEnt = tk.Entry(self.frame4)
        self.synTextEnt.grid(row=6, column=1, padx=5, pady=5)

        self.maxSub = ttk.Button(self.frame4, text="Submit")
        self.maxSub.grid(row=7,column=0, padx=5, pady=5)

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

    def toggle(self):
        if self.trialTog['text'] == 'Practice':
            self.trialTog.configure(text='Testing')
        else:
            self.trialTog.configure(text='Practice')

def launchGUI():
    root = tk.Tk()
    GUI(root)
    tk.mainloop()
    

if __name__=='__main__':
    launchGUI()
