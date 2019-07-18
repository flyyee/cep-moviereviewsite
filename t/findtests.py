from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

db_url = "postgres://lgttpdhhguejbs:f4d62fb55654bc4926db58ad57b54674c779415c1febfcf87246574937f04fcf@ec2-107-20-173-2.compute-1.amazonaws.com:5432/d98ghsgms2kp76"
engine = create_engine(db_url)
db = scoped_session(sessionmaker(bind=engine))

# res = db.execute("""CREATE TABLE reviewstest2 (
#       id SERIAL PRIMARY KEY,
#       username VARCHAR NOT NULL,
#       review VARCHAR NOT NULL,
#       score VARCHAR NOT NULL
#   );""")
# res = db.execute("INSERT INTO reviewstest2 ")
print(res)
res = db.execute("SELECT * FROM reviewstest2").fetchall()
# db.execute("ALTER TABLE reviewstest1 ADD COLUMN score VARCHAR")
# res = db.commit()
print (res)