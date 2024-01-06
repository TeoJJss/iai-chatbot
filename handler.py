import discord
import responses
import os
import speech_recognition as sr

if os.path.isfile("config_sensitive.py"):
    from config_sensitive import TOKEN, ID
else:
    from config import TOKEN, ID

async def send_msg(msg: str, user_msg: str, is_private: bool):
    try:
        resp = await responses.reply(user_msg)
        await msg.author.send(resp) if is_private else await msg.channel.send(resp)
        if user_msg == "hi":
            await msg.channel.send(file=discord.File("images/hi.gif"))
    except Exception as error:
        print(error)
        return "Something went wrong! Please try again. "

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
            if message.attachments:
                attachment = message.attachments[0]
                voice_message = await attachment.read()

                audio_data = sr.AudioData(voice_message, sample_rate=48000, sample_width=2)

                text = convert_voice_to_text(audio_data)

                # print(f"User {username} message to {client.user}:", text)
                user_msg = text
            else:
                user_msg = str(message.content)

            # print(f"User {username} message to {client.user}:", user_msg)

            await send_msg(message, user_msg, False)

    def convert_voice_to_text(audio_data):
        recognizer = sr.Recognizer()
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""

    client.run(TOKEN)