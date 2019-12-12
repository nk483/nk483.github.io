#After aggregating, there were a lot of points where I realized I needed to make changes to either the values in aggregate_stats or the
#structure of aggregate_stats(i.e adding a new column), this file is a record of those changes.
from cs50 import SQL
from serpapi.google_search_results import GoogleSearchResults
db = SQL("sqlite:///basketball.db")
#I realized that average stats such as Field Goal Percentage would actually not produce the career Field Goal Percentage of a player, as
#it gives all season's equal weight, whereas a player might have shot 1000 shots one season but only one shot the next season. So instead
#to compute stats like these, I summed the relevant component parts, (like Fields Goals Made and Field Goals Attempted for example) and
#divided them. The following loops show these changes for percentage stats as well as advanced stats.
for i in range(24691):
    if db.execute("SELECT COUNT(id) FROM aggregate_stats WHERE id = :id", id = i)[0]['COUNT(id)'] == 0:
      continue
    points = db.execute("SELECT Points FROM aggregate_stats WHERE id = :id", id = i)[0]['Points']
    FGA = db.execute("SELECT Field_Goals_Attempted FROM aggregate_stats WHERE id = :id", id = i)[0]['Field_Goals_Attempted']
    FTA = db.execute("SELECT Free_Throws_Attempted FROM aggregate_stats WHERE id = :id", id = i)[0]['Free_Throws_Attempted']
    TSA = FGA + .44*FTA
    if TSA == 0:
        TSP = 0.00
    else:
        TSP = round(points/ (2*TSA),3)*100
    db.execute("UPDATE aggregate_stats SET True_Shooting_Percentage = :TSP WHERE id = :id", TSP = TSP, id = i)
for i in range(24691):
    if db.execute("SELECT COUNT(id) FROM aggregate_stats WHERE id = :id", id = i)[0]['COUNT(id)'] == 0:
        continue
    player = db.execute("SELECT Player FROM aggregate_stats WHERE id = :id", id = i)[0]['Player']
    threePointers = db.execute("SELECT SUM(Three_P) FROM stats WHERE player = :player", player = player)[0]['SUM(Three_P)']
    db.execute("UPDATE aggregate_stats SET Three_Pointers_Made = :threePointers WHERE id = :id", threePointers = threePointers, id = i)
for i in range(24691):
    if db.execute("SELECT COUNT(id) FROM aggregate_stats WHERE id = :id", id = i)[0]['COUNT(id)'] == 0:
        continue
    player = db.execute("SELECT Player FROM aggregate_stats WHERE id = :id", id = i)[0]['Player']
    twoPointersAttempted = db.execute("SELECT SUM(Two_PA) FROM stats WHERE player = :player", player = player)[0]['SUM(Two_PA)']
    db.execute("UPDATE aggregate_stats SET Two_Pointers_Attempted = :twoPointersAttempted WHERE id = :id", twoPointersAttempted = twoPointersAttempted, id = i)
for i in range(24691):
    if db.execute("SELECT COUNT(id) FROM aggregate_stats WHERE id = :id", id = i)[0]['COUNT(id)'] == 0:
        continue
    player = db.execute("SELECT Player FROM aggregate_stats WHERE id = :id", id = i)[0]['Player']
    twoPointers = db.execute("SELECT SUM(Two_P) FROM stats WHERE player = :player", player = player)[0]['SUM(Two_P)']
    db.execute("UPDATE aggregate_stats SET Two_Pointers_Made = :twoPointers WHERE id = :id", twoPointers = twoPointers, id = i)
for i in range(24691):
    if db.execute("SELECT COUNT(id) FROM aggregate_stats WHERE id = :id", id = i)[0]['COUNT(id)'] == 0:
        continue
    else:
        threepm = db.execute("SELECT Three_Pointers_Made FROM aggregate_stats WHERE id = :id", id = i)[0]['Three_Pointers_Made']
        threepa = db.execute("SELECT Three_Pointers_Attempted FROM aggregate_stats WHERE id = :id", id = i)[0]['Three_Pointers_Attempted']
        if threepa == 0:
            threepercent = 0.00
        else:
            threepercent = round((threepm/threepa)*100,1)
        db.execute("UPDATE aggregate_stats SET Three_Point_Percentage = :threepercent WHERE id=:id", threepercent = threepercent, id = i)
        twopm = db.execute("SELECT Two_Pointers_Made FROM aggregate_stats WHERE id = :id", id = i)[0]['Two_Pointers_Made']
        twopa = db.execute("SELECT Two_Pointers_Attempted FROM aggregate_stats WHERE id = :id", id = i)[0]['Two_Pointers_Attempted']
        if twopa == 0:
            twopercent = 0.00
        else:
            twopercent = round((twopm/twopa)*100,1)
        db.execute("UPDATE aggregate_stats SET Two_Point_Percentage = :twopercent WHERE id=:id", twopercent = twopercent, id = i)
        ftm = db.execute("SELECT Free_Throws_Made FROM aggregate_stats WHERE id = :id", id = i)[0]['Free_Throws_Made']
        fta = db.execute("SELECT Free_Throws_Attempted FROM aggregate_stats WHERE id = :id", id = i)[0]['Free_Throws_Attempted']
        if fta == 0:
            ftpercent = 0.00
        else:
            ftpercent = round(ftm/fta*100,1)
            print(ftpercent)
        db.execute("UPDATE aggregate_stats SET Free_Throw_Percentage = :ftpercent WHERE id = :id", ftpercent = ftpercent, id = i)
for i in range(24691):
    if db.execute("SELECT COUNT(id) FROM aggregate_stats WHERE id = :id", id = i)[0]['COUNT(id)'] == 0:
        continue
    elif db.execute("SELECT Field_Goal_Percentage FROM aggregate_stats WHERE id =:id", id = i)[0]['Field_Goal_Percentage'] == None:
        db.execute("UPDATE aggregate_stats SET Field_Goal_Percentage = 0.0 WHERE id = :id", id = i)
    else:
        fgpercent = 100*db.execute("SELECT Field_Goal_Percentage FROM aggregate_stats WHERE id =:id", id = i)[0]['Field_Goal_Percentage']
        db.execute("UPDATE aggregate_stats SET Field_Goal_Percentage = :fgpercent WHERE id = :id", fgpercent = fgpercent, id = i)
# This function uses a Google Images API to, given a name as input, get an image of that person. More specifically it pulls the first
#image comes up in Google Images where you type the person's name plus the word 'basketball'.
def pictureUrl(name):
   nameKeyword = "'" + name + " basketball + '"
   params = {
   "api_key": "5953e1e6264c6019fa48feea446a6ff68616adc5789be4e1fed149f11a89b020",
   "engine": "google",
   "ijn": "0",
   "q": nameKeyword,
   "google_domain": "google.com",
   "tbm": "isch",
   }
   client = GoogleSearchResults(params)
   results = client.get_dict()
   url = results["images_results"][0]["original"]
   return url
#Problem ids: 12356, 4638, 13575, 21562
#I added a url column to my aggregate_stats table and this loop populates that column with the url of the player at each id.
for i in range(24691):
    if db.execute("SELECT COUNT(id) FROM aggregate_stats WHERE id = :id", id = i)[0]['COUNT(id)'] == 0:
        continue
    player = db.execute("SELECT Player FROM aggregate_stats WHERE id = :id", id = i)[0]['Player']
    url = pictureUrl(player)
    db.execute("UPDATE aggregate_stats SET url = :url WHERE id=:id", url=url, id=i)

