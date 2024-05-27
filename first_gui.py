import tkinter as tk

def choose():
    print("choose")

# window
root = tk.Tk()

root.title("the TTDP sorting hat")
root.geometry("500x150") # sets size of the window

# title
label = tk.Label(root, text="Come and sort your favourite TTDP songs!", font=("Georgia", 12, "bold"))
label.pack(padx=20, pady=20)

# Battle field
input_frame = tk.Frame(root)
# entry = tk.Entry(input_frame)
button1 = tk.Button(input_frame, text="Song 1", font=('Georgia', 10), height=1, width=15, command=choose)
button2 = tk.Button(input_frame, text="Song 2", font=('Georgia', 10), height=1, width=15, command=choose)
button3 = tk.Button(input_frame, text="I cannot choose", font=('Georgia', 10), height=1, width=15, command=choose)


# entry.pack(side='left')
button1.pack(padx=5, side='left')
button2.pack(padx=5, side='left')
button3.pack(padx=5, side='left')


input_frame.pack()

#output
output_label = tk.Label(root, text="output", font=("Georgia", 12))
output_label.pack(padx=10)


# run window
root.mainloop()

