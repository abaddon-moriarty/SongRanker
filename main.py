import os
import string  
import random
import filecmp

import tkinter as tk

from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfile, askopenfilename

### TO DO: * right now the window size gets re-calculated at each choice, there must be a better way: calculating only when display option is changed and on start. check "update_size()"


def defineSongOrder(songList):
    # I am going to generate a list of all possible combinations, then randomise them, because I don't want to compare all A & x then all B and x, but rather 2 random songs each time.
    order = []
    for i in range(0, len(songList)):
        for j in range(0, len(songList)):
            if (i != j) and not [j,i] in order:
                order.append([i,j])
    
    order = sorted(order, key=lambda x: random.random()) # Randomise the song order 
    # random.shuffle(order)

    return order
    
def on_click(i, j, choice, max_height, max_width, current_pair, ranking_status, order, short_song_list, check_var):
    
    # Updates the matrix based on user choice
    if choice == 1:
        ratingMatrix[i][j] = 1.0
    elif choice == 2:
        ratingMatrix[i][j] = 2.0
    else:
        ratingMatrix[i][j] = 0.5
    next_pair(max_height, max_width, current_pair, ranking_status, order, short_song_list)
    calculate_ranking(check_var, ranking_status)

def display_toggle(check_var, ranking_status):
    # Displays or not the ranking based on display option
    if check_var.get() == True: # This will only update the ranking if display option is selected
        calculate_ranking(check_var, ranking_status)
        update_size()
    else: # This removes the ranking if the hide option is selected in the middle of the selections otherwise last rank remains on screen.
        remove_height = output_label.winfo_height()
        output_label.pack_forget()
        update_size()
    
def next_pair(max_height, max_width, current_pair, ranking_status, order, short_song_list):

    if current_pair < len(order):
        i, j = order[current_pair]
        button1.configure(text=short_song_list[i], 
                          command=lambda: on_click(i, j, 1, max_height, max_width, current_pair, ranking_status, order, short_song_list, check_var)) #, width = max_width)
        button2.configure(text=short_song_list[j], 
                          command=lambda: on_click(i, j, 2, max_height, max_width, current_pair, ranking_status, order, short_song_list, check_var)) #, width = max_width)
        button3.configure(command=lambda: on_click(i, j, 3, max_height, max_width, current_pair, ranking_status, order, short_song_list, check_var)) #, width = max_width)
        
        pg_title.configure(text = f"{current_pair}/{len(order)-1}")
        progress_bar['value'] = current_pair
        current_pair += 1
        
def calculate_ranking():
    scores = [0] * len(songList)
    for l in range(len(songList)):
        for m in range(len(songList)):
            if ratingMatrix[l][m] == 1.0: 
                scores[l] += 1
            if ratingMatrix[l][m] == 2.0:  
                scores[m] += 1
            if ratingMatrix[l][m] == 0.5:
                scores[l] += 0.5
                scores[m] += 0.5

    # Create a list of tuples (song, score) for ranking
    song_scores = [(song, score) for song, score in zip(songList, scores)]

    # Sort the list based on scores to get the ranking
    ranking = sorted(song_scores, key=lambda x: x[1], reverse=True)

    #output
    output_label['text'] = "\n".join([f"{i+1}. {song}: {score} points" for i, (song, score) in enumerate(ranking)])
    output_label.pack(pady=10)

def update_size():
    global remove_height

    root.update_idletasks()

    if remove_height:
        root.geometry(f"{root.winfo_reqwidth()}x{(root.winfo_reqheight() - remove_height)}")
    else:
        root.geometry(f"{root.winfo_reqwidth()}x{(root.winfo_reqheight())}")

def start(tracklist_dir):

    global songList, ratingMatrix

    start_button.pack_forget()
    
    # displaying the battle field
    button1.pack(padx=5, side='left')
    button2.pack(padx=5, side='left')
    button3.pack(pady=5)
    battle_frame.pack()
    input_frame.pack()
    output_label.pack()
    pg_frame.pack()
    progress_bar.pack(pady=5)
    pg_title.pack(pady=5)
    result_frame.pack()

    remove_height = 0
    update_size()
    

    # If no tracklist has been imported it will default to the ttpd tracklist
    if not tracklist_dir:
        tracklist_dir = f"{os.path.dirname(os.path.realpath(__file__))}\\test.txt"

    # this opens the source tracklist
    with open(tracklist_dir, encoding="utf-8", mode="r") as f:
        songList = f.readlines()
        for i, song in enumerate(songList):
            songList[i] = song.replace("\n", "")
        order = defineSongOrder(songList)

        ratingMatrix = [[-1.0] * len(songList) for _ in range(len(songList))] # creates a matrix of shape[NumSongs][NumSongs] to store the rating.

        current_pair = 0
        progress_bar.configure(maximum = len(order))

        next_pair()

def export_songs(ranking_status):
    files = [('Text Document', '*.txt'),
             ('All Files', '*.*')] 

    file = asksaveasfile(filetypes = files, 
                         defaultextension = files[0],
                         title="Save File",
                         mode="w") 
    if file is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    
    # if the ranking it displayed it can directly access the output label
    # however if it's hidden it returns empty for some reason, so I recalculate save and remove.
    if output_label['text']:
        file.write(output_label['text'])
    else:
        calculate_ranking(check_var, ranking_status)
        file.write(output_label['text'])
        output_label.grid_forget()        

def import_songs(ranking_status, tracklist_dir):
    
    filetypes = [('text files', '*.txt'),
                ('All files', '*.*')]
    

    new_tracklist = askopenfilename(filetypes=filetypes, defaultextension=".txt")
    if new_tracklist is None:
        return
    # checks if the file the user is trying to open is already the one they're ranking.
    if filecmp.cmp(new_tracklist, tracklist_dir):
        messagebox.showinfo(title="No need", message='You are currently ranking this tracklist')
    else:
        # if there is already an on-going Ranking, pop-up window to ask if the user wants to start a new one.
        # if yes: starts over with the chosen txt file, else: continues
        if ratingMatrix:
            answer = messagebox.askquestion('Are you sure?', 'Do you want to stop the current ranking?')
            if answer == "yes":
                start()
                update_size()
            else:
                return



##########################################
###### GUI window & basic variables ######
##########################################

root = tk.Tk()
root.title("the TTDP sorting hat")
root.geometry("500x150") # sets size of the window

# title
label = tk.Label(root, text="Come and sort your favourite TTDP songs!", font=("Georgia", 12, "bold"))
label.pack(padx=75, pady=20)

tracklist_dir = ""

######################
###### THE MENU ######
######################
menu = tk.Menu(root)

# sub_menu
file_menu = tk.Menu(menu, tearoff=False)
display_option = tk.Menu(menu, tearoff=False)
check_var = tk.BooleanVar()

file_menu.add_cascade(label = "Export results", command=lambda: import_songs(ranking_status, tracklist_dir))
file_menu.add_cascade(label = "Import tracklist", command=lambda: import_songs(ranking_status, tracklist_dir))

menu.add_cascade(label="File", menu=file_menu)  

# display options
display_option.add_radiobutton(label="View Ranking Evolution", value=1, variable = check_var, 
                               command=lambda : display_toggle(check_var, ranking_status))
display_option.add_radiobutton(label="Leave Ranking as Surprise", value=0, variable = check_var, 
                               command=lambda : display_toggle(check_var, ranking_status))
menu.add_cascade(label="Ranking Display", menu=display_option)
root.configure(menu=menu)


########################
###### THE BUTTONS #####
########################

# Configure style of buttons
style = ttk.Style()
style.configure("elder.TButton", font=('Georgia', 10))

# Battle field
battle_frame = ttk.Frame(root)
input_frame = ttk.Frame(root)
pg_frame = ttk.Frame(root)
result_frame = ttk.Frame(root)

button1 = ttk.Button(battle_frame, style="elder.TButton")
button2 = ttk.Button(battle_frame, style="elder.TButton")
button3 = ttk.Button(input_frame, text="I can't choose", style="elder.TButton")
progress_bar = ttk.Progressbar(pg_frame, orient="horizontal", length = 300, mode='determinate')
pg_title = ttk.Label(pg_frame)
output_label = ttk.Label(result_frame, font=("Georgia", 11))

# This is the only button that will be displayed from the start, on click it will disapear and reveal the rest of the battle field.
start_button = ttk.Button(root, text="Start Here", command=start, style="elder.TButton")
start_button.pack()


# run window
root.mainloop()