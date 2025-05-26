# Discord Bot Benchmark

Performance comparison between Python, Rust, C++, and JavaScript through Discord bots.

## Motivation

This project was born from a concrete optimization need. I had initially developed a Discord bot in Python (Linkify) for its development simplicity. Although the code was well-organized and functional, the performance was not optimal.

Wanting to maximize performance before production deployment, I wanted to explore the impact of programming language choice. I therefore implemented the same bot in different languages:
- **Rust** and **C++** for their native performance
- **JavaScript** with the official Discord.js library for comparison

The benchmark performs the same intensive mathematical calculation to measure the pure performance of each language, independently of the Discord API:

**Tested operation:** Loop of 1,000,000 iterations with for each iteration `i`:
```
x = i × 1.0
result += sin(x × π) + cos(x ÷ e) + (√x × √2)
```

Where:
- `π ≈ 3.14159` (pi approximation)
- `e ≈ 2.71828` (Euler's number approximation)
- `√2 ≈ 1.414` (square root of 2 approximation)

This operation combines trigonometric calculations (sine, cosine) and algebraic operations (square root, multiplications, divisions) to intensively stress the processor and reveal performance differences between languages.

## Observed Results

The execution time differences are significant and mainly come from the programming language used. Although each Discord library may have its own optimizations, the performance impact remains negligible compared to the gaps between languages during intensive calculations.

This analysis demonstrates the value of rewriting critical bots in Rust or C++ to:
- **Reduce response times**
- **Save server resources**
- **Improve error handling** (especially with Rust vs Python)

*Note: If you check my GitHub, the Linkify bot might be available in Python version, Rust version, or both depending on the progress of the rewrite project.*

## Tested Languages

- **Python** - Debug mode ([discord.py](https://discordpy.readthedocs.io/en/stable/))
- **Rust** - Release mode ([Serenity](https://docs.rs/serenity/latest/serenity/index.html))
- **C++** - Release/debug mode ([DPP 10.1](https://dpp.dev/))
- **JavaScript** - Node.js ([discord.js](https://discord.js.org/docs/packages/discord.js/14.19.3))

## Installation

### Prerequisites
- Python 3.x
- Rust (cargo)
- Node.js
- Visual Studio (for C++)

### Configuration

Create a `.env` file at the root based on `.env.example`

### C++ Dependencies

For the C++ bot, you must install DPP 10.1 dependencies manually.
Follow this installation video: https://www.youtube.com/watch?v=JGqaQ9nH5sk

The `dependencies` folder is not included in git to avoid large files.

## Usage

### Launch all bots
```bash
# Windows
scripts/launch_all.bat
```

### Launch individually

#### Python
```bash
cd bots/python
python bot.py
```

#### Rust
```bash
cd bots/rust
cargo run --release
```

#### JavaScript
```bash
cd bots/js
npm install
node bot.js
```

#### C++
Compile with Visual Studio then run `MyBot.exe`

## Benchmark Test

In Discord, type `?benchmark` to launch the performance test.

## Example

![Benchmark Results](https://cdn.discordapp.com/attachments/1240372726791929941/1376673993633042442/image.png?ex=68362f11&is=6834dd91&hm=67428cf55c57ed20b6ec32642a10ff9c3736c74a8dd27f7e4d8cea3848da0e61&)

## Future Improvements

### Docker Containerization
Currently, dependency management for each language can be complex and requires installing multiple development environments. A planned improvement consists of encapsulating each bot in a Docker container to:
- **Simplify installation** - A single `docker-compose up` to launch all bots
- **Isolate environments** - Each language in its own container
- **Standardize deployment** - Same behavior on all systems
- **Facilitate maintenance** - Centralized version and dependency management

This approach would transform the current multi-step installation into a single command, regardless of operating system.

### Cross-platform launch script
Addition of a `launch_all.sh` script for macOS and Linux systems, equivalent to the Windows `launch_all.bat` script, to enable bot launching on all Unix-like systems.

## Structure

```
bots/
├── python/     # Python Bot
├── rust/       # Rust Bot
├── cpp/        # C++ Bot
└── js/         # JavaScript Bot
scripts/
└── launch_all.bat  # Windows Script
```