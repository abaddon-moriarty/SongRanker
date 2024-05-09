import random

def defineSongOrder(songList):
    # I am going to generate a list of all possible combinations, then randomise them, because I don't want to compare all A & x then all B and x, but rather 2 random songs each time.
    order = []
    for i in range(0, len(songList)):
        for j in range(0, len(songList)):
            if (i != j) and not [j,i] in order:
                order.append([i,j])
    
    order = sorted(order, key=lambda x: random.random()) # Randomise the song order 
    return order

# Input List of Songs: Start by obtaining a list of songs from the user or from a file.
file = "./ttdp.txt"


# Pairwise Comparison: Implement a pairwise comparison mechanism where the user is presented with pairs of songs and asked to choose their preferred song from each pair. This process continues until all pairs have been compared.
    # To ensure that each song is compared with every other song exactly once, you can use a round-robin tournament-style approach.
    # Start by randomly selecting a song to be compared against every other song in the list.
    # I want to randomly select songs to compare. Which is not the same as randomising the list then looping through each one.
with open(file, encoding="utf-8", mode="r") as f:
    songList = f.readlines()
    for i, song in enumerate(songList):
        songList[i] = song.replace("\n", "")

    order = defineSongOrder(songList)

    ratingMatrix = [[-1.0] * len(songList) for _ in range(len(songList))] # creates a matrix of shape[NumSongs][NumSongs] to store the rating.

    

    print("For all of the following songs, choose your favourite, by writting 1 for the first, 2 for the second or 3 if you cannot choose.")

    # Once a song has been compared against all others, move to the next song in the list and repeat the process until all songs have been compared.
    for battle in order:
        i, j = battle[0], battle[1]
        print(i,j)
        result = int(input(f"{songList[i]} or {songList[j]}. "))
        if result == 1 or result == 2:
            ratingMatrix[i][j] = float(result)
            print(f"{float(result)}, {ratingMatrix[i][j]}")
        if result == 3:
            ratingMatrix[i][j] = float(0.5)
            print(f"{float(result)}, {ratingMatrix[i][j]}")

    print(ratingMatrix)




# Data Structure: Decide on a suitable data structure to store the results of the pairwise comparisons. You might use a matrix, a list of tuples, or a dictionary to represent the comparisons.
    # You can use a matrix or a similar structure to store the results of the pairwise comparisons.
    # For example, if you have 5 songs, you can create a 5x5 matrix where matrix[i][j] represents the number of times song i was chosen over song j.
    # Initialize the matrix with zeros and update it based on user input during the comparison process.
        # Matrix:
            # A matrix is a two-dimensional array with rows and columns.
            # Each element in the matrix is identified by its row and column indices.
            # In the context of ranking songs, a matrix can be used to store the results of pairwise comparisons between songs.
        # Pairwise Comparisons:
            # Pairwise comparisons involve comparing each song against every other song exactly once.
            # For example, if you have 5 songs (let's label them as A, B, C, D, and E), you'll have the following pairwise comparisons:
            # A vs. B, A vs. C, A vs. D, A vs. E
            # B vs. C, B vs. D, B vs. E
            # C vs. D, C vs. E
            # D vs. E
            # Each comparison results in one song being chosen over the other.
        # Matrix Representation:
            # To store the results of pairwise comparisons, you can use a matrix where each row and column represents a song.
            # For example, in a 5x5 matrix:
            # Row 1 represents Song A
            # Row 2 represents Song B
            # Row 3 represents Song C
            # Row 4 represents Song D
            # Row 5 represents Song E
            # Each cell in the matrix represents the number of times a song was chosen over another song.
            # The cell at matrix[i][j] stores the count of times Song i was chosen over Song j.
        # Initialization:
            # Initially, you'll create a matrix filled with zeros.
            # This matrix will represent the initial state where no songs have been chosen over others.
        # Updating the Matrix:
            # During the comparison process, whenever a user chooses one song over another, you'll update the corresponding cell in the matrix.
            # For example, if the user chooses Song A over Song B, you'll increment the count in matrix[1][2] (assuming 1-based indexing).
        # Example Usage:
            # Let's say the user chooses Song A over Song B. You'll update matrix[1][2] by incrementing its value by 1.
            # If later the user chooses Song B over Song C, you'll update matrix[2][3] similarly.

# Algorithm: Develop an algorithm to generate pairs of songs for comparison. This algorithm should ensure that each song is compared with every other song exactly once.
    # Once all pairwise comparisons have been made, you can calculate a score for each song based on how many times it was chosen as the preferred option.
    # The score can be calculated by summing up the values in the row or column corresponding to each song in the comparison matrix.
    # The higher the score, the higher the rank of the song.
# User Interface: Create a user interface that presents pairs of songs to the user and allows them to select their preferred song from each pair.
# Processing User Input: Write code to process the user's selections and update the data structure accordingly.
# Ranking: Once all comparisons have been made, use the results to determine the final ranking of the songs. This might involve sorting the songs based on the number of times each song was chosen as the preferred option.
# Output: Finally, display the ranked list of songs to the user.
    # Finally, you can present the ranked list of songs to the user based on their scores.
    # You can sort the songs based on their scores to determine the final ranking.