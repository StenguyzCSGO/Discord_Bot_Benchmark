import { Client, Events, GatewayIntentBits } from 'discord.js';
import { config } from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const envPath = join(__dirname, '..', '..', '.env');
config({ path: envPath });
const TOKEN = process.env.DISCORD_JAVASCRIPT_TOKEN;

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.DirectMessages,
        GatewayIntentBits.MessageContent
    ]
});

function formatDuration(durationSeconds) {
    return `${(durationSeconds * 1000).toFixed(2)}ms`;
}

function runBenchmark() {
    const start = performance.now();
    
    let result = 0.0;
    const iterations = 1_000_000;
    
    for (let i = 0; i < iterations; i++) {
        const x = i * 1.0;
        result += Math.sin(x * 3.14159) + Math.cos(x / 2.71828) + (Math.sqrt(x) * 1.414);
    }
    
    const duration = (performance.now() - start) / 1000;
    
    return `**Benchmark JavaScript**\n• Test: ${iterations.toLocaleString()} itérations avec opérations mathématiques\n• Résultat: ${result.toFixed(6)}\n• Temps d'exécution: ${formatDuration(duration)}`;
}

client.on(Events.ClientReady, () => {
    console.log('Bot JavaScript démarré!');
});

client.on(Events.MessageCreate, async (message) => {
    if (message.author.bot) return;
    
    if (message.content.startsWith('?benchmark')) {
        try {
            await message.channel.send('Exécution du benchmark...');
            
            const result = runBenchmark();
            
            await message.channel.send(result);
            
        } catch (error) {
            console.error(`Erreur d'envoi: ${error}`);
        }
    }
});

if (!TOKEN) {
    console.error('Erreur: TOKEN non défini dans le fichier .env');
} else {
    client.login(TOKEN);
}