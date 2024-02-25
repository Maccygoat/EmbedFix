
import discord, requests, re



class __main__(discord.Client, discord.TextChannel):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


intents = discord.Intents.default()
intents.message_content = True

client = __main__(intents=intents)

tokenfile = open('config.json')
tokenfilecontents = tokenfile.read()
print(tokenfilecontents)
client.run(tokenfilecontents)