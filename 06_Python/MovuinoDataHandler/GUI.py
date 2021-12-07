import tkinter as tk

def saveFile(text):
    print(text)

window = tk.Tk()
button = tk.Button(text="Save", command=lambda : saveFile('ok'))
button.pack()
window.mainloop()