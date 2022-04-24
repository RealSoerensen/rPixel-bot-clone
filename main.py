import discord
import os
from discord.ext import commands
import API
from PIL import Image

bot = commands.Bot(command_prefix="$", help_command=None)


def send_image(ctx, img):
    discord_id = ctx.message.guild.id
    resized_img = img.resize((500, 500), Image.Resampling.NEAREST)
    resized_img.save(f"images\\{discord_id}_resized.png", format="png")
    with open(f"images\\{discord_id}_resized.png", "rb") as f:
        return ctx.send(file=discord.File(f))


@bot.command()
async def help(ctx):
    commands = discord.Embed(
        title="Help", 
        description="Here are the commands you can use:", 
    )
    commands.add_field(name="$help", 
        value="Shows this message", 
        inline=False
    )
    commands.add_field(name="$ping", 
        value="Pings the bot!", 
        inline=False
    )
    commands.add_field(
        name="$place x y color",
        value="Places a pixel at x, y with the color selected",
        inline=False,
    )
    commands.add_field(name="$show", 
        value="Shows the image", 
        inline=False
    )
    await ctx.send(embed=commands)


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command()
async def place(ctx, x, y, color):
    try:
        x = int(x)
        y = int(y)
        color = str(color).lower()

    except ValueError:
        return await ctx.send(
            "Please provide x, y and color.\nRemember to format as '$place x y color'"
        )

    discord_id = ctx.message.guild.id
    image_path = f"images\\{discord_id}.png"

    if not os.path.isfile(image_path):
        new_img = Image.new("RGB", (w, h), color="white")
        new_img.save(image_path, format="png")
    img = Image.open(image_path)

    color_dict = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "black": (0, 0, 0),
        "white": (255, 255, 255),
    }
    if color not in color_dict:
        return await ctx.send(
            "Invalid color.\nValid colors are: red, green, blue, yellow, cyan, magenta, black, white"
        )

    if x < 0 or x > w or y < 0 or y > h:
        return await ctx.send(
            "Invalid coordinates.\nPlease provide coordinates between 0 and 50"
        )

    img.putpixel((x, y), color_dict[color])
    img.save(image_path)
    await send_image(ctx, img)


@bot.command()
async def show(ctx):
    try:
        with open(f"images\\{ctx.message.guild.id}_resized.png", "rb") as f:
            await ctx.send(file=discord.File(f))
    except FileNotFoundError:
        return await ctx.send("No image to show!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"{ctx.author.mention} are currently on cooldown.\nPlease wait {error.retry_after:.2f} seconds"
        )

w = 50
h = 50

bot.run(API.TOKEN)
