import discord,time
from responses import reply
import os
from config_sensitive import chk_tdy_holiday

if os.path.isfile("config_sensitive.py"):
    from config_sensitive import TOKEN, ID
else:
    from config import TOKEN, ID

async def send_msg(msg: str, user_msg: str, is_private: bool):
    try:
        resp = await reply(user_msg)
        resp = resp[:2000]
        await msg.author.send(resp) if is_private else await msg.channel.send(resp)
        if user_msg == "hi":
            time.sleep(2)
            await msg.channel.send(file=discord.File("images/hi.gif"))
        if "parking rates" in resp.lower():
            time.sleep(2)
            await msg.channel.send(file=discord.File("images/apu_map.jpeg"))
        if "next shuttle" in resp.lower():
            if await chk_tdy_holiday():
                time.sleep(3)
                await msg.channel.send("As today is holiday, please take note that the shuttle schedule may be revised.\
                                       \nPlease refer to APSpace or https://new.apu.edu.my/apu-holiday-schedule.")
    except Exception as error:
        print(error)
        await msg.channel.send("Something went wrong! Please try again.")

def bot_launch():
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f"{client.user} is running!")

    @client.event
    async def on_message(message):
        if ID and str(message.channel.id) not in ID:
            return
        else:
            if message.author.id == client.user.id:
                return
            username = str(message.author)
            
            user_msg = str(message.content)

            await send_msg(message, user_msg, False)

    client.run(TOKEN)