#!/usr/bin/python
# -*- coding: utf-8 -*

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
try:
    import tkFileDialog as tkFD
except ImportError:
    import tkinter.filedialog as tkFD
from pygnovpn import pygnovpn


class Menu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.parent = parent
        self.menuFile = tk.Menu(self)
        self.menuFile.add_command(label="Quit", command=self.parent.quit)
        self.add_cascade(label="File", menu=self.menuFile)



class Main(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.lbl = tk.Label(self, text="Please select ovpn file and output directory")
        self.lbl.pack(padx=5, pady=5, fill="x",side="top")
        self.btnOVPN = tk.Button(self, text="Choose OVPN file", command=self.parent.dialogSelectOvpn)
        self.btnOVPN.pack(padx=5,pady=5, fill="x")
        self.btnOutDir = tk.Button(self, text="Choose output directory", command=self.parent.dialogSelectOutDir)
        self.btnOutDir.pack(padx=5, pady=5, fill="x")
        self.lblComment = tk.Label(self, text="Options to comment out")
        self.lblComment.pack(padx=5, pady=5, side="top")
        self.txtCommentOut = tk.Text(self, height=6, width=30)
        self.txtCommentOut.pack(padx=5, pady=5)
        self.btnGenerate = tk.Button(self, text="Generate", command=self.parent.generate)
        self.btnGenerate.config(state="disabled")
        self.btnGenerate.pack(padx=5, pady=5, fill="x")


class PygnovpnGui(tk.Frame):
    font9 = "-family {DejaVu Sans} -size 0 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
    ovpnfile = ""
    outdir = ""

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.option_add("*Font", self.font9)

        self.menu = Menu(self)
        self.main = Main(self)

        self.parent.config(menu=self.menu)
        self.main.pack(side="left", fill="both")

    def generate(self):
        pygnovpn(self.ovpnfile, self.outdir, False, True, [i.strip() for i in self.main.txtCommentOut.get("1.0","end").splitlines()])

    def quit(self):
        self.parent.quit()

    def dialogSelectOvpn(self):
        self.ovpnfile = tkFD.askopenfilename(initialdir="/",title="Select ovpn file", filetypes = (("ovpn","*.ovpn"),("all files","*.*")))
        self.updateInfo()

    def dialogSelectOutDir(self):
        self.outdir = tkFD.askdirectory(initialdir="/",title="Select output directory")
        self.updateInfo()

    def updateInfo(self):
        if(len(self.outdir)>0)and(len(self.ovpnfile)>0):
            self.main.lbl.config(text="Files will be saved to "+self.outdir+" from "+self.ovpnfile)
            self.main.btnGenerate.config(state="normal")
        else:
            if(len(self.ovpnfile)==0):
                self.main.lbl.config(text="Please select ovpn file")
            if(len(self.outdir)==0):
                if(len(self.ovpnfile)==0):
                    self.main.lbl.config(text="Please select ovpn file and output directory")
                else:
                    self.main.lbl.config(text="Please select output directory")

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0,0)
    root.wm_title("pyGnovpn")
    PygnovpnGui(root).pack(side="top", fill="both", expand=True)
    root.mainloop()