import discord
import os
import telebot

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
DISCORD_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
DISCORD_CHANNEL_ID = None

discord_client = discord.Client()
telegram_bot = telebot.TeleBot(TELEGRAM_TOKEN)

@telegram_bot.message_handler(content_types=['text'])
def receive_message(message):
    if discord_client.is_ready() and DISCORD_CHANNEL_ID is not None:
        discord_channel = discord_client.get_channel(int(DISCORD_CHANNEL_ID))
        discord_channel.send(f"Message from Telegram: {message.text}")

@discord_client.event
async def on_ready():
    global DISCORD_CHANNEL_ID
    print(f"Logged in as {discord_client.user}")
    DISCORD_CHANNEL_ID = (lambda a: a if a != "" else None)(open('DISCORD_CHANNEL').read())

@discord_client.event
async def on_message(message):
    if message.content.startswith("/setchannel") and message.author.guild_permissions.administrator:
        global DISCORD_CHANNEL_ID
        DISCORD_CHANNEL_ID = message.content.split()[1]
        await message.channel.send(f"Discord channel set to {DISCORD_CHANNEL_ID}")
    elif message.content.startswith("/setchannel") and not message.author.guild_permissions.administrator:
        await message.channel.send("You do not have permission to use this command.")

discord_client.run(DISCORD_TOKEN)
telegram_bot.polling()
