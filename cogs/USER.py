import discord,json,os,asyncio,psycopg2
from discord.ext.commands import *
from discord_components import Button
from functions import *

con = psycopg2.connect(os.environ.get("DATABASE_URL"))
cur = con.cursor()

class USER(Cog):

    def __init__(self,client):

        self.client = client

    @command()
    async def start(self,ctx):
        cur.execute("ROLLBACK")
        cur.execute(f"SELECT * FROM Main WHERE ID = {ctx.author.id}")
        if cur.rowcount == 0:
            cur.execute(f"INSERT INTO Main (ID,MONEY,LEVEL,XP,BUFF1T,BUFF2T,BUFF3T,JOB,STAMINA,MSTAMINA,HOUSE,HOUSESOWNED,FOODSOWNED,WSTREAK,DSTREAK,DAILYELAPSED,VSTREAK,HUNGER,SLEEPINESS) VALUES ({ctx.author.id},0,1,0,0,0,0,'Fast Food',10,10,'Homeless','','',0,0,24,0,70,70);")
            con.commit()
            embed = discord.Embed(title = "Welcome", color = discord.Color.blue())
            embed.set_author(name = ctx.author)
            embed.set_thumbnail(url = ctx.author.avatar_url)
            embed.add_field(name = "Umm Hello Adventurer. What Can I help you with today?",value = "Used command 1start.",inline = False)
            msg = await ctx.send(embed = embed)
            
        else:
            embed = discord.Embed(title = "Welcome", color = discord.Color.blue())
            embed.set_author(name = ctx.author)
            embed.set_thumbnail(url = ctx.author.avatar_url)
            embed.add_field(name = "Error using this command. Can\'t make an existance exist.",value = "Used command 1start.",inline = False)
            msg = await ctx.send(embed = embed)
            
    @command(aliases=["pf",])
    async def profile(self,ctx,user : discord.Member = None):
        
        if user == None:
            user = ctx.author
            
        cur.execute(f"SELECT MONEY,LEVEL,XP,WORKPLACE,STAMINA,MSTAMINA,HOUSE,VSTREAK,DSTREAK FROM Main WHERE ID={ctx.author.id};")
        d = cur.fetchall()[0]
        embed = discord.Embed(title="Profile", description="Do 1houses and 1foods for more options.",color = discord.Color.random())
        embed.set_author(name=ctx.author.name)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name=f"Money : {d[0]}",value=f"Buffs : {buffs}",inline=False)
        embed.add_field(name=f"Stamina : { d[4]}",value=f"Maximum Stamina : {d[5]}",inline=False)
        exp = xplevel(ctx.author)
        embed.add_field(name=f"Level : {d[1]}",value=f"Exp : {d[2]}/{exp}",inline=False)
        embed.add_field(name=f"Home : {d[6]}",value=f"Workplace : {d[3]}",inline=False)
        embed.add_field(name=f"Daily Streak : {d[8]}",value=f"Voting Streak : {d[7]}")
        await ctx.send(embed=embed)
        
    @command()
    async def daily(self,ctx):
        
        cur.execute(f"SELECT DSTREAK,DAILYELAPSED FROM Main WHERE ID={ctx.author.id};")
        d = cur.fetchall()[0]
        if d[1]>=1440 and d[1]<=2880:
            inc = (d[0]*50)+100
            cur.execute(f"UPDATE Main SET DSTREAK=DSTREAK+1,DAILYELAPSED=0,MONEY=MONEY+{inc} WHERE ID={ctx.author.id};")
            con.commit()
            await ctx.send(f"You got your daily {inc}$. Current streak : {d[0]+1}")
        elif d[1]>2060:
            inc = 100
            cur.execute(f"UPDATE Main SET DSTREAK=0,DAILYELAPSED=0,MONEY=MONEY+{inc} WHERE ID={ctx.author.id};")
            con.commit()
            await ctx.send(f"You got your daily {inc}. Streak got resetted.")
        elif d[1]<1440:
            t = (1440-d[1])//60
            await ctx.send(f"No gotta wait for {t} more hours.")
            
    @command(aliases=["stam","hunger","sleepiness"])
    async def stamina(self,ctx):
        
        cur.execute(f"SELECT STAMINA,MSTAMINA,HUNGER,SLEEPINESS FROM Main WHERE ID={ctx.author.id}")
        d = cur.fetchall()[0]
        await ctx.send(f"Stamina : {d[0]}/{d[1]}\nHunger : {d[2]}/100\nSleepiness : {d[3]}/100")

def setup(client):
    client.add_cog(USER(client))