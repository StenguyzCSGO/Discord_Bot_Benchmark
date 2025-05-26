#include <dpp/dpp.h>
#include <cmath>
#include <chrono>
#include <sstream>
#include <iomanip>
#include <fstream>
#include <string>
#include <unordered_map>
#include <iostream>

std::string loadEnvVariable(const std::string& filepath, const std::string& key) {
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cerr << "Error: Cannot open .env file at " << filepath << std::endl;
        return "";
    }

    std::string line;
    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') {
            continue;
        }

        size_t pos = line.find('=');
        if (pos != std::string::npos) {
            std::string fileKey = line.substr(0, pos);
            if (fileKey == key) {
                std::string value = line.substr(pos + 1);
                if (value.front() == '"' && value.back() == '"') {
                    value = value.substr(1, value.length() - 2);
                }
                return value;
            }
        }
    }

    return "";
}

std::string format_duration(double duration_seconds) {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(2) << (duration_seconds * 1000.0) << "ms";
    return oss.str();
}

std::string run_benchmark() {
    auto start = std::chrono::high_resolution_clock::now();
    
    double result = 0.0;
    int iterations = 1000000;
    
    for (int i = 0; i < iterations; ++i) {
        double x = i * 1.0;
        result += std::sin(x * 3.14159) + std::cos(x / 2.71828) + (std::sqrt(x) * 1.414);
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;
    
    std::ostringstream oss;
    oss << "**Benchmark C++**\n"
        << "• Test: " << iterations << " itérations avec opérations mathématiques\n"
        << "• Résultat: " << std::fixed << std::setprecision(6) << result << "\n"
        << "• Temps d'exécution: " << format_duration(duration.count());
    return oss.str();
}

int main() {
    const std::string env_path = "..\\..\\..\\..\\.env";

    std::string TOKEN = loadEnvVariable(env_path, "DISCORD_CPP_TOKEN");

    if (TOKEN.empty()) {
        std::cerr << "Error: DISCORD_CPP_TOKEN not found in " << env_path << std::endl;
        return 1;
    }
    
    dpp::cluster bot(TOKEN, dpp::i_default_intents | dpp::i_message_content);
    
    bot.on_log(dpp::utility::cout_logger());
    
    bot.on_ready([&bot](const dpp::ready_t&) {
        std::cout << "Bot C++ demarre!" << std::endl;
    });
    
    bot.on_message_create([&bot](const dpp::message_create_t& event) {
        if (event.msg.author.id == bot.me.id) return;
        
        const std::string& content = event.msg.content;
        
        if (content == "?benchmark") {
            bot.message_create(dpp::message(event.msg.channel_id, "Exécution du benchmark..."));
            std::string result = run_benchmark();
            bot.message_create(dpp::message(event.msg.channel_id, result));
        }
    });
    
    bot.start(dpp::st_wait);
    return 0;
}
