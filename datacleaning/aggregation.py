# This file is a record of how I took the season-by-season data and aggregated it into career statistics
from cs50 import SQL
from csv import DictReader
db = SQL("sqlite:///basketball.db")
#This is a for loop that loops through all of the entries of the original dataset by id
for i in range(24692):
    #Makes sure i is a valid id, as some ids were not present
    if db.execute("SELECT COUNT(id) FROM stats WHERE id = :id", id = i)[0]['COUNT(id)'] == 0:
       continue
    year = db.execute("SELECT year FROM stats WHERE id = :id", id = i)
    player = db.execute("SELECT player FROM stats WHERE id = :id", id = i)
    playerValue = player[0]['player']
    position = db.execute("SELECT position FROM stats WHERE id = :id", id = i)
    age = db.execute("SELECT age FROM stats WHERE id = :id", id = i)
    team = db.execute("SELECT team FROM stats WHERE id = :id", id = i)
    games = db.execute("SELECT SUM(games) FROM stats WHERE player = :player", player = playerValue)
    gamesStarted = db.execute("SELECT SUM(GS) FROM stats WHERE player = :player", player = playerValue)
    minutesPlayed = db.execute("SELECT SUM(MP) FROM stats WHERE player = :player", player = playerValue)
    PER = db.execute("SELECT AVG(PER) FROM stats WHERE player = :player", player = playerValue)
    TS = db.execute("SELECT AVG('TS%') FROM stats WHERE player = :player", player = playerValue)
    OWS = db.execute("SELECT SUM(OWS) FROM stats WHERE player = :player", player = playerValue)
    DWS = db.execute("SELECT SUM(DWS) FROM stats WHERE player = :player", player = playerValue)
    WS = db.execute("SELECT SUM(WS) FROM stats WHERE player = :player", player = playerValue)
    WSper48 = db.execute("SELECT AVG(WS/48) FROM stats WHERE player = :player", player = playerValue)
    OBPM = db.execute("SELECT AVG(OBPM) FROM stats WHERE player = :player", player = playerValue)
    DBPM = db.execute("SELECT AVG(DBPM) FROM stats WHERE player = :player", player = playerValue)
    BPM = db.execute("SELECT AVG(BPM) FROM stats WHERE player = :player", player = playerValue)
    VORP = db.execute("SELECT AVG(VORP) FROM stats WHERE player = :player", player = playerValue)
    FG = db.execute("SELECT SUM(FG) FROM stats WHERE player = :player", player = playerValue)
    FGA = db.execute("SELECT SUM(FGA) FROM stats WHERE player = :player", player = playerValue)
    #Makes sure I am not dividing by zero in calculating fgPercent
    if FGA[0]['SUM(FGA)'] > 0:
        fgPercent = round(FG[0]['SUM(FG)']/FGA[0]['SUM(FGA)'],3)
    else:
        fgPercent = None
    threeP = db.execute("SELECT SUM('3P') FROM stats WHERE player = :player", player = playerValue)
    threePA = db.execute("SELECT SUM('3PA') FROM stats WHERE player = :player", player = playerValue)
    if threePA[0]["SUM('3PA')"] > 0:
        threePercent = round(threeP[0]["SUM('3P')"]/threePA[0]["SUM('3PA')"],3)
    else:
        threePercent = None
    twoP = db.execute("SELECT SUM('2P') FROM stats WHERE player = :player", player = playerValue)
    twoPA = db.execute("SELECT SUM('2PA') FROM stats WHERE player = :player", player = playerValue)
    if twoPA[0]["SUM('2PA')"] > 0:
        twoPercent = round(twoP[0]["SUM('2P')"]/twoPA[0]["SUM('2PA')"],3)
    else:
        twoPercent = None
    if FGA[0]['SUM(FGA)'] > 0:
        eFG = round((FG[0]['SUM(FG)'] + .5*threeP[0]["SUM('3P')"])/FGA[0]['SUM(FGA)'],3)
    else:
        eFG = None
    FT = db.execute("SELECT SUM(FT) FROM stats WHERE player = :player", player = playerValue)
    FTA = db.execute("SELECT SUM(FTA) FROM stats WHERE player = :player", player = playerValue)
    if FTA[0]['SUM(FTA)'] > 0:
        FTpercent = round(FT[0]['SUM(FT)']/FTA[0]['SUM(FTA)'],3)
    else:
        FTpercent = None
    ORB = db.execute("SELECT SUM(ORB) FROM stats WHERE player = :player", player = playerValue)
    DRB = db.execute("SELECT SUM(DRB) FROM stats WHERE player = :player", player = playerValue)
    TRB = db.execute("SELECT SUM(TRB) FROM stats WHERE player = :player", player = playerValue)
    assists = db.execute("SELECT SUM(assists) FROM stats WHERE player = :player", player = playerValue)
    steals = db.execute("SELECT SUM(steals) FROM stats WHERE player = :player", player = playerValue)
    blocks = db.execute("SELECT SUM(blocks) FROM stats WHERE player = :player", player = playerValue)
    turnovers = db.execute("SELECT SUM(turnovers) FROM stats WHERE player = :player", player = playerValue)
    PF = db.execute("SELECT SUM(PF) FROM stats WHERE player = :player", player = playerValue)
    points = db.execute("SELECT SUM(points) FROM stats WHERE player = :player", player = playerValue)
    #Here I insert all of the values that I have aggregated for the given id, into a new table called aggregate_stats
    db.execute("INSERT INTO aggregate_stats VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", i, year[0]['year'],
    player[0]['player'], position[0]['position'], age[0]['age'], team[0]['team'], games[0]['SUM(games)'], gamesStarted[0]['SUM(GS)'],
    minutesPlayed[0]['SUM(MP)'], round(PER[0]['AVG(PER)'],3), round(TS[0]["AVG('TS%')"],3), round(OWS[0]['SUM(OWS)'],3), round(DWS[0]['SUM(DWS)'],3), round(WS[0]['SUM(WS)'],3), round(WSper48[0]['AVG(WS/48)'],3),
    round(OBPM[0]['AVG(OBPM)'],3), round(DBPM[0]['AVG(DBPM)'],3), round(BPM[0]['AVG(BPM)'],3), round(VORP[0]['AVG(VORP)'],3), FG[0]['SUM(FG)'],FGA[0]['SUM(FGA)'],
    fgPercent, threeP[0]["SUM('3P')"], threePA[0]["SUM('3PA')"], threePercent, twoP[0]["SUM('2P')"], twoPA[0]["SUM('2PA')"], twoPercent, eFG, FT[0]['SUM(FT)'], FTA[0]['SUM(FTA)'],
    FTpercent, ORB[0]['SUM(ORB)'], DRB[0]['SUM(DRB)'], TRB[0]['SUM(TRB)'], assists[0]['SUM(assists)'], steals[0]['SUM(steals)'], blocks[0]['SUM(blocks)'],
    turnovers[0]['SUM(turnovers)'], PF[0]['SUM(PF)'], points[0]['SUM(points)'])
