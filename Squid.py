import discord
from discord.ext import commands, tasks
from datetime import date, datetime, time
import calendar
from random import *
import os
import random
import asyncio
from itertools import cycle
import scrapy as sc

kas = '@562100990610898976'
client = discord.Client()
bot = commands.Bot("!")
target_channel_id = 387793673775218690
promo_code_channel = 488187995518664704
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'used_codes.txt')
token = ""
with open("C:\\Users\\sphay\\.credentials\\squidbot_token.txt", "r") as f:
        lines = f.readlines()
        token = lines[0].strip()

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

async def check_for_codes():
    await client.wait_until_ready()
    while not client.is_closed():
        channel = client.get_channel(promo_code_channel)
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
                        emoji = discord.utils.get(client.emojis, name=reward[0])
                        code['Code_rewards'][i][0] = str(emoji)
                        code['Code_rewards'][i] = "".join(code['Code_rewards'][i])
                        print(code['Code_rewards'][i])
                    code['Code_rewards'] = "  ".join(code['Code_rewards'])
                    embed = discord.Embed(title=code['Coupon_code'], colour=0x4262F4)
                    embed.set_thumbnail(url="https://sph-sw-bot-image-hosting.s3.us-east-2.amazonaws.com/sw.png")
                    embed.add_field(name="Rewards", value=f"{code['Code_rewards']}")
                    await channel.send(content=None, embed=embed)
                    await save_new_codes(code['Coupon_code'])
            print("going to sleep for 5 minutes")
            await asyncio.sleep(300)
        except Exception as e:
            print(f"Exception happened: {e}")
            await asyncio.sleep(300)

@client.event
async def on_ready():
    print('Bot is ready')

async def on_message(message):
    if message.author == client.user:
        return
    chicken_shit = [
        'WHERE IS MY CHICKEN, BITCH??, <@562100990610898976>',
        '<@562100990610898976>? KAS?!?!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt,'
            'Wheres my fookin chicken mate <@562100990610898976>'
        ),
        '<@562100990610898976>, HAVE YOU SEEN MY CHICKEN?!?!?!',
        '<@562100990610898976>, where have you been hiding my chicken',
        'My chicken is missing. Where has it gone? <@562100990610898976>',
        '<@562100990610898976>, :chicken: :chicken: :chicken:'
    ]
    if message.content == '$chicken':
        response = random.choice(chicken_shit)
        await message.channel.send(response)
    if message.content =='$defense':
        await message.channel.send('@everyone CHANGE YOUR DEFENSES YOU SLOOTS')

async def change_defense():
    await client.wait_until_ready()
    while not client.is_closed():
        weekday = calendar.day_name[datetime.now().weekday()]
        sleep = 0
        channel = client.get_channel(target_channel_id)
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



async def chicken():
    await client.wait_until_ready()
    discord_users = [
        '179098163947372545'
    ]
    channel = client.get_channel(target_channel_id)
    print('squid wants his chickens')
    chicken_shit = [
        'How can you be so bad',
        'Step it up mate',
        'Squid said he will suck you',
        '1000+ days and still no ld5 rip'
    ]
    if client.is_closed():
        print(client.is_closed())
        print('not running just yet')
    while not client.is_closed():
        time = randint(100000,900000)
        print(time)
        print('My Time Has Come')
        response = "{} <@{}>".format(random.choice(chicken_shit),random.choice(discord_users))
        print(response)
        await channel.send(response)
        await asyncio.sleep(time)
        

#client.loop.create_task(chicken())
client.loop.create_task(check_for_codes())
client.loop.create_task(change_defense())

client.run(token)