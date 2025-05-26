@echo off
echo Lancement de tous les bots Discord...
echo Mode release = optimisé
echo Mode debug = pour le développement
echo.

cd /d %~dp0
cd ..

echo Demarrage du bot Python (mode debug)
start "Bot Python (Debug)" cmd.exe /k "cd /d %cd%\bots\python && python bot.py"

echo Demarrage du bot Rust (release)
start "Bot Rust (Release)" cmd.exe /k "cd /d %cd%\bots\rust && cargo run --release"

echo Verification du bot C++
if exist "%cd%\bots\cpp\x64\Release\MyBot.exe" (
    echo Bot C++ trouvé en mode Release, demarrage
    start "Bot C++ (Release)" cmd.exe /k "cd /d %cd%\bots\cpp\x64\Release && MyBot.exe"
) else if exist "%cd%\bots\cpp\x64\Debug\MyBot.exe" (
    echo ATTENTION: éxécution en mode Debug
    echo Pour avoir les meilleures performances, compilez en mode Release (dans Visual Studio mettre release en haut et faire CTRL + SHIFT + B)
    start "Bot C++ (Debug)" cmd.exe /k "cd /d %cd%\bots\cpp\x64\Debug && MyBot.exe"
) else (
    echo ATTENTION: MyBot.exe non trouvé
)

echo.
echo Appuyez sur une touche pour fermer cette fenetre
pause >nul