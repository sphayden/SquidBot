from discord.ext import commands, tasks
import discord
from datetime import date, datetime, time
import calendar
import os
from dotenv import load_dotenv
import asyncio
import scrapy as sc
load_dotenv()

kas = '@562100990610898976'
#client = discord.Client()
bot = commands.Bot(command_prefix='!', description="bitch")
target_channel_id = 387793673775218690
promo_code_channel = 774665918067769354
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'used_codes.txt')
guilds_dict = {}

### Saves Code to txt file ###
async def save_new_codes(code):
    try:
        with open(my_file, "a") as f:
            f.write(f"\n{code}")
    except Exception as e:
        print(e)

### return txt file of used codes ###
async def check_old_codes():
    with open(my_file, "r") as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
        return lines

### Gets codes from scrapy.py ###
async def get_codes():
    codes = sc.main()
    return codes

@bot.command(name="gid")
async def get_guild_id(ctx):
    id = ctx.message.guild.id
    await ctx.channel.send("Guild id: " + str(id))

@bot.command(name="check-codes")
async def check_for_codes(ctx):
    await ctx.channel.send("Checking for valid codes")
    channel = bot.get_channel(promo_code_channel)
    #Create list of embeds for codes
    codes = await get_codes()
    used_codes = await check_old_codes()
    try:
        for code in codes:
            if code['Coupon_code'] in used_codes:
                print(f"{code['Coupon_code']} has already been posted")
                #await channel.send(f"No new codes at this time.")
            else:
                for i, reward in enumerate(code['Code_rewards']):
                    emoji = discord.utils.get(bot.emojis, name=reward[0])
                    code['Code_rewards'][i][0] = str(emoji)
                    code['Code_rewards'][i] = "".join(code['Code_rewards'][i])
                    print(code['Code_rewards'][i])
                code['Code_rewards'] = "  ".join(code['Code_rewards'])
                embed = discord.Embed(title=code['Coupon_code'], colour=0x4262F4)
                embed.set_thumbnail(url="https://sph-sw-bot-image-hosting.s3.us-east-2.amazonaws.com/sw.png")
                embed.add_field(name="Rewards", value=f"{code['Code_rewards']}")
                await channel.send(content=None, embed=embed)
                await save_new_codes(code['Coupon_code'])
        await ctx.channel.send("Process complete")
    except Exception as e:
        print(f"Exception happened: {e}")

@bot.command(name="set-codes-channel")
@commands.has_permissions(administrator=True)
@commands.has_role("The Editor")
async def set_guild_codes_channel(ctx, channel_id):
    guild_id = ctx.message.guild.id
    guilds_dict = {
        guild_id:{
            "guild_name": ctx.message.guild.name,
            "codes_channel": channel_id
        }
    }
    print(guilds_dict)



@bot.event
async def on_ready():
    print('Bot is ready')

async def change_defense():
    await bot.wait_until_ready()
    while not bot.is_closed():
        weekday = calendar.day_name[datetime.now().weekday()]
        sleep = 0
        channel = bot.get_channel(target_channel_id)
        print(weekday)
        if weekday == 'Sunday' or weekday == 'Thursday':
            current_time = datetime.now().time()
            print('im in', current_time)
            check_time_a = time(19,00)
            check_time_b = time(22,00)
            if current_time > check_time_a and current_time < check_time_b:
                if weekday == 'Sunday':
                    await channel.send("@everyone Change your GW defense to 1/1 please!")
                else:
                    await channel.send("@everyone Change to strong defense!")
                sleep = 12600
            else:
                sleep = 3600
        else:
            sleep = 43200
        await asyncio.sleep(sleep)
       
@bot.event
async def on_command_error(ctx, error):
    await ctx.channel.send(f"Command failed due to {error}")
#bot.loop.create_task(check_for_codes(commands.Context()))
#bot.loop.create_task(change_defense())
bot.load_extension('cogs.SetupCommands')
bot.run(os.getenv("BOT_TOKEN"))