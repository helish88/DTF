import discord
from discord.ext import commands, tasks
import logging
import random
import json
import os
import sys
import string
import asyncio
import traceback

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    f.close()
    return prefixes[str(message.guild.id)]



bot = commands.Bot(command_prefix = get_prefix)
# bot.remove_command('help')

@bot.event
async def on_ready():

    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

initial_extensions = ['cogs.utils', 'cogs.errors']

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            traceback.print_exc()

@bot.command()
async def test(ctx):
    await ctx.send("test ok")

#Когда бот первый раз заходит на сервер
@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefixes[str(guild.id)] = '!'

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


#меняем префикс
@bot.command(aliases=['префикс', 'prefix'])
@commands.bot_has_permissions(send_messages=True)
@commands.has_permissions(manage_roles=True)
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)


        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        f.close()
    #await ctx.message.delete()
    await ctx.send(f'Ваш новый префикс: `{prefix}`')

@changeprefix.error
async def changeprefix_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(color=discord.Color.red(), description= f'{ctx.author.mention} Укажите префикс'))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=discord.Embed(color=discord.Color.red(), description= f'{ctx.author.mention} Укажите символ префикс  к примеру \n {ctx.prefix}pefix !'))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(color=discord.Color.red(), description= f'{ctx.author.mention} У вас нет прав!'))
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.author.send(embed=discord.Embed(color=discord.Color.red(), description= f'{ctx.author.mention} у меня нет права писать в том канале'))


bot.run(os.environ["DTF_BOT"])
