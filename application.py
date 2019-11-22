import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
# Creates two new tables, one for purchase history, the other for each user's aggregate holdings
db.execute("CREATE TABLE IF NOT EXISTS history ('id' INTEGER, 'ticker' VARCHAR, 'shares' INTEGER, 'price' FLOAT, 'bought' BIT, 'date' DATETIME, FOREIGN KEY (id) REFERENCES users(id))")
db.execute("CREATE TABLE IF NOT EXISTS holdings ('id' INTEGER, 'ticker' VARCHAR, 'shares' INTEGER, FOREIGN KEY (id) REFERENCES users(id))")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        holdingDict = db.execute("SELECT * FROM holdings WHERE id = :id", id= session['user_id'])
        for row in holdingDict:
            # Adding rows so I can get the table column values more easily
            row['name'] = lookup(row['ticker'])['name']
            row['currentprice'] = usd(lookup(row['ticker'])['price'])
            row['total'] = usd(row['shares']*lookup(row['ticker'])['price'])
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id= session['user_id'])[0]['cash']
        shareSum = 0
        #To calculate value of total holdings
        for row in holdingDict:
            shareSum += row['shares']*lookup(row['ticker'])['price']
        total = cash + shareSum
        return render_template("index.html", holdingDict=holdingDict, cash=usd(cash),total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        if not request.form.get("symbol"):
            return apology("Please Enter a Symbol", 403)
        if not request.form.get("shares"):
            return apology("Please enter a number of shares", 403)
        try:
            shares = int(request.form.get("shares").replace(",",""))
        except ValueError:
            return apology("Please enter an integer", 403)
        if shares <= 0:
            return apology("Please enter a positive number of shares", 403)
        # Making sure the symbol appears in all caps as that is standard
        symbol = request.form.get("symbol").upper()
        if not lookup(symbol):
            return apology("Please provide a valid ticker", 403)
        lookupDict = lookup(symbol)
        shareCost = lookupDict["price"]
        totalCost = shareCost * shares
        cashDict = db.execute("SELECT cash FROM users WHERE id = :id", id= session['user_id'])
        if totalCost > cashDict[0]['cash']:
            return apology("Insufficient Funds for this Transaction", 403)
        newBalance = cashDict[0]['cash'] - totalCost
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=newBalance, id= session['user_id'])
        #Checking if ticker is already in holdings to avoid repetitions
        if len(db.execute("SELECT * FROM holdings WHERE ticker = :ticker AND id = :id", ticker=symbol, id = session['user_id'])) >= 1:
            db.execute("UPDATE holdings SET shares = shares + :amount WHERE ticker = :ticker", amount=shares, ticker=symbol)
        else:
            db.execute("INSERT INTO holdings(id,ticker,shares) VALUES (?,?,?)", session['user_id'], symbol, shares)
        db.execute("INSERT INTO history VALUES (?,?,?,?,?,?)", session['user_id'], symbol, shares, shareCost, 1, datetime.now())
        return render_template("bought.html", shares=shares, company=lookupDict['name'], symbol=symbol, shareCost=usd(shareCost), totalCost=usd(totalCost))



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    historyDict = db.execute("SELECT * FROM history WHERE id = :id", id=session['user_id'])
    for row in historyDict:
        lookupDict = lookup(row['ticker'])
        name = lookupDict['name']
        row['name'] = name
    return render_template("history.html",historyDict=historyDict)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")
    else:
        if not request.form.get("quote"):
            return apology("must provide a quote", 403)
        symbol = request.form.get("quote")
        if not lookup(symbol):
            return apology("must provide a valid quote",403)
        quoteDict = lookup(symbol)
        return render_template("quoted.html", name=quoteDict['name'],symbol=quoteDict['symbol'], price= usd(quoteDict['price']))



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation to password", 403)
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("Passwords must match", 403)
        password_hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users(username, hash) VALUES (?,?)", request.form.get("username"), password_hash)
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("sell.html")
    else:
        if not request.form.get("symbol"):
            return apology("Please Enter a Symbol", 403)
        if not request.form.get("shares"):
            return apology("Please enter a number of shares", 403)
        symbol = request.form.get("symbol").upper()
        if not lookup(symbol):
            return apology("Please provide a valid ticker", 403)
        try:
            shares = int(request.form.get("shares").replace(",",""))
        except ValueError:
            return apology("Please enter an integer", 403)
        if shares <= 0:
            return apology("Please enter a positive number of shares", 403)
        currentShareAmountDict = db.execute("SELECT shares FROM holdings WHERE ticker = :symbol AND id=:id", symbol=symbol, id=session['user_id'])
        if len(currentShareAmountDict) < 1 or currentShareAmountDict[0]['shares'] == 0:
            return apology("Please enter a stock you own", 403)
        if shares > currentShareAmountDict[0]['shares']:
            return apology("You do not own the number of shares you are trying to sell", 403)
        # Update the number of shares
        db.execute("UPDATE holdings SET shares = shares - :amount WHERE ticker = :symbol AND id = :id", amount=shares, symbol=symbol, id=session['user_id'])
        lookupDict = lookup(symbol)
        sharePrice = lookupDict['price']
        totalRev = sharePrice * shares
        # Add the cash gained
        db.execute("UPDATE users SET cash = cash + :revenue WHERE id = :id", revenue = totalRev, id = session["user_id"])
        db.execute("INSERT INTO history VALUES (?,?,?,?,?,?)", session['user_id'], symbol, shares, sharePrice, 0, datetime.now())
        return render_template("sold.html", shares=shares, company=lookupDict['name'], symbol=symbol, sharePrice = usd(sharePrice), totalRevenue = usd(totalRev))


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    if request.method == "GET":
        return render_template("deposit.html")
    else:
        if not request.form.get("depositAmount"):
            return apology("Please enter a deposit amount", 403)
        try:
            depositAmount = float(request.form.get("depositAmount").replace(",","").replace("$",""))
        except ValueError:
            return apology("Please type in a numerical deposit amount", 403)
        if depositAmount < 0:
            return apology("Please enter a positive deposit amount", 403)
        # Add deposit amount
        db.execute("UPDATE users SET cash = cash + :deposit WHERE id = :id", deposit=depositAmount, id = session['user_id'])
        cashDict = db.execute("SELECT cash FROM users WHERE id = :id", id = session['user_id'])
        return render_template("deposited.html",depositAmount=usd(depositAmount), cash= usd(cashDict[0]['cash']))

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
