import cfg
import discord
import pyTigerGraph as tg
import time


client = discord.Client()

# conn = tg.TigerGraphConnection(host="blog.i.tgcloud.io", graphname="OpiodGraph",
#                                username="tigergraph", password="tigergraph", apiToken="tmt8jvqpbicjv24a3kbth83domvn8ism")


cfg.token = tg.TigerGraphConnection(
    host="https://blog.i.tgcloud.io", graphname="OpiodGraph").getToken(cfg.secret, "1000")[0]

conn = tg.TigerGraphConnection(
    host="https://blog.i.tgcloud.io", graphname="OpiodGraph", password=cfg.password, apiToken=cfg.token)



@client.event
async def on_message(m):
    print(m.content)
    print(m.content == "!showSchema")
    '''
    Schema Functions
    '''
    if m.content == "!intro":
        await m.channel.send("**Welcome, Futurist Academy.**")
        time.sleep(3)
        await m.channel.send("**I am TGbot. :tiger: :robot:**")
        time.sleep(3)
        await m.channel.send("**I can interact with your TG servers.**")
        time.sleep(3)
        await m.channel.send("**Check out my commands:**")
        await m.channel.send("```\n!graphName\n!getEdges\n!getVertices\n!getVertex <vertex>\n!getEdge <edge>\n!countVertex <vertex>\n!countEdge <edge>\n```")
    elif m.content == "!showSchema": # Maxes out
        sch = conn.getSchema()
        await m.channel.send("Your Schema:\n" + '\n'.join([str(i) + " + " + str(sch[i]) for i in sch]))
    elif m.content == '!graphName':
        await m.channel.send("Your Graph is called " + conn.getSchema()['GraphName'])
    elif m.content == '!getEdges':
        await m.channel.send("__Edges__\n```\n" + '\n'.join(conn.getEdgeTypes()) + "```")
    elif m.content == '!getVertices':
        await m.channel.send("__Vertices__\n```\n" + '\n'.join(conn.getVertexTypes()) + "```")
    elif m.content[:10] == '!getVertex':
        await m.channel.send('```' + '\n'.join((str(conn.getVertexType(m.content[11:].strip()))[1:-1]).split(', ')) + '```')
    elif m.content[:8] == '!getEdge':
        await m.channel.send('```' + '\n'.join((str(conn.getEdgeType(m.content[9:].strip()))[1:-1]).split(', ')) + '```')
    elif m.content[:12] == "!countVertex":
        await m.channel.send("There are "  + str(conn.getVertexCount(m.content[13:])) + " vertices with " + m.content[13:])
    elif m.content[:10] == "!countEdge":
        await m.channel.send("There are " + str(conn.getEdgeCount(m.content[11:])) + " vertices with " + m.content[11:])



@client.event
async def on_ready():
    print(conn.getVertexTypes())
    print(f"We have logged in as {client.user}")
    print(conn.getVertexCount('_NPI'))
    # print(conn.getEndpoints())
    # print(conn.getSchema())

# client.loop.create_task(alerts())
client.run("NzM4NzU1MzUwODc4MDkzMzIz.XyQhiQ.KOwvVO5Iziz4hPV_Ztj1BTzikW4")
