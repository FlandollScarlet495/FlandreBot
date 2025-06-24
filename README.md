# 🌟 FlandreBot (ふらんちゃんBot_V4.5)

ふらんちゃんBotは、かわいくて多機能な日本語Discordボットです！  
TRPGやエンタメ、読み上げ、ポイント制、再起動などたくさんの機能を備え、  
あなたのサーバーをにぎやかに盛り上げてくれます♡

---

## 📦 機能一覧

### 🎉 エンタメ・便利コマンド
- `/hello` あいさつ
- `/dice` TRPGサイコロ（例: `2d6+1`）
- `/omikuji` おみくじ
- `/quote` 名言ランダム表示
- `/cat` 猫画像で癒される
- `/weatherjp 東京` 日本の天気取得（APIキー不要）
- `/translate` 翻訳（日英対応）
- `/math` 数式計算
- **`/gif` キーワードでGIFを検索（Tenor API利用）** ✨ NEW!

### 🔊 ボイスチャンネル読み上げ機能
- `/voicejoin` VCに接続
- `/voicesay` ふらんちゃんの声で喋る（OpenJTalk）
- VC内のテキストメッセージを自動で読み上げ
- `/voiceleave` VCから退出

> ※ FFmpeg + pyopenjtalk によるTTS（ふらんちゃんボイス）で再生

### 💬 ポイント＆ランク機能
- `text_points`：メッセージ送信で自動加算
- `voice_points`：VCにいると定期加算（1分ごと）
- `/rank`：自分のランク＆ポイント確認

> 💾 `points.json` に自動保存され、Bot再起動でも維持されます。

### 🔁 自動再起動
- 毎秒単位で再起動までのカウントダウンを表示
- Botの安定運用のため、最大4時間ごとに再起動（設定可能）

---

## 🚀 導入方法

### 1. Pythonとライブラリをインストール

```bash
pip install -r requirements.txt
# もしくは個別に：
# pip install discord.py python-dotenv aiohttp beautifulsoup4 pyopenjtalk soundfile requests
2. .envファイルを作成
プロジェクトのルートに .env を作って下記を記述：

コード スニペット

DISCORD_TOKEN=あなたのBotトークン
GUILD_ID=（任意）ギルドID
OWNER_ID=Botの管理者ユーザーID
CONSOLE_OUTPUT_CHANNEL_ID=（任意）コンソールからのメッセージ送信用チャンネルID
TENOR_API_KEY=あなたのTenor APIキー
⚠️ TENOR_API_KEY は、Tenor Developer Dashboard から取得してね！

🔧 実行方法
Bash

python flandre_bot.py
🔍 管理者向け：コマンド定義のカスタマイズ
commands.json: コンソールコマンドの設定・エイリアス・処理タイプを定義
helps.json: /help などで表示される説明文を管理

---

### `README.txt` (プレーンテキスト形式)

＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
🌟 FlandreBot（ふらんちゃんBot_V4.3） - Discord用日本語Bot
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

ふらんちゃんBotは、東方Projectのフランドール・スカーレット風の
かわいくて多機能な Discord Bot です！

雑談からTRPG、画像検索、VC読み上げ、ランクポイント管理まで
色んなことができるすごい子だよ♡

【主な機能】

● エンタメ・便利系コマンド
・/hello         あいさつ
・/dice          サイコロ（例: 2d6+1）
・/omikuji       おみくじ
・/quote         名言を教えてくれる
・/cat           猫画像で癒される
・/translate     翻訳（英⇔日）
・/math          数式計算
・/weatherjp     日本の天気（API不要）
・/gif           キーワードでGIFを検索（Tenor API利用）✨NEW!

● ボイスチャンネル 読み上げ機能
・/voicejoin     ボイスチャンネルに入る
・/voicesay      メッセージをふらんちゃんボイスで読み上げ
・/voiceleave    VCから抜ける

※ pyopenjtalk + FFmpegで音声合成するよ！

● ランクポイント機能（ProBot風）
・text_points  : メッセージごとに自動加算
・voice_points : VCにいる間 1分ごと加算
・/rank         現在のポイントとランク表示

💾 points.json に自動保存され、Bot再起動でも維持されます。

● 自動再起動
・1時間ごとに自動で再起動（変更可）
・コンソールに残り時間を毎分表示してくれる

【導入方法】

必要なライブラリをインストール

pip install -r requirements.txt

もしくは手動で：

pip install discord.py python-dotenv aiohttp pyopenjtalk soundfile requests beautifulsoup4

.envファイルを作成
プロジェクトのルートに .env を作って下記を記述：

DISCORD_TOKEN=あなたのBotトークン
GUILD_ID=（任意）ギルドID
OWNER_ID=Botの管理者ユーザーID
CONSOLE_OUTPUT_CHANNEL_ID=（任意）コンソールからのメッセージ送信用チャンネルID
TENOR_API_KEY=あなたのTenor APIキー

⚠️ TENOR_API_KEY は、Tenorの開発者ダッシュボードから取得してね！

🔧 実行方法

python flandre_bot.py
🔍 管理者向け：コマンド定義のカスタマイズ
commands.json: コンソールコマンドの設定・エイリアス・処理タイプを定義
helps.json: /help などで表示される説明文を管理