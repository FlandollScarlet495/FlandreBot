# 🌟 FlandreBot (ふらんちゃんBot)

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
もしくは個別に：

bash
コピーする
編集する
pip install -r requirements.txt
2. .envファイルを作成
プロジェクトのルートに .env を作って下記を記述：

env
コピーする
編集する
DISCORD_TOKEN=あなたのBotトークン
GUILD_ID=（任意）ギルドID
OWNER_ID=Botの管理者ユーザーID
CONSOLE_OUTPUT_CHANNEL_ID=（任意）ログ出力チャンネルID
🔧 実行方法
bash
コピーする
編集する
python flandre_bot.py
🔍 管理者向け：コマンド定義のカスタマイズ
commands.json: コマンドの設定・エイリアス・処理タイプを定義

helps.json: /help などで表示される説明文を管理

commands.json 例
json
コピーする
編集する
{
  "name": "/say",
  "aliases": ["say", "/speak"],
  "usage": "/say <メッセージ>",
  "description": "ふらんちゃんが喋るよ♡",
  "type": "say"
}
📋 開発のヒント
flandre_bot.py: メインのBotコード、全てのロジックがここに集約

スラッシュコマンドは @bot.tree.command(...) で定義

テキストコマンド（エイリアス）は commands.json を見て判定

auto_restart_loop() により自動再起動を制御

🛠️ 特殊機能
🎮 コンソール操作（Bot起動中にターミナルから直接コマンド操作可能）

📡 Ping応答速度計測（Discord + ネット）

🔁 Botの再起動 /restart（管理者限定）

🧪 テスト用Tips
再起動間隔を auto_restart_loop(interval_seconds=10) のように変更可

/voicesay は OpenJTalk 音声をFFmpegで再生。ffmpeg 実行可能にしておいてね！

📜 ライセンス
このプロジェクトは MITライセンス です。

🩷 特記事項
東方ProjectのファンBotとしても使えます（TRPGやキャラ紹介対応予定）

VoiceVox非依存でTTS対応済（pyopenjtalk + soundfile）

🖼️ スクリーンショット（例）
📸 /help コマンドや /rank 実行時の画像をここに貼ると親切です！

🙏 最後に
ふらんちゃんBotを使ってくれてありがとう♡
不具合報告や改善提案も待ってるよ〜！