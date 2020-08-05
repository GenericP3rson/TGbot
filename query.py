import cfg
import discord
import pyTigerGraph as tg
import time


client = discord.Client()

cfg.token = tg.TigerGraphConnection(
    host="https://blog.i.tgcloud.io", graphname="TGbot").getToken(cfg.secret, "1000")[0]

conn = tg.TigerGraphConnection(
    host="https://blog.i.tgcloud.io", graphname="TGbot", password=cfg.password, apiToken=cfg.token)

msg = "vertex"
words = msg.split()
possible_options = []
for word in words:
    x = conn.runInstalledQuery("similarArticles", {"word": word})
    for opt in x[0]["blogs"]:
        possible_options.append(opt["attributes"]["message"])
    # print(x[0]["blogs"][0]["attributes"]["message"])

word_counter = {}
for word in possible_options:
    if word in word_counter:
        word_counter[word] += 1
    else:
        word_counter[word] = 1
popular_words = sorted(word_counter, key=word_counter.get, reverse=True)

print(popular_words)