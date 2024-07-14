from src.discord_bot import InitialBot
from app import check_naver
import discord
from discord.ext import commands, tasks
import time
import sys


initialized_bot = InitialBot()
bot = initialized_bot.bot


@bot.event
async def on_ready():
    sys.stdout.write('Login...\n')
    sys.stdout.write(f'Login bot: {bot.user}\n')
    sys.stdout.write(f'{bot.user}에 로그인하였습니다.\n')
    sys.stdout.write(f'ID: {bot.user.name}\n')
    print(initialized_bot.guild_id)
    guild = discord.utils.get(bot.guilds, id=initialized_bot.guild_id)
    if guild is None:
        print("Bot is not connected to the specified guild.")
        return

    print(f"Channel ID: {initialized_bot.channel_id}")
    main_channel = bot.get_channel(initialized_bot.channel_id)
    if main_channel is None:
        print("Channel not found. Please check the channel ID and ensure the bot has access to it.")
        return
    else:
        print(f"Found channel: {main_channel.name}")

    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Intellij로 개발'))

    embed = discord.Embed(title="USFK Crime Tracking Bot is Initialized",
                          description="Get the newest media interest.",
                          color=discord.Colour.from_rgb(0, 0, 128))
    embed.set_author(name='CrimeInfo')
    embed.set_footer(text="What Happened about USFK")

    await main_channel.send(embed=embed)
    media_checker.start(main_channel)




@tasks.loop(minutes=30)
async def media_checker(channel):
    new_flag, new_posts, response = check_naver()


    # 만약 기존에 가져왔던 뉴스랑 겹치면 디스코드로 보내지 않고 다음 뉴스를 기다림
    if not new_flag:
        embed = discord.Embed(description="There is Nothing Significant to Report, So far.",
                              color=discord.Colour.from_rgb(0, 0, 128))
        embed.set_author(name='CrimeInfo')
        embed.set_footer(text="What Happened about USFK")

    else:
        await channel.send(f"The Total of Today's New Media Interest: [{len(new_posts)}]")

        for post in new_posts:
            score = post["similarity"]
            title = post["title"]
            link = post["link"]
            if 7 <= len(title):
                title = title[:8]
            if 0.9 <= score:
                embed = discord.Embed(title=f"[HOT] {title}...",
                                      description=f"Link: {link}",
                                      color=discord.Colour.from_rgb(255, 49, 49))
            else:
                embed = discord.Embed(title=f"[NOR] {title}...",
                                      description=f"Link: {link}",
                                      color=discord.Colour.from_rgb(0, 0, 128))
            embed.set_author(name='CrimeInfo')
            embed.set_footer(text=f"The Media Interest Score :[{score}]")
            await channel.send(embed=embed)


if __name__ == "__main__":
    try:
        bot.run(initialized_bot.token)
    except discord.errors.LoginFailure as e:
        print("Improper token has been passed.")
