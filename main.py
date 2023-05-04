import discord
import config
import re
from discord.ext import commands

description = '''A discord bot that assists families decide on what foods to eat during the week. This works better in hand with the paprika app.'''


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=config.bot_settings['prefix'], description=description, intents=intents)

class BotActions:
    def __init__(self, message):
        self.message = message

    def react():
        self.message.add_reaction()

# Functions
def is_admin():
    def predicate(ctx):
        return config.user_settings['admin_allowed'] and commands.has_permissions(administrator=True)
    return commands.check(predicate)




# Commands

@commands.check_any(commands.has_role(config.user_settings['allowed_role']), is_admin()) 
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
@commands.check_any(commands.has_role(config.user_settings['allowed_role']), is_admin()) 
async def on_message(message):
    if message.channel.name == config.message_settings['suggestions_channel']:
        await add_reaction




bot.run(config.bot_settings['token'])