@echo off
chcp 65001
cd /d %~dp0
EM Pythonでflandre_bot.pyを実行する（仮想環境優先・なければ通常のpython）
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe flandre_bot.py
) else (
    python flandre_bot.py
)
You  You   22 minutes ago (July 3rd, 2025 10:02 AM) 

Uncommitted changes

Working Tree       |    Explain

- REM Pythonでflandre_bot.pyを実行する（仮想環境優先・なければ通常のpython）
+ 
Chan