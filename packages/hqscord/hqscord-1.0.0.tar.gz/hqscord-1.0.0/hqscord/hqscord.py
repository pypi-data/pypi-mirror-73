# ----------------------------------------------#
# hqs.bot ©                                     #
# by phillip.hqs ∫ Thanks to alphaSnosh         #
# ----------------------------------------------#
from discord.ext import commands
import discord
import time

path = commands.Cog

cmd = commands.command()
listener = commands.Cog.listener
bot_has_role = commands.bot_has_role
bot_has_perm = commands.bot_has_permissions
user_has_role = commands.has_permissions
user_has_perm = commands.has_permissions


async def send(ctx, msg):
    await ctx.send(msg)

async def send_embed(ctx, embed):
    await ctx.send(embed=embed)

async def send_file(ctx, file):
    await ctx.send(file=discord.File(f'{file}'))

async def activity_game(self_bot, text):
    await self_bot.change_presence(activity=discord.Game(name=text))

async def activity_stream(self_bot, text, twitch_url):
    await self_bot.change_presence(activity=discord.Streaming(name=text, url=twitch_url))

async def activity_listen(self_bot, text):
    await self_bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))

async def activity_watch(self_bot, text):
    await self_bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))

async def active_activity_game(self_bot, sec, text1, text2, text3, text4):
    while True:
        await activity_game(self_bot, text1)
        time.sleep(sec)
        await activity_game(self_bot, text2)
        time.sleep(sec)
        await activity_game(self_bot, text3)
        time.sleep(sec)
        await activity_game(self_bot, text4)
        time.sleep(sec)

async def active_activity_stream(self_bot, sec, twitch_url, text1, text2, text3, text4):
    while True:
        while True:
            await activity_stream(self_bot, twitch_url, text1)
            time.sleep(sec)
            await activity_stream(self_bot, twitch_url, text2)
            time.sleep(sec)
            await activity_stream(self_bot, twitch_url, text3)
            time.sleep(sec)
            await activity_stream(self_bot, twitch_url, text4)
            time.sleep(sec)

async def active_activity_listen(self_bot, sec, text1, text2, text3, text4):
    while True:
        await activity_listen(self_bot, text1)
        time.sleep(sec)
        await activity_listen(self_bot, text2)
        time.sleep(sec)
        await activity_listen(self_bot, text3)
        time.sleep(sec)
        await activity_listen(self_bot, text4)
        time.sleep(sec)

async def active_activity_watch(self_bot, sec, text1, text2, text3, text4):
    while True:
        await activity_watch(self_bot, text1)
        time.sleep(sec)
        await activity_watch(self_bot, text2)
        time.sleep(sec)
        await activity_watch(self_bot, text3)
        time.sleep(sec)
        await activity_watch(self_bot, text4)
        time.sleep(sec)

async def join(channel):
    await channel.connect()

async def leave(ctx):
    await ctx.message.guild.voice_client.disconnect()

async def lock_textchannel(channel, ctx, reason):
    if ctx.guild.default_role not in channel.overwrites:
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False,
                                                                reason=reason)
        }
        await channel.edit(overwrites=overwrites)
    elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[
        ctx.guild.default_role].send_messages == None:
        overwrites = channel.overwrites[ctx.guild.default_role]
        overwrites.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites,
                                      reason=reason)
    else:
        overwrites = channel.overwrites[ctx.guild.default_role]
        overwrites.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites,
                                      reason=reason)

async def clear_messages(channel, amount):
    messages = []
    async for message in channel.history(limit=amount):
        messages.append(message)
    await channel.delete_messages(messages)

async def load_cog(self_bot, cog):
    self_bot.load_extension(cog)

async def load_cogs(self_bot, cogs):
    l = cogs
    for cog in cogs:
        self_bot.load_extension(f'{l}')

async def unload_cog(self_bot, cog):
    self_bot.unload_extension(cog)

async def unload_cogs(self_bot, cogs):
    l = cogs
    for cog in cogs:
        self_bot.unload_extension(f'{l}')

async def edit_nick(user, nick):
    await user.edit(nick=nick)

