from dbm import error

import discord
import validators
from discord import option

import loader
import job_database
import datetime
from discord.ext import tasks

env = loader.Config()

intents = discord.Intents.default()
client = discord.Bot(intents=intents)

log_channel = None
jobs_to_send = []

@client.event
async def on_ready():
    global log_channel
    print(f'We have logged in as {client.user}')
    log_channel = await client.fetch_channel(env.DISCORD_LOG_CHANNEL_ID)
    send_all_jobs.start()

@tasks.loop(seconds=120)
async def send_all_jobs():
    #print("Sending job postings.")
    global jobs_to_send
    for job in jobs_to_send:
        await sendJob(job)
    jobs_to_send = []

async def sendJob(job):
    try :
        embed = discord.Embed(
            title=job.title,
            url=job.url if validators.url(job.url) else "",
            description= "```markdown\n" + (str(job.description) if len(str(job.description)) <= 1250 else job.description[:1250] + "...").replace("\n\n\n", "\n\n") + "```",
            color=discord.Colour.blurple() if job.remote else discord.Colour.green(),
        )

        embed.add_field(name="Salary Type", value=job.salary_type, inline=True)
        embed.add_field(name="Salary Interval", value=str(job.salary_interval[0]) + " - " + str(job.salary_interval[1]) + " (USD)", inline=True)

        embed.add_field(name='\u200b', value='\u200b', inline=True)

        embed.add_field(name="Location", value=job.location, inline=True)
        embed.add_field(name="Remote", value="Yes" if job.remote else "No", inline=True)

        embed.add_field(name='\u200b', value='\u200b', inline=True)

        t = job.date.strftime("%I:%M%p on %B %d, %Y") if isinstance(job.date, datetime.datetime) else str(job.date)

        embed.set_footer(text="Posted on " + job.site + " at " + t, icon_url='https://cdn.discordapp.com/attachments/901556415682998282/1283826600701460510/image.png?ex=66e46831&is=66e316b1&hm=217b118edfb77107b91e17dd8b8ec52f15a7c9e16fa2f545dbc2d143ebd159aa&')  # footers can have icons too
        embed.set_author(name=job.company, icon_url=job.company_photo if validators.url(job.company_photo) else "")
        #embed.set_thumbnail(url=job.company_photo if validators.url(job.company_photo) else "")
        #embed.set_image(url="https://example.com/link-to-my-banner.png")

        await log_channel.send(content=None, embed=embed)  # Send the embed with some text
    except Exception as e:
        print("Error sending listing: " + e)
        await log_channel.send(content="Error sending job listing. To view all jobs, please export the Database using the `\export_jobdb` command.")


@client.command(description="Test the embed formatting for Job Posts.")
async def test_format(ctx):

    t = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

    jb = job_database.Job()
    jb.id = -1
    jb.site = 'Testing Site'
    jb.url = 'https://manishkandpal-random-gif-generator.vercel.app'
    jb.title = 'Job Title'
    jb.company = 'TestInc.'
    jb.location = 'Cloud'
    jb.date = t
    jb.salary_type = 'Hourly'
    jb.salary_interval = (15.0, 35.0)
    jb.remote = False
    jb.description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras aliquet nisl sed mattis fermentum. Nullam ac nibh magna. Quisque sit amet dictum neque. Maecenas pretium lacus hendrerit leo convallis, eu tincidunt purus cursus. Vestibulum placerat aliquam lorem a congue. Sed est lorem, congue ultricies magna sed, mattis pretium ligula. Aenean ultrices bibendum tellus non venenatis. Nullam euismod justo libero, in rutrum neque sagittis non. Ut libero ipsum, gravida eget arcu ac, ultrices auctor erat. Aenean massa diam, iaculis vel ullamcorper et, aliquam vitae lectus. Pellentesque vitae magna mattis, feugiat arcu in, hendrerit dolor. Fusce non ligula condimentum, porttitor dolor id, gravida diam. Duis ac erat porttitor, auctor velit vel, facilisis nulla. Sed cursus luctus quam sit amet consequat. Sed malesuada nisi at mi euismod, hendrerit iaculis mauris tempus. Curabitur aliquam facilisis sem, ut sagittis eros iaculis vitae.Sed vitae lorem ac neque varius maximus vel quis quam. Donec quis leo congue, tincidunt purus ac, aliquet nisi. Mauris mi mauris, bibendum sit amet sapien sed, facilisis sollicitudin sapien. Nunc sit amet semper massa. Aliquam erat volutpat. Suspendisse fringilla est vitae lacus ultricies, sit amet varius nisl finibus. Pellentesque ornare facilisis nisi, ut maximus metus imperdiet in. Curabitur euismod, ipsum quis ornare vulputate, eros metus rhoncus urna, et blandit risus nisi nec sem. Donec et orci vehicula, dapibus arcu ut, rutrum ex.Integer dignissim odio at purus sodales, id varius justo varius. Aliquam sodales ex vel commodo volutpat. Nulla congue, metus sit amet porttitor lacinia, odio quam hendrerit ex, id tristique tortor erat at massa. Nam a pharetra felis. Quisque eget blandit massa, id hendrerit ipsum. Donec eu lacus dapibus, blandit neque non, auctor ex. Ut aliquet pharetra tellus, id rhoncus quam. Sed vitae facilisis diam. Mauris iaculis arcu ac sapien ornare, in ultrices lectus condimentum. Aliquam sit amet luctus lorem. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ut fringilla eros. Mauris semper, mi quis sagittis dictum, eros ante auctor mi, quis semper nisl velit vel erat. Duis posuere faucibus orci vel pulvinar.Duis tincidunt ornare sem, quis hendrerit elit consequat porta. Fusce sit amet eros metus. Aliquam aliquet metus vel risus eleifend fermentum. Morbi eget turpis venenatis orci porttitor vestibulum ut et orci. Aliquam justo massa, blandit eleifend felis eget, dignissim aliquet odio. Mauris rhoncus mattis sapien non consequat. Pellentesque sagittis sagittis molestie. Sed sed leo sed augue dictum eleifend id egestas est. Duis vel placerat est. Proin erat sapien, lobortis ac elit sodales, cursus eleifend risus.Proin pulvinar magna vel posuere blandit. Donec consectetur odio at lacinia pellentesque. Mauris tincidunt rutrum purus in rutrum. Suspendisse pulvinar ipsum dui, et blandit purus feugiat sed. Nulla risus eros, egestas sed euismod ac, rhoncus eget libero. Suspendisse justo augue, imperdiet id mattis ut, convallis vel justo. Aliquam aliquet maximus massa, sed convallis tellus convallis eu. Maecenas mattis risus quis nibh tempus, id euismod libero pharetra. Donec est justo, aliquet a tempor eu, posuere a neque. Praesent sit amet neque nulla. Quisque nec erat eu neque vehicula lobortis vel quis enim. Duis commodo mauris ut metus vestibulum, ac imperdiet nunc consectetur.Etiam nec turpis sit amet dui imperdiet accumsan at non neque. Cras bibendum risus risus, quis tempus arcu tincidunt ac. Vivamus imperdiet leo elit, ac vulputate dui posuere in. Cras ut justo congue, porttitor ante a, congue leo. Donec auctor diam odio. Donec lacus erat, pretium in elit id, iaculis consectetur magna. Mauris tempus scelerisque nulla vel consectetur.Quisque eros felis, efficitur eu venenatis quis, dignissim vitae sem. Phasellus auctor nisi ante, eget volutpat velit euismod ut. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean non erat consectetur urna efficitur accumsan. Mauris consectetur leo orci, id accumsan sem interdum eu. Integer ut'
    jb.company_url = 'discord.com'
    jb.company_photo = 'https://cdn.discordapp.com/attachments/901556415682998282/1283811272244068435/discord-logo-icon-editorial-free-vector.png?ex=66e459eb&is=66e3086b&hm=3d81129e493cf2aabd10145e46b8eace258583d8232629dfe77c05cb2dfd055a&'

    await sendJob(jb)

    await ctx.respond(f"Test complete.")

@client.command(description="Change configurations for setup and search results.")
@option("channel_id",str,description="ID of the channel to send the listings in")
@option("periodicity",int,description="How often to search for new jobs, in seconds")
@option("db_size",int,description="Maximum size of the database")
@option("search_term",str,description="Name of the positions to search for")
@option("location",str,description="Location of the positions to search for (format e.g., \"New York, NY\"")
@option("max_results",int,description="Maximum number of jobs to look for per site")
@option("job_age",int,description="Maximum time in hours since the long jobs ware posted")
@option("country",str,description="Country of the jobs to look for (format e.g., \"US\"")
@option("max_distance",int,description="Maximum distance of the jobs from the selected location in miles")
async def change_configs(ctx, channel_id, periodicity, db_size, search_term, location, max_results, job_age, country, max_distance):
    if channel_id is not None:
        env.update_value("DISCORD_LOG_CHANNEL_ID", channel_id)
    if periodicity is not None:
        env.update_value("LOOKUP_TIME_PERIODICITY", periodicity)
    if db_size:
        env.update_value("MAX_DB_SIZE", db_size)
    if search_term is not None:
        env.update_value("SEARCH_TERM", search_term)
    if location is not None:
        env.update_value("LOCATION", location)
    if max_results is not None:
        env.update_value("MAX_RESULTS", max_results)
    if job_age is not None:
        env.update_value("PERIODICITY", job_age)
    if country is not None:
        env.update_value("COUNTRY", country)
    if max_distance is not None:
        env.update_value("DISTANCE", max_distance)
    await ctx.respond(f"Changes successfully applied.")

@client.command(description="Export the database to .csv file")
async def export_db(ctx):
    file = discord.File("database_export.csv")
    await ctx.respond(file=file, content="Database export successful.")

@client.command(description="Show the current bot configurations")
async def show_configs(ctx):
    text = (f"**Current configurations**:\n```markdown\nLog Channel ID: {env.DISCORD_LOG_CHANNEL_ID}\nPeriodicity: {env.LOOKUP_TIME_PERIODICITY}\nDB Size: {env.MAX_DB_SIZE}\nSearch Term: {env.SEARCH_TERM}"
            f"\nLocation: {env.LOCATION}\nMax Results: {env.MAX_RESULTS}\nJob Age: {env.PERIODICITY}\nCountry: {env.COUNTRY}\nMax Distance: {env.DISTANCE}```")
    await ctx.respond(content=text)

def appendJob(jb):
    global jobs_to_send
    jobs_to_send.append(jb)