@echo off
chcp 65001
cd /d %~dp0
REM Pythonでflandre_bot.pyを実行する（仮想環境優先・なければ通常のpython）
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe flandre_bot.py
) else (
    python flandre_bot.py
)
pause