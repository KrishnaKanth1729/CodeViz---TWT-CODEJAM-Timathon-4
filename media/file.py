# from discord.ext import commands
from dadjokes import Dadjoke
from youtubesearchpython import VideosSearch
import discord
import time
import asyncio
import requests
import random
import wikipedia

messages = joined = 0


def read_token():
    with open('token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = discord.Client()


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open('stats.txt', 'a') as f:
                f.write(f'Time: {int(time.time())} Messages: {messages} Members Joined: {joined}\n')
            messages = 0
            joined = 0
            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)


@client.event  # This event runs whenever a user updates: status, game playing, avatar, nickname or role
async def on_member_update(before, after):
    n = after.nick
    if n:  # Check if they updated their username
        if n.lower().count("AWAKENED") > 0:  # If username contains tim
            last = before.nick
            if last:  # If they had a username before change it back to that
                await after.edit(nick=last)
            else:  # Otherwise set it to "NO STOP THAT"
                await after.edit(nick="copycat")


@client.event
async def avatar(ctx, *, member: discord.Member = None):  # set the member object to None
    if not member:
        member = ctx.message.author  # set member as the author
    userAvatar = member.avatar_url
    await ctx.send(userAvatar)


@client.event
async def on_member_update(before, after):
    n = after.nick
    if n:
        if n.lower().count('tim') > 0:
            last = before.nick
            if last:
                await after.edit(nick=last)
            else:
                await after.edit(nick='NO STOP THAT!')


@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == 'general':
            await client.send(f'Welcome the nerd "{member.mention}", to ĀWĀKĒṆĒḌ!')


@client.event
async def on_message(message):
    global messages
    messages += 1
    id = client.get_guild(801725579531517962)
    channels = ['general']
    bad_words = ['stupid', 'sucker', 'idiot', 'mental']

    for word in bad_words:
        if message.content.count(word) > 0:
            await asyncio.sleep(1)
            await message.edit(content='****')
            await message.channel.send(f"Your message was hashed as it contained a bad word")

    if message.content == '$help':
        embed = discord.Embed(title='Commands for help')
        embed.add_field(name='$hello', value='Greets the user')
        embed.add_field(name='$users', value='Returns the number of users')
        embed.add_field(name='$joke <dad/mom>', value='Returns a classic Yo Mamma So fat joke')
        embed.add_field(name='$meme', value='Returns funny gaming-related memes')
        embed.add_field(name='$kill <Person> <image/gif>', value='Kills a person with a gif/image')
        embed.add_field(name='$inspire', value='Get an inspirational quote that will make your day')
        embed.add_field(name='$rank', value='Returns your roles in the server')
        embed.add_field(name='$avatar', value='Returns your avatar')
        embed.add_field(name='$ytsearch <search>', value='Does a youtube search and returns results')
        embed.add_field(name='functions:', value='Recognizes bad words and removes them')
        await message.channel.send(
            content=f'Ah, when will you stop being a bother {message.author.mention}\nBTW here u go and let me sleep',
            embed=embed)

    if '$avatar' in message.content:
        member = ''
        k = ''
        for user in message.mentions:
            k = user.avatar_url_as(size=128)
            member = user.mention

        if k == '':
            k = message.author.avatar_url_as(size=128)
            member = message.author.mention
        await message.channel.send(member)
        await message.channel.send(k)

    if message.content.startswith('$hit'):
        k = ''
        l = ''
        for user in message.mentions:
            l = user
            k = user.avatar_url_as(size=128)
        img1 = message.author.avatar_url_as(size=128)
        e = discord.Embed(title='Hit Command', description='Hit another fellow', color=discord.Colour.green())
        e.set_image(url=img1)
        e.set_image(url='hook.jpg')
        e.set_image(url=k)
        await message.channel.send(content=f'{message.author} has hit {l}', embed=e)

    if message.content == '$rank':
        rank = message.author.roles
        try:
            k2 = rank[1]
        except IndexError:
            k2 = ''
        try:
            k3 = rank[2]
        except IndexError:
            k3 = ''
        try:
            k4 = rank[3]
        except IndexError:
            k4 = ''
        try:
            k5 = rank[4]
        except IndexError:
            k5 = ''

        msg = f'{message.author.mention} => {k2}, {k3}, {k4}, {k5}'
        await message.channel.send(msg)

    if message.content == '$kill':
        await message.channel.send('You have killed yourself. RIP')
        await message.channel.send(file=discord.File('1Jkh.gif'))

    if message.content.startswith('$kill'):
        if 'gif' in message.content:
            k = ''
            for user in message.mentions:
                k = user.avatar_url_as(size=128)

            await message.channel.send(message.author.avatar_url_as(size=128))
            await message.channel.send(file=discord.File('killer.gif'))
            await message.channel.send(k)

        if 'image' in message.content:
            m = ''
            for user in message.mentions:
                m = user.avatar_url_as(size=128)

            await message.channel.send(message.author.avatar_url_as(size=128))
            await message.channel.send(file=discord.File('img_3.png'))
            await message.channel.send(m)

    if message.content.startswith('$slap'):
        k = ''
        for user in message.mentions:
            k = user.avatar_url_as(size=128)

        if k == '':
            k = 'Great! You slapped yourself'

        await message.channel.send(message.author.avatar_url_as(size=128))
        await message.channel.send(file=discord.File('2eNz.gif'))
        await message.channel.send(k)

    if message.content.startswith('$ytsearch'):
        try:
            search = str(message.content).split()
            no = len(search)
            searchword = search[1]
            videosSearch = VideosSearch(searchword, limit=2)
            finalresult = videosSearch.result()
            embed = discord.Embed(title='Youtube Search', description=f'{searchword}', color=discord.Color.blue())
            videoname = finalresult['result'][0]['title']
            timepublish = finalresult['result'][0]['publishedTime']
            views = finalresult['result'][0]['viewCount']['short']
            thumbnail = finalresult['result'][0]['thumbnails'][0]['url']
            channel = finalresult['result'][0]['channel']['name']
            channellink = finalresult['result'][0]['channel']['link']
            embed.add_field(name='name:', value=videoname)
            embed.add_field(name='channel:', value=channel)
            embed.add_field(name='published:', value=timepublish)
            embed.add_field(name='views', value=views)
            embed.add_field(name='Channel URL:', value=channellink)
            embed.set_image(url=thumbnail)
            await message.channel.send(embed=embed)
            print(videosSearch.result())
        except IndexError:
            await message.channel.send(f'{message.author.mention}, You gotta mention something for search. LMAO')

        """    if message.content.startswith('$wksearch'):
        try:
            search = str(message.content).split()
            searchword = search[1]
            k =  wikipedia.summary(searchword, sentences=5)
            await message.channel.send(k)
        except IndexError:
            await message.channel.send('You gotta search something. LMAO')"""

    if message.content == '$meme':
        await message.channel.send('Oh Memes i love them as a kid(But i never grew up!)')
        integer = random.randint(1, 7)
        await message.channel.send(file=discord.File(f'{integer}.jpg'))

    if message.content.startswith('$joke'):
        lol = str(message.content).split()
        try:
            if lol[1] == 'dad':
                dadjoke = Dadjoke()
                await message.channel.send(dadjoke.joke)
            elif lol[1] == 'mom':
                url = 'https://api.yomomma.info/'
                k = requests.get(url).json()
                await message.channel.send(k['joke'])
                await message.channel.send(file=discord.File('img_5.png'))
                k.clear()
            if not lol[1]:
                dadjoke = Dadjoke()
                await message.channel.send(dadjoke.joke)
        except IndexError:
            dadjoke = Dadjoke()
            await message.channel.send(dadjoke.joke)

    if message.content == '$inspire':
        url = 'https://zenquotes.io/api/random'
        l = requests.get(url).json()
        await message.channel.send(file=discord.File('AQI.gif'))
        await message.channel.send(f"{l[0]['q']} - by {l[0]['a']}")

    if str(message.channel) in channels:
        if message.content.find('$hello') != -1:
            await message.channel.send(file=discord.File('img_1.png'))
            await message.channel.send(f'Sup {message.author.mention}!')
        elif message.content == '$users':
            await message.channel.send(f""""# of users {id.member_count}""")

client.loop.create_task(update_stats())
client.run(token)
