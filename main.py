import random
import tkinter as tk
from tkinter import ttk

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
    
def on_click(songList, i, j, ratingMatrix, choice):

    # Updates the matrix based on user choice
    if choice == 1:
        ratingMatrix[i][j] = 1.0
    elif choice == 2:
        ratingMatrix[i][j] = 2.0
    else:
        ratingMatrix[i][j] = 0.5

    # Displays or not the ranking based on display option
    if check_var.get() == True: # This will only update the ranking if display option is selected
        calculate_ranking()
        update_size()
    else: # This removes the ranking if the hide option is selected in the middle of the selections otherwise last rank remains on screen.
        output_label['text'] = "" 
        update_size()
    next_pair()
    
def next_pair():
    global current_pair, check_var

    if current_pair < len(order):
        i, j = order[current_pair]
        button1.config(text=songList[i], command=lambda: on_click(songList, i, j, ratingMatrix, 1))
        button2.config(text=songList[j], command=lambda: on_click(songList, i, j, ratingMatrix, 2))
        button3.config(command=lambda: on_click(songList, i, j, ratingMatrix, 3))
        pg_title.configure(text = f"{current_pair}/{len(order)}")
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
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")
    
def start():
    global current_pair, order, ratingMatrix, songList

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
    update_size()
    
    # Opens the list of songs, right now path hardcoded but later will add option to import txt file.
    with open(file, encoding="utf-8", mode="r") as f:
        songList = f.readlines()
        for i, song in enumerate(songList):
            songList[i] = song.replace("\n", "")
        order = defineSongOrder(songList)

        ratingMatrix = [[-1.0] * len(songList) for _ in range(len(songList))] # creates a matrix of shape[NumSongs][NumSongs] to store the rating.

        current_pair = 0
        progress_bar.configure(maximum = len(order))

        next_pair()


##########################################
###### GUI window & basic variables ######
##########################################

global check_var


root = tk.Tk()
root.title("the TTDP sorting hat")
root.geometry("500x150") # sets size of the window

# title
label = tk.Label(root, text="Come and sort your favourite TTDP songs!", font=("Georgia", 12, "bold"))
label.pack(padx=75, pady=20)

# Input List of Songs: Start by obtaining a list of songs from the user or from a file.
file = "C:/Users/munau/OneDrive/Desktop/Machine_Learning/SongRanker/ttpd.txt"

######################
###### THE MENU ######
######################
menu = tk.Menu(root)

# sub_menu
file_menu = tk.Menu(menu, tearoff=False)
check_var = tk.BooleanVar()

# display options
file_menu.add_radiobutton(label="View Ranking Evolution", value=1, variable = check_var)
file_menu.add_radiobutton(label="Leave Ranking as Surprise", value=0, variable = check_var)
menu.add_cascade(label="Ranking", menu=file_menu)  
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
