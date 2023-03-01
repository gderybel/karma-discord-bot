import discord
import myclient
import config_parser

intents = discord.Intents.default()
intents.message_content = True
client = myclient.MyClient(intents=intents)

token = config_parser.parse_configuration()

client.run(token)
