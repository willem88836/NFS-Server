import tkinter as tk
from tkinter import ttk


root = tk.Tk() 

root.title("asdf 1")
# root.resizable(False, False)

a_label = ttk.Label(root, text="lable A")
a_label.grid(column=0, row=0)
print(a_label)

def click_me():
    action.configure(text="I have been clicked")
    a_label.configure(foreground="red")
    a_label.configure(text="A red label")

action = ttk.Button(root, text="click me", command=click_me)
action.grid(column=1, row=0)



root.mainloop()