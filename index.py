import cfg
import discord
import pyTigerGraph as tg
import time


client = discord.Client()

# conn = tg.TigerGraphConnection(host="blog.i.tgcloud.io", graphname="OpiodGraph",
#                                username="tigergraph", password="tigergraph", apiToken="tmt8jvqpbicjv24a3kbth83domvn8ism")


cfg.token = tg.TigerGraphConnection(
    host="https://blog.i.tgcloud.io", graphname="TGbot").getToken(cfg.secret, "1000")[0]

conn = tg.TigerGraphConnection(
    host="https://blog.i.tgcloud.io", graphname="TGbot", password=cfg.password, apiToken=cfg.token)


@client.event
async def on_message(msg):
    print(msg.content)
    # print(msg.content == "!showSchema")
    '''
    Schema Functions
    '''
    if (msg.author.name != "TGbot" and msg.content[-2:] == "??"):
        words = msg.content[:-2].split()
        # possible_options = []
        # for word in words:
        #     x = conn.runInstalledQuery(word)
        # msg = "vertex"
        # words = msg.split()
        possible_options = []
        for word in words:
            x = conn.runInstalledQuery("similarArticles", {"word": word})
            for opt in x[0]["blogs"]:
                possible_options.append(opt["attributes"]["url"])
            # print(x[0]["blogs"][0]["attributes"]["message"])

        word_counter = {}
        for word in possible_options:
            if word in word_counter:
                word_counter[word] += 1
            else:
                word_counter[word] = 1
        popular_words = sorted(word_counter, key=word_counter.get, reverse=True)

        # print(popular_words)
        if len(popular_words) == 0:
            await msg.channel.send("I couldn't find anything like that.")
        else:
            await msg.channel.send("You might want to check out this: " + popular_words[0])



@client.event
async def on_ready():
    print(conn.getVertexTypes())
    print(f"We have logged in as {client.user}")
    # print(conn.getVertexCount('_NPI'))
    # print(conn.getEndpoints())
    # print(conn.getSchema())

# client.loop.create_task(alerts())
client.run("NzM4NzU1MzUwODc4MDkzMzIz.XyQhiQ.KOwvVO5Iziz4hPV_Ztj1BTzikW4")
