@echo off
chcp 65001
REM ==== FlandreBot Web Dashboard ====
REM ふらんちゃんBot Webダッシュボードを起動しています...
echo.
echo Installing required packages / 必要なパッケージをインストールしています...
pip install -r requirements.txt
echo.
echo Starting Web Dashboard / Webダッシュボードを起動しています...
echo Access in your browser: http://localhost:5000
echo ブラウザで http://localhost:5000 にアクセスしてください
echo ユーザー名: admin
echo パスワード: flandre123
echo.
echo ※Bot本体が起動中の場合、ダッシュボードに本物のBot情報がリアルタイム表示されます
echo.
python web_dashboard.py
pause 