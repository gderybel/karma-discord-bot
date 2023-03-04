from os import getcwd, path, walk
from fnmatch import filter as fnfilter
from math import ceil
from datetime import datetime
import discord
from discord.ext import commands
from discord.utils import get
import config_parser

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Define the bot is ready to handle commands
    """
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game("I'm back."))

@bot.command(name='karma')
async def karma(context: commands.context.Context, subcommand: str = None, parameter1: str = None):
    """Main bot funtion

    Parameters
    ----------
    context : commands.context.Context
        The context (provided by discord)
    subcommand : str, optional
        The sub command : play | list | leave, by default None
    parameter1 : str, optional
        A parameter that can be used for sound definition or pagination, by default None
    """
    if subcommand == "play" and parameter1:
        await play(context, parameter1)
    elif subcommand == "list":
        if not parameter1 or parameter1 == "0":
            parameter1 = "1"
        try:
            parameter1 = int(parameter1)
        except ValueError:
            parameter1 = 1
        await list_available_sounds(context, parameter1)
    elif subcommand == "leave":
        await leave(context)
    else:
        print(f"\
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \
SUCCESS\tkarma help invoked by \
{str(context.author)} ({context.author.id}).\
")
        await context.reply(f"""
Here are the available commands :

{bot.command_prefix}karma help -> show this menu
{bot.command_prefix}karma play [sound] -> play the given sound
{bot.command_prefix}karma list [page:optional]-> list available sounds
{bot.command_prefix}karma leave -> Karma leaves the voice channel
""")

async def play(context: commands.context.Context, sound: str):
    """Joins a user channel and play a sound

    Parameters
    ----------
    context : commands.context.Context
        The context, provided by discord
    sound : str
        The sound to play
    """
    file_name = f"{getcwd()}/sounds/{sound}.mp3"

    if not path.exists(file_name):
        print(f"\
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \
ERROR\tkarma play invoked by \
{str(context.author)} ({context.author.id}).\
")
        return await context.reply(
            'This sound does not exist, please use \'/karma list\' to list available sounds.'
        )
    else:
        try:
            bot_voice_channel = get(bot.voice_clients, guild=context.guild)
            if bot_voice_channel and bot_voice_channel.is_connected():
                await bot_voice_channel.move_to(context.author.voice.channel)
            else:
                bot_voice_channel = await context.author.voice.channel.connect()
        except (discord.ClientException, discord.DiscordException):
            print(f"\
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \
ERROR\tkarma play invoked by \
{str(context.author)} ({context.author.id}).\
")
            return await context.reply('Failed to connect to the voice channel!')

        sound_stream = discord.FFmpegPCMAudio(file_name)
        bot_voice_channel.play(sound_stream)
    print(f"\
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \
SUCCESS\tkarma play invoked by \
{str(context.author)} ({context.author.id}).\
")

async def list_available_sounds(context: commands.context.Context, page: int):
    """List all available sounds, includes mp3 files in project_root/sounds/

    Parameters
    ----------
    context : commands.context.Context
        The context, provided by Discord
    page : int
        The page to display
    """
    folder_path = f"{getcwd()}/sounds/"
    pattern = '*.mp3'

    available_sounds = []

    for _, _, files in walk(folder_path):
        for filename in fnfilter(files, pattern):
            if filename.count('.') == 1:
                available_sounds.append(f"- {filename.replace('.mp3', '')}")

    paged_available_sounds = available_sounds[page*10-10:page*10]

    if len(paged_available_sounds) <= 0:
        print(f"\
            {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \
            ERROR\tkarma list invoked by \
            {str(context.author)} ({context.author.id}).\
        ")
        return await context.reply("Invalid list page.")
    else:
        available_sounds_text = '\n'.join(
            [f'{available_sound}' for available_sound in paged_available_sounds]
        )
        await context.reply(f"""
Here's a list of available sounds :

{available_sounds_text}

Page {page}/{ceil(len(available_sounds)/10)}, You can display the others by specifying the page e.g : {bot.command_prefix}karma list 2
""")
    print(f"\
        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \
        SUCCESS\tkarma list invoked by \
        {str(context.author)} ({context.author.id}).\
    ")

async def leave(context: commands.context.Context):
    """Leaves the voice channel

    Parameters
    ----------
    context : commands.context.Context
        The context (provided by Discord)
    """
    if context.voice_client:
        print(f"\
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \
SUCCESS\tkarma leave invoked by \
{str(context.author)} ({context.author.id}).\
")
        await context.voice_client.disconnect()
    else:
        print(f"\
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \
ERROR\tkarma leave invoked by \
{str(context.author)} ({context.author.id}).\
")
        await context.reply("I am not currently connected to a voice channel.")

token = config_parser.parse_configuration()

bot.run(token)
