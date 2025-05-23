import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
import asyncio
from time import perf_counter
import math

# Load environment variables
load_dotenv(dotenv_path="env")
TOKEN = os.getenv("DISCORD_PYTHON_TOKEN")
print(TOKEN)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="?", intents=intents)


def is_prime(n):
    """Check if a number is prime (optimized version)"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def format_duration(duration_seconds):
    """Format duration to show seconds and milliseconds"""
    seconds = int(duration_seconds)
    milliseconds = int((duration_seconds - seconds) * 1000)
    return f"{seconds}s {milliseconds}ms"


def run_cpu_benchmark():
    """CPU intensive benchmark - prime number calculation"""
    start = perf_counter()

    # CPU intensive test (prime number calculation)
    count = 0
    for n in range(2, 100000):
        if is_prime(n):
            count += 1

    duration = perf_counter() - start
    return (
        f"**Benchmark CPU**\n• Test: Calcul de nombres premiers jusqu'à 100000\n• Nombres premiers trouvés: {count}\n• Temps d'exécution: {format_duration(duration)}",
        duration,
    )


def run_memory_benchmark():
    """Memory intensive benchmark - large dictionary operations"""
    start = perf_counter()

    # Memory intensive test (creating and manipulating a large collection)
    data_map = {}
    for i in range(1000000):
        data_map[i] = str(i)

    # Some operations on the collection
    total_sum = 0
    for i in range(10000):
        if i in data_map:
            total_sum += len(data_map[i])

    duration = perf_counter() - start
    return (
        f"**Benchmark Mémoire**\n• Test: Création et manipulation d'un dictionnaire de 1 million d'éléments\n• Somme de contrôle: {total_sum}\n• Temps d'exécution: {format_duration(duration)}",
        duration,
    )


def run_io_benchmark():
    """Simulated I/O benchmark - data creation and processing"""
    start = perf_counter()

    # Simulate I/O operations with calculations and allocations
    data = []
    for _ in range(100):
        inner_list = []
        for i in range(10000):
            inner_list.append(i % 255)
        data.append(inner_list)

    # Data processing
    total = 0
    for vec in data:
        total += sum(vec)

    duration = perf_counter() - start
    return (
        f"**Benchmark I/O simulé**\n• Test: Création et traitement de 100 listes de 10000 éléments\n• Somme totale: {total}\n• Temps d'exécution: {format_duration(duration)}",
        duration,
    )


def run_all_benchmarks():
    """Run all benchmarks and return combined results"""
    cpu_result, cpu_time = run_cpu_benchmark()
    memory_result, memory_time = run_memory_benchmark()
    io_result, io_time = run_io_benchmark()

    total_time = cpu_time + memory_time + io_time

    return f"# Résultats des benchmarks\n\n{cpu_result}\n\n{memory_result}\n\n{io_result}\n\n**Temps total: {format_duration(total_time)}**\n\nUtilisez `?benchmark cpu`, `?benchmark memory` ou `?benchmark io` pour des tests individuels."


@bot.event
async def on_ready():
    print("Bot Python démarré!")


@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Check if message starts with "?benchmark"
    if message.content.startswith("?benchmark"):
        parts = message.content.split()
        benchmark_type = parts[1] if len(parts) > 1 else "all"

        try:
            # Send confirmation message
            await message.channel.send(f"Exécution du benchmark '{benchmark_type}'...")

            # Run appropriate benchmark
            if benchmark_type == "cpu":
                result, _ = run_cpu_benchmark()
            elif benchmark_type == "memory":
                result, _ = run_memory_benchmark()
            elif benchmark_type == "io":
                result, _ = run_io_benchmark()
            else:  # "all" or any other value
                result = run_all_benchmarks()

            # Send benchmark results
            await message.channel.send(result)

        except Exception as e:
            print(f"Erreur d'envoi: {e}")

    # Process other commands
    await bot.process_commands(message)


# Alternative command-based approach (more Pythonic)
@bot.command(name="bench")
async def benchmark_command(ctx, bench_type: str = "all"):
    """Alternative command-based benchmark"""
    await ctx.send(f"Exécution du benchmark '{bench_type}'...")

    if bench_type == "cpu":
        result, _ = run_cpu_benchmark()
    elif bench_type == "memory":
        result, _ = run_memory_benchmark()
    elif bench_type == "io":
        result, _ = run_io_benchmark()
    else:
        result = run_all_benchmarks()

    await ctx.send(result)


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
