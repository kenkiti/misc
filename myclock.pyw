from Tkinter import *
from datetime import *

class App(Frame):
  def __init__(self, master = None):
    Frame.__init__(self, master)
    self.master.title("clock")
    self.master.attributes("-topmost",1)
    self.master.attributes("-toolwindow",1)
    self.clock = Label(self, text="00:00:00")
    self.clock.pack({'side': 'left'})
    self.pack()
    self.timer()

  def timer(self):
    self.clock.configure(text=str(datetime.now())[11:19])
    self.after(1000, self.timer)

root = Tk()
app = App()
app.mainloop()
root.destroy()

