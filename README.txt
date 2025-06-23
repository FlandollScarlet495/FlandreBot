＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
🌟 FlandreBot（ふらんちゃんBot） - Discord用日本語Bot
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

● ボイスチャンネル 読み上げ機能
・/voicejoin     ボイスチャンネルに入る
・/voicesay      メッセージをふらんちゃんボイスで読み上げ
・/voiceleave    VCから抜ける

※ pyopenjtalk + FFmpegで音声合成するよ！

● ランクポイント機能（ProBot風）
・text_points  : メッセージごとに自動加算
・voice_points : VCにいる間 1分ごと加算
・/rank         現在のポイントとランク表示

● 自動再起動
・1時間ごとに自動で再起動（変更可）
・コンソールに残り時間を毎分表示してくれる


【導入方法】

1. 必要なライブラリをインストール

    pip install -r requirements.txt

   もしくは手動で：

    pip install discord.py python-dotenv aiohttp pyopenjtalk soundfile requests beautifulsoup4

2. .envファイルを用意

   ファイル名：.env

   中身の例：

   DISCORD_TOKEN=あなたのボットのトークン
   GUILD_ID=123456789012345678
   OWNER_ID=あなたのユーザーID
   CONSOLE_OUTPUT_CHANNEL_ID=ログ出力先のチャンネルID（任意）


3. Botを起動！

    python flandre_bot.py


【補足ファイル】

・flandre_bot.py       メインのコード
・commands.json        コマンド設定とエイリアス
・helps.json           /helpコマンドの説明文
・points.json          ランクポイント保存ファイル（自動生成）
・.env                 環境変数ファイル（手動で作成）


【特殊機能】

・コンソール操作（Bot起動中にターミナルでコマンド送信可能）
・再起動系コマンド（/shutdown, /restart）あり
・ネットとDiscordの応答速度を測る /ping
・Pixabay画像やGIFをキーワードで検索


【ライセンス】

MITライセンス（改変・再配布OK！）


【最後に】

ふらんちゃんBotでDiscordをもっとにぎやかにしようねっ♡
TRPG勢も、雑談鯖も、みーんなに使ってほしいよ！

―― From ふらんちゃん
