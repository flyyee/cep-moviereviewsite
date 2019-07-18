from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

db_url = "postgres://lgttpdhhguejbs:f4d62fb55654bc4926db58ad57b54674c779415c1febfcf87246574937f04fcf@ec2-107-20-173-2.compute-1.amazonaws.com:5432/d98ghsgms2kp76"
engine = create_engine(db_url)
db = scoped_session(sessionmaker(bind=engine))

# db.execute("""CREATE TABLE moviestest1 (
#       id SERIAL PRIMARY KEY,
#       title VARCHAR NOT NULL,
#       year VARCHAR NOT NULL,
#       runtime VARCHAR NOT NULL,
#       imdbid VARCHAR NOT NULL,
#       imdbrating VARCHAR NOT NULL
# );""")
# db.commit()
# db.execute("INSERT INTO moviestest1 (title, year, runtime, imdbid, imdbrating) VALUES (:title, :year, :runtime, :imdbid, :imdbrating)", {"title": "Boy", "year": "2019", "runtime": "120", "imdbid": "tt123123", "imdbrating": "100"})
# db.commit()
# res = db.execute("SELECT imdbid FROM moviestest2").fetchall()

with open("./r/movies.csv") as f:
    data = f.read().splitlines()
    data.pop(0)
    # print(data)
    for movie in data:
        title, year, runtime, id, rating = movie.split(";")
        db.execute("INSERT INTO moviestest1 (title, year, runtime, imdbid, imdbrating) VALUES (:title, :year, :runtime, :imdbid, :imdbrating)", {"title": title, "year": year, "runtime": runtime, "imdbid": id, "imdbrating": rating})
        db.commit()
        print(title)
        print(year)
        print(runtime)
        print(id)
        print(rating)
