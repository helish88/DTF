import discord
from discord.ext import commands
import random
import json
import os
import string
import datetime
from datetime import date, time
import aiohttp
import traceback
import asyncio
from tags import DTF_TAGS
from dtf_subsites_english import all_dtf_subsites_english


DTF_TOKEN = os.environ["DTF_TOKEN"]

class utils(commands.Cog, name='utils'):
    def __init__(self, bot):
        self.bot = bot
    # async def cog_check(self, ctx):
    #     if ctx.guild is None:
    #         await ctx.author.send(embed=discord.Embed(color=discord.Color.red(), description= f'{ctx.author.mention} команда не работает в ЛС'))
    #         return False
    @commands.command(aliases = ["дтф"])
    @commands.bot_has_permissions(send_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def dtf(self, ctx, *, type:str = None):
            if not type:
                type =  all_dtf_subsites_english[random.choice(list(all_dtf_subsites_english.keys()))]
            else:
                if type.lower() not in list(all_dtf_subsites_english.keys()):
                    return await ctx.send(embed = discord.Embed(color = ctx.author.top_role.color, description = f"{ctx.author.mention} такого подсайта нет, что бы узнать все подсайты,напишите {ctx.prefix}подсайты"))
            type =  all_dtf_subsites_english[type.lower()]
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.dtf.ru/v1.8/timeline/{type}/recent?apikey={DTF_TOKEN}') as r:
                    if r.status == 200:
                        js = await r.json()

            number = 0
            title = js["result"][int(number)]['title']
            url = js["result"][int(number)]['url']
            blocks=js["result"][int(number)]['blocks']

            likes = js["result"][int(number)]['likes']['count']
            text_description=""
            for block in blocks:
                if block['type'] == "text":
                    textapi = block['data']['text']
                    text_description="".join(textapi)
            for block in blocks:
                if block['type'] == "link":
                    sitelinks = block['data']['link']["data"]["url"]
            if js["result"][int(number)]['cover']:
                coverurl = js["result"][int(number)]['cover']['thumbnailUrl']
                msg1 = await ctx.send(embed = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title = title, description = f"[{text_description}]({url})", url = url).set_image(url=coverurl+"jpg").set_footer(text=f"Запросил: {ctx.author.display_name} категория {type} * powered by DTF.ru | 👍 {likes}", icon_url = ctx.author.avatar_url))
            else:
                msg1 = await ctx.send(embed = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title = title, description = f"[{text_description}]({url})", url = url).set_footer(text=f"Запросил: {ctx.author.display_name} категория {type} * powered by DTF.ru | 👍 {likes}", icon_url = ctx.author.avatar_url))
            def checkuser(reaction, user):
                return user == ctx.author and reaction.message.id == msg1.id
            reactions = ["⏮️", "◀️", "▶️", "⏭️", "❌"]
            for reaction in reactions:
                await msg1.add_reaction(reaction)
            flag = 0
            while flag == 0:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=100, check=checkuser)
                except asyncio.TimeoutError:
                    flag = 1
                    await msg1.clear_reactions()
                else:
                    if str(reaction) == "▶️":
                        if number < len(js["result"])-1:
                            number += 1
                            title = js["result"][int(number)]['title']
                            likes = js["result"][int(number)]['likes']['count']
                            url = js["result"][int(number)]['url']
                            blocks=js["result"][int(number)]['blocks']
                            text_description=""
                            coverurl = js["result"][int(number)]['cover']['thumbnailUrl'] if js["result"][int(number)]["cover"] else None
                            for block in blocks:
                                if block['type'] == "text":
                                    textapi = block['data']['text']
                                    text_description="".join(textapi)
                            for block in blocks:
                                if block['type'] == "link":
                                    sitelinks = block['data']['link']["data"]["url"]
                                    sitelinksembed = sitelinks
                                else:
                                    sitelinksembed = "https://dtf.ru/"
                            await asyncio.sleep(1)
                            if coverurl:
                                await msg1.edit(embed = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title = title, description = f"[{text_description}]({url})", url = sitelinksembed if sitelinksembed else None).set_image(url=coverurl+"jpg")\
                                .set_footer(text=f"Запросил: {ctx.author.display_name} категория {type} * powered by DTF.ru | 👍 {likes}", icon_url = ctx.author.avatar_url))
                            else:
                                await msg1.edit(embed = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title = title, description = f"[{text_description}]({url})", url = sitelinksembed if sitelinksembed else None)\
                                .set_footer(text=f"Запросил: {ctx.author.display_name} категория {type} * powered by DTF.ru | 👍 {likes}", icon_url = ctx.author.avatar_url))
                            await reaction.remove(ctx.author)
                        else:
                            await reaction.remove(ctx.author)
                    if str(reaction) == "◀️":
                        if number > 0:
                            await asyncio.sleep(1)
                            number -= 1
                            title = js["result"][int(number)]['title']
                            likes = js["result"][int(number)]['likes']['count']
                            url = js["result"][int(number)]['url']
                            blocks=js["result"][int(number)]['blocks']
                            text_description=""
                            coverurl = js["result"][int(number)]['cover']['thumbnailUrl'] if js["result"][int(number)]["cover"] else None
                            for block in blocks:
                                if block['type'] == "text":
                                    textapi = block['data']['text']
                                    text_description="".join(textapi)
                            for block in blocks:
                                if block['type'] == "link":
                                    sitelinks = block['data']['link']["data"]["url"]

                            sitelinksembed = sitelinks
                            if coverurl:
                                await msg1.edit(embed = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title = title, description = f"[{text_description}]({url}) )", url = sitelinksembed if sitelinksembed else None).set_image(url=coverurl+"jpg")\
                                .set_footer(text=f"Запросил: {ctx.author.display_name} категория {type} * powered by DTF.ru | 👍 {likes}", icon_url = ctx.author.avatar_url))
                            else:
                                await msg1.edit(embed = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title = title, description = f"[{text_description}]({url}) )", url = sitelinksembed if sitelinksembed else None)\
                            .set_footer(text=f"Запросил: {ctx.author.display_name} категория {type} * powered by DTF.ru | 👍 {likes}", icon_url = ctx.author.avatar_url))
                            await asyncio.sleep(1)
                            await reaction.remove(ctx.author)
                        else:
                            await reaction.remove(ctx.author)

                    if str(reaction) == "⏭️":
                        number = len(js["result"])-1
                        title = js["result"][int(number)]['title']
                        likes = js["result"][int(number)]['likes']['count']
                        url = js["result"][int(number)]['url']
                        blocks=js["result"][int(number)]['blocks']
                        text_description=""
                        coverurl = js["result"][int(number)]['cover']['thumbnailUrl'] if js["result"][int(number)]["cover"] else None
                        for block in blocks:
                            if block['type'] == "text":
                                textapi = block['data']['text']
                                text_description="".join(textapi)
                        for block in blocks:
                            if block['type'] == "link":
                                sitelinks = block['data']['link']["data"]["url"]
                                sitelinksembed = sitelinks
                            else:
                                sitelinksembed = "https://dtf.ru/"
                        await asyncio.sleep(1)
                        if coverurl:
                            await msg1.edit(embed = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title = title, description = f"[{text_description}]({url})", url = sitelinksembed if sitelinksembed else None).set_image(url=coverurl+"jpg")\
                            .set_footer(text=f"Запросил: {ctx.author.display_name} категория {type} * powered by DTF.ru | 👍 {likes}", icon_url = ctx.author.avatar_url))
                        else:
                            await msg1.edit(embed = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title = title, description = f"[{text_description}]({url})", url = sitelinksembed if sitelinksembed else None)\
                            .set_footer(text=f"Запросил: {ctx.author.display_name} категория {type} * powered by DTF.ru | 👍 {likes}", icon_url = ctx.author.avatar_url))
                        await reaction.remove(ctx.author)
                    else:
                        await reaction.remove(ctx.author)


                    if str(reaction) == "⏮️":
                        print(len(js["result"]))
                        number = 0
                        title = js["result"][int(number)]['title']
                        likes = js["result"][int(number)]['likes']['count']
                        url = js["result"][int(number)]['url']
                        blocks=js["result"][int(number)]['blocks']
                        text_description=""
                        coverurl = js["result"][int(number)]['cover']['thumbnailUrl'] if js["result"][int(number)]["cover"] else None
                        for block in blocks:
                            if block['type'] == "text":
                                textapi = block['data']['text']
                                text_description="".join(textapi)
                        for block in blocks:
                            if block['type'] == "link":
                                sitelinks = block['data']['link']["data"]["url"]
                                sitelinksembed = sitelinks
                            else:
                                sitelinksembed = "https://dtf.ru/"
                        await asyncio.sleep(1)
                        if coverurl:
                            await msg1.edit(embed = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title = title, description = f"[{text_description}]({url})", url = sitelinksembed if sitelinksembed else None).set_image(url=coverurl+"jpg")\
                            .set_footer(text=f"Запросил: {ctx.author.display_name} категория {type} * powered by DTF.ru | 👍 {likes}", icon_url = ctx.author.avatar_url))
                        else:
                            await msg1.edit(embed = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title = title, description = f"[{text_description}]({url})", url = sitelinksembed if sitelinksembed else None)\
                            .set_footer(text=f"Запросил: {ctx.author.display_name} категория {type} * powered by DTF.ru | 👍 {likes}", icon_url = ctx.author.avatar_url))
                        await reaction.remove(ctx.author)
                    else:
                        await reaction.remove(ctx.author)

                    if str(reaction) == "❌":
                        flag = 1
                        await msg1.delete()
    @dtf.error
    async def dtf_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description= f'{ctx.author.mention} вы сможете использовать эту команду через {error.retry_after:.1f} секунд'), delete_after=16)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.author.send(embed=discord.Embed(color=discord.Color.red(), description= f'{ctx.author.mention} у меня нет права писать в канале **{ctx.channel}**'))

    @commands.command(aliases = ["подсайты"])
    @commands.bot_has_permissions(send_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def subsites(self, ctx):
        msg1 = await ctx.send(embed = discord.Embed(color = ctx.author.top_role.color, description = "\n".join(DTF_TAGS[:43])))
        def checkuser(reaction, user):
            return user == ctx.author and reaction.message.id == msg1.id
        reactions = ["◀️", "▶️", "❌"]
        for reaction in reactions:
            await msg1.add_reaction(reaction)
        flag = 0
        while flag == 0:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=100, check=checkuser)
            except asyncio.TimeoutError:
                flag = 1
                await msg1.delete()
            else:
                if str(reaction) == "▶️":
                    await reaction.remove(ctx.author)
                    await msg1.edit(embed = discord.Embed(color = ctx.author.top_role.color, description = "\n".join(DTF_TAGS[44:])))
                if str(reaction) == "◀️":
                    await reaction.remove(ctx.author)
                    await msg1.edit(embed = discord.Embed(color = ctx.author.top_role.color, description = "\n".join(DTF_TAGS[:43])))
                if str(reaction) == "❌":
                    flag = 1
                    await msg1.delete()
def setup(bot):
    bot.add_cog(utils(bot))
    print('utils is loaded.')
