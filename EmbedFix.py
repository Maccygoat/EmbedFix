
import discord, discord.ui, requests, re, json, random
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

# set bot intents

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)




@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

class main_bot():
    @bot.event
    async def on_message(message):
        original_author = message.author.id
        original_message = message.id
        print(f'Message from {message.author} in #{message.channel} in the {message.guild} Server \n{message.content} \n---')
        if message.author.id == bot.user.id:
            return
        if only_react_in_specific_channels is True:
            if str(message.channel.id) in allowed_channels:
                pass
            else:
                return
        if only_react_in_specific_channels is False:
            pass
        if 'test' in message.content.lower():
            # Generate a random color
            random_color = random.randint(0, 0xFFFFFF)
            print(f'#####\nRandom colour was selected for embeds: ', random_color, '\n#####')
            embed = discord.Embed(title=f'test',description=f'**test** : ``test``', color=random_color )
            await message.reply(embed=embed, mention_author=False)
        # Check if the message contains one of the Instagram links
        for prefix in instagram_prefix:
            if prefix in message.content:
                fixedinstagram_link = message.content.replace(prefix, 'https://www.ddinstagram.com/', 1)
                view = Confirm(message)
                await message.reply(f'{fixedinstagram_link}', mention_author=False, view=view)


class Confirm(main_bot, discord.ui.View):
    def __init__(self, message):
        super().__init__()
        self.message = message

    @discord.ui.button(label='Delete Bot Message', style=discord.ButtonStyle.red)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.message.author:  # Check if the button was clicked by the original message author
            await interaction.message.delete()  # Delete the bot message
            await interaction.response.send_message('Bot message deleted!', ephemeral=True)
        # Check if the user has the Manage Messages permission
        permissions = interaction.channel.permissions_for(interaction.user)
        if permissions.manage_messages:
            await interaction.message.delete()  # Delete the bot message
            await interaction.response.send_message('Bot message deleted!', ephemeral=True)
    
    @discord.ui.button(label='Delete All Buttons', style=discord.ButtonStyle.grey)
    async def delete_buttons(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.message.author: 
            # Stop the View to remove all buttons
            self.stop()
            await interaction.response.send_message('All buttons deleted!', ephemeral=True)
        # Check if the user has the Manage Messages permission
        permissions = interaction.channel.permissions_for(interaction.user)
        if permissions.manage_messages:
            # Stop the View to remove all buttons
            self.stop()
            await interaction.response.send_message('All buttons deleted!', ephemeral=True)

    # @discord.ui.button(label='Delete Original Message', style=discord.ButtonStyle.primary)
    # async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     if interaction.user == self.message.author:  # Check if the button was clicked by the original message author
    #         await self.message.delete()  # Delete the original message
    #         await interaction.response.send_message('Original message deleted!', ephemeral=True)
    #     # Check if the user has the Manage Messages permission
    #     permissions = interaction.channel.permissions_for(interaction.user)
    #     if permissions.manage_messages:
    #         await interaction.message.delete()  # Delete the bot message
    #         await interaction.response.send_message('Original message deleted!', ephemeral=True)


@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")

@bot.command(description="Shows the bot source.") # this decorator makes a slash command
async def source(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"You can find the source code [here](https://github.com/Maccygoat/EmbedFix)", ephemeral=True)

bot.run(config_token_value)