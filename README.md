# SongRanker

The goal is to create a song list ranker without needing to assign explicit numerical rankings to each song. The sorting will be done by choosing the prefered song out of two.
The ranking will be made with a tournament style called Round-Robin Tournament:
In a round-robin tournament, each song competes against every other song exactly once. Each win earns a song 1 point, and each draw earns 0.5 points. After all matches are played, songs are ranked based on the total points earned.
advantage you have an accurate representation of your favourites, the disadvantage is: because each song has to go up against every other song once, it can get very very long.

# Basic app:
The first version of the app will work with the Tortured Poet Department album from Taylor Swift (as I developped this litteraly so I wouldn't have to manually rank it). 
You can choose wether you want to see the list of songs as you rank them or if you want to wait until the end.
Once you have finished, you can choose to export your ranking in a text file.


## Improuvements
- Option to import a new list of songs and rank those.
- Adding little icons in the ranking (if you choose to display it) to see which song won or lost a place.
- the best thing would be to have a music snippet for each song, to be able to hear it before choosing, but that seems hard to do. I don't really know how to integrate spotify or equivalent.
