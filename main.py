import discord
from discord.ext import tasks
from functions.aufteilen import split_large_file
from functions.zusammenfügen import combine_chunks
import os
import json
import requests

paths = ["./in/", "./out/", "./chunks/", "./chunks_to_combine/"]

for dir_path in paths:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

bot = discord.Bot()

def extract_number(file_name):
    return int(''.join(filter(str.isdigit, file_name)))




@tasks.loop(seconds=1.0)
async def slow_count():
    if not os.path.exists("./in/"):
        os.makedirs("./in/")
    
    files = os.listdir("./in/")
    if files != []:
        for file in files:
            folder_path = file.split("@@@")
            folder_path.pop()
            folder_path = "/".join(folder_path)
            folder_path = folder_path.replace("@@@", "/") + "/"

            file_name = file.split("@@@")
            file_name = file_name[-1]
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

                        with open("./files" + folder_path + "files.json", "r+") as data_file:
                            try:
                                json_file = json.load(data_file)
                            except:
                                json_file = {}
                        json_file[file_name] = message_ids

                        with open("./files" + folder_path + "files.json", "w") as data_file:
                            data_file.write(json.dumps(json_file, indent=4))

    with open("files_to_get.txt", "r") as file:
        file_content = file.read()
        empty = file_content == ""
        file.seek(0)
        lines = file.readlines()
        
        files_to_get = [line.split("###")[1].strip() for line in lines]
        paths_to_get = [line.split("###")[0].strip() for line in lines]
        
    if empty:
        pass
    else:
        
        hallo = range(len(files_to_get))
        for index in range(len(files_to_get)):
            with open(paths_to_get[index], "r") as data_file:
                json_file = json.load(data_file)
            for guild in bot.guilds:
                for channel in guild.channels:
                    if type(channel) == discord.channel.TextChannel:
                        chunk_count = 1
                        for msg_id in json_file[files_to_get[index]]:
                            message = await channel.fetch_message(msg_id)     
                            print(message)
                            print(message.attachments[0].url)
                            request = requests.get(message.attachments[0].url)
                            with open("./chunks_to_combine/chunk_" + str(chunk_count), "wb") as chunk_file:
                                chunk_file.write(request.content)
                            chunk_count += 1
                        
                        combine_chunks("./chunks_to_combine", f"out/{files_to_get[index]}")
        with open("files_to_get.txt", "wb"):
            pass    



@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="free cloud"))
    slow_count.start()


if __name__ == '__main__':
    bot.run("") 
