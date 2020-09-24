import discord
from discord.ext import commands
import random
import os
import string
import asyncio
import traceback

permissions_translate = {"create_instant_invite":"создать приглашение",
                         "kick_members":"кикать участников сервера",
                         "ban_members":"банить частников сервера",
                         "administrator":"администратор сервера",
                         "manage_channels":"управление каналами",
                         "manage_guild":"управление серверов",
                         "add_reactions":"добавлять реакции(емоджи)",
                         "view_audit_log":"видеть логи аудита",
                         "stream":"стримить",
                         "read_messages":"читать сообщения",
                         "send_messages":"отправлять сообщения",
                         "send_messages":"управлять сообщениями",
                         "embed_links":"отправлять ссылки",
                         "attach_files":"отправлять файлы",
                         "read_message_history":"читать историю сообщ.",
                         "external_emojis":"использовать внешние емоджи",
                         "connect":"подключаться к войс каналу",
                         "speak":"говорить в войс каналов(играть)",
                         "move_members":"перемещать участников",
                         "manage_nicknames":"управлять никами(менять ник другим участником)",
                         "manage_roles":"управление ролями"}

class errors(commands.Cog, name='errors'):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
          pass

        if isinstance(error, commands.CommandOnCooldown):
            pass
        if isinstance(error, commands.BadArgument):
            pass
        if isinstance(error, commands.MissingPermissions):
            pass
        if isinstance(error, commands.MissingRequiredArgument):
            pass
        if isinstance(error, commands.BadUnionArgument):
            pass
        if isinstance(error, commands.NotOwner):
            pass
        if isinstance(error, commands.CheckFailure):
            pass
        if isinstance(error, discord.NotFound):
            pass
        if isinstance(error, discord.Forbidden):
            await ctx.send(permissions_translate[str(",".join(error.missing_perms))])
        else:
            channel = self.bot.get_channel(687985406599364628)
            errors = traceback.format_exception(type(error), error, error.__traceback__)
            await ctx.send(error, delete_after=30)

            print(errors)



def setup(bot):
    bot.add_cog(errors(bot))
    print('errors is loaded.')
