# whm
What is the point of this?

I wanted to do data analysis of the movies covered by the podcast 'We Hate Movies.' Specifically, I wanted to look at what were the most quintessential We Hate Movies movies were. To do this I took the basic idea of Google's page rank. Instead of important links making a page more important, and therefore its outgoing links more important I am using Actors, Directors and Authors if the movie is based on a book.

The output of this can give a basic rank of all of the movies or it can give the rank of the people involved in created the movie.

A quick overview of how the algorithm works. For the time I'm just going to cover the main.py file but in the future will update this to discuss the various util files that gathered and cleaned the data.

The algorithm:
	1. First round only. Give a person a point for each movie they are associated with *  
	2. Add all points for each person associated with a movie to be a movie gross score  
	3. Calculate the average gross movie score and standard deviation gross movie score  
	4. Assign the movie the z-score based on its gross movie score, average gross movie score and standard deviation gross movie score  
	5. Check the difference between the current z-score and the previous rounds' z-score to see if it is within a given percentage   
	6. If the percentage is within a certain bound for all movies break  
	7. If the percentage is not within that bound give all people associated with the movie the z-score as a point, just like in step 1  
* = Points are based on the number of people associated with the movie. Without this, movies with small casts were penalized and could never rise up.

The output for the time is a simple print function and in the future I want to write this to files or move it to a SQL server so I can query the data.
See out/all_scores.txt and out/movie_score_only.txt for most recent results.

Basic analysis:
Looking at the movie_score_only file we can see that the lowest ranked movie is Casablanca (as of the time of this writting). What this means is that the people who made this movie are the least connected with the people who made the other movies covered by We Hate Movies. Meanwhile, Armageddon is the top ranked movie. Looking at the all_scores file we can see not only the score of the movie, but we can also see the score of all the people associated with the movie. Just as a reminder, a movie's score is the z-score and the actor's score is the sum of all of the z-scores from each movie they're in.
Getting back to Armageddon, we can see that Michael Bay has a high score of 41.9 and other actors have higher scores. This means that they have all been a part of other movies that have high scores.

What is interesting is we can search for Sean Connery who comes up 12 times in this file, but only has a score of -0.04. A shockingly low number for someone who shows up in so many movies. He appears in movies with other people who are not associated with any other movie in this list which drives his score, and interestingly, any movie he is associated with is driven down.

Future plans:
	* This could be used as a heuristic for a longest movie marathon chain
	* I would like to get this to a website to make it easy for anyone to query the data

Data sourced from api.themoviedb.org/3


