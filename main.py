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
        result_frame.configure(height=0)
        output_label.grid_forget()
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
        
        # this will pad the buttons to match the highest number of lines so the buttons don't change size throughout the ranking.
        if "\n" not in short_song_list[i] and "\n" not in short_song_list[j]:
            button1.grid(ipady = max_height, pady=5, padx=5)
            button2.grid(ipady = max_height, pady=5, padx=5)
        else:
            button1.grid(ipady = 0, pady=5, padx=5)
            button2.grid(ipady = 0, pady=5, padx=5)
        
        for button in [button1, button2]:
            if not button.winfo_reqwidth() == max_width:
                button.grid(ipadx = ((max_width- button.winfo_reqwidth())/2))
            else:
                button.grid(ipadx = 0)
        update_size()
    else:
        ranking_status = True
        end_screen(ranking_status)
        
def calculate_ranking(check_var, ranking_status):
    global songList, ratingMatrix

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

    #this will place the ranking in the grid if the toggle is on or if the ranking is over.
    if check_var.get() == True or ranking_status == True:
        output_label['background'] = "#BA704F"
        output_label.configure(anchor = "center")
        output_label.grid(row=0, column=1, sticky="we")#, columnspan=4, sticky="ns", pady=(10, 20))
        result_frame.configure(height=result_frame.winfo_reqheight())
    update_size()

def update_size():
    root.update_idletasks()
        root.geometry(f"{root.winfo_reqwidth()}x{(root.winfo_reqheight())}")

def start(tracklist_dir):

    global songList, ratingMatrix

    start_button.grid_forget()
    mise_en_place()
    

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

        short_song_list = wrap_song_title(songList)
        
        # if any of the track titles need multiple lines, it will make all the buttons that max size, so it doesn't change at every click.
        if short_song_list:
            max_height, max_width = find_max_button_size(short_song_list)
        next_pair(max_height, max_width, current_pair, ranking_status, order, short_song_list)

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
            if ranking_status == False:
            answer = messagebox.askquestion('Are you sure?', 'Do you want to stop the current ranking?')
            if answer == "yes":
                    tracklist_dir = new_tracklist
                    restart(ranking_status, tracklist_dir)
            else:
                tracklist_dir = new_tracklist
                restart(ranking_status, tracklist_dir)
            
# makes the end_screen, calculates & resizes if display off
def end_screen(ranking_status):

    # removing useless frames
    battle_frame.grid_forget()
    undecided_frame.grid_forget()
    progress_bar_frame.grid_forget()

    restart_frame.grid(row= 1, sticky="nsew")#row=0, column=0, columnspan=3, sticky="nswe")
    end_credits.grid(column=0, row=0, columnspan=3, pady=(10,20), ipadx=((500-end_credits.winfo_reqwidth())/2), sticky="nswe" )
    end_credits.configure(anchor = "center")


    new_start.grid(row=0, column=0, sticky="e", pady=5)#, padx=(10,0), pady=(0,10))
    new_songs.grid(row=0, column=1, pady=5)#, pady=(0,10))
    close_window.grid(row=0, column=2, sticky="w", pady=5)#, padx=(0,10), pady=(0,10))

    calculate_ranking(check_var, ranking_status)

# puts all the back back to zero so we can start a new session.
def restart(ranking_status, tracklist_dir):

    restart_frame.grid_forget()
    output_label.grid_forget()
    end_credits.grid_forget()

    ranking_status = False
    
    mise_en_place()
    start(tracklist_dir)

# when using grid & bc we have different length song titles, the button size constantly updates and moves the whole grid around. 
#This finds the longest song title in the list and uses that width everytime, so there's no shiftin around.
def find_max_button_size(new_song_list):

    max_height = 0
    max_width = 0
    test_button = ttk.Button(root, style="elder.TButton")

    for song in new_song_list:
        test_button['text'] = song
        test_button.grid(row = 0, column = 0, sticky="nse", pady=5, padx=5)#, sticky="ns", padx=(10,0))

        height = test_button.winfo_reqheight()
        width = test_button.winfo_reqwidth()
        if height > max_height:
            max_height = height
        if width > max_width:
            max_width = width
    
    max_height = (max_height - button1.winfo_height())/2

    test_button.grid_forget()
    return max_height, max_width
    
# if the song title is too long, I prefer to wrap it around that to have 10m long buttons
def wrap_song_title(songList):
    max_chars = 15
    new_song_list = []
    # this will loop over the song title and find the closest space to the max char index and split it there.
    for s, song in enumerate(songList):
        min_diff = int(100)
        closest_index = -1
        if len(song) > max_chars:
            # loops over each char in the song
            if " " in song:
                #if there is a space otherwise it's hard to cut anywhear
                for i in range(len(song)):
                    # if the char is a punctation
                    if song[i] == " ":
                        # Calculate the absolute difference between the current char and the max_chars
                        diff = abs(i - max_chars)
                        # if the difference is lower than the previous one, it becomes the closest
                        if diff < min_diff:
                            min_diff = diff
                            closest_index = i
                # once we've looped through the string, we cut at the closest punction found.
                new_song_list.append(f"{song[:int(closest_index)].strip()}\n{(song[int(closest_index):]).strip()}")
            else:
                new_song_list.append(song)
        else:
            new_song_list.append(song)
    return new_song_list

def mise_en_place():
    battle_frame.grid(row=1, sticky="nswe")#row=0, column=0, columnspan=3, sticky="nswe")
    undecided_frame.grid(row=2, sticky="nswe")#row=0, column=0, columnspan=3, sticky="nswe")
    progress_bar_frame.grid(row=3, sticky="nswe")#row=1, column=0, columnspan=3, sticky="nswe")
    result_frame.grid(row=4, sticky="nswe")#row=1, column=0, columnspan=3, sticky="nswe")
    result_frame.configure(height=0)
    
      # displaying the battle field
    button1.grid(row = 0, column = 0, sticky="nse", pady=5, padx=5)#, sticky="ns", padx=(10,0))
    button2.grid(row = 0, column = 1, sticky="nsw", pady=5, padx=5)#, sticky="ns", padx=(0,10))
    button3.grid(row = 0, column = 1, sticky="ns", pady=(0,5))#, padx=5, pady=5)#, sticky="ns")
    progress_bar.grid(row = 0, column = 1, pady=5)#, columnspan=3, pady=(10,0), sticky="ns")
    pg_title.grid(row = 1, column = 1)#, ipady=(10))
    update_size()

##########################################
###### GUI window & basic variables ######
##########################################

root = tk.Tk()
root.title("the TTDP sorting hat")
root.geometry("500x90") # sets size of the window
# root.resizable(False, False)




        #Styling
########################

# Configure style of buttons
style = ttk.Style()
style.configure("elder.TButton", font=('Georgia', 10), justify = "center")
style.configure("start.TButton", font=('Georgia', 11), justify = "center")
style.configure("mainFrame.TFrame", background = "#6C3428")
style.configure("result.TFrame", background = "#BA704F")
style.configure("button.TFrame", background = "#DFA878")
style.configure("progress_bar.TFrame", background = "#CEE6F3")




# # visual frames to debug
# s = ttk.Style()
# style.configure('debug.TFrame', background='red')
# style.configure('culprit.TFrame', background='blue')
######################## 
    # Grids & Frames

main_frame = ttk.Frame(root, width = 500, height = 150, style="mainFrame.TFrame")
main_frame.columnconfigure(index=(0,1,2), weight=1)
main_frame.grid(sticky="nswe")#row=0, column=0, columnspan=3, sticky="nswe")

restart_frame = ttk.Frame(root, width = 500, height = 150, style="progress_bar.TFrame")
restart_frame.columnconfigure(index=(0,1,2), weight=1, uniform="a")

battle_frame = ttk.Frame(root, width = 500, height = 150, style="button.TFrame")
battle_frame.columnconfigure(index=(0,1), weight=1, uniform="a")

undecided_frame = ttk.Frame(root, width = 500, height = 150, style="button.TFrame")
undecided_frame.columnconfigure(index=(0,1,2), weight=1)

progress_bar_frame = ttk.Frame(root, width = 500, height = 100,style="progress_bar.TFrame")
progress_bar_frame.columnconfigure(index=(0,1,2), weight=1)

result_frame= ttk.Frame(root, width = 500, style="result.TFrame")
result_frame.columnconfigure(index=(0,1,2), weight=1, uniform="a")#, uniform="a")



# title & end credits
label = tk.Label(main_frame, text="Come and sort your favourite TTDP songs!", font=("Georgia", 12, "bold"))
end_credits = ttk.Label(main_frame, text="Congratulations, You're all done !", font=("Georgia", 12))


global songList, ratingMatrix


tracklist_dir = f"{os.path.dirname(os.path.realpath(__file__))}\\test.txt"
songList = []
ratingMatrix = []
ranking_status = False

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

# Battle field
button1 = ttk.Button(battle_frame, style="elder.TButton")
button2 = ttk.Button(battle_frame, style="elder.TButton")
button3 = ttk.Button(undecided_frame, text="I can't choose", style="elder.TButton")

progress_bar = ttk.Progressbar(progress_bar_frame, orient="horizontal", length = 300, mode='determinate')
pg_title = ttk.Label(progress_bar_frame, font=('Georgia', 9))#, style='debug.TFrame')

output_label = ttk.Label(result_frame, font=("Georgia", 11))

# This is the only button that will be displayed from the start, on click it will disapear and reveal the rest of the battle field.
start_button = ttk.Button(main_frame, text="Start Here", style="start.TButton",
                          command=lambda : start(tracklist_dir))

# Restart buttons
new_start = ttk.Button(restart_frame, text="Start Again", style="elder.TButton",
                       command=lambda: restart(ranking_status, tracklist_dir=))
new_songs = ttk.Button(restart_frame, text="Rank new songs", style="elder.TButton",
                       command=lambda: import_songs(ranking_status, tracklist_dir))
close_window = ttk.Button(restart_frame, text="Close window", style="elder.TButton",
                          command=lambda : root.destroy())
    

     
# place the widgets
# the ipadx on the label serves to block the window width at 500, otherwise it sometimes collapses to the text width
label.grid(row = 0, column = 0, columnspan=3, pady=(10,20), ipadx=((500-label.winfo_reqwidth())/2))
start_button.grid(row = 1, column=1, pady=(0,10))# sticky='ns',#, columnspan=3, sticky='nswe', padx=10) 


# run window
root.mainloop()