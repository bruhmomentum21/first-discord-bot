from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions
import discord
import asyncio
import random
import requests
import uuid
from pathlib import Path


p = Path('.')

call = ['based,','cringe!','tututut']
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
    await message.channel.send(f'{message.author.mention}: said "{message.content}" in #{message.channel}. deleted at {message.channel} ')

@client.command(name='list_members')
async def reaction(ctx: discord.message):
    guild = ctx.guild
    message = ctx.message
    await ctx.channel.send(f'members in this server so far: {len(guild.members)}')
    for I in range(len(guild.members)):
        await message.author.send(guild.members[I])

@client.command(name='call')
async def based(ctx):
    edit = await ctx.message.channel.send('calling based department')
    await asyncio.sleep(3)
    await edit.edit(content = call[random.randint(0,1)])


@client.command()
async def attach(ctx):

    f = ctx.message.attachments[0]

    if f.url.endswith(".png") or f.url.endswith(".jpg"):
        with open(f'{uuid.uuid4()}.jpg', 'wb') as handle:
            response = requests.get(f.url, stream=True)

            if not response.ok:
                print (response)
            else:
                handle.write(response.iter_content(1024))
    else:
        await ctx.message.channel.send('format not supported!')
        await ctx.message.channel.send(':rage: :rage:')

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason = None):
    amount = 2
    user = ctx.author

    if reason == '':
            ctx.message.channel.send(member + ' you need to put a reason')
    else:
        shrek = await member.kick(reason=reason)
        await ctx.message.channel.send(f'{member} has been kicked by {user}')

@kick.error
async def kick_error(ctx, error : MissingPermissions):
    message = ctx.message
    if error:
        await message.channel.send('Unepic error detected')
        await message.channel.send(' :pensive: :pensive: :rage: ')




client.run('client token here')

