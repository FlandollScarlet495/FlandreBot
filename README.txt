提供していただいたスクリーンショットは、FlandreBotがDiscord上でどのように表示されるかを示していますね。特に、コマンド一覧の一部が表示されており、ボットが正常に動作している様子が伺えます。

このスクリーンショットをREADME.mdに組み込むことで、ボットの見た目や使い方がより直感的に伝わるようになります。

以下に、スクリーンショットを活用したREADME.mdの更新提案をします。ダウンロード可能な形式で提供しますので、既存のREADME.mdを置き換えるか、該当箇所を更新してください。

ここから下のテキストをコピーして、README.md というファイル名で保存してください。
FlandreBot
（任意: ボットのロゴ画像があれば上記URLを実際の画像URLに置き換えてください。もし不要であれば行ごと削除してください）

FlandreBotは、あなたのDiscordサーバーを彩り豊かにし、日々のコミュニケーションやサーバー運営をサポートするための多機能Discordボットです。楽しいエンターテイメントコマンドから便利なユーティリティ機能まで、様々なニーズに対応します。

目次
FlandreBotとは？
主な特徴
はじめる前に (準備)
FlandreBotの導入方法
使い方
コマンド一覧 (一部)
ボットの動作イメージ
開発者の方へ
貢献したい！
ライセンス
FlandreBotとは？
FlandreBotは、Discordサーバーの活性化と利便性向上を目指して開発された、日本語に特化した Discordボットです。ユーザーが直感的に操作できるスラッシュコマンドを中心に、様々な機能を提供します。

主な特徴
FlandreBotは、以下のような多彩な機能を提供し、あなたのサーバーライフを豊かにします。

🎉 エンターテイメント機能:
おみくじ: 運勢を占います。
ランダムコンテンツ: 画像、GIF、動画、音楽など、様々なランダムコンテンツで会話を盛り上げます。
TRPG風サイコロ: 2d6+1 のような形式でサイコロを振ることができます。
名言: 心に響く名言を届けます。
猫画像: かわいい猫の画像で癒やしを提供します。
東方キャラクター紹介: 東方Projectのキャラクターについて教えてくれます。
🛠️ 便利なユーティリティ機能:
URL短縮: 長いURLを短くします。
天気予報: 日本の主要都市の天気をお知らせします。
翻訳: 英語と日本語間の翻訳を行います。
リマインダー: 指定した時間にメッセージを通知します。
投票: サーバーメンバーで簡単に投票を作成できます。
数式計算: 簡単な数式を計算します。
Urban Dictionary検索: 英単語のスラングや俗語の意味を調べます。
ℹ️ 情報提供コマンド:
ボット情報、サーバー情報、ユーザー情報、アバター表示など、必要な情報を素早く取得できます。
🔧 簡単なコマンド管理:
commands.json と helps.json ファイルを編集するだけで、コマンドの追加、変更、削除が容易に行えます。
🔄 安定稼働:
設定された時間間隔での自動再起動機能を備え、ボットの安定した動作をサポートします。
⚡ スラッシュコマンド対応:
Discordのネイティブなスラッシュコマンドに対応しており、コマンド入力がよりスムーズで直感的です。
はじめる前に (準備)
FlandreBotを稼働させるには、いくつかの準備が必要です。

Pythonのインストール: お使いのシステムにPython 3.8以降がインストールされていることを確認してください。 Python公式サイト からダウンロードできます。
Discordボットトークンの取得:
Discord Developer Portal にアクセスします。
「New Application」をクリックし、新しいアプリケーションを作成します。
作成したアプリケーションの「Bot」タブに移動し、「Add Bot」をクリックしてボットを作成します。
「TOKEN」セクションの「Reset Token」をクリックし、表示されたトークンをコピーしておきます。このトークンは誰にも教えないでください。
「Privileged Gateway Intents」の「MESSAGE CONTENT INTENT」をオンにしてください。
ボットをサーバーに招待:
「OAuth2」タブの「URL Generator」に移動します。
SCOPESでbotとapplications.commandsにチェックを入れます。
BOT PERMISSIONSで必要な権限（例: Send Messages, Read Message History, Use Slash Commandsなど）を選択します。
生成されたURLをコピーし、ブラウザで開いてボットをあなたのサーバーに招待します。
FlandreBotの導入方法
以下の手順に従って、FlandreBotをセットアップし、実行してください。

リポジトリをクローンする:
まず、このプロジェクトをローカル環境にダウンロードします。

Bash

git clone https://github.com/yourusername/yourrepository.git
cd FlandreBot
(yourusername と yourrepository は、ご自身のGitHubアカウントとリポジトリ名に置き換えてください。)

必要なライブラリをインストールする:
ボットの実行に必要なPythonライブラリを一括でインストールします。

Bash

pip install -r requirements.txt
(requirements.txt がない場合、flandre_bot.py の import 文から必要なライブラリを手動でリストアップし、インストールしてください。例: discord.py, python-dotenv, aiohttp, beautifulsoup4, pyopenjtalk, soundfile, requests)

環境変数を設定する:
プロジェクトのルートディレクトリに .env という名前の新しいファイルを作成し、以下の内容を記述してください。

コード スニペット

DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
GUILD_ID=YOUR_GUILD_ID_HERE # スラッシュコマンドを特定のサーバーに即座に同期する場合のみ必要です。不要なら行ごと削除してください。
YOUR_BOT_TOKEN_HERE には、「はじめる前に」 のステップで取得したDiscordボットのトークンを貼り付けてください。
YOUR_GUILD_ID_HERE には、スラッシュコマンドをすぐに同期したいDiscordサーバーのIDを入力します。これは開発中にコマンドの反映を速くしたい場合に便利です。グローバルに同期する場合はこの行は不要です。
JSONファイルの確認:
commands.json と helps.json ファイルが flandre_bot.py と同じディレクトリに配置されていることを確認してください。これらのファイルはボットのコマンド定義とヘルプメッセージを管理します。

FlandreBotを起動する:
以下のコマンドを実行してボットを起動します。

Bash

python flandre_bot.py
ボットが正常に起動すると、コンソールに「ログインしました」などのメッセージが表示されます。

使い方
FlandreBotは、Discordサーバーに参加後、以下の方法で利用できます。

スラッシュコマンド (/):
Discordのテキストチャンネルで / を入力すると、FlandreBotが提供するコマンドのリストが表示されます。表示されたリストから使いたいコマンドを選択し、必要な情報を入力して実行します。
例: /hello と入力してEnterキーを押す。

テキストコマンド (エイリアス):
一部のコマンドは、プレフィックスなしで直接メッセージとして入力することもできます（例: ping）。どのコマンドがテキストコマンドに対応しているかは commands.json ファイルの aliases フィールドを参照してください。

コマンド一覧 (一部)
FlandreBotが提供するすべてのコマンドを見るには、Discordサーバー内で /help コマンドを使用してください。または、helps.json ファイルを直接参照することもできます。

以下に、利用頻度の高いコマンドの一部を抜粋してご紹介します。

コマンド名	説明	使用例
/hello	ふらんちゃんがあいさつするよ♡	/hello
/ping	ふらんちゃんがネットとDiscordの応答速度をチェックするよ♡	/ping
/info	ふらんちゃんの情報を教えるよ♡	/info
/help	ふらんちゃんの使い方を教えるよ♡	/help
/dice <回数>d<面数>+<加算値>	TRPG風サイコロ（例: 2d6+1）を振るよ！	/dice 1d20+5
/omikuji	ふらんちゃんがおみくじ引いてあげるよ♡	/omikuji
/say <message>	ふらんちゃんに好きなメッセージを言わせるよ♡	/say こんにちは
/translate <テキスト>	英語⇔日本語を翻訳するよ♡	/translate Hello
/weatherjp <都市名>	日本の主要都市の天気を教えるよ♡	/weatherjp 東京
/poll <質問> <選択肢1> ...	みんなで投票しよう！	/poll 好きな食べ物 ラーメン カレー
/cat	ランダムな猫の画像を送るよ♡	/cat
/urban <word>	英単語の意味を調べるよ（Urban Dictionary風）	/urban LOL
/remind <時間> <メッセージ>	指定した時間後にリマインドするよ♡	/remind 1h 宿題をやる
/math <数式>	数式を計算するよ♡	/math (5+3)*2
/random_image	ふらんちゃんがランダムな画像を送るよ♡	/random_image
/serverinfo	このサーバーの情報を教えるよ♡	/serverinfo
/userinfo <ユーザー>	指定したユーザーの情報を表示するよ♡	/userinfo @ユーザー名
/avatar <ユーザー>	指定したユーザーのアイコンを表示するよ♡	/avatar @ユーザー名
/quote	ふらんちゃんが名言を教えるよ♡	/quote
/shorten <URL>	URLを短縮するよ♡	/shorten https://example.com
/shutdown	ボットを終了するよ（管理者権限が必要）	/shutdown
ボットの動作イメージ
FlandreBotがDiscord上でどのように動作するかを視覚的に確認できます。

（この画像は、FlandreBotの/helpコマンド実行時の表示例です。実際の画像パスに合わせてください）

開発者の方へ
FlandreBotの内部構造やコマンドの追加・変更について説明します。

プロジェクトの主要ファイル
flandre_bot.py: ボットのメインスクリプト。Discord APIとの連携、イベントハンドリング、コマンドの処理ロジックが含まれています。
commands.json: ボットが提供するすべてのコマンドの定義（スラッシュコマンド名、エイリアス、使用法、説明、コマンドタイプ）がJSON形式で記述されています。新しいコマンドを追加する際には、このファイルを編集します。
helps.json: /help コマンドを実行した際に表示される、各コマンドの詳細な説明がJSON形式で記述されています。
新しいコマンドの追加・既存コマンドの変更
新しい機能を追加したり、既存のコマンドの動作を変更したりするには、主に以下のファイルを編集します。

commands.json の編集:
新しいコマンドの定義を追加するか、既存のコマンドのエントリを更新します。

JSON

{
  "name": "/my_new_command",
  "aliases": ["/mnc", "mynewcmd"],
  "usage": "/my_new_command [オプション]",
  "description": "これは新しいコマンドの短い説明です。",
  "type": "custom_command_type" // 処理ロジックと紐づく任意のタイプ名
}
name: スラッシュコマンド名です。
aliases: テキストコマンドとして認識させたい別名（エイリアス）のリストです。
usage: コマンドの使用方法の簡単な説明です。
description: コマンドの概要です。
type: flandre_bot.py 内で、このコマンドがどのような処理を行うかを識別するためのカスタムタイプです。
flandre_bot.py のロジック追加:
commands.json で定義した type に対応する処理ロジックを flandre_bot.py 内の適切な箇所に追加します。通常は、@bot.tree.command デコレータを使ったスラッシュコマンドの定義や、on_message イベント内でテキストコマンドを処理する部分になります。

helps.json の編集 (任意):
/help コマンドで表示される詳細な説明を追加・更新します。

JSON

{
  "name": "/my_new_command",
  "description": "新しいコマンドの具体的な機能や使い方についての詳細な説明だよ♡"
}
変更を適用するには、ボットを再起動してください。

貢献したい！
FlandreBotの改善にご協力いただける方を心から歓迎します！バグ報告、機能の提案、コードの改善（プルリクエスト）など、どのような形でも貢献を歓迎いたします。

貢献の手順は以下の通りです。

このリポジトリをフォーク（Fork）します。
新機能開発やバグ修正のための新しいブランチを作成します (git checkout -b feature/your-feature-name または bugfix/issue-description)。
変更を加え、コミットします (git commit -m 'feat: Add amazing new feature')。
変更をあなたのフォークにプッシュします (git push origin feature/your-feature-name)。
このリポジトリに対してプルリクエスト（Pull Request）を作成し、変更内容を説明してください。
ライセンス
このプロジェクトはMIT Licenseのもとで公開されています。

MIT License

Copyright (c) 2024 [あなたの名前 または 著作権所有者名]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ANCTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.