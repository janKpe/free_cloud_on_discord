import discord
from discord.ext import tasks
import datetime

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@tasks.loop()
async def slow_count(seconds=5.0, count=5):

    for guild in client.guilds:
        print(type(guild))
        for Category in guild.channels:
            print(type(Category))
            await Category.send("jo")
            for channel in Category.channels:
                print(type(channel))
                if type(channel) == discord.TextChannel:
                
                    await channel.send(datetime.datetime.now())
                    print("gesendet")


@slow_count.after_loop
async def after_slow_count():
    print('done!')

slow_count.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('ist dominik gay'):
        await message.channel.send('ja!')
        
    else:
        await message.channel.send('Hello!')


client.run('MTE3ODYwNzcyMTc2MzgzMTg0OQ.GgMu54.Q8ZkYo3VHpKf68GxW6X8fNVjBfTrzHimFu5X7g')