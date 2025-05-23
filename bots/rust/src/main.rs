use dotenv::from_path;
use std::env;
use std::path::Path;

use serenity::async_trait;
use serenity::model::channel::Message;
use serenity::prelude::*;

use std::time::Instant;

struct Handler;

#[async_trait]
impl EventHandler for Handler {
    async fn message(&self, ctx: Context, msg: Message) {
        if msg.content.starts_with("?benchmark") {
            if let Err(why) = msg.channel_id.say(&ctx.http, "Exécution du benchmark...").await {
                println!("Erreur d'envoi : {why:?}");
                return;
            }

            let result = run_benchmark();

            if let Err(why) = msg.channel_id.say(&ctx.http, result).await {
                println!("Erreur d'envoi des résultats : {why:?}");
            }
        }
    }
}

fn run_benchmark() -> String {
    let start = Instant::now();
    
    let mut result: f64 = 0.0;
    let iterations = 1_000_000u64;
    
    for i in 0..iterations {
        let x = i as f64;
        result += (x * 3.14159).sin() + (x / 2.71828).cos() + (x.sqrt() * 1.414);
    }
    
    let duration = start.elapsed();
    
    format!(
        "**Benchmark Rust**\n• Test: {} itérations avec opérations mathématiques\n• Résultat: {:.6}\n• Temps d'exécution: {:.2?}",
        iterations,
        result,
        duration
    )
}

#[tokio::main]
async fn main() {
    let env_path = Path::new("../../.env");
    from_path(env_path).expect("Échec du chargement du fichier .env");

    let token = env::var("DISCORD_RUST_TOKEN")
        .expect("DISCORD_RUST_TOKEN non défini dans le fichier .env");

    let intents = GatewayIntents::GUILD_MESSAGES
        | GatewayIntents::DIRECT_MESSAGES
        | GatewayIntents::MESSAGE_CONTENT;

    let mut client =
        Client::builder(&token, intents).event_handler(Handler).await.expect("Err creating client");

    println!("Bot Rust démarré!");

    if let Err(why) = client.start().await {
        println!("Client error: {why:?}");
    }
}
