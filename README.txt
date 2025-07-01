＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
🌟 FlandreBot（ふらんちゃんBot_V6.3） - Discord用日本語Bot
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

ふらんちゃんBotは、東方Projectのフランドール・スカーレット風の
かわいくて多機能な Discord Bot です！

雑談からTRPG、画像検索、VC読み上げ、BGM再生、人狼ゲーム、ランクポイント管理、
AIチャット、画像生成、多言語翻訳まで色んなことができるすごい子だよ♡


【主な機能】

● AI・チャット機能（無料版）
・/chat              無料AIふらんちゃんと会話（Hugging Face API）
・/chat_reset        AIチャット履歴リセット
・/generate_image    完全無料画像検索（APIキー不要）
・/translate_advanced 多言語翻訳（9言語対応）

● エンタメ・便利系コマンド
・/hello         あいさつ
・/dice          サイコロ（例: 2d6+1）
・/omikuji       おみくじ
・/quote         名言を教えてくれる
・/cat           猫画像で癒される
・/translate     翻訳（英⇔日）
・/math          数式計算
・/weatherjp     日本の天気（API不要）
・/gif           キーワードでGIFを検索（Tenor API利用）
・/pixabay_large 高画質画像検索
・/fortune       今日の運勢
・/choose        選択肢からランダム選択
・/poll          投票機能
・/remind        リマインダー機能

● BGM・音楽機能
・/join          VCに接続
・/leave         VCから退出
・/play          YouTubeのBGMを再生
・/search_music  YouTubeで音楽検索・再生
・/stop          BGMを停止
・/volume        音量調整（0-100）
・/nowplaying    現在再生中の曲を確認
・/bgm           テキストチャンネルでBGM再生
・/bgm_stop      テキストチャンネルのBGM停止

● プレイリスト機能
・/playlist_create   プレイリスト作成
・/playlist_add      プレイリストに曲を追加
・/playlist_show     プレイリスト表示
・/playlist_play     プレイリスト再生
・/playlist_list     自分のプレイリスト一覧
・/playlist_delete   プレイリスト削除
・/playlist_remove   プレイリストから曲を削除
・/playlist_export   プレイリストをエクスポート
・/playlist_youtube  YouTubeプレイリストを読み込み

● ゲーム機能
・人狼ゲーム：/jinro, /jijoin, /start_jinro, /divine, /guard, /attack など
・TRPGキャラクター管理：/trpg_char_create, /trpg_char_show, /trpg_char_edit など
・じゃんけんゲーム：/rps グー・チョキ・パー
・数字当てゲーム：/number_guess, /guess 数字を当てよう

● ボイスチャンネル 読み上げ機能
・/voicejoin     ボイスチャンネルに入る
・/voicesay      メッセージをふらんちゃんボイスで読み上げ
・/voiceleave    VCから抜ける

※ VoiceVox + FFmpegで音声合成するよ！

● ランクポイント機能（ProBot風）
・text_points  : メッセージごとに自動加算
・voice_points : VCにいる間 1分ごと加算
・/rank         現在のポイントとランク表示

💾 points.json に自動保存され、Bot再起動でも維持されます。

● 統計・情報機能
・/server_stats   サーバー統計情報
・/user_stats     ユーザー統計情報
・/system_info    Botシステム情報
・/logs           Botログ表示（管理者専用）

● カスタマイズ機能
・/custom_command     カスタムコマンド作成
・/custom_command_list カスタムコマンド一覧

● ウェルカム機能
・新メンバー歓迎メッセージ
・メンバー退出メッセージ
・自動統計更新

● 自動再起動
・4時間ごとに自動で再起動（変更可）
・コンソールに残り時間を毎秒表示してくれる

● 管理者機能
・/shutdown      Botをシャットダウン
・/restart       Botを再起動
・/sync_commands スラッシュコマンド同期
・/delete        メッセージ削除
・コンソールからのコマンド実行


【導入方法】

1. 必要なライブラリをインストール

    pip install -r requirements.txt

   もしくは手動で：

    pip install discord.py python-dotenv aiohttp pyopenjtalk soundfile requests beautifulsoup4 yt-dlp PyNaCl urllib3 openai psutil asyncio-mqtt python-dateutil

2. .envファイルを用意

   ファイル名：.env

   中身の例：

   DISCORD_TOKEN=あなたのボットのトークン
   GUILD_ID=123456789012345678
   OWNER_ID=あなたのユーザーID
   CONSOLE_OUTPUT_CHANNEL_ID=ログ出力先のチャンネルID（任意）
   WELCOME_CHANNEL_ID=ウェルカムメッセージ送信用チャンネルID（任意）
   FFMPEG_PATH=ffmpegのパス
   VOICEVOX_PATH=VoiceVoxのパス
   VOICEVOX_API_URL=http://127.0.0.1:50021
   TENOR_API_KEY=LIVDSRZULELA
   HUGGINGFACE_API_KEY=Hugging Face APIキー（無料AI機能使用時、任意）

3. Botを起動！

    python flandre_bot.py


【補足ファイル】

・flandre_bot.py       メインのコード
・commands.json        コマンド設定とエイリアス
・helps.json           /helpコマンドの説明文
・points.json          ランクポイント保存ファイル（自動生成）
・custom_commands.json カスタムコマンド保存ファイル（自動生成）
・bot.log              Botログファイル（自動生成）
・.env                 環境変数ファイル（手動で作成）


【特殊機能】

・AIチャット機能（Hugging Face API使用、無料）
・画像検索機能（完全無料・APIキー不要）
・多言語翻訳機能（9言語対応）
・コンソール操作（Bot起動中にターミナルでコマンド送信可能）
・再起動系コマンド（/shutdown, /restart）あり
・ネットとDiscordの応答速度を測る /ping
・Pixabay画像やGIFをキーワードで検索
・YouTubeのBGM再生機能
・プレイリスト管理機能
・人狼ゲーム機能
・TRPGキャラクター管理機能
・ポイント・ランクシステム
・じゃんけんゲーム・数字当てゲーム
・サーバー・ユーザー統計機能
・ウェルカム機能
・カスタムコマンド機能
・詳細ログ機能


【新機能詳細】

● AIチャット機能（無料版）
・Hugging Face APIを使用（無料）
・ふらんちゃんの性格設定で会話
・ユーザー別チャット履歴管理
・履歴リセット機能

● 画像検索機能（完全無料版）
・APIキー不要で完全無料
・複数の画像ソースを自動切り替え
・Pixabay、Unsplash、Pexels、代替画像を順次試行
・カテゴリ別の代替画像機能
・エラー時も確実に画像を表示

● 多言語翻訳機能
・9言語対応（日本語、英語、韓国語、中国語、スペイン語、フランス語、ドイツ語、イタリア語、ポルトガル語、ロシア語）
・Google翻訳API使用

● 音楽機能強化
・YouTube検索機能
・yt-dlpによる高品質再生
・プレイリスト管理強化

● ゲーム機能追加
・じゃんけんゲーム
・数字当てゲーム
・統計機能付き

● 統計・ログ機能
・サーバー統計表示
・ユーザー統計表示
・システム情報表示
・詳細ログ機能


【ライセンス】

MITライセンス（改変・再配布OK！）


【最後に】

ふらんちゃんBotでDiscordをもっとにぎやかにしようねっ♡
TRPG勢も、雑談鯖も、みーんなに使ってほしいよ！

―― From ふらんちゃん
