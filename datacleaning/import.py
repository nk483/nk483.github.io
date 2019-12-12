#The initial csv to db import had every data type as TEXT even the numbers, so I created a new database called stats with the correct
#data types for each column, and imported my csv file line by line into stats here:
from cs50 import SQL
from csv import DictReader
db = SQL("sqlite:///basketball.db")
with open('Seasons_Stats.csv', newline='') as csvfile:
    reader = DictReader(csvfile)
    for row in reader:
        db.execute("INSERT INTO stats VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row[''], row['Year'],
        row['Player'], row['Pos'], row['Age'],row['Tm'], row['G'], row['GS'], row['MP'], row['PER'], row['TS%'], row['OWS'], row['DWS'], row['WS'],
        row['WS/48'], row['OBPM'], row['DBPM'], row['BPM'], row['VORP'], row['FG'], row['FGA'], row['FG%'], row['3P'], row['3PA'], row['3P%'],
        row['2P'], row['2PA'], row['2P%'], row['eFG%'], row['FT'], row['FTA'], row['FT%'], row['ORB'], row['DRB'], row['TRB'], row['AST'],
        row['STL'], row['BLK'], row['TOV'], row['PF'], row['PTS'])


