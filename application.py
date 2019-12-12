#Same imports as for finance.db
import os
import sqlite3
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

#Google Images API
from serpapi.google_search_results import GoogleSearchResults

# Configure application
app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
   response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
   response.headers["Expires"] = 0
   response.headers["Pragma"] = "no-cache"
   return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///basketball.db")
#My website's homepage, only accepts "GET" method
@app.route("/")
def index():
    #These will be the columns of the statistical dropdown menus, I didn't use a SQL statement to get column names as I made a lot of
    #changes to make them more readable for humans (like taking out '_' and writing spaces instead)
    columns = ['Points', 'Assists', 'Rebounds', 'Steals', 'Blocks', 'Field Goals Made', 'Games', 'Games Started', 'Field Goal %', 'Two Point %',
    'Three Point %', 'Value Over Replacement', 'Win Shares per 48', 'Win Shares', 'Offensive Win Shares', 'Defensive Win Shares','Minutes Played',
    'Box Score +/-', 'Offensive +/-', 'Defensive +/-', 'Offensive Rebounds', 'Defensive Rebounds', 'Effective Field Goal %', 'True Shooting %',
    'Player Efficiency Rating', 'Free Throw %', 'Free Throws Made', 'Free Throws Attempted', 'Two Pointers Made', 'Two Pointers Attempted',
    'Three Pointers Made', 'Three Pointers Attempted', 'Field Goals Attempted']
    return render_template("index.html", columns = columns)
# This corresponds to many different pages actually, it is a different url based on the input given from index.html. But it is the page
# that comes up when users press the "Go!" button on the homepage.
@app.route('/<input>')
def page(input):
    #I insert tildas between the words and numbers in input in index.html so I can get the words and numbers back by just splitting input based on tildas.
    split = input.split("~")
    #split[0] is the stat chosen in the first dropdown menu
    inputStat = split[0]
    stat = split[0]
    #This series of if else statements are so I can go from dropdown menu entries back to column names
    if inputStat == "Win Shares per 48":
        inputStat = "Win_Shares_per_Fourty_Eight_Minutes"
    elif inputStat == "Box Score Box Plus Minus":
        inputStat = "Box_Plus_Minus"
    elif inputStat == "Rebounds":
        inputStat = "Total_Rebounds"
    else:
        inputStat = inputStat.replace(" ", "_").replace("%","Percentage")
    #This is the case where len(split) = 1, meaning a statistic was entered but no condition
    if len(split) == 1:
        #In this case we will simply grab the player with the highest amount of the given stat
        originalPlayer = db.execute("SELECT Player FROM aggregate_stats ORDER BY {} DESC LIMIT 1".format(inputStat))[0]['Player']
        #This line is because in the original data, certain players received an asterisk next to their name, so when printing
        #out their name I didn't want to print the asterisk too
        player = originalPlayer.replace("*","")
        #Selects the value of the stat that that player had the most of. For example if the condition was Player with the
        # Most Points who also played more than a 100 games, this would select the number of Points that player had.
        statValue = db.execute("SELECT {} FROM aggregate_stats ORDER BY {} DESC LIMIT 1".format(inputStat, inputStat))[0][inputStat]
        #Gets the url column value for the given player, so it can be fed in render_template and their picture can be pulled up.
        url = db.execute("SELECT url FROM aggregate_stats WHERE Player = :player", player = originalPlayer)[0]['url']
        return render_template("statTemplate.html", player=player, statValue=statValue, stat=stat, url = url, conditions=0)
    elif len(split) == 4:
        #This implies that only one condition was filled out as that is why there are 4 entries in split.
        conditions = 1
        #split[1] is the statistic chosen in condition 1
        conditionStat1 = split[1]
        conditionStatOriginal1 = split[1]
        #split[2] is the comparator symbol (<,>,=) chosen in condition 1
        comparator1 = split[2].replace("greater_than",">").replace("less_than","<")
        #split[3] is the number written in condition 1
        number1 = split[3]
        if conditionStat1 == "Win Shares per 48":
            conditionStat1 = "Win_Shares_per_Fourty_Eight_Minutes"
        elif conditionStat1 == "Box Score Box Plus Minus":
            conditionStat1 = "Box_Plus_Minus"
        elif conditionStat1 == "Rebounds":
            conditionStat1 = "Total_Rebounds"
        else:
            conditionStat1 = conditionStat1.replace(" ", "_").replace("%","Percentage")
        #This checks if there even is a player in the database with the requisite statistical specifications
        if len(db.execute("SELECT Player FROM aggregate_stats WHERE {} {} {} ORDER BY {} DESC LIMIT 1".format(conditionStat1, comparator1, number1,inputStat))) == 0:
            #If there isn't I redirect the user to an error page
            return redirect("/No_Player")
        else :
            #Selects the Player with the most of the first statistic provided that they meet the condition
            originalPlayer = db.execute("SELECT Player FROM aggregate_stats WHERE {} {} {} ORDER BY {} DESC LIMIT 1".format(conditionStat1, comparator1, number1,inputStat))[0]['Player']
            #This line is because in the original data, certain players received an asterisk next to their name, so when printing
            #out their name I didn't want to print the asterisk too
            player = originalPlayer.replace("*","")
            #Need to make the player's name a string to use it in SQL queries
            statPlayer = "'" + originalPlayer + "'"
            #Selects the value of the stat that that player had the most of. For example, if the condition was Player with the
            #Most Points who also played more than a 100 games, this would select the number of Points that player had.
            statValue = db.execute("SELECT {} FROM aggregate_stats WHERE Player = {}".format(inputStat, statPlayer))[0][inputStat]
            #Selects the value of the stat that was used in the condition. For example, if the condition was Player with the Most Points who also played
            #more than a 100 games, this would select the names of games that player had played in.
            conditionStatValue1 = db.execute("SELECT {} FROM aggregate_stats WHERE Player = {}".format(conditionStat1,statPlayer))[0][conditionStat1]
            #Gets the url column value for the given player, so it can be fed in render_template and their picture can be pulled up.
            url = db.execute("SELECT url FROM aggregate_stats WHERE Player = :player", player = originalPlayer)[0]['url']
            return render_template("statTemplate.html",
            player=player, statValue=statValue, stat=stat, url = url, conditions = 1, conditionStatValue1=conditionStatValue1,
            conditionStatOriginal1=conditionStatOriginal1)
    elif len(split) == 7:
        #split[1] is the statistic chosen in condition 1
        conditionStat1 = split[1]
        conditionStatOriginal1 = split[1]
        #split[2] is the comparator symbol (<,>,=) chosen in condition 1
        comparator1 = split[2].replace("greater_than",">").replace("less_than","<")
        #split[3] is the number written in condition 1
        number1 = split[3]
        #split[4] is the statistic chosen in condition 1
        conditionStat2 = split[4]
        conditionStatOriginal2 = split[4]
        #split[5] is the comparator symbol (<,>,=) chosen in condition 1
        comparator2 = split[5].replace("greater_than",">").replace("less_than","<")
        #split[6] is the number written in condition 1
        number2 = split[6]
        if conditionStat1 == "Win Shares per 48":
            conditionStat1 = "Win_Shares_per_Fourty_Eight_Minutes"
        elif conditionStat1 == "Box Score Box Plus Minus":
            conditionStat1 = "Box_Plus_Minus"
        elif conditionStat1 == "Rebounds":
            conditionStat1 = "Total_Rebounds"
        else:
            conditionStat1 = conditionStat1.replace(" ", "_").replace("%","Percentage")
        if conditionStat2 == "Win Shares per 48":
            conditionStat2 = "Win_Shares_per_Fourty_Eight_Minutes"
        elif conditionStat2 == "Box Score Box Plus Minus":
            conditionStat2 = "Box_Plus_Minus"
        elif conditionStat2 == "Rebounds":
            conditionStat2 = "Total_Rebounds"
        else:
            conditionStat2 = conditionStat2.replace(" ", "_").replace("%","Percentage")
        #This checks if there even is a player in the database with the requisite statistical specifications
        if len(db.execute("SELECT Player FROM aggregate_stats WHERE {} {} {} AND {} {} {} ORDER BY {} DESC LIMIT 1".format(
            conditionStat1, comparator1, number1, conditionStat2, comparator2, number2, inputStat))) == 0:
            #If there isn't, I redirect the user to an error page
            return redirect("/No_Player")
        else:
            #Selects the Player with the most of the first statistic provided that they meet the conditions
            originalPlayer = db.execute("SELECT Player FROM aggregate_stats WHERE {} {} {} AND {} {} {} ORDER BY {} DESC LIMIT 1".format(
            conditionStat1, comparator1, number1, conditionStat2, comparator2, number2, inputStat))[0]['Player']
            #This line is because in the original data, certain players received an asterisk next to their name, so when printing
            #out their name I didn't want to print the asterisk too
            player = originalPlayer.replace("*","")
            #Need to make the player's name a string to use it in SQL queries
            statPlayer = "'" + originalPlayer + "'"
            #Selects the value of the stat that that player had the most of. For example, if the condition was Player with the
            #Most Points who also played more than a 100 games and had more than 1000 assists, this would select the number of Points that player had.
            statValue = db.execute("SELECT {} FROM aggregate_stats WHERE Player = {}".format(inputStat, statPlayer))[0][inputStat]
            #Selects the value of the stat that was used in the first condition. For example, if the condition was Player with the Most Points who also played
            #more than a 100 games and had more than 1000 assists, this would select the names of games that player had played in.
            conditionStatValue1 = db.execute("SELECT {} FROM aggregate_stats WHERE Player = {}".format(conditionStat1,statPlayer))[0][conditionStat1]
            #Selects the value of the stat that was used in the first condition. For example, if the condition was Player with the Most Points who also played
            #more than a 100 games and had more than 1000 assists, this would select the number of assists that player had.
            conditionStatValue2 = db.execute("SELECT {} FROM aggregate_stats WHERE Player = {}".format(conditionStat2,statPlayer))[0][conditionStat2]
            #Gets the url column value for the given player, so it can be fed in render_template and their picture can be pulled up.
            url = db.execute("SELECT url FROM aggregate_stats WHERE Player = :player", player = originalPlayer)[0]['url']
            return render_template("statTemplate.html",
            player=player, statValue=statValue, stat=stat, url = url, conditions = 2, conditionStatValue1=conditionStatValue1,
            conditionStatOriginal1=conditionStatOriginal1, conditionStatValue2=conditionStatValue2, conditionStatOriginal2=conditionStatOriginal2)
        #This means all 3 conditions were filled out
    elif len(split) == 10:
    #split[1] is the statistic chosen in condition 1
        conditionStat1 = split[1]
        conditionStatOriginal1 = split[1]
        #split[2] is the comparator symbol (<,>,=) chosen in condition 1
        comparator1 = split[2].replace("greater_than",">").replace("less_than","<")
        #split[3] is the number written in condition 1
        number1 = split[3]
        #split[4] is the statistic chosen in condition 1
        conditionStat2 = split[4]
        conditionStatOriginal2 = split[4]
        #split[5] is the comparator symbol (<,>,=) chosen in condition 1
        comparator2 = split[5].replace("greater_than",">").replace("less_than","<")
        #split[6] is the number written in condition 1
        number2 = split[6]
        #split[4] is the statistic chosen in condition 1
        conditionStat3 = split[7]
        conditionStatOriginal3 = split[7]
        #split[5] is the comparator symbol (<,>,=) chosen in condition 1
        comparator3 = split[8].replace("greater_than",">").replace("less_than","<")
        #split[6] is the number written in condition 1
        number3 = split[9]
        if conditionStat1 == "Win Shares per 48":
            conditionStat1 = "Win_Shares_per_Fourty_Eight_Minutes"
        elif conditionStat1 == "Box Score Box Plus Minus":
            conditionStat1 = "Box_Plus_Minus"
        elif conditionStat1 == "Rebounds":
            conditionStat1 = "Total_Rebounds"
        else:
            conditionStat1 = conditionStat1.replace(" ", "_").replace("%","Percentage")
        if conditionStat2 == "Win Shares per 48":
            conditionStat2 = "Win_Shares_per_Fourty_Eight_Minutes"
        elif conditionStat2 == "Box Score Box Plus Minus":
            conditionStat2 = "Box_Plus_Minus"
        elif conditionStat2 == "Rebounds":
            conditionStat2 = "Total_Rebounds"
        else:
            conditionStat2 = conditionStat2.replace(" ", "_").replace("%","Percentage")
        if conditionStat3 == "Win Shares per 48":
            conditionStat3 = "Win_Shares_per_Fourty_Eight_Minutes"
        elif conditionStat3 == "Box Score Box Plus Minus":
            conditionStat3 = "Box_Plus_Minus"
        elif conditionStat3 == "Rebounds":
            conditionStat3 = "Total_Rebounds"
        else:
            conditionStat3 = conditionStat3.replace(" ", "_").replace("%","Percentage")
        #This checks if there even is a player in the database with the requisite statistical specifications
        if len(db.execute("SELECT Player FROM aggregate_stats WHERE {} {} {} AND {} {} {} AND {}{}{} ORDER BY {} DESC LIMIT 1".format(
            conditionStat1, comparator1, number1, conditionStat2, comparator2, number2, conditionStat3, comparator3, number3, inputStat))) == 0:
            #If there isn't, I redirect the user to an error page
            return redirect("/No_Player")
        else:
            #Selects the Player with the most of the first statistic that meets all three conditions
            originalPlayer = db.execute("SELECT Player FROM aggregate_stats WHERE {} {} {} AND {} {} {} AND {}{}{} ORDER BY {} DESC LIMIT 1".format(
            conditionStat1, comparator1, number1, conditionStat2, comparator2, number2, conditionStat3, comparator3, number3, inputStat))[0]['Player']
            #This line is because in the original data, certain players received an asterisk next to their name, so when printing
            #out their name I didn't want to print the asterisk too
            player = originalPlayer.replace("*","")
            #Need to make the player's name a string to use it in SQL queries
            statPlayer = "'" + originalPlayer + "'"
            #Selects the value of the stat that that player had the most of. For example, if the condition was Player with the
            #Most Points who also played more than a 100 games, had more than 1000 assists, and had less than 500 turnovers this would select the number of Points that player had.
            statValue = db.execute("SELECT {} FROM aggregate_stats WHERE Player = {}".format(inputStat, statPlayer))[0][inputStat]
            #Selects the value of the stat that was used in the first condition. For example, if the condition was Player with the Most Points who also played
            #more than a 100 games had more than 1000 assists, and had less than 500 turnovers, this would select the names of games that player had played in.
            conditionStatValue1 = db.execute("SELECT {} FROM aggregate_stats WHERE Player = {}".format(conditionStat1,statPlayer))[0][conditionStat1]
            #Selects the value of the stat that was used in the first condition. For example, if the condition was Player with the Most Points who also played
            #more than a 100 games, had more than 1000 assists, and had less than 500 turnovers this would select the number of assists that player had.
            conditionStatValue2 = db.execute("SELECT {} FROM aggregate_stats WHERE Player = {}".format(conditionStat2,statPlayer))[0][conditionStat2]
            #Selects the value of the stat that was used in the first condition. For example, if the condition was Player with the Most Points who also played
            #more than a 100 games, had more than 1000 assists, and had less than 500 turnovers this would select the number of turnovers that player had.
            conditionStatValue3 = db.execute("SELECT {} FROM aggregate_stats WHERE Player = {}".format(conditionStat3,statPlayer))[0][conditionStat3]
            #Gets the url column value for the given player, so it can be fed in render_template and their picture can be pulled up.
            url = db.execute("SELECT url FROM aggregate_stats WHERE Player = :player", player = originalPlayer)[0]['url']
            return render_template("statTemplate.html",
            player=player, statValue=statValue, stat=stat, url = url, conditions = 3, conditionStatValue1=conditionStatValue1,
            conditionStatOriginal1=conditionStatOriginal1, conditionStatValue2=conditionStatValue2, conditionStatOriginal2=conditionStatOriginal2,
            conditionStatOriginal3=conditionStatOriginal3, conditionStatValue3=conditionStatValue3)
    else:
        return redirect("/Error")
#If no player fits the statistical specifications of the user, they are redirected to this error page
@app.route("/No_Player")
def noPlayer():
    return render_template("No_Player.html")
@app.route("/Error")
def error():
    return render_template("error.html")






























