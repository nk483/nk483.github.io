    My project started with a .csv file called "Season_Stats.csv" that has near 25,000 rows and a bit more than a million cells.
I downloaded it off of Kaggle and it contained NBA season-by-season statistical data from
1950-2017. I used import local files to get the "Season_Stats.csv" file the datacleaning folder of project. I created a SQL database
called basketball and created a table in it called stats. It was possible to directly import the "Season_Stats.csv" as a table,
but when I tried that all of the column data types where TEXT whereas I wanted integer and floats for a lot of them, so instead
I created stats which had the data type I wanted for all columns and executed import.py. What import.py did was it went row by row
in the .csv file and inputted the cell values in stats under the corresponding column. After this I created a new table called
aggregate_stats, because in the end I did not want season-by-season player data but rather player statistics aggregated over
their entire careers. So I then executed aggregation.py which summed the columns of stats (averaged if the column was a percentage)
where the rows had the same player and then inputted the value into aggregate_stats. This gave me aggregated stats but a bunch
of duplicate entries as for every season a player played there was an entry containing his aggregated stats. So then I executed
removeDuplicates.py to remove all duplicate entries. And I executed post_aggregation.py to recompute some percentages and advanced
stats, I go into more detail in the comments for both removeDuplicates.py and post_aggregation.py.

    So, now I have a dataset which has exactly what I want, NBA career player data. Basically what I need code that will take
user input and use it run queries on basketball.db, the results of which will then be displayed to the user. The python, jinja,
html, css, javascript combination of the finance pset would be very well suited for this I thought so I went with that.
I went over to my finance pset and copied the css files, found a basketball favicon to use, and copied the initial lines of
finance's application.py that set up flask. My application.py has 4 app.route lines total, one of them is the homepage "/",
and two of them are error messages. The fourth actually represents any possible query a user can make. When I started off,
I was making a different python function and html template if user selected assists than if they selected points, and so on,
it was getting to be a lot of lines of redundant code but I did not know how to combine in into one function and one app route.
However, I then realized that if a user inputted points I could save that as an html/javascript variable which I then pass to
app.route as a variable. Now that app.route didn't have to be a fixed string I cutdown all these different functions into one,
that simply takes in the statistic as input. I had the same realization for my html templates. So the python function "page" and
then html template "statTemplate" can represent any query a user makes.

    Another design decision I had to make had to do with displaying images of players. I thought in addition to their name and
statistic it would be a nice feature to show a player's image. Now there are 4,000 unique players in my database so manually
getting pictures for each one of them would have been infeasible. Instead, I looked around and was able to find a Google Images
API called serpAPI. I coded a python function called pictureUrl that takes in a name as input and outputs the first image that
results when name + basketball is concatenated and type into google images. This solved the automation problem, but introduced
a new one: time. Each api call took on average 7 seconds making pages that were previously taking a fraction of a second to load
comparatively very slow. I realized that if I had these urls stored locally, it would be much faster than having the api look
them up each time, instead I could just use a database query. So I created a new row in aggregate_stats and populated it with
the pictureUrl output of the name of each player. This sped things up dramatically

