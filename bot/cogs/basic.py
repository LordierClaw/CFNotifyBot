from discord import Embed
from discord.ext import commands
from .utils.ContestManager import ContestManager

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.targetChannels = []

    @commands.command(name="contest", description="Get information about the upcoming contest")
    async def contest(self, ctx):
        id, name, duration, startTime, relativeTime = ContestManager.getUpcomingInfor()
        contestUrl = "https://codeforces.com/contest/" + str(id)
        contestInfor = Embed(title=name, color=0x00ff00, url=contestUrl)
        contestInfor.add_field(name="ID", value=str(id), inline=True)
        contestInfor.add_field(name="Duration", value=str(duration), inline=True)
        contestInfor.add_field(name="Start Time", value=str(startTime.strftime("%d-%m-%Y --- %H:%M:%S")), inline=False)
        await ctx.send(embed=contestInfor)
    
    async def check(self):
        ContestManager.setup()
        if len(self.targetChannels) == 0: return
        contests = ContestManager.contestsToday()
        if len(contests) == 0: return

        notifyMsg = Embed(title="Today's contests", color=0xff0000)
        for contest in contests:
            id, name, duration, startTime, relativeTime = ContestManager.parseData(contest)
            notifyMsg.add_field(name=name, value=str(startTime.strftime("Start at %H:%M:%S")), inline=False)
            
        for channel in self.targetChannels:
            ctx = self.bot.get_channel(channel)
            await ctx.send(f"There is {len(contests)} contests today!")
            await ctx.send(embed=notifyMsg)

    @commands.command(name="setup")
    async def setup(self, ctx):
        ContestManager.setup()
        channel = ctx.channel.id
        if (self.targetChannels.count(channel) == 0):
            self.targetChannels.append(channel)
        #schedule contest checker
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        from apscheduler.triggers.cron import CronTrigger
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.check, CronTrigger(hour="9"))
        scheduler.start()

        await ctx.send(f"Setup Completed!")

    @commands.command(name="remove")
    async def remove(self, ctx):
        channel = ctx.channel.id
        if (self.targetChannels.count(channel) != 0):
            self.targetChannels.remove(channel)
        await ctx.send("This channel has been removed from the list. I will no longer notify in this channel anymore.")
    
    @commands.command(name="debugchecker")
    async def debugchecker(self, ctx):
        await ctx.send(self.targetChannels)
        await self.check()
        await ctx.send("check() function is called and finished")