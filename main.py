import os, requests, json, openai
from requests.auth import HTTPBasicAuth

max = 10
news = os.environ['news']
openai.organisation = os.environ['organisationID']
openai.api_key = os.environ['openai']
openai.Model.list()

country = "us"
url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={news}"

result = requests.get(url)
data = result.json()

responses = []

counter = 0
for article in data["articles"]:
  counter += 1
  if counter > max:
    break
  prompt = (f"""Summarise {article["url"]} in no more than four words.""")
  response = openai.Completion.create(model="text-davinci-002",
                                      prompt=prompt,
                                      temperature=0,
                                      max_tokens=50)
  #print(response["choices"][0]["text"].strip())
  responses.append(response["choices"][0]["text"].strip())

clientID = os.environ['CLIENT_ID']
clientSECRET = os.environ['CLIENT_SECRET']

url = "https://accounts.spotify.com/api/token"
data = {"grant_type": "client_credentials"}
auth = HTTPBasicAuth(clientID, clientSECRET)

response = requests.post(url, data=data, auth=auth)
accessToken = response.json()["access_token"]
headers = {"Authorization": f"Bearer {accessToken}"}

songs = []

for response in responses:
  headline = response.replace(" ", "%20")
  headline = response.replace(".", "")
  url = "https://api.spotify.com/v1/search"
  search = f"?q={headline}&type=track"
  fullURL = f"{url}{search}"
  #print(fullURL)
  response = requests.get(fullURL, headers=headers)
  data = response.json()
  #print(json.dumps(data, indent=2))
  try:
    songs.append(data["tracks"]["items"][0])
  except:
    songs.append({"name": None, "preview_url": None})

for i in range(max):
  if songs[i]["name"] != None:
    print(responses[i])
    print(songs[i]["name"])
    print(songs[i]["preview_url"])
    print()
