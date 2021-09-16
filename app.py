from threading import Timer
from threading import *
import os
import sys
import threading
import discord
import time
import requests
import asyncio
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('Discord_Token')
ChannelName = os.getenv('OWO_Name')
ClientID = os.getenv('Client_id')
ClientSecret = os.getenv('Client_secret')
TTvToken = os.getenv('TTv-Token')

client = discord.Client()


@client.event
async def on_ready():
    print("Should say hello")
    channel = await client.fetch_channel(os.getenv('Channel_id'))
    await channel.send("機器人已進入頻道")


@client.event
async def send_msg(embed):
    channel = await client.fetch_channel(os.getenv('Channel_id'))
    await channel.send(embed=embed)


ChannelStatus = False


async def Check_Online():
    global ChannelStatus
    await client.wait_until_ready()

    while True:
        result = requests.get(
            url="https://api.twitch.tv/helix/streams?user_login=" + ChannelName, headers={
                "Client-Id": ClientID,
                "authorization": "Bearer " + TTvToken
            })

        try:
            data = result.json()["data"][0]
            GameName = data["game_name"]

            if not ChannelStatus and data["type"] == 'live':
                ChannelStatus = True
                embed = discord.Embed(
                    title="開台啦!", description=data["user_name"] + " 已經開台拉")
                embed.add_field(name="實況標題", value=data["title"])
                embed.add_field(name="正在遊玩", value=GameName)
                embed.add_field(name="觀看人數", value=data["viewer_count"])

                await send_msg(embed)
        except:
            if ChannelStatus:
                ChannelStatus = False
                embed = discord.Embed(
                    title="悲報!", description="OWO主播 已經關台了"
                )

                await send_msg(embed)

        await asyncio.sleep(1)


if __name__ == "__main__":
    # Check_Online()
    client.loop.create_task(Check_Online())
    client.run(TOKEN)
