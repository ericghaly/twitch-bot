import os
from twitchio.ext import commands
import random
import openai
import asyncio
import requests

# set up the bot
bot = commands.Bot(
    token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

openai.api_key = os.environ['OPEN_AI']

model_engine = 'text-davinci-002'

command_list = ['!socials', '!discord', '!twitter', '!youtube', '!instagram', '!insult', '!ask']

@bot.event
async def event_ready():
    print(f"{os.environ['BOT_NICK']} is online!")


@commands.cooldown(rate=1, per=60, bucket=commands.Bucket.channel)    
@bot.command(name='insult')
async def insult(ctx):
    prompt = [
            f"Insult {ctx.message.author.name}. Insult options can include their height, weight, balding status, smell, and social status. Be as vulgar and innapropriate as possible, include profanity. Not all options for the insult need to be used.", 
            f"Insult {ctx.message.author.name} by making up a horrible story about them. Have them be the loser in their story and have everyone dislike them.", 
            f"Sarcasticly thank {ctx.message.author.name} for their wonderfully horrible contributions to not only this channel, but society as a whole. And list things that would be better off without them. Make sure it shows how useless they are.",
            f"Childishly insult {ctx.message.author.name} in the most stereotypical way possible."
    ]
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt[random.randint(0,len(prompt)-1)],
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.9,
    )
    await ctx.reply(completions.choices[0].text)
    

@commands.cooldown(rate=1, per=60, bucket=commands.Bucket.channel)    
@bot.command(name='ask')
async def ask(ctx, *arg):
    prompt = ' '.join(arg)
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2048,
        n=2,
        stop=None,
        temperature=0.7,
    )
    await ctx.reply(completions.choices[0].text)
    

@bot.command(name='shoutout')
async def shoutout(ctx, arg):
    if ctx.author.name == 'washedgamerbro':
        await ctx.channel.send(f'Go follow {arg} over at twitch.tv/{arg}')
    else:
        print('Invalid user attempted to use shoutout command.')
       
    
@commands.cooldown(rate=1, per=120, bucket=commands.Bucket.channel)    
@bot.command(name='help')
async def help(ctx):
    response = 'The current commands are: '
    for i in command_list:
        response += i + ' '
    await ctx.reply(response)
    
    
@commands.cooldown(rate=1, per=120, bucket=commands.Bucket.channel)    
@bot.command(name='socials')
async def socials(ctx):
    await ctx.reply('You can find all my socials at linktr.ee/washedgamerbro')    
    
    
@commands.cooldown(rate=1, per=120, bucket=commands.Bucket.channel)    
@bot.command(name='discord')
async def discord(ctx):
    await ctx.reply('You can join the Discord at discord.gg/BBcgf5NwUm')
    
    
@commands.cooldown(rate=1, per=120, bucket=commands.Bucket.channel)    
@bot.command(name='twitter')
async def twitter(ctx):
    await ctx.reply('You can follow my Twitter at https://twitter.com/washedgamerbro')    

    
@commands.cooldown(rate=1, per=120, bucket=commands.Bucket.channel)    
@bot.command(name='youtube')
async def youtube(ctx):
    await ctx.reply('You can subscribe my YouTube at https://www.youtube.com/@washedgamerbro')     


@commands.cooldown(rate=1, per=120, bucket=commands.Bucket.channel)    
@bot.command(name='instagram')
async def instagram(ctx):
    await ctx.reply('You can follow my Instagram at https://www.instagram.com/washedgamerbro/')    
    
    
bot.run()
#pipenv run python twitch_bot.py