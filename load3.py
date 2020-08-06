'''
POST request testing here
'''


import requests
import json
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


stop_words = set(stopwords.words('english'))

url = ""

# x = requests.post(url, data=myobj)
x = requests.get(
    "https://community.tigergraph.com/posts.json")
data = json.loads(x.text)["latest_posts"]

print(data[0]["raw"])

print("https://community.tigergraph.com/t/" +
      data[0]["topic_slug"] + "/" + str(data[0]["topic_id"]))

words = []
msgs = []
ids = []
urls = []

for msg in data:
    # print(msg)
    raw_msg = "<br>".join(("".join(msg["raw"].split(","))).split("\n"))
    individual_words = raw_msg.split()
    word_tokens = word_tokenize(raw_msg.lower())
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = [w for w in filtered_sentence if not w in [
        '.', ',', '!', '?', ':', ';']]
    for word in filtered_sentence:
        words.append(word)
        msgs.append(raw_msg)
        ids.append(msg["id"])
        urls.append("https://community.tigergraph.com/t/" +
                    msg["topic_slug"] + "/" + str(msg["topic_id"]))

df = {"words": words, "ids": ids, "urls": urls, "messages": msgs}
# df = {"words": words, "ids": ids, "urls": urls}
df = pd.DataFrame(data=df)
df.to_csv("graph/data/Words2.csv")
