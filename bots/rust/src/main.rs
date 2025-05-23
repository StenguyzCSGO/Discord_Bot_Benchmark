use dotenv::from_path;
use std::env;
use std::path::Path;

use serenity::async_trait;
use serenity::model::channel::Message;
use serenity::prelude::*;

use std::time::Instant;
use std::collections::HashMap;

struct Handler;

#[async_trait]
impl EventHandler for Handler {
    async fn message(&self, ctx: Context, msg: Message) {
        // Vérifier si le message commence par "?benchmark"
        if msg.content.starts_with("?benchmark") {
            let parts: Vec<&str> = msg.content.split_whitespace().collect();
            let benchmark_type = if parts.len() > 1 { parts[1] } else { "all" };

            // Envoyer un message de confirmation
            if let Err(why) = msg.channel_id.say(&ctx.http, format!("Exécution du benchmark '{}'...", benchmark_type)).await {
                println!("Erreur d'envoi : {why:?}");
                return;
            }

            let result = match benchmark_type {
                "cpu" => run_cpu_benchmark(),
                "memory" => run_memory_benchmark(),
                "io" => run_io_benchmark(),
                "all" | _ => run_all_benchmarks(),
            };

            // Envoyer les résultats du benchmark
            if let Err(why) = msg.channel_id.say(&ctx.http, result).await {
                println!("Erreur d'envoi des résultats : {why:?}");
            }
        }
    }
}

fn run_cpu_benchmark() -> String {
    let start = Instant::now();

    // Test CPU intensif (calcul de nombres premiers)
    let mut count = 0;
    for n in 2..100000 {
        if is_prime(n) {
            count += 1;
        }
    }

    let duration = start.elapsed();
    format!("**Benchmark CPU**\n• Test: Calcul de nombres premiers jusqu'à 100000\n• Nombres premiers trouvés: {}\n• Temps d'exécution: {:.2?}", count, duration)
}

fn is_prime(n: u32) -> bool {
    if n <= 1 {
        return false;
    }
    if n <= 3 {
        return true;
    }
    if n % 2 == 0 || n % 3 == 0 {
        return false;
    }
    let mut i = 5;
    while i * i <= n {
        if n % i == 0 || n % (i + 2) == 0 {
            return false;
        }
        i += 6;
    }
    true
}

fn run_memory_benchmark() -> String {
    let start = Instant::now();

    // Test intensif de mémoire (création et manipulation d'une grande collection)
    let mut map = HashMap::new();
    for i in 0..1000000 {
        map.insert(i, i.to_string());
    }

    // Quelques opérations sur la collection
    let mut sum = 0;
    for i in 0..10000 {
        if let Some(val) = map.get(&i) {
            sum += val.len();
        }
    }

    let duration = start.elapsed();
    format!("**Benchmark Mémoire**\n• Test: Création et manipulation d'une HashMap de 1 million d'éléments\n• Somme de contrôle: {}\n• Temps d'exécution: {:.2?}", sum, duration)
}

fn run_io_benchmark() -> String {
    let start = Instant::now();

    // Simuler des opérations d'I/O avec des calculs et des allocations
    let mut data = Vec::new();
    for _ in 0..100 {
        let mut inner_vec = Vec::with_capacity(10000);
        for i in 0..10000 {
            inner_vec.push(i % 255);
        }
        data.push(inner_vec);
    }

    // Traitement des données
    let mut total = 0;
    for vec in &data {
        total += vec.iter().sum::<i32>();
    }

    let duration = start.elapsed();
    format!("**Benchmark I/O simulé**\n• Test: Création et traitement de 100 vecteurs de 10000 éléments\n• Somme totale: {}\n• Temps d'exécution: {:.2?}", total, duration)
}

fn run_all_benchmarks() -> String {
    let start_all = Instant::now();
    
    let cpu_result = run_cpu_benchmark();
    let memory_result = run_memory_benchmark();
    let io_result = run_io_benchmark();
    
    let total_duration = start_all.elapsed();
    
    format!("# Résultats des benchmarks\n\n{}\n\n{}\n\n{}\n\n**Temps total d'exécution: {:.2?}**\n\nUtilisez `?benchmark cpu`, `?benchmark memory` ou `?benchmark io` pour des tests individuels.",
            cpu_result, memory_result, io_result, total_duration)
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
