#After making my aggregate database, there were a lot of duplicate entries as each player had an entry for each season he played, which were now all
#aggregated and identical. This is a record of my sql commands to remove the duplicates.
from cs50 import SQL
db = SQL("sqlite:///basketball.db")
for i in range(24691):
    if db.execute("SELECT COUNT(id) FROM aggregate_stats WHERE id = :id", id = i)[0]['COUNT(id)'] == 0:
        continue
    player = db.execute("SELECT player FROM aggregate_stats WHERE id = :id", id = i)[0]['player']
    #Deletes all entries of the same player with a greater id, this will leave only one entry for each player.
    db.execute("DELETE FROM aggregate_stats WHERE id > :id AND player = :player", id = i, player = player)