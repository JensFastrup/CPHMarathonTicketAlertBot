import os
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks
from dotenv import load_dotenv  

load_dotenv()

# Discord Configuration, set the below variables in .env.    
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')  
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))   
URL = 'https://secure.onreg.com/onreg2/bibexchange/?eventid=6591'

intents = discord.Intents.default()
client = discord.Client(intents=intents)

ticket_notified = False

# Presumably, if this text is not available, then there should be a ticket available. 
def check_ticket_availability():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    page_text = soup.get_text()
    no_tickets_message = "Der er ikke nogen startnumre til salg i øjeblikket. Prøv igen lidt senere."
    
    if no_tickets_message not in page_text:
        return True
    return False

@tasks.loop(minutes=5)
async def ticket_check():
    global ticket_notified
    if check_ticket_availability():
        if not ticket_notified:  
            channel = client.get_channel(CHANNEL_ID)
            await channel.send(f'Ticket available! Check the page here: {URL}')
            ticket_notified = True  
    else:
        ticket_notified = False  

@client.event
async def on_ready():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('Bot has started and is now monitoring ticket availability.')
    print(f'Logged in as {client.user}')
    ticket_check.start()

async def bot_shutdown():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('Bot is shutting down.')

try:
    client.run(DISCORD_TOKEN)
except KeyboardInterrupt:
    client.loop.run_until_complete(bot_shutdown())
    client.loop.stop()
