import discord
from discord.ext import tasks
import datetime
from aufteilen import split_large_file
import os
import json
import requests
from zusammenfügen import combine_chunks

bot = discord.Bot()


@tasks.loop(seconds=10.0)
async def slow_count():
    print("loop")

    files = os.listdir("./in")
    if files != []:
        for file in files:
            split_large_file("./in/" + file, "chunks", 10)

            for guild in bot.guilds:
                for channel in guild.channels:
                    if type(channel) == discord.channel.TextChannel:
                        message_ids = []
                        for discord_file_pth in os.listdir("./chunks"):
                            discord_file = discord.File("./chunks/" + discord_file_pth)
                            message = await channel.send(file=discord_file)

                            message_ids.append(message.id)
                            os.remove("./chunks/" + discord_file_pth)
                        os.remove("./in/" + file)

                        with open("files.json", "r+") as data_file:
                            try:
                                json_file = json.load(data_file)
                            except:
                                json_file = {}
                        json_file[file] = message_ids

                        with open("files.json", "w") as data_file:
                            data_file.write(json.dumps(json_file, indent=4))

    with open("files_to_get.txt", "r+") as file:
        if file.read() == "":
            pass
        else:
            files_to_get = file.readlines()

            with open("files.json", "r") as data_file:
                json_file = json.load(data_file)
            

            for file_to_get in files_to_get:
                for guild in bot.guilds:
                    for channel in guild.channels:
                        if type(channel) == discord.channel.TextChannel:
                            chunk_count = 1
                            for msg_id in json_file[file_to_get]:
                                message = await channel.fetch_message(msg_id)     
                                print(message)
                                print(message.attachments[0].url)
                                request = requests.get(message.attachments[0].url)
                                with open("./chunks to combine/chunk_" + str(chunk_count), "wb") as chunk_file:
                                    chunk_file.write(request.content)
                                chunk_count += 1
                        file.write("")
                        combine_chunks("./chunks to combine", "out/neue_datei.txt")





@slow_count.after_loop
async def after_slow_count():
    print('done!')



@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    # print(discord.utils.get(await channel.history(limit=100).flatten(), author=bot.user))
    slow_count.start()

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")

bot.run("MTE3ODYwNzcyMTc2MzgzMTg0OQ.GgMu54.Q8ZkYo3VHpKf68GxW6X8fNVjBfTrzHimFu5X7g") # run the bot with the token