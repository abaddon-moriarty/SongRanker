import tkinter as tk
from tkinter import ttk

########### FIRST ROUND
# def exercice1_command():
#    entry_text = entry.get() # retrieves content of text
#    #updating label
   
#    label['text'] = entry_text
#    entry['state'] = 'disabled'

#    exercice1button2.pack()


# def exercice1_go_back():
#     label['text'] = "Some text again"
#     entry['state'] = 'normal'
 
# def exercice2_command():
    # print("hello")


# entry = tk.Entry(input_frame)
# entry.pack()

# exercice1button = ttk.Button(root, text="Some text", command=exercice1_command)
# exercice1button.pack()
# exercice1button2 = ttk.Button(root, text="Go back", command=exercice1_go_back)
# exercice2button = ttk.Button(battle_frame, text="my label", command=exercice2_command)


######################

# window
root = tk.Tk("")
root.title('Tkinter Variables')
root.geometry("500x250") # sets size of the window

# tkinter variables
string_var = tk.StringVar() #tk.DoubleVar  #tk.BooleanVar()   #tk.IntVar()    


#widgets

label = ttk.Label(root, text = 'label', textvariable=string_var)
label.pack()

entry = ttk.Entry(root, textvariable=string_var)
entry.pack()


# run
root.mainloop()