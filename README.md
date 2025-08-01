# 🌟 FlandreBot (ふらんちゃんBot_V6.3)

ふらんちゃんBotは、かわいくて多機能な日本語Discordボットです！  
TRPGやエンタメ、読み上げ、BGM再生、人狼ゲーム、ポイント制、再起動、AIチャット、画像生成などたくさんの機能を備え、  
あなたのサーバーをにぎやかに盛り上げてくれます♡

## 🌟 新機能: Webダッシュボード

### 概要
管理者向けのWebインターフェースを提供し、Botの状態監視や管理を簡単に行えます。

### 機能
- **リアルタイム監視**: Botの状態、リソース使用率、統計情報をリアルタイムで表示
- **コマンド管理**: 利用可能なコマンド一覧の表示と管理
- **設定確認**: 現在の設定内容の確認
- **ログ表示**: リアルタイムログの表示と自動更新
- **レスポンシブデザイン**: スマートフォンやタブレットでも快適に操作可能

### 起動方法

1. **依存関係のインストール**
```bash
pip install -r requirements.txt
```

2. **ダッシュボードの起動**
```bash
python web_dashboard.py
```
または
```bash
start_dashboard.bat
```

3. **ブラウザでアクセス**
- URL: `http://localhost:5000`
- ユーザー名: `admin`
- パスワード: `flandre123`

### セキュリティ
- 管理者認証システム
- セッション管理
- ログイン必須のページ保護

### 画面構成
- **ダッシュボード**: Bot状態、統計情報、リソース使用率
- **コマンド**: 利用可能なコマンド一覧
- **設定**: 現在の設定内容確認
- **ログ**: リアルタイムログ表示

---

## 📦 機能一覧

### 🤖 AI・チャット機能（無料版）

- `/chat` 無料AIふらんちゃんと会話（Hugging Face API）
- `/chat_reset` AIチャット履歴リセット
- `/generate_image` 完全無料画像検索（APIキー不要）
- `/translate_advanced` 多言語翻訳（9言語対応）

### 🎉 エンタメ・便利コマンド

- `/hello` あいさつ
- `/dice` TRPGサイコロ（例: `2d6+1`）
- `/omikuji` おみくじ
- `/quote` 名言ランダム表示
- `/cat` 猫画像で癒される
- `/weatherjp 東京` 日本の天気取得（APIキー不要）
- `/translate` 翻訳（日英対応）
- `/math` 数式計算
- `/gif` キーワードでGIFを検索（Tenor API利用）
- `/pixabay_large` 高画質画像検索
- `/fortune` 今日の運勢
- `/choose` 選択肢からランダム選択
- `/poll` 投票機能
- `/remind` リマインダー機能

### 🎵 BGM・音楽機能

- `/join` VCに接続
- `/leave` VCから退出
- `/play` YouTubeのBGMを再生
- `/search_music` YouTubeで音楽検索・再生
- `/stop` BGMを停止
- `/volume` 音量調整（0-100）
- `/nowplaying` 現在再生中の曲を確認
- `/bgm` テキストチャンネルでBGM再生
- `/bgm_stop` テキストチャンネルのBGM停止

### 🎵 BGM・音楽機能（拡張）
- `/playlist_loop` プレイリストのループ再生ON/OFF
- `/playlist_shuffle` プレイリストをシャッフル再生
- `/playlist_history` 再生履歴を表示
- `/playlist_favorite` お気に入り曲一覧を表示
- `/playlist_favorite_add` お気に入りに曲を追加
- `/playlist_favorite_remove` お気に入りから曲を削除
- BGMフェードイン/アウト対応
- SoundCloud対応の下準備

### 📋 プレイリスト機能

- `/playlist_create` プレイリスト作成
- `/playlist_add` プレイリストに曲を追加
- `/playlist_show` プレイリスト表示
- `/playlist_play` プレイリスト再生
- `/playlist_list` 自分のプレイリスト一覧
- `/playlist_delete` プレイリスト削除
- `/playlist_remove` プレイリストから曲を削除
- `/playlist_export` プレイリストをエクスポート
- `/playlist_youtube` YouTubeプレイリストを読み込み

### 🎮 ゲーム機能

- **人狼ゲーム**：`/jinro`, `/jijoin`, `/start_jinro`, `/divine`, `/guard`, `/attack` など
- **TRPGキャラクター管理**：`/trpg_char_create`, `/trpg_char_show`, `/trpg_char_edit` など
- **じゃんけんゲーム**：`/rps` グー・チョキ・パー
- **数字当てゲーム**：`/number_guess`, `/guess` 数字を当てよう

### 🎮 ゲーム・娯楽機能（拡張）
- `/quiz` クイズを出題
- `/quiz_answer` クイズの答えを送信
- `/shiritori` しりとり開始
- `/shiritori_word` しりとり単語送信
- `/slot` スロットマシン
- `/tictactoe` ○×ゲーム（2人用）
- `/tictactoe_move` ○×ゲームのマス指定
- `/ranking` 勝利数ランキング
- TRPG支援コマンド強化

### 🔊 ボイスチャンネル読み上げ機能

- `/voicejoin` VCに接続
- `/voicesay` ふらんちゃんの声で喋る（VoiceVox）
- VC内のテキストメッセージを自動で読み上げ
- `/voiceleave` VCから退出

> ※ VoiceVox + FFmpeg によるTTS（ふらんちゃんボイス）で再生

### 💰 ポイント＆ランク機能

- `text_points`：メッセージ送信で自動加算
- `voice_points`：VCにいると定期加算（1分ごと）
- `/rank`：自分のランク＆ポイント確認

> 💾 `points.json` に自動保存され、Bot再起動でも維持されます。

### 📊 統計・情報機能

- `/server_stats` サーバー統計情報
- `/user_stats` ユーザー統計情報
- `/system_info` Botシステム情報
- `/logs` Botログ表示（管理者専用）

### 🎨 カスタマイズ機能

- `/custom_command` カスタムコマンド作成
- `/custom_command_list` カスタムコマンド一覧

### 🎉 ウェルカム機能

- 新メンバー歓迎メッセージ
- メンバー退出メッセージ
- 自動統計更新

### 🔁 自動再起動

- 毎秒単位で再起動までのカウントダウンを表示
- Botの安定運用のため、最大4時間ごとに再起動（設定可能）

### 🛠️ 管理者機能

- `/shutdown` Botをシャットダウン
- `/restart` Botを再起動
- `/sync_commands` スラッシュコマンド同期
- `/delete` メッセージ削除
- コンソールからのコマンド実行

### 🛡️ サーバー管理機能（拡張）
- NGワード検知・自動削除
- スパム検知・自動BAN/KICK
- メンバー入退室ログ強化
- 自動ロール付与
- `/ban` ユーザーをBAN（管理者専用）
- `/kick` ユーザーをKICK（管理者専用）
- `/mute` ユーザーをミュート（管理者専用）
- `/unmute` ユーザーのミュート解除（管理者専用）
- `/warn` ユーザーに警告（管理者専用）
- 違反時の管理者通知

### 🔔 通知・リマインダー機能（拡張）
- `/remind` 指定時間後にリマインド
- `/remind_daily` 毎日のリマインド設定
- `/remind_weekly` 毎週のリマインド設定
- `/calendar_add` カレンダーにイベント追加
- `/calendar_show` イベント一覧表示
- `/birthday_add` 誕生日登録
- `/birthday_show` 誕生日一覧表示
- 自動通知システム

---

## 🚀 導入方法

### 1. Pythonとライブラリをインストール

```bash
pip install -r requirements.txt
```

### 2. .envファイルを作成

プロジェクトのルートに `.env` を作成して下記を記述：

```env
DISCORD_TOKEN=あなたのBotトークン
GUILD_ID=（任意）ギルドID
OWNER_ID=Botの管理者ユーザーID
CONSOLE_OUTPUT_CHANNEL_ID=（任意）コンソールからのメッセージ送信用チャンネルID
WELCOME_CHANNEL_ID=（任意）ウェルカムメッセージ送信用チャンネルID
FFMPEG_PATH=ffmpegのパス
VOICEVOX_PATH=VoiceVoxのパス
VOICEVOX_API_URL=http://127.0.0.1:50021
TENOR_API_KEY=LIVDSRZULELA
HUGGINGFACE_API_KEY=（任意）Hugging Face APIキー（無料AI機能使用時）
```

### 3. 実行方法

```bash
python flandre_bot.py
```

---

## 📁 ファイル構成

- `flandre_bot.py` - メインのBotコード
- `commands.json` - コンソールコマンド設定
- `helps.json` - ヘルプメッセージ設定
- `points.json` - ポイントデータ（自動生成）
- `custom_commands.json` - カスタムコマンド（自動生成）
- `bot.log` - Botログ（自動生成）
- `.env` - 環境変数設定
- `requirements.txt` - 必要なライブラリ一覧

---

## 🎯 主な特徴

- **多機能**：エンタメ、ゲーム、音楽、読み上げ、AIチャット、画像生成など幅広い機能
- **AI対応**：OpenAI APIを使用したチャットと画像生成
- **安定性**：自動再起動機能で長時間運用に対応
- **カスタマイズ性**：JSONファイルでコマンドやヘルプをカスタマイズ可能
- **ユーザーフレンドリー**：日本語対応で使いやすい
- **拡張性**：新しい機能を簡単に追加可能
- **統計機能**：サーバーとユーザーの詳細統計
- **ウェルカム機能**：新メンバー歓迎システム

---

## 🔧 新機能詳細

### AIチャット機能（無料版）
- Hugging Face APIを使用（無料）
- ふらんちゃんの性格設定で会話
- ユーザー別チャット履歴管理
- 履歴リセット機能

### 画像検索機能（完全無料版）
- APIキー不要で完全無料
- 複数の画像ソースを自動切り替え
- Pixabay、Unsplash、Pexels、代替画像を順次試行
- カテゴリ別の代替画像機能
- エラー時も確実に画像を表示

### 多言語翻訳機能
- 9言語対応（日本語、英語、韓国語、中国語、スペイン語、フランス語、ドイツ語、イタリア語、ポルトガル語、ロシア語）
- Google翻訳API使用

### 音楽機能強化
- YouTube検索機能
- yt-dlpによる高品質再生
- プレイリスト管理強化

### ゲーム機能追加
- じゃんけんゲーム
- 数字当てゲーム
- 統計機能付き

### 統計・ログ機能
- サーバー統計表示
- ユーザー統計表示
- システム情報表示
- 詳細ログ機能

### ゲーム・娯楽機能（拡張）
- `/quiz` クイズを出題
- `/quiz_answer` クイズの答えを送信
- `/shiritori` しりとり開始
- `/shiritori_word` しりとり単語送信
- `/slot` スロットマシン
- `/tictactoe` ○×ゲーム（2人用）
- `/tictactoe_move` ○×ゲームのマス指定
- `/ranking` 勝利数ランキング
- TRPG支援コマンド強化

### 通知・リマインダー機能（拡張）
- `/remind` 指定時間後にリマインド
- `/remind_daily` 毎日のリマインド設定
- `/remind_weekly` 毎週のリマインド設定
- `/calendar_add` カレンダーにイベント追加
- `/calendar_show` イベント一覧表示
- `/birthday_add` 誕生日登録
- `/birthday_show` 誕生日一覧表示
- 自動通知システム

---

## 📝 ライセンス

MITライセンス（改変・再配布OK！）

---

## 🌸 最後に

ふらんちゃんBotでDiscordをもっとにぎやかにしようねっ♡  
TRPG勢も、雑談鯖も、みーんなに使ってほしいよ！

―― From ふらんちゃん

## 🚀 Bot本体とWebダッシュボードの同時運用ガイド

### 構成例
- `flandre_bot.py`（Bot本体）
- `web_dashboard.py`（Webダッシュボード）

### 推奨起動方法

**1. 2つのコマンドプロンプト/ターミナルを開く**

- 1つ目でBot本体を起動：
  ```bash
  python flandre_bot.py
  ```
- 2つ目でWebダッシュボードを起動：
  ```bash
  python web_dashboard.py
  ```
  または
  ```bash
  start_dashboard.bat
  ```

**同時に起動してもお互いの動作に影響しません。**

### 注意点
- Bot本体とWebダッシュボードは**完全に独立したプロセス**です。
- どちらかが落ちても、もう一方は動作し続けます。
- サーバー運用時は`screen`や`tmux`、Windowsなら複数のコマンドプロンプト/PowerShellを活用してください。
- サーバー自動起動・監視には`pm2`や`Supervisor`などのプロセス管理ツールもおすすめです。

---

## 📝 導入・運用ガイド（日本語）

### 必要なもの
- Python 3.8以上
- Discord Botトークン
- 必要なPythonパッケージ（`requirements.txt`）

### セットアップ手順
1. **リポジトリのダウンロード**
   ```bash
   git clone <このリポジトリのURL>
   cd fran_bot
   ```
2. **依存パッケージのインストール**
   ```bash
   pip install -r requirements.txt
   ```
3. **環境変数の設定**
   - `env.txt`または`.env`ファイルを作成し、以下の内容を記入：
     ```
     DISCORD_TOKEN=あなたのBotトークン
     OWNER_ID=あなたのDiscordユーザーID
     FFMPEG_PATH=ffmpeg.exeのパス
     VOICEVOX_PATH=voicevox_engine.exeのパス
     RESOURCE_ALERT_CHANNEL_ID=通知用チャンネルID（任意）
     ```
4. **Botの起動**
   ```bash
   python flandre_bot.py
   ```
5. **Webダッシュボードの起動（任意）**
   ```bash
   python web_dashboard.py
   ```
   または
   ```bash
   start_dashboard.bat
   ```

### よくあるトラブルと対策
- **Botが起動しない/エラーが出る**
  - Pythonバージョンや依存パッケージを確認
  - トークンやパスが正しいか確認
  - `ffmpeg`や`voicevox_engine`が正しくインストールされているか確認
- **音楽再生ができない**
  - `yt-dlp`がインストールされているか確認
  - `FFMPEG_PATH`が正しいか確認
- **Webダッシュボードが開けない**
  - `Flask`がインストールされているか確認
  - ポート5000が他のアプリで使われていないか確認
- **リマインダーや通知が届かない**
  - `OWNER_ID`や`RESOURCE_ALERT_CHANNEL_ID`が正しいか確認

### FAQ（よくある質問）
- **Q. Botのコマンド一覧を知りたい**
  - `/help`コマンドまたはWebダッシュボードの「コマンド」タブで確認できます。
- **Q. Botの再起動・シャットダウン方法は？**
  - `/shutdown`コマンド（管理者専用）でシャットダウンできます。
  - 再起動はBotを一度終了し、再度`python flandre_bot.py`で起動してください。
- **Q. サーバーに複数Botを入れても大丈夫？**
  - 問題ありませんが、コマンドの競合に注意してください。
- **Q. コマンドのカスタマイズは？**
  - `custom_commands.json`や`helps.json`を編集することでカスタムコマンドや説明を追加できます。

---

## 📝 コマンド一覧（自動生成）

以下は`helps.json`から自動生成されたコマンド一覧です（一部抜粋）：

| コマンド名 | 説明 | 使い方 | エイリアス | カテゴリ |
|:---|:---|:---|:---|:---|
{% for cmd in category_commands.values()|sum(start=[]) %}
| {{ cmd.name }} | {{ cmd.description }} | {{ cmd.usage or '-' }} | {{ cmd.aliases|join(', ') if cmd.aliases else '-' }} | {{ cmd.category or '-' }} |
{% endfor %}

---

## 📝 ヘルプ・サポート
- 詳しい使い方は `/help` コマンド、またはWebダッシュボードの「コマンド」タブをご覧ください。
- それでも解決しない場合は、GitHubのIssuesや管理者までご連絡ください。

---