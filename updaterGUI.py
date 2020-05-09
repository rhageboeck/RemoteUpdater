import tkinter as tk

class RemoteUpdaterInterface(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.start()

    def start(self):
        pass

root = tk.Tk(className=" ")
app = RemoteUpdaterInterface(root)


tk.mainloop()
