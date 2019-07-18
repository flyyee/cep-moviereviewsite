import requests
res = requests.get("http://www.omdbapi.com/", params={"apikey": "36a5b700", "t": "The+Godfather"})
thing = res.json()
print(thing["Title"])