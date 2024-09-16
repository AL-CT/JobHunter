import asyncio

import loader
import job_database
import time, threading
import discord_bot

env = loader.Config()
job_db = job_database.JobDatabase()

def lookUpNewJobs():
    print("Starting new Job Search at: " + time.ctime())
    job_db.updateDB()
    for jb in job_db.temp_db:
        discord_bot.appendJob(jb)
    time.sleep(int(env.LOOKUP_TIME_PERIODICITY))

def runBot():
    discord_bot.client.run(env.DISCORD_BOT_TOKEN)

if __name__ == '__main__':
    discThread = threading.Thread(target=runBot).start()
    while True:
        lookUpNewJobs()
