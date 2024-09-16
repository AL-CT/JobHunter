# JobHunter

 A discord bot for easily finding job listings!

![example](/assets/example.png)

 ---

 ## Setup

 First, open your terminal or CMD in the root directory:
 ```
 cd JobHunter
 ```

Install the necessary requirements, using pip:
 ```
pip install -r requirements.txt
 ```

Setup the necessary configurations in the `settings.env` file:
 ```
# Deployment Variables
DISCORD_BOT_TOKEN=xxxxxxxxxxxxx
DISCORD_LOG_CHANNEL_ID=xxxxxxxxxxxxxxxx
LOOKUP_TIME_PERIODICITY=1800 #how often to check for new jobs in seconds
MAX_DB_SIZE=500 #number of entries to store

# Search Variables
SEARCH_TERM=graphic designer
LOCATION=New York, NY
MAX_RESULTS=25
PERIODICITY=24 # how long is ago was the job posted in hours
COUNTRY=USA
DISTANCE=50 # in miles
PROXIES=None
 ```

 It's possible to change these settings using a slash command, but you must first define `DISCORD_BOT_TOKEN` to get it running.

 Finally, start the program (WINDOWS USERS):
 ```
 py ./main.py
 ```

 **NOTE: Please make sure your bot has the necessary intents and permissions enabled in the [Discord Developer Portal](https://discord.com/developers/docs/intro)!**

---

## Usage

This program makes use of the [JobSpy](https://github.com/Bunsly/JobSpy) python library to gather jobs from various websites. Visit their page for a better understanding of the formatting of the available fields.

The program will periodically gather listings, store them in a .csv file, and post the ones not previously recorded to the selected channel. This is done automatically.

The following commands are available as well:

![commands](/assets/commands.png)

Different settings might be necessary depending on the country of search, as the bot was mainly developed for function within the USA.


