import os
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks
from dotenv import load_dotenv  # Import the load_dotenv function

# Load environment variables from the .env file
load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')  # Get the token from the .env file
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))   # Get the channel ID from the .env file

# URL of the ticket resale page
URL = 'https://secure.onreg.com/onreg2/bibexchange/?eventid=6591'

# Set up the Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Variable to track ticket availability status
ticket_notified = False

# Function to check ticket availability
def check_ticket_availability():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for the specific text on the page
    page_text = soup.get_text()
    no_tickets_message = "Der er ikke nogen startnumre til salg i øjeblikket. Prøv igen lidt senere."
    
    # If the specific text is not found, a ticket might be available
    if no_tickets_message not in page_text:
        return True
    return False

# Task to periodically check for ticket availability
@tasks.loop(minutes=5)
async def ticket_check():
    global ticket_notified
    if check_ticket_availability():
        if not ticket_notified:  # Only notify if not already notified
            channel = client.get_channel(CHANNEL_ID)
            await channel.send(f'Ticket available! Check the page here: {URL}')
            ticket_notified = True  # Set the flag to avoid repeated notifications
    else:
        ticket_notified = False  # Reset the flag if tickets are no longer available

# Event to run once the bot is ready
@client.event
async def on_ready():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('Bot has started and is now monitoring ticket availability.')
    print(f'Logged in as {client.user}')
    ticket_check.start()

# Function to send a message when the bot stops
async def bot_shutdown():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('Bot is shutting down.')

# Graceful exit handler
try:
    # Run the Discord bot
    client.run(DISCORD_TOKEN)
except KeyboardInterrupt:
    # Handle when the script is interrupted (e.g., Ctrl+C)
    client.loop.run_until_complete(bot_shutdown())
    client.loop.stop()
