import asyncio
import json
import random
from itertools import cycle
import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions


Token = "TOKEN"


client = commands.Bot(command_prefix='m.')


players = {}
queues = {}


def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()


@client.event
async def on_ready():
    print('Mei is ready.')


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def whoami(ctx):
    msg = "Du hast etwas erreicht aber leider nur hier, da du Admin bist {}".format(ctx.message.author.mention)
    await client.send_message(ctx.message.channel, msg)


@whoami.error
async def whoami_error(error, ctx):
        msg = "Du bist nur ein Pleb tut mir leid {}".format(ctx.message.author.mention)
        await client.send_message(ctx.message.channel, msg)


@client.command(name="kick", pass_context=True)
@has_permissions(administrator=True)
async def kick(ctx, member: Member):
    await client.kick(member)
    await client.say("Member gekickt")


@kick.error
async def kick_error(error, ctx):
        text = "{} was ist nur falsch mit dir!".format(ctx.message.author)
        await client.send_message(ctx.message.channel, text)


@client.command(name="ban", pass_context=True)
@has_permissions(administrator=True)
async def ban(ctx, member: Member):
    await client.ban(member)
    await client.say("Member gebannt")


@kick.error
async def ban_error(error, ctx):
        text = "{} was ist nur falsch mit dir!".format(ctx.message.author)
        await client.send_message(ctx.message.channel, text)


@client.command(pass_context=True)
@has_permissions(administrator=True)
async def clear(ctx, number):
    mgs = []
    number = int(number)
    async for x in client.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await client.delete_messages(mgs)


@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)


@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()


@client.command(pass_context=True)
async def play(ctx,url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()


@client.command()
async def hot():
    possible_response = ('Du kriegst nie eine', 'Ah geh in den Puff', 'Wofür gibt es pornhub?', 'Hier gibt es keine für dich')
    await client.say(random.choice(possible_response))


@client.command()
async def boobs():
    possible_response = ('Really?', 'Fick dich', 'Pornhub maybe?', 'Lass mich inruh', 'Du willst wohl kastriert werden <3', 'https://imgur.com/a/Ss12US3', 'https://imgur.com/a/TBuKShj', 'https://imgur.com/a/L2Jbp7x', 'https://imgur.com/a/wKQK6Dm')
    await client.say(random.choice(possible_response))


@client.command()
async def osu():
    await client.say('https://tenor.com/view/idubbbz-im-gay-filthyfrank-gif-6128368')


@client.command()
async def settings():
    await client.say('https://prosettings.net/overwatch-pro-settings-gear-list/')


@client.command()
async def iostux():
    await client.say('https://www.youtube.com/channel/UCBPCmP5El1BqpItqCswvMkw')


@client.command()
async def jayne():
    await client.say('https://www.youtube.com/channel/UCMoNOUJPZTjA1w3ttT819SA')


@client.command()
async def ptr():
    await client.say('https://us.forums.blizzard.com/en/overwatch/t/overwatch-ptr-patch-notes-october-23-2018/230684')


@client.command()
async def araxya():
    await client.say('Araxya 2018: Reeses für alle! All Hail Reeses')


@client.command()
async def owl():
    await client.say('https://www.twitch.tv/overwatchleague')


@client.command()
async def lul():
    await client.say('DOoMfiST LuL, HaNzO LuL')


@client.command()
async def patch():
    await client.say('https://playoverwatch.com/en-us/news/patch-notes/pc/')


@client.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Video in der Warteschlange!')


@client.event
async def on_member_join(member):
    with open("users.json", "r") as f:
        users = json.load(f)

        await update_data(users, member)

        with open("users.json", "w") as f:
            json.dump(users, f)


@client.event
async def on_message(message):
    with open("users.json", "r") as f:
        users = json.load(f)

        if message.author.bot:
            return
        else:
            await update_data(users, message.author)
            number = random.randint(1, 1)
            await add_experience(users, message.author, number)
            await level_up(users, message.author, message.channel)

        with open("users.json", "w") as f:
            json.dump(users, f)
    await client.process_commands(message)


async def update_data(users, user):
    if not user.name in users:
        users[user.name] = {}
        users[user.name]["experience"] = 0
        users[user.name]["level"] = 1


async def add_experience(users, user, exp):
    users[user.name]["experience"] += exp


async def level_up(users, user, channel):
    experience = users[user.name]["experience"]
    lvl_start = users[user.name]["level"]
    lvl_end = int(experience ** (1/7))

    if lvl_start < lvl_end:
        await client.send_message ( channel, '{} has leveled up to level {}'.format ( user.mention, lvl_end ) )
        users[user.name]['level'] = lvl_end


@client.command()
async def author():
    embed = discord.Embed(
        title='First real Project',
        description='Thank you for using my first real Project please join my Discord for help.',
        colour=discord.Colour.blue()
    )

    embed.set_footer(text='Support server https://discord.gg/4UkCced.')
    embed.set_image(
        url='https://cdn.discordapp.com/avatars/462182133285519370/a_57e6dc1d18520d5ffdd0dc446ce1516a.gif?size=128')
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/avatars/462182133285519370/a_57e6dc1d18520d5ffdd0dc446ce1516a.gif?size=128')
    embed.set_author(name='Neko#3333',
                     icon_url='https://cdn.discordapp.com/avatars/462182133285519370/a_57e6dc1d18520d5ffdd0dc446ce1516a.gif?size=128')
    embed.add_field(name='You are always welcome', value='Write me directly Neko#3333 or Join me', inline=False)

    await client.say(embed=embed)


status = ['Hilf mir', 'KEKSE', 'Delete Brig', 'Tea Time', 'Doomfist <3']


async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(1200)


client.loop.create_task(change_status())


client.run(Token)
