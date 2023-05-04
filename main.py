import discord
import config
from discord.ext import commands

description = 'A discord bot that assists families decide on what foods to eat during the week. This works better in hand with the paprika app.'


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=config.bot_settings['prefix'], description=description, intents=intents)

class Button(discord.ui.View):
    @discord.ui.button(label="Finalize", style=discord.ButtonStyle.green)
    async def green_button(self, interaction: discord.Integration, button: discord.ui.Button):
        finalize_channel = bot.get_channel(config.message_settings['finalize_channel_id'])
        await interaction.message.delete()
        await finalize_channel.send(interaction.message.content)


    
class BotActions:
    def __init__(self, message):
        # Re-send message as a bot to attach button
        self.message = message

    async def remove(self):
        await self.message.delete()

    async def resend_message(self):
        self.bots_message = await self.message.channel.send(f"<@{self.message.author.id}> " + self.message.content, view=Button())

    async def react(self):
        for x in config.reaction_settings['emojis']:
            await self.bots_message.add_reaction(x)
    
        

# Functions
def is_admin():
    def predicate(ctx):
        return config.user_settings['admin_allowed'] and commands.has_permissions(administrator=True)
    return commands.check(predicate)
# Events

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
@commands.check_any(commands.has_role(config.user_settings['allowed_role']), is_admin(), ) 
async def on_message(message):
    if message.channel.name == config.message_settings['suggestions_channel'] and message.author:
        if message.author.bot: # does not affect bot's own message
            return
        response_message = BotActions(message)
        await response_message.resend_message()
        await response_message.react()
        await response_message.remove()

bot.run(config.bot_settings['token'])
