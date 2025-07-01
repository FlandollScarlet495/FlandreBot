@echo off
echo ふらんちゃんBot Webダッシュボードを起動しています...
echo.
echo 必要なパッケージをインストールしています...
pip install -r requirements.txt
echo.
echo Webダッシュボードを起動しています...
echo ブラウザで http://localhost:5000 にアクセスしてください
echo ユーザー名: admin
echo パスワード: flandre123
echo.
python web_dashboard.py
pause 