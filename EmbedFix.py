
import discord, discord.ui, json, random, time, logging, uuid
from discord.ext import commands
from discord import default_permissions
from datetime import datetime


with open('config.json', 'r') as f:
    config = json.load(f)
config_token_value = config['Token']
only_react_in_specific_channels = config['OnlySpecificChannels']
allowed_channels = config['AllowedChannels']
instagram_prefix = config['Instagram']
twitter_prefix = config['Twitter']
tiktok_prefix = config['TikTok']
enable_delete_button = config['EnableDeleteButton']
owner_id = config['OwnerID']
test_guild_id = config['TestGuildID']
# print(config_token_value)
# print("Instagram prefixes", instagram_prefix)
# print("Twitter prefixes", twitter_prefix)
# print("TikTok prefixes", tiktok_prefix)

# set bot intents

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)


def remove_oldest_id_if_needed_authors():
    with open('original_authors.json', 'r+') as f:
        data = json.load(f)
        if len(data['OriginalAuthors']) > 20:
            data['OriginalAuthors'].sort(key=lambda x: x['timestamp'])
            del data['OriginalAuthors'][0]
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)


def remove_oldest_id_if_needed_messages():
    with open('original_messages.json', 'r+') as d:
        data = json.load(d)
        if len(data['OriginalMessages']) > 20:
            data['OriginalMessages'].sort(key=lambda x: x['timestamp'])
            del data['OriginalMessages'][0]
            d.seek(0)
            d.truncate()
            json.dump(data, d, indent=4)


def add_id_to_list_authors(str):
    with open('original_authors.json', 'r+') as f:
        data = json.load(f)
        data['OriginalAuthors'].append({"ID": str, "timestamp": time.time()})
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)


def add_id_to_list_messages(str):
    with open('original_messages.json', 'r+') as d:
        data = json.load(d)
        data['OriginalMessages'].append({"ID": str, "timestamp": time.time()})
        d.seek(0)
        d.truncate()
        json.dump(data, d, indent=4)


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

class main_bot():
    @bot.event
    async def on_message(message):
        original_author_id = message.author.id
        original_message_id = message.id
        remove_oldest_id_if_needed_authors()
        remove_oldest_id_if_needed_messages()
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
        if str(message.guild) in test_guild_id:
            if 'test' in message.content.lower():
                # Generate a random color
                random_color = random.randint(0, 0xFFFFFF)
                print(f'#####\nRandom colour was selected for embeds: ', random_color, '\n#####')
                embed = discord.Embed(title=f'test',description=f'**test** : ``test``', color=random_color )
                await message.reply(embed=embed, mention_author=False)
                return
        # Check if the message contains one of the Instagram links
        for inprefix in instagram_prefix:
            if inprefix in message.content:
                add_id_to_list_authors(original_author_id)
                add_id_to_list_messages(original_message_id)
                fixedinstagram_link = message.content.replace(inprefix, 'https://www.ddinstagram.com/', 1)
                if enable_delete_button is True:
                    view = Confirm(message)
                    await message.reply(f'{fixedinstagram_link}', mention_author=False, view=view)
                    return
                else:
                    await message.reply(f'{fixedinstagram_link}', mention_author=False)
                    return
        for twprefix in twitter_prefix:
            if twprefix in message.content:
                add_id_to_list_authors(original_author_id)
                add_id_to_list_messages(original_message_id)
                fixedtwitter_link = message.content.replace(twprefix, 'https://www.fxtwitter.com/')
                if enable_delete_button is True:
                    view = Confirm(message)
                    await message.reply(f'{fixedtwitter_link}', mention_author=False, view=view)
                    return
                else:
                    await message.reply(f'{fixedtwitter_link}', mention_author=False)
                    return
        for tkprefix in tiktok_prefix:
            if tkprefix in message.content:
                add_id_to_list_authors(original_author_id)
                add_id_to_list_messages(original_message_id)
                fixedtiktok_link = message.content.replace(tkprefix, 'https://www.tnktok.com/')
                if enable_delete_button is True:
                    view = Confirm(message)
                    await message.reply(f'{fixedtiktok_link}', mention_author=False, view=view)
                    return
                else:
                    await message.reply(f'{fixedtiktok_link}', mention_author=False)
                    return
        else:
            return



class Confirm(main_bot, discord.ui.View):
    def __init__(self, message):
        super().__init__()
        self.message = message
        with open('original_authors.json', 'r') as g:
            original_authors_data = json.load(g)
            self.original_authors = [author['ID'] for author in original_authors_data['OriginalAuthors']]
            # print(f'#####\nOriginal Author IDs: ', self.original_authors, '\n#####')
        with open('original_messages.json', 'r') as d:
            original_messages_data = json.load(d)
            self.original_messages = [message['ID'] for message in original_messages_data['OriginalMessages']]
            # print(f'#####\nOriginal Message IDs: ', self.original_messages, '\n#####')
    @discord.ui.button(label='Delete Bot Message', style=discord.ButtonStyle.red)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        print(f'#####\nInteraction User ID: ', interaction.user.id, '\n#####')
        if interaction.user.id in self.original_authors:  # Check if the button was clicked by the original message author
            await interaction.message.delete()  # Delete the bot message
            await interaction.response.send_message('Bot message deleted!', ephemeral=True)
            return
        # Check if the user has the Manage Messages permission
        permissions = interaction.channel.permissions_for(interaction.user)
        if permissions.manage_messages:
            await interaction.message.delete()  # Delete the bot message
            await interaction.response.send_message('Bot message deleted!', ephemeral=True)
            return
    
    @discord.ui.button(label='Delete All Buttons', style=discord.ButtonStyle.grey)
    async def delete_buttons(self, button: discord.ui.Button, interaction: discord.Interaction):
        print(f'#####\nInteraction User ID: ', interaction.user.id, '\n#####')
        if interaction.user.id in self.original_authors: 
            # Stop the View to remove all buttons
            await interaction.message.edit(view=None)
            await interaction.response.send_message('All buttons deleted!', ephemeral=True)
            return
        # Check if the user has the Manage Messages permission
        permissions = interaction.channel.permissions_for(interaction.user)
        if permissions.manage_messages:
            # Stop the View to remove all buttons
            await interaction.message.edit(view=None)
            await interaction.response.send_message('All buttons deleted!', ephemeral=True)
            return
        
    @discord.ui.button(label='Delete Last Message', style=discord.ButtonStyle.green)
    async def delete_last_message(self, button: discord.ui.Button, interaction: discord.Interaction):
        print(f'#####\nInteraction User ID: ', interaction.user.id, '\n#####')
        if interaction.user.id in self.original_authors: 
            last_message_id = self.original_messages[-1]
            channel = interaction.channel
            message = await channel.fetch_message(last_message_id)
            await message.delete()
            await interaction.response.send_message('Last message deleted!', ephemeral=True)
            return
        # Check if the user has the Manage Messages permission
        permissions = interaction.channel.permissions_for(interaction.user)
        if permissions.manage_messages:
            last_message_id = self.original_messages[-1]
            channel = interaction.channel
            message = await channel.fetch_message(last_message_id)
            await message.delete()
            await interaction.response.send_message('Last message deleted!', ephemeral=True)
            return




@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")

@bot.command(description="Shows the bot source.") # this decorator makes a slash command
async def source(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"You can find the source code [here](https://github.com/Maccygoat/EmbedFix)", ephemeral=True)

@bot.command(description="Restarts the bot.")  # this decorator makes a slash command
@default_permissions(administrator=True)
async def restart(ctx):
    if str(ctx.author.id) in owner_id:
        with open('restart.txt', 'w') as f:
            f.write('restart')
        await ctx.respond("Restarting...", ephemeral=False)
        await bot.close()
    else:
        await ctx.respond(f"You do not have permission to use this command. \nThe Owner of this bot has been notified.\n <@{owner_id}>", ephemeral=False)
        return

bot.run(config_token_value)