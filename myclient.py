import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discord.message):
        print(dir(message))
        if message.content == "/karma":
            print(message.author)
