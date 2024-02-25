
import discord, discord.ui, requests, re, json
from discord.ext import commands


# open and parse config.json

with open('config.json', 'r') as f:
    config = json.load(f)
config_token_value = config['Token']
only_react_in_specific_channels = config['OnlySpecificChannels']
allowed_channels = config['AllowedChannels']
instagram_prefix = config['Instagram']
twitter_prefix = config['Twitter']
tiktok_prefix = config['TikTok']
# print(config_token_value)
print("Instagram prefixes", instagram_prefix)
print("Twitter prefixes", twitter_prefix)
print("TikTok prefixes", tiktok_prefix)

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    if only_react_in_specific_channels is True:
        if str(message.channel.id) in allowed_channels:
            pass
        else:
            return
    if only_react_in_specific_channels is False:
        pass
    if 'test' in message.content.lower():
        embed = discord.Embed(title=f'test',description=f'**test** : ``test``', color=0x001fff )
        await message.reply(embed=embed, mention_author=False)

@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")

@bot.command(description="Shows the bot source.") # this decorator makes a slash command
async def source(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"You can find the source code [here](https://github.com/Maccygoat/EmbedFix)", ephemeral=True)

bot.run(config_token_value)