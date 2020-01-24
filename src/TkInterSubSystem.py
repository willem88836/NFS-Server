import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Scrollbar


root = tk.Tk() 

root.title("Wizard")
root.resizable(False, False)

#label
a_label = ttk.Label(root, text="Enter a name:")
a_label.grid(column=0, row=0)
print(a_label)

def click_me():
    action.configure(text="I have been clicked")
    a_label.configure(foreground="red")
    a_label.configure(text="Hi, %s %s!" % (name.get(), number.get()))

#inputfield
name = tk.StringVar()
name_entered = ttk.Entry(root, width=12, textvariable=name)
name_entered.grid(column=0, row=1)

#button
action = ttk.Button(root, text="click me", command=click_me)
action.grid(column=1, row=1)
action.configure(state='enabled')


ttk.Label(root, text="Choose a number:").grid(column=0, row=2)
#dropdown
number = tk.StringVar()
number_chosen = ttk.Combobox(root, width = 12, textvariable=number, state="readonly")
number_chosen['values'] = (1, 2, 4, 8, 16, 32)
number_chosen.grid(column=1, row = 2)
number_chosen.current(3)

#checkbutton
chVar = tk.IntVar()
check1 = tk.Checkbutton(root, text="checkbutton!", variable=chVar, state="active")
check1.grid(column=0, row=4, sticky=tk.W)
check1.select()


#radiobutton
def RadCall():
    colors = ["Green", "Blue", "Gold"]
    a_label.configure(foreground=colors[rbVar.get()])


rbVar = tk.IntVar()

rad1=tk.Radiobutton(root, text="Color1", variable = rbVar, value = 0, command=RadCall)
rad1.grid(column=0, row = 5, sticky=tk.W, columnspan=3)

rad2=tk.Radiobutton(root, text="Color2", variable = rbVar, value = 1, command=RadCall)
rad2.grid(column=1, row = 5, sticky=tk.W, columnspan=3)

rad3=tk.Radiobutton(root, text="Color3", variable = rbVar, value = 2, command=RadCall)
rad3.grid(column=2, row = 5, sticky=tk.W, columnspan=3)


scroll_w = 30
scroll_h = 3
scr=scrolledtext.ScrolledText(root, width = scroll_w, height=scroll_h, wrap=tk.WORD)
scr.grid(column=0, row=6)


buttons_frame = ttk.Labelframe(root, text="labels in a frame")
buttons_frame.grid(column=0, row=7)


for i in range(5):
    ttk.Label(buttons_frame, text="Label_%s" % str(i)).grid(column=i, row=0, sticky=tk.W)



# ttk.Label(buttons_frame,text="Label1")








name_entered.focus() #sets that field to be automatically selected 
root.mainloop()
