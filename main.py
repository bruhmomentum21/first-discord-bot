from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions
import discord
import asyncio
import random
import requests
import uuid
from pathlib import Path
import sqlite3
import datetime

p = Path('.')
call = ['based.', 'cringe! you\'re going to lose subscriber!']
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)


@client.event
async def on_message_delete(message):
    await message.channel.send(
        f'{message.author.mention}: said "{message.content}" in #{message.channel}. and it got deleted ')


@client.command(name='list_members')
async def reaction(ctx: discord.message):
    guild = ctx.guild
    message = ctx.message
    await ctx.channel.send(f'members in this server so far: {len(guild.members)} users')
    for I in range(len(guild.members)):
        await message.author.send(guild.members[I])


@client.command(name='call')
async def based(ctx):
    edit = await ctx.message.channel.send('calling based department')
    await asyncio.sleep(3)
    await edit.edit(content=call[random.randint(0, 1)])


async def mysql(image_name_aka_uuuid,the_id_of_the_uploader,date):
    TheDatabaseItself = sqlite3.connect('discordbot_database.db')
    c = TheDatabaseItself.cursor()
    c.execute("INSERT INTO discord_database VALUES (?,?,?)", (image_name_aka_uuuid, the_id_of_the_uploader, date))
    TheDatabaseItself.commit()
    TheDatabaseItself.close()

# !attach [image] to upload images to pc
@client.command()
async def attach(ctx):
    f = ctx.message.attachments[0]
    date = datetime.datetime.now()
    hoorah = f'{uuid.uuid4()}.jpg'
    if f.url.endswith(".png") or f.url.endswith(".jpg"):
        await mysql(str(hoorah), int(ctx.message.author.id), date.strftime("%m/%d/%Y, %H:%M:%S"))
        with open(f'{hoorah}', 'wb') as handle:
            response = requests.get(f.url, stream=True)
            for block in response.iter_content(1024):
                if not response.ok:
                    print(response)
                else:
                    handle.write(block)

        await ctx.message.channel.send('Image saved!')
    else:
        await ctx.message.channel.send('format not supported!')
        await ctx.message.channel.send(':rage: :rage:')


# upload images from my pc in a random order
@client.command()
async def show(ctx):
    sans = list(p.glob('*.jpg'))
    leng = len(sans)
    rando = random.randint(0, leng)
    await ctx.channel.send(file=discord.File(sans[rando]))


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    amount = 2
    user = ctx.author
    await member.kick(reason=reason)
    await ctx.message.channel.send(f'{member.mention} has been kicked by {user.mention}')


@kick.error
async def kick_error(ctx, error: MissingPermissions):
    message = ctx.message
    if error:
        await message.channel.send(f'{error}')
        await message.channel.send(' :pensive: :pensive: :rage: ')


client.run('NzM1ODMyMDE2OTA5NzYyNjUw.Xxl-9w.khqhKrt_fwKJbii3ebZ3lp1y3jQ')