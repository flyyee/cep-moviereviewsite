import os

from flask import Flask, session, render_template, request, redirect, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from hashlib import sha256

app = Flask(__name__)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
db_url = "postgres://lgttpdhhguejbs:f4d62fb55654bc4926db58ad57b54674c779415c1febfcf87246574937f04fcf@ec2-107-20-173-2.compute-1.amazonaws.com:5432/d98ghsgms2kp76"
# engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine(db_url)
db = scoped_session(sessionmaker(bind=engine))


# @app.route("/")
# def index():
#     return render_template("index.html")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/signup", methods=["GET"])
def signup():
    signinfo = False
    if request.args.get('signinfo') == "badusername":
        signinfo = True
    return render_template("signup.html", signinfo=signinfo)

@app.route("/signup", methods=["POST"])
def createuser():
    username = request.form.get("username")
    password = sha256(request.form.get("password").encode()).hexdigest()
    res = db.execute("SELECT id FROM userstest1 WHERE username = '" + username + "'").fetchall()
    if res:  #not empty
        return redirect("/signup?signinfo=badusername")
    
    res = db.execute("INSERT INTO userstest1 (username, password) VALUES (:username, :password)", {
                     "username": username, "password": password})
    res = db.commit()
    return redirect("/?success=true")


@app.route("/login", methods=["POST"])
def checklogin():
    username = request.form.get("username")
    password = sha256(request.form.get("password").encode()).hexdigest()
    
    res = db.execute("SELECT password FROM userstest1 WHERE username = '" + username + "' AND password = '" + password + "'").fetchall()
    if res:
        session["who"] = [username, password]
        return redirect("/?success=true")
    else:
        session["who"] = "notset"
        return render_template("login.html", signinfo=True)

@app.route("/logout", methods=["GET"])
def logout():
    session["who"] = "notset"
    return redirect("/")

@app.route("/")
def index():
    success = False
    if request.args.get('success') == "true":
        success = True
    loggedin = False
    if "who" not in session:
        session["who"] = "notset"
    elif session["who"] != "notset":
        loggedin = True
    return render_template("site.html", success=success, loggedin=loggedin)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    movies = db.execute("SELECT * FROM moviestest1").fetchall()
    matches = []
    if not query:
        return render_template("404.html", object="Query")
    if query[0:2] == "tt":
        print("query is a imdbid")
        for item in movies:
            if query in item[4]:
                print("Found result for query: ")
                print(item)
                matches.append(item)
    elif all(char in '1234567890' for char in query):
        print("query is a year")
        for item in movies:
            if query in item[2]:
                print("Found result for query: ")
                print(item)
                matches.append(item)
    else:
        print("query is a movie title")
        for item in movies:
            if query.lower() in item[1].lower():
                print("Found result for query: ")
                print(item)
                matches.append(item)
            
    nomatches = not bool(matches)

    loggedin = False
    if "who" not in session:
        session["who"] = "notset"
    if session["who"] != "notset":
        loggedin = True

    return render_template("search.html", results=matches, loggedin=loggedin, nomatches=nomatches)


@app.route("/catalogue")
def catalogue():
    if request.args.get('id')[0:2] == "tt":
        myimdbid = request.args.get('id')
        if "who" not in session:
            session["who"] = "notset"
        myusername = session["who"][0]
        mypassword = session["who"][1]
        movieinfo = db.execute(
            "SELECT * FROM moviestest1 WHERE imdbid = '" + myimdbid + "'").fetchall()
        print("successful call")
        print(movieinfo)
        if movieinfo:  # not empty
            loggedin = False
            if "who" in session:
                if session["who"] != "notset":
                    usernames = db.execute(
            "SELECT username FROM userstest1 WHERE password = '" + mypassword + "' AND username = '" + myusername + "'").fetchall()
                    if usernames:
                        myusername = usernames[0][0]
                        loggedin = True

            reviews = db.execute(
                "SELECT * FROM reviewstest2 WHERE imdbid = '" + myimdbid + "'").fetchall()

            reviewed = False
            print(myusername)
            for review in reviews:
                print(review[2])
                if review[2] == myusername:
                    reviewed = True
                    break

            res = requests.get(
                "http://www.omdbapi.com/?apikey=36a5b700&i=" + myimdbid)
            omdbinfo = []
            if "Plot" in res.json():
                omdbinfo.append(res.json()["Plot"])
            else:
                omdbinfo.append("Not available")
            if "Genre" in res.json():
                omdbinfo.append(res.json()["Genre"])
            else:
                omdbinfo.append("Not available")
            if "Director" in res.json():
                omdbinfo.append(res.json()["Director"])
            else:
                omdbinfo.append("Not available")
            if "Actors" in res.json():
                omdbinfo.append(res.json()["Actors"])
            else:
                omdbinfo.append("Not available")
            if "Poster" in res.json():
                omdbinfo.append(res.json()["Poster"])
            else:
                omdbinfo.append(
                    "https://upload.wikimedia.org/wikipedia/en/d/d1/Image_not_available.png")

            # reviewed = db.execute("SELECT * FROM reviewstest2 WHERE username = '" + myusername + "'").fetchall()
            # reviewed = bool(reviewed) #if empty = false
            return render_template("movie.html", movieinfo=movieinfo[0], loggedin=loggedin, reviews=reviews, reviewed=reviewed, omdbinfo=omdbinfo)
        else:
            return redirect("/site")
    return redirect("/site")


@app.route("/submitreview", methods=["POST"])
def submitreview():
    id = request.args.get("id")
    score = request.form.get("reviewrangevalue")
    print(score)
    review = request.form.get("review")
    if "who" not in session:
        session["who"] = "notset"
    usernames = db.execute(
            "SELECT username FROM userstest1 WHERE password = '" + session["who"][1] + "' AND username = '" + session["who"][0] + "'").fetchall()
    user = usernames[0][0]
    res = db.execute("INSERT INTO reviewstest2 (imdbid, username, review, score) VALUES (:imdbid, :username, :review, :score)", {
                     "imdbid": id, "username": user, "review": review, "score": score})
    res = db.commit()
    return redirect("/catalogue?id=" + id)


@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")
    return render_template("hello.html", name=name)


@app.route("/api/<imdbid>", methods=["GET"])
def api(imdbid):
    res = db.execute(
        "SELECT * FROM moviestest1 WHERE imdbid = '" + imdbid + "'").fetchall()
    if not res:
        # return abort(404)
        return render_template("404.html", object="Movie")
    print(imdbid)
    # imdbid = request.path
    res = requests.get("http://www.omdbapi.com/?apikey=36a5b700&i=" + imdbid)
    info = {
        "title": "",
        "year": 0,
        "imdb_id": imdbid,
        "director": "",
        "actors": "",
        "imdb_rating": 0,
        "review_count": 0,
        "average_score": 0,
    }
    if "Title" in res.json():
        info["title"] = res.json()["Title"]
    if "Year" in res.json():
        info["year"] = res.json()["Year"]
    if "Director" in res.json():
        info["director"] = res.json()["Director"]
    if "Actors" in res.json():
        info["actors"] = res.json()["Actors"]
    if "imdbRating" in res.json():
        info["imdb_rating"] = res.json()["imdbRating"]

    scores = db.execute(
        "SELECT score FROM reviewstest2 WHERE imdbid = '" + imdbid + "'").fetchall()

    info["review_count"] = len(scores)

    # print(scores)
    totalscore = 0.0
    average = 0.0
    for score in scores:
        totalscore += float(score[0])
    if len(scores) != 0:
        average = totalscore / len(scores)
    info["average_score"] = average
    return jsonify(info)