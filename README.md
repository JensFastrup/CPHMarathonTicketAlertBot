# CPHMarathonTicketAlertBot
All tickets are sold out for Copenhagen Marathon 2025. There is no system notification system for resale of tickets. I made a bot that checks the page and notifies through Discord. 
Website: https://secure.onreg.com/onreg2/bibexchange/?eventid=6591

Pull repo and do the following.

## Setup
### Discord
  1. Open the Discord Developer Portal:
  Visit https://discord.com/developers/applications and log in using your Discord account.
  
  2. Create a New Application:
  Click on the "New Application" button in the top-right corner.
  Then name the application.
 
  3. Set Up the Bot:
  In the left-hand sidebar of the application page, click on the "Bot" tab.
  Click the "Add Bot" button.

  4. Copy the Bot Token:
  In the "Build-A-Bot" section, copy "TOKEN." Save this, as you will use it to authenticate the bot in your script later.

  5. Add bot to server:
     In the left-hand sidebar, go to the "OAuth2" tab and click on "URL Generator.".
     In the "Scopes" section, select bot.
     Scroll down to the "Bot Permissions" section and select the permissions your bot needs. For the script in question, you will need:
     *Send Messages* – to allow the bot to post messages in a channel.
     Copy the generated URL at the bottom of the page.
     Invite the bot to the server by following the generated URL thorugh a browser address bar.
     (Consider making a dedicated server for this)

   6. Get Channel ID
      Thorugh enabling developer mode in discord, through user settings, get the channel ID, by the text-channel you want to use. From here it is just running the code. 
       
### Code
1. pip install requests beautifulsoup4 discord.py python-dotenv


2. create .env file in root folder with: 
  - DISCORD_TOKEN = {YOUR TOKEN}
  - CHANNEL_ID ={YOUR CHANNEL ID}

3 . Run script in terminal/cmd:
  - python TicketAlertBot.py

(potentially as *pythonw* as a background process)

## Considerations
Set this up on a virtual machine on a virtual private server, for it to run 24/7 - never miss a chance for a ticket :) 

  


