import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
import asyncio
from time import perf_counter
import math

load_dotenv(dotenv_path="../../.env")
TOKEN = os.getenv("DISCORD_PYTHON_TOKEN")
print(TOKEN)

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="?", intents=intents)


def format_duration(duration_seconds):
    """Format duration to show milliseconds with 2 decimal places"""
    return f"{duration_seconds * 1000:.2f}ms"


def run_benchmark():
    """Simple benchmark - large loop with mathematical operations"""
    start = perf_counter()

    result = 0.0
    iterations = 1_000_000

    for i in range(iterations):
        x = i*1.0
        result += math.sin(x * 3.14159) + math.cos(x / 2.71828) + (math.sqrt(x) * 1.414)

    duration = perf_counter() - start

    return f"**Benchmark Python**\n• Test: {iterations:,} itérations avec opérations mathématiques\n• Résultat: {result:.6f}\n• Temps d'exécution: {format_duration(duration)}"


@bot.event
async def on_ready():
    print("Bot Python démarré!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("?benchmark"):
        try:
            await message.channel.send("Exécution du benchmark...")

            result = run_benchmark()

            await message.channel.send(result)

        except Exception as e:
            print(f"Erreur d'envoi: {e}")

    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    """Simple ping command"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! Latence: {latency}ms")


if __name__ == "__main__":
    if not TOKEN:
        print("Erreur: TOKEN non défini dans le fichier .env")
    else:
        bot.run(TOKEN)
