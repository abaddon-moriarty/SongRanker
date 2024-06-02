import string

max_chars = 15
new_song_list = []



for song in ["Fortnight (featuring Post Malone)", "The Tortured Poets Department", "My Boy Only Breaks His Favorite Toys", "Down Bad", "So Long, London", "But Daddy I Love Him", "Fresh Out The Slammer", "Florida!!! (featuring Florence + the Machine)", "Guilty As Sin?", "Who's Afraid Of Little Old Me?", "I Can Fix Him (No Really I Can)", "loml", "I Can Do It With A Broken Heart", "The Smallest Man Who Ever Lived", "The Alchemy", "Clara Bow"]:    
    min_diff = int(100)
    closest_index = -1
    if len(song) > max_chars:
        # print(f"the song: {song} is too long")
        # loops over each char in the song
        if " " in song:
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
            print(f"{song[:closest_index].strip()}\n{(song[closest_index:]).strip()}\n\n")
