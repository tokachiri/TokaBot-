from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, has_permissions, MissingPermissions
import discord
import random 
import json
import os
import asyncio
from itertools import cycle
from io import BytesIO
import keep_alive
import praw

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='',
                     password='',
                     user_agent='')

bot = commands.Bot(command_prefix="t!")
bot.sniped_messages = {}
bot.remove_command("help")

kiss = [
  "https://media2.giphy.com/media/bGm9FuBCGg4SY/giphy.gif","https://i.pinimg.com/originals/e3/4e/31/e34e31123f8f35d5c771a2d6a70bef52.gif",
  "https://acegif.com/wp-content/uploads/anime-kiss-m.gif",
  "https://i.imgur.com/So3TIVK.gif",
  "https://media1.giphy.com/media/oHZPerDaubltu/giphy.gif"
]
grabify = [
    "lovebird.guru", "trulove.guru", "dateing.club", "otherhalf.life",
    "shrekis.life", "headshot.monster", "gaming-at-my.best",
    "progaming.monster", "yourmy.monster", "screenshare.host",
    "imageshare.best", "screenshot.best", "gamingfun.me", "catsnthing.com",
    "mypic.icu", "catsnthings.fun", "curiouscat.club", "joinmy.site",
    "fortnitechat.site", "fortnight.space", "freegiftcards.co", "stopify.co",
    "leancoding.co", "grabify.link", "you.tube.com"
]

dice = [
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
]

status = cycle(["t!help | Made by Toka#8008",
                "t!help | Stop Reading This Status.",
                "t!help | 😏",
                "t!help | There are Secret Commands!",
                "t!help | This Bot is Terr- I mean Awesome!",
                "t!help | This Bot was Written in Python!",
                "t!help | OwO",
                "t!help | ZzzzzzZzzzzZzzz",
                "t!help | Who Woke me Up From My Nap!",
                "t!help | Don't Question Me.",
                "t!help | Quack!",
                "t!help | w o w",
             ])


@bot.event
async def on_ready():
  print("This Bot is Up and Running!")
  await bot.change_presence(status=discord.Status.online)
  change_status.start()


keep_alive.keep_alive()

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

# Snipe Command

@bot.event
async def on_message_delete(message):
    bot.sniped_messages[message.guild.id] = (message.content,                                           message.author,
                                             message.channel.name,
                                             message.created_at)


@bot.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = bot.sniped_messages[
            ctx.guild.id]

    except:
        await ctx.channel.send("Nothing to snipe dummy.")
        return
    embed = discord.Embed(description=contents,
                          color=ctx.author.color,
                          timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}",
                     icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in #{channel_name}")

    await ctx.send(embed=embed)

# Ping Command

@bot.command()
async def ping(ctx):
  await ctx.send(f"Pong! `{round(bot.latency * 1000)}`ms")

# Purge Command

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

# Anti Bypass
@bot.listen("on_message")
async def el_message(message):
  for word in grabify:
    if word in message.content:
      await message.channel.purge(limit=1)
      msg = await message.channel.send(
          f"Nobody falls for those grabify links stupid. <@{message.author.id}>"
          )

# Say Command

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, arg):
      await ctx.channel.purge(limit=1)
      say_embed = discord.Embed(color=ctx.author.color,)
      say_embed.add_field(name="Somebody has Said -",value=f"{arg}")
      await ctx.send(embed=say_embed)

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!(Missing Permmisions)")

# Rick Roll Command

@bot.command()
async def rickroll(ctx, arg):
  await ctx.channel.purge(limit=1)
  await ctx.send(f'You\'ve Been RickRolled by {ctx.message.author.mention}, {arg}!')
  await ctx.send('https://media4.giphy.com/media/Vuw9m5wXviFIQ/giphy.gif')

# Kiss Command
@bot.command()
async def kiss(ctx, arg):
  await ctx.send(f'{ctx.message.author.mention} has given a kiss to {arg}!')
  await ctx.send('https://i.imgur.com/So3TIVK.gif')

# Dale Yeah! Command
@bot.command()
async def DaleYeah(ctx):
  await ctx.send("Denson says Dale Yeah!")
  await ctx.send("https://media.discordapp.net/attachments/779472056949276672/808478079319932968/Yoshi.gif?width=225&height=225")

# Rock Paper Scissors Command
@bot.command()
async def rps(ctx):
    rpsGame = ['rock', 'paper', 'scissors']
    await ctx.send(f"Rock, paper, or scissors? Choose wisely...")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

    user_choice = (await bot.wait_for('message', check=check)).content

    comp_choice = random.choice(rpsGame)
    if user_choice == 'rock' or 'Rock':
        if comp_choice == 'rock':
            await ctx.send(f'Well, that was weird. We tied.')
        elif comp_choice == 'paper':
            await ctx.send(f'Nice try, but I won that time!!')
        elif comp_choice == 'scissors':
            await ctx.send(f"Aw, you beat me. It won't happen again!")

    elif user_choice == 'paper' or 'Paper':
        if comp_choice == 'rock':
            await ctx.send(f'The pen beats the sword? More like the paper beats the rock!')
        elif comp_choice == 'paper':
            await ctx.send(f'Oh, wacky. We just tied. I call a rematch!!')
        elif comp_choice == 'scissors':
            await ctx.send(f"Aw man, you actually managed to beat me.")

    elif user_choice == 'scissors' or 'Scissors':
        if comp_choice == 'rock':
            await ctx.send(f'HAHA!! I JUST CRUSHED YOU!! I rock!!')
        elif comp_choice == 'paper':
            await ctx.send(f'Bruh. >: |')
        elif comp_choice == 'scissors':
            await ctx.send(f"Oh well, we tied.")   
    rps_choices = discord.Embed(colour = discord.Colour.red()
    )
    rps_choices.set_author(name="Rock, Paper, Scissors Results:")
    rps_choices.add_field(name="Computer Choice -", value=f"{comp_choice}")
    rps_choices.add_field(name="Your Choice -", value=f"{user_choice}")
    await ctx.send(embed=rps_choices)

# Nick Command
@bot.command(pass_context=True)
@commands.has_permissions(manage_nicknames=True)
async def setnick(ctx, member: discord.Member, *, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')

@setnick.error
async def setnick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

# Slowmode Command
@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

# Ban Command
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban (ctx, member:discord.User=None, *, reason =None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself.. Just leave the server..")
        return
    if reason == None:
        reason = "For being a jerk!"
    message = f"You have been banned from {ctx.guild.name} for {reason}"
    await member.send(message)
    ban_embed = discord.Embed(colour = discord.Colour.red()
    )
    ban_embed.add_field(name="Banned!",value=f"{member} was banned from {ctx.guild.name} for {reason}!")
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=ban_embed)
    await member.ban(reason = reason)

@ban.error
async def ban_error(error, ctx):
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await bot.send_message(ctx.message.channel, text)

# UnBan Command
@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            unban_embed = discord.Embed(colour = discord.Colour.green()
            )
            unban_embed.add_field(name="Unbanned!",value=f"{user} has been unbanned!")
            ctx.send(embed=unban_embed)
            return

# Kick Command
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick (ctx, member:discord.User=None, *, reason =None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot kick yourself.. Just leave the server..")
        return
    if reason == None:
        reason = "For being a jerk!"
    message = f"You have been kicked from {ctx.guild.name} for {reason}"
    await member.send(message)
    # await ctx.guild.ban(member, reason=reason)
    kick_embed = discord.Embed(colour = discord.Colour.red()
    )
    kick_embed.add_field(name="Kicked!",value=f"{member} was kicked from {ctx.guild.name} for {reason}!")
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=kick_embed)
    await member.kick(reason = reason)

# CoinFlip Command
@bot.command(aliases=['cf','coin'])
async def coinflip(ctx):
  coinsides = ['Heads', 'Tails']
  await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

# Random Integer Command
@bot.command()
async def randint(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.content.isdigit() and \
               msg.channel == ctx.channel

    await ctx.send("Type a number.")
    msg1 = await bot.wait_for("message", check=check)
    await ctx.send("Type a second, larger number.")
    msg2 = await bot.wait_for("message", check=check)
    x = int(msg1.content)
    y = int(msg2.content)
    if x < y:
        value = random.randint(x,y)
        await ctx.send(f"You got {value}.")
    else:
        await ctx.send(":warning: Please ensure the first number is smaller than the second number.")


    
# Welcome and Leave
@bot.event
async def on_member_join(member: discord.Member):
    join_embed = discord.Embed(
        color = discord.Color.magenta(),
    )
    join_embed.set_author(name="Welcome!")
    join_embed.add_field(name=f"Welcome to {member.guild.name}! Make sure to Read The Rules! Failure to follow the Rules will result in punishments.")
    join_embed.set_thumbnail(url="https://media.discordapp.net/attachments/774404924075016232/809127716690984980/image0.png?width=452&height=452")
    await member.send(embed=join_embed)

# Avatar Command
@bot.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url

    av_embed = discord.Embed(colour = discord.Colour.blurple()
    )
    av_embed.set_image(url=userAvatarUrl)
    await ctx.send(embed=av_embed)

# 8ball Command
@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
  responses = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes - definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."
  ]
  _8ball = discord.Embed(colour=discord.Colour.greyple()
  )
  _8ball.set_author(name="The Magical EightBall!")
  _8ball.add_field(name="Question:", value=f"{question}")
  _8ball.add_field(name="Answer:", value=f"{random.choice(responses)}")
  await ctx.send(embed=_8ball)

# Dice Command
@bot.command()
async def roll(ctx, sides, amount):
  try:
    sides = int(sides.split("d")[1])
    rolls_list = []
    for number in range(int(amount)):
       # 1 is the minimum number the dice can have
       rolls_list.append(random.randint(1, sides))
    rolls = ", ".join(str(number) for number in rolls_list)
    await ctx.send("Your dice rolls were: " + rolls)
  except Exception as e:
    # You should catch different exceptions for each problem and then handle them
    # Exception is too broad
    print(e)
    await ctx.send("Incorrect format for sides of dice (try something like \"t!roll d6 1\").")

# Invite Link
@bot.command()
async def invite(ctx):
  invite_em = discord.Embed(colour = discord.Colour.blurple()
  )
  invite_em.set_author(name="Invite Me To Your Server!",url="https://discord.com/api/oauth2/authorize?client_id=806921203294011483&permissions=1547037942&scope=bot")
  invite_em.add_field(name="Link",value="https://discord.com/api/oauth2/authorize?client_id=806921203294011483&permissions=1547037942&scope=bot")

  await ctx.send(embed=invite_em)

# Server-Info Command
@bot.command()
async def serverinfo(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Server Information",
      description=description,
      color=discord.Color.blue()
    )
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)

  await ctx.send(embed=embed)

@bot.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)

@bot.command()
async def aww(ctx):
    subreddit = reddit.subreddit("Aww")
    all_subs = []
    top = subreddit.top(limit=100)
    for submission in top:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title=name)
    em.set_image(url=url)
    await ctx.send(embed=em)

@bot.command()
async def meme(ctx):
    subreddit = reddit.subreddit("dankmemes")
    all_subs = []
    top = subreddit.top(limit=100)
    for submission in top:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title=name)
    em.set_image(url=url)
    await ctx.send(embed=em)


# Help Commands
@bot.command()
async def help(ctx):
  author = ctx.message.author

  help_tableofcontents_embed = discord.Embed(colour = discord.Colour.blue()
  )
  help_tableofcontents_embed.set_author(name="BOT PREFIX = t!")
  help_tableofcontents_embed.add_field(name="1 - Moderation",value="Do t!h1 to figure out all of the Moderation Commands and what they do! Some of these commands require some permissions in order to be used!")
  help_tableofcontents_embed.add_field(name="2 - Fun",value="Do t!h2 to figure out all of the Fun commands.")
  help_tableofcontents_embed.add_field(name="3 = Pictures",value="Do t!h3 to figure out all of the image commands!")
  help_tableofcontents_embed.set_footer(text="There are lots for Hidden Commands! Look on Toka's Github for the Bot's Code!")

  await ctx.send(embed=help_tableofcontents_embed)

# Help Command - Moderation
@bot.command(aliases=['mod','moderation','Moderation','Mod'])
async def h1(ctx):
  author = ctx.message.author

  mod_help = discord.Embed(colour = discord.Colour.red()
  )
  mod_help.set_author(name="Moderation Commands")
  mod_help.add_field(name="Ban",value="Bans a Mentioned User.")
  mod_help.add_field(name="Kick",value="Kicks a Mentioned User.")
  mod_help.add_field(name="Purge",value="Purges the Chat.")
  mod_help.add_field(name="Unban", value="UnBans a User. (Format - BannedUser#0000)")
  mod_help.add_field(name="Slowmode", value="Sets the slowmode in seconds.")
  mod_help.add_field(name="SetNick", value="Sets a Nickname for another user!")
  mod_help.add_field(name="Avatar", value="Display's A User's Avatar!")

  await ctx.send(embed=mod_help)

# Help Command - Fun
@bot.command(aliases=['fun','Fun'])
async def h2(ctx):
  author = ctx.message.author

  fun_help = discord.Embed(colour = discord.Colour.green()
  )
  fun_help.set_author(name="Fun Commands")
  fun_help.add_field(name="Say",value="Forces the bot to say things against it's will.")
  fun_help.add_field(name="RickRoll",value="We/'re no strangers to love, You know the Rules and so do I, A full commitment is what I'm thinking of... RickRoll someone!")
  fun_help.add_field(name="RPS",value="Play Rock Paper Scissors with this Bot. (There are some bugs)")
  fun_help.add_field(name="RandInt", value="Choose 2 numbers and generate a Random Number between both of them.")
  fun_help.add_field(name="CoinFlip", value="Flips a Coin for you!")
  fun_help.add_field(name="8ball", value="Ask the Magical Eightball a Question!🎱")
  fun_help.add_field(name="Dice", value="Rolls a Dice with a specified amount of sides, and multiple dices. Example - t!roll d6 1. In this, you are rolling one six sided die.")
  await ctx.send(embed=fun_help)

# Help Command - Pictures
@bot.command(aliases=['Pics','pics','Pictures','pictures','memes'])
async def h3(ctx):
  author = ctx.message.author

  memes_help = discord.Embed(colour = discord.Colour.orange()
  )
  memes_help.set_author(name="Picture Commands")
  memes_help.add_field(name="Meme",value="Pulls a DankMeme from r/dankememes.")
  memes_help.add_field(name="Aww",value="Pulls a cute picture from r/awww.")

  await ctx.send(embed=memes_help)
bot.run('BOT TOKEN UWU')
