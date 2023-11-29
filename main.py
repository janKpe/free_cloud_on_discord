import discord
from discord.ext import tasks
from functions.aufteilen import split_large_file
from functions.zusammenfügen import combine_chunks
import os
import json
import requests


bot = discord.Bot()

def extract_number(file_name):
    return int(''.join(filter(str.isdigit, file_name)))


@tasks.loop(seconds=1.0)
async def slow_count():
    files = os.listdir("./in/")
    if files != []:
        for file in files:
            split_large_file("./in/" + file, "chunks", 10)
            for guild in bot.guilds:
                for channel in guild.channels:
                    if type(channel) == discord.channel.TextChannel:
                        message_ids = []
                        discord_files = os.listdir("./chunks/")
                        discord_files = sorted(discord_files, key=extract_number)
                        for discord_file_pth in discord_files:
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

    with open("files_to_get.txt", "r") as file:
        file_content = file.read()
        empty = file_content == ""
        file.seek(0)
        files_to_get = [line.strip() for line in file.readlines()]
        
    if empty:
        pass
    else:
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
                            with open("./chunks_to_combine/chunk_" + str(chunk_count), "wb") as chunk_file:
                                chunk_file.write(request.content)
                            chunk_count += 1
                        
                        combine_chunks("./chunks_to_combine", f"out/{file_to_get}")
        with open("files_to_get.txt", "wb"):
            pass    



@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="free cloud"))
    slow_count.start()


if __name__ == '__main__':
    bot.run("") 
