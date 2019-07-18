from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

db_url = "postgres://lgttpdhhguejbs:f4d62fb55654bc4926db58ad57b54674c779415c1febfcf87246574937f04fcf@ec2-107-20-173-2.compute-1.amazonaws.com:5432/d98ghsgms2kp76"
engine = create_engine(db_url)
db = scoped_session(sessionmaker(bind=engine))

db.execute("INSERT INTO reviewstest1 (imdbid,user,review) VALUES (:imdbid, :user, :review)", {"imdbid": "id", "user": "user", "review": "review"})
res = db.commit()
# res = db.execute("SELECT * FROM reviewstest1").fetchall()
print (res)

# res = db.execute("SELECT * FROM moviestest1 WHERE id < 5").fetchall()
# print(res)

# query = "2014"
# if query[0:2] == "tt":
#     print("query is a imdbid")
#     for item in res:
#         if item[4] == query:
#             print("Found result for query: ")
#             print(item)
# elif all(char in '1234567890' for char in query):
#     print("query is a year")
#     for item in res:
#         if item[2] == query:
#             print("Found result for query: ")
#             print(item)
# else:
#     print("query is a movie title")
#     for item in res:
#         if item[1] == query:
#             print("Found result for query: ")
#             print(item)


# # q1 = "The Lego Movie"
# # for item in res:
# #     if item[1] == q1:
# #         print("Found result for q1: ")
# #         print(item)

# # q2 = "The Lego Movie"
# # for item in res:
# #     if item[2] == q2:
# #         print("Found result for q1: ")
# #         print(item)

