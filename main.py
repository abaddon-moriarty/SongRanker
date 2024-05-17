import random
import time
import tkinter as tk
from tkinter import ttk


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
    
def button_func(songList, i, j, ratingMatrix, choice):
    # print("A button was pressed")
    if choice == 1:
        ratingMatrix[i][j] = 1.0
    elif choice == 2:
        ratingMatrix[i][j] = 2.0
    else:
        ratingMatrix[i][j] = 0.5
    #update the button with next pair of songs
    next_pair()
    
def next_pair():
    global current_pair
    if current_pair < len(order):
        i, j = order[current_pair]
        button1.config(text=songList[i], command=lambda: button_func(songList, i, j, ratingMatrix, 1))
        button2.config(text=songList[j], command=lambda: button_func(songList, i, j, ratingMatrix, 2))
        button3.config(command=lambda: button_func(songList, i, j, ratingMatrix, 3))
        pg_title.configure(text = f"{current_pair}/{len(order)}")
        current_pair += 1
        progress_bar['value'] += 1

    else:
        calculate_ranking()
    

def calculate_ranking():
    scores = [0] * len(songList)
    for l in range(len(songList)):
        for m in range(len(songList)):
            if ratingMatrix[l][m] == 1: 
                scores[l] += 1
            if ratingMatrix[l][m] == 2:  
                scores[m] += 1
            if ratingMatrix[l][m] == 0.5:
                scores[l] += 0.5
                scores[m] += 0.5

        # Create a list of tuples (song, score) for ranking
        song_scores = [(song, score) for song, score in zip(songList, scores)]

        # Sort the list based on scores to get the ranking
        ranking = sorted(song_scores, key=lambda x: x[1], reverse=True)

        # Print the ranking
        for i, (song, score) in enumerate(ranking, start=1):
            print(f"{i}. {song}: {score} points")
    
    #output
    output_label['text'] = "\n".join([f"{i+1}. {song}: {score} points" for i, (song, score) in enumerate(ranking)])
    output_label.pack(padx=10)

def start():
    start_button.pack_forget()

    button1.pack(padx=5, side='left')
    button2.pack(padx=5, side='left')
    button3.pack(pady=5)
    battle_frame.pack()
    input_frame.pack()
    pg_frame.pack()
    progress_bar.pack(padx=5)
    pg_title.pack()



    # Pairwise Comparison: Implement a pairwise comparison mechanism where the user is presented with pairs of songs and asked to choose their preferred song from each pair. This process continues until all pairs have been compared.
    # To ensure that each song is compared with every other song exactly once, you can use a round-robin tournament-style approach.
    # Start by randomly selecting a song to be compared against every other song in the list.
    # I want to randomly select songs to compare. Which is not the same as randomising the list then looping through each one.
    global current_pair, order, ratingMatrix, songList
    with open(file, encoding="utf-8", mode="r") as f:
        songList = f.readlines()
        for i, song in enumerate(songList):
            songList[i] = song.replace("\n", "")

        order = defineSongOrder(songList)


        ratingMatrix = [[-1.0] * len(songList) for _ in range(len(songList))] # creates a matrix of shape[NumSongs][NumSongs] to store the rating.

        global current_pair
        current_pair = 0
        progress_bar.configure(maximum = len(order))

        next_pair()



# GUI window
root = tk.Tk()

root.title("the TTDP sorting hat")
root.geometry("500x250") # sets size of the window

# title
label = tk.Label(root, text="Come and sort your favourite TTDP songs!", font=("Georgia", 12, "bold"))
label.pack(padx=20, pady=20)


# Input List of Songs: Start by obtaining a list of songs from the user or from a file.
file = "C:/Users/munau/OneDrive/Desktop/Machine_Learning/SongRanker/ttpd.txt"

# Battle field
battle_frame = ttk.Frame(root)
input_frame = ttk.Frame(root)
pg_frame = ttk.Frame(root)


start_button = ttk.Button(root, text="Start Here", command=start)
start_button.pack()


button1 = ttk.Button(battle_frame) #battle_frame, font=('Georgia', 10), height=1, width=15, command=choose1)
button2 = ttk.Button(battle_frame) #battle_frame, font=('Georgia', 10), height=1, width=15, command=choose2)
button3 = ttk.Button(input_frame, text="neither") #input_frame, text="I cannot choose", font=('Georgia', 10), height=1, width=15, command=neither)

progress_bar = ttk.Progressbar(pg_frame, orient="horizontal", length = 300, mode='determinate')
pg_title = ttk.Label(pg_frame)

output_label = ttk.Label(root, font=("Georgia", 12))


# run window
root.mainloop()
