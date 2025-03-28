import discord
from discord.ext import commands
import asyncio
import os

# دریافت توکن‌های بات از متغیرهای محیطی
TOKENS = [
    os.getenv("MTM1NDQ0MjgzODMwNTI3NjAzNQ.GAOUqL.UIAUorjZYL7pi1fz1VW8Z8aIelBmPgGpKzhBVk"),  # بات 1 (مدیریت تیکت‌ها)
    os.getenv("MTM1NDM3ODUzMTI1NzE5MjQ4OQ.G0MZdh.L1XyVARyXGrFGh4DW2gEnaCRLz8-DoPpeByygw")   # بات 2 (مدیریت دستورات)
]

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

async def start_bot(index, token):
    bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

    @bot.event
    async def on_ready():
        print(f"✅ {bot.user} آنلاین شد!")

    # 🔹 بات 1 - مدیریت تیکت‌ها
    if index == 0:
        @bot.command(name="help")
        async def custom_help(ctx):
            embed = discord.Embed(
                title="📜 لیست دستورات بات 1",
                description="✅ **!new** → ساخت تیکت\n"
                            "✅ **!close** → بستن تیکت\n",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

        @bot.command(name="new")
        async def create_ticket(ctx):
            """ایجاد تیکت"""
            category = discord.utils.get(ctx.guild.categories, name="تیکت‌ها")
            if not category:
                category = await ctx.guild.create_category("تیکت‌ها")

            ticket_channel = await category.create_text_channel(f"ticket-{ctx.author.name}")

            await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)
            await ticket_channel.set_permissions(ctx.author, read_messages=True)

            embed = discord.Embed(
                title="🎟️ تیکت شما ایجاد شد!",
                description=f"سلام {ctx.author.mention}، تیکت شما با موفقیت ایجاد شد.\n"
                            "برای بستن تیکت از `!close` استفاده کنید.",
                color=discord.Color.blue()
            )
            await ticket_channel.send(embed=embed)

            confirmation = await ctx.send(f"✅ تیکت شما ایجاد شد: {ticket_channel.mention}")
            await asyncio.sleep(3)
            await ctx.message.delete()
            await confirmation.delete()

        @bot.command(name="close")
        async def close_ticket(ctx):
            """بستن تیکت"""
            if ctx.channel.name.startswith("ticket-"):
                await ctx.channel.delete()
            else:
                await ctx.send("❌ این کانال تیکت نیست!", delete_after=5)

    # 🔹 بات 2 - مدیریت دستورات
    elif index == 1:
        @bot.command(name="help")
        async def custom_help(ctx):
            embed = discord.Embed(
                title="📜 لیست دستورات بات 2",
                description="✅ **!send [متن]** → ارسال پیام توسط بات\n"
                            "✅ **!delmessage [تعداد]** → حذف پیام‌ها\n"
                            "✅ **!lock** → قفل کردن کانال\n"
                            "✅ **!unlock** → باز کردن کانال\n"
                            "✅ **!botinfo** → نمایش اطلاعات بات\n"
                            "✅ **!serverinfo** → نمایش اطلاعات سرور\n",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

        @bot.command(name="send")
        async def send_message(ctx, *, message: str):
            """ارسال پیام توسط بات"""
            await ctx.message.delete()
            await ctx.send(message)

        @bot.command(name="delmessage")
        @commands.has_permissions(manage_messages=True)
        async def del_message(ctx, amount: int):
            """حذف پیام‌ها"""
            if amount > 100 or amount <= 0:
                await ctx.send("❌ لطفاً عددی بین 1 تا 100 انتخاب کنید.", delete_after=3)
                return
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"✅ {amount} پیام حذف شد!", delete_after=3)

        @bot.command(name="lock")
        @commands.has_permissions(manage_channels=True)
        async def lock_channel(ctx):
            """قفل کردن کانال"""
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.send("🔒 این کانال قفل شد!")

        @bot.command(name="unlock")
        @commands.has_permissions(manage_channels=True)
        async def unlock_channel(ctx):
            """باز کردن کانال"""
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.send("🔓 این کانال باز شد!")

        @bot.command(name="botinfo")
        async def bot_info(ctx):
            """نمایش اطلاعات بات"""
            embed = discord.Embed(
                title=f"🤖 اطلاعات بات - {bot.user.name}",
                description=f"🔹 شناسه بات: `{bot.user.id}`\n"
                            f"🔹 تعداد سرورها: `{len(bot.guilds)}`\n"
                            f"🔹 تعداد کاربران: `{sum(g.member_count for g in bot.guilds)}`\n\n"
                            "👨‍💻 **Developed By: Dayan**",
                color=discord.Color.blue()
            )
            if bot.user.avatar:
                embed.set_thumbnail(url=bot.user.avatar.url)
            await ctx.send(embed=embed)

        @bot.command(name="serverinfo")
        async def server_info(ctx):
            """نمایش اطلاعات سرور"""
            guild = ctx.guild
            embed = discord.Embed(
                title=f"🌍 اطلاعات سرور - {guild.name}",
                description=f"🔹 آیدی سرور: `{guild.id}`\n"
                            f"🔹 تعداد اعضا: `{guild.member_count}`\n"
                            f"🔹 تعداد نقش‌ها: `{len(guild.roles)}`\n"
                            f"🔹 تاریخ ساخت: `{guild.created_at.strftime('%Y-%m-%d')}`",
                color=discord.Color.green()
            )
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
            await ctx.send(embed=embed)

    await bot.start(token)

async def main():
    tasks = [asyncio.create_task(start_bot(index, token)) for index, token in enumerate(TOKENS) if token]
    await asyncio.gather(*tasks)

asyncio.run(main())
