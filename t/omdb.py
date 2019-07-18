import requests
res = requests.get("http://www.omdbapi.com/?apikey=36a5b700&i=tt0068646")
print(res.json())
# if "ads" in res.json():
#     print(res.json()["ads"])
# print(res.json()["Plot"])
# print(res.json()["Genre"])
# print(res.json()["Director"])
# print(res.json()["Actors"])
# print(res.json()["Poster"])