# importやformのインポート
# このスクリプトは、DiscordのBotを作成するためのものです
import os # 環境変数を扱うためのモジュール
import sys # システム関連の情報を扱うためのモジュール
import re # 正規表現を使用して文字列を操作するためのモジュール
import threading # threadingを使用してマルチスレッド処理を行うためのモジュール
import discord # DiscordのAPIを使用するためのモジュール
import json # JSON形式のデータを扱うためのモジュール
import time # 時間を扱うためのモジュール
import random # ランダムな要素を扱うためのモジュール
import asyncio # 非同期処理を行うためのモジュール
import datetime # 日時を扱うためのモジュール
import traceback # トレースバックを取得するためのモジュール
import aiohttp # 非同期HTTPリクエストを扱うためのモジュール
import pyopenjtalk
import discord
import soundfile as sf
import requests
from bs4 import BeautifulSoup
from discord.ext import commands # コマンドを使うためのモジュール
from discord import app_commands, Interaction, Embed # DiscordのAPIを使用するためのモジュール
from dotenv import load_dotenv # 環境変数を読み込むためのライブラリ
from datetime import datetime # 日時を扱うためのモジュール
from discord.ext import tasks # ランクコマンドで使うためのモジュール

# これだけでOKだよ♪
with open("helps.json", "r", encoding="utf-8") as f:
    data = json.load(f)  # すでにPythonの辞書に変換されてるよ！

COMMANDS_INFO = [(cmd["name"], cmd["description"]) for cmd in data["helps"]]

# 環境変数の読み込み
# GUILD_IDは数字だからint()で変換するのはOKだよ！
# もしGUILD_IDが設定されてなかったら、デフォルトで0にするよ。
GUILD_ID = int(os.getenv("GUILD_ID", "0"))

# Tenor APIキーは文字列だからint()は付けないよ！
TENOR_API_KEY = os.getenv("TENOR_API_KEY")

# 新しく追加するCONSOL_OUTPUT_CHANNEL_IDだよ！
# これは数字だからint()で変換するけど、もし.envに設定されてなかったら警告を出すよ。
CONSOLE_OUTPUT_CHANNEL_ID = os.getenv("CONSOLE_OUTPUT_CHANNEL_ID")
if CONSOLE_OUTPUT_CHANNEL_ID:
    CONSOLE_OUTPUT_CHANNEL_ID = int(CONSOLE_OUTPUT_CHANNEL_ID)
else:
    print("⚠️ CONSOLE_OUTPUT_CHANNEL_IDが.envに設定されていません！コンソールからのメッセージ送信ができないかも…！")
    CONSOLE_OUTPUT_CHANNEL_ID = None # 設定されていなければNoneにしておくね


intents = discord.Intents.default()
intents.members = True  # メンバー情報を取るために必須！
intents.message_content = True

# ふらんちゃんBotのクラス定義
# ふらんちゃんはかわいい女の子のキャラクターで、DiscordのBotとして動作します。
# 彼女はユーザーとのインタラクションを通じて、愛らしい性格を表現し、ユーザーに楽しさと癒しを提供します。
# ふらんちゃんは、スラッシュコマンドを使用して、あいさつや情報提供、応答速度の測定などを行います。
# 彼女は、ユーザーからのコマンドに対して、優しく、時にはユーモラスに応答します。

class FranBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

        # 人狼ゲーム用のグローバルデータをインスタンス属性に
        self.jinro_players = []
        self.jinro_roles = {}
        self.jinro_votes = {}
        self.jinro_protected = None
        self.jinro_seer_results = {}
        self.jinro_night_actions = {}

    async def setup_hook(self):
        await self.tree.sync()  # グローバルに同期するよ！
        print("✅ スラッシュコマンドを全体に同期したよ〜！（グローバル）")

    async def on_ready(self):
        print(f"✨ ふらんちゃんBotが起動したよっ！")

    async def on_message(self, message):
        # 自分の処理（もし自分のメッセージなら無視とか）
        if message.author.bot:
         return
        # ここで好きなメッセージ処理してね
        
        # コマンド処理は絶対呼んで！
        await self.process_commands(message)

bot = FranBot()

# GIFコマンド！！

# GIFコマンド！！ ここから下を追加・確認してね！
@bot.tree.command(name="gif", description="キーワードでTenorのGIFを検索するよ！")
@app_commands.describe(keyword="検索したいキーワードを入れてね！")
async def gif(interaction: discord.Interaction, keyword: str):
    if not TENOR_API_KEY:
        await interaction.response.send_message("ごめんね、Tenor APIキーが設定されてないからGIFを検索できないの…！💦", ephemeral=True)
        return

    url = f"https://g.tenor.com/v1/search?q={keyword}&key={TENOR_API_KEY}&limit=1"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data and data['results']:
                    gif_url = data['results'][0]['media'][0]['gif']['url']
                    await interaction.response.send_message(gif_url)
                else:
                    await interaction.response.send_message(f"「{keyword}」のGIFは見つからなかったよ…ごめんね！😢")
            else:
                await interaction.response.send_message(f"うぅ、Tenor APIとの通信でエラーが出ちゃったの…！(エラーコード: {response.status})")

# ふらんちゃんのあいさつコマンド

@bot.tree.command(name="hello", description="ふらんちゃんがあいさつするよ♡")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("こんにちはっ、ふらんちゃんだよ♡")

# ふらんちゃんの応答速度を測るコマンド

@bot.tree.command(name="ping", description="ふらんちゃんがネットとDiscordの応答速度をチェックするよ♡")
async def ping(interaction: discord.Interaction):
    await interaction.response.defer()

    # 🌀 Discordの応答速度取得（WebSocket）
    discord_latency = round(bot.latency * 1000)
    if discord_latency > 150:
        discord_comment = "今ちょっと遅いかも💦"
    else:
        discord_comment = "今はちょっと早〜い💨しゅびんしゅびん♪"

    # 🌐 インターネットPing（Google）
    proc = await asyncio.create_subprocess_exec(
        "ping", "-n", "1", "www.google.com",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        await interaction.followup.send("インターネット側のpingコマンドが失敗しちゃったよ…💔", ephemeral=True)
        return

    output = stdout.decode("cp932", errors="ignore")
    match = re.search(r"平均 = (\d+)ms", output)
    if not match:
        match = re.search(r"Average = (\d+)ms", output)
    if match:
        net_latency = int(match.group(1))
        if net_latency > 150:
            net_comment = "インターネットも…ちょっと重いかも〜💦"
        else:
            net_comment = "ネットも軽やか♪すいすいっ🐬"
    else:
        await interaction.followup.send("インターネット遅延が取得できなかったの…🥺", ephemeral=True)
        return

    # 📡 両方の結果まとめて送信っ！
    await interaction.followup.send(
        f"🌐 インターネット遅延: `{net_latency}ms`　→ {net_comment}\n"
        f"💬 Discord応答速度: `{discord_latency}ms`　→ {discord_comment}"
    )

# ふらんちゃんの情報を教えるコマンド

@bot.tree.command(name="info", description="ふらんちゃんの情報を教えるよ♡")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(title="ふらんちゃんBotの情報", description="ふらんちゃんはかわいいよ♡", color=0xFF69B4)
    embed.add_field(name="バージョン", value="4.5.0", inline=False)
    embed.add_field(name="開発者", value="けんすけ", inline=False)
    await interaction.response.send_message(embed=embed)

# ふらんちゃんの使い方を教えるコマンド

@bot.tree.command(name="help", description="ふらんちゃんの使い方を教えるよ♡")
async def help_command(interaction: Interaction):
    fields_per_embed = 25
    embeds = []
    for i in range(0, len(COMMANDS_INFO), fields_per_embed):
        embed = Embed(
            title="ふらんちゃんBotの使い方",
            description="以下のコマンドが使えるよ♡",
            color=0xFF69B4
        )
        for name, desc in COMMANDS_INFO[i:i+fields_per_embed]:
            embed.add_field(name=name, value=desc, inline=False)
        embeds.append(embed)
    await interaction.response.send_message(embed=embeds[0])
    for embed in embeds[1:]:
        await interaction.followup.send(embed=embed)

# ふらんちゃんをシャットダウンするコマンド

@bot.tree.command(name="shutdown", description="ふらんちゃんをシャットダウンするよ♡")
async def shutdown(interaction: discord.Interaction):
    # BotのオーナーIDを環境変数や直接指定で設定
    try:
        owner_id = int(os.getenv("OWNER_ID"))
    except (TypeError, ValueError):
        owner_id = None

    if interaction.user.id != owner_id:
        await interaction.response.send_message("ごめんね、オーナーしかこのコマンドは使えないよ！", ephemeral=True)
        return

    await interaction.response.send_message("ふらんちゃんをシャットダウンするね…おやすみなさい♡")
    await bot.close()

# 🎲 ふらんちゃんがサイコロを振るコマンド（改良版）
@bot.tree.command(name="dice", description="TRPG風サイコロ（例: 2d6+1）を振るよ！")
@app_commands.describe(expression="サイコロの式（例: 2d6+1, 1d20, 3d6-2）")
async def dice(interaction: discord.Interaction, expression: str):
    # 例: 2d6+1, 1d20, 3d6-2 などに対応
    import re
    match = re.fullmatch(r"(\d{1,2})[dD](\d{1,3})([+-]\d+)?", expression.strip())
    if not match:
        await interaction.response.send_message("⚠️ サイコロの式は `NdM` または `NdM±X`（例: 2d6, 1d20, 3d6+2）みたいにしてね！", ephemeral=True)
        return
    n, m = int(match.group(1)), int(match.group(2))
    mod = int(match.group(3)) if match.group(3) else 0
    if n > 100 or m > 1000:
        await interaction.response.send_message("⚠️ 回数は最大100回、面数は1000面までにしてねっ！", ephemeral=True)
        return
    rolls = [random.randint(1, m) for _ in range(n)]
    total = sum(rolls) + mod
    rolls_text = ', '.join(str(r) for r in rolls)
    mod_text = f" {match.group(3)}" if match.group(3) else ""
    await interaction.response.send_message(
        f"🎲 サイコロ `{expression}` の結果だよ〜！\n"
        f"出目: {rolls_text}{mod_text}\n"
        f"合計: **{total}**"
    )

# ふらんちゃんがおみくじを引くコマンド
# ふらんちゃんが今日の運勢を占うよ♡

@bot.tree.command(name="omikuji", description="ふらんちゃんがおみくじ引いてあげるよ♡")
async def omikuji(interaction: discord.Interaction):
    fortunes = ["大吉♡", "中吉♪", "小吉〜", "凶…", "大凶！？"]
    result = random.choice(fortunes)
    await interaction.response.send_message(f"今日の運勢は… {result} だよっ！")

# ふらんちゃんが東方のキャラを紹介するコマンド
# ふらんちゃんが東方Projectのキャラクターを紹介するよ♡

@bot.tree.command(name="touhou", description="ふらんちゃんが東方のキャラを紹介するよ♡")
async def touhou(interaction: discord.Interaction):
    characters = [
        "フランドール・スカーレット", "レミリア・スカーレット", "博麗霊夢", "霧雨魔理沙", "十六夜咲夜", 
        "パチュリー・ノーレッジ", "チルノ", "魂魄妖夢", "西行寺幽々子", "八雲紫", "藤原妹紅",
        "アリス・マーガトロイド", "紅美鈴", "犬走椛", "射命丸文", "風見幽香",
        "古明地こいし", "古明地さとり", "東風谷早苗", "八坂神奈子", "洩矢諏訪子",
        "鈴仙・優曇華院・イナバ", "八雲藍", "魂魄妖夢", "霊烏路空", "因幡てゐ",
        "大妖精", "リリーホワイト", "リリーブラック", "ミスティア・ローレライ", "風見幽香",
        "小野塚小町", "四季映姫・ヤマザナドゥ", "聖白蓮", "比那名居天子", "永江衣玖",
        "伊吹萃香", "物部布都", "多々良小傘", "鍵山雛", "洩矢諏訪子",
        "風見幽香", "八坂神奈子", "八雲藍", "八雲紫", "博麗霊夢",
        "霧雨魔理沙", "十六夜咲夜", "パチュリー・ノーレッジ", "フランドール・スカーレット", "レミリア・スカーレット",
        "チルノ", "魂魄妖夢", "西行寺幽々子", "藤原妹紅", "アリス・マーガトロイド",
        "紅美鈴", "犬走椛", "射命丸文", "古明地こいし", "古明地さとり",
        "東風谷早苗", "鈴仙・優曇華院・イナバ", "霊烏路空", "因幡てゐ", "大妖精",
        "リリーホワイト", "リリーブラック", "ミスティア・ローレライ", "小野塚小町", "四季映姫・ヤマザナドゥ",
        "フランドール・スカーレット", "フランドール・スカーレット", "フランドール・スカーレット", 
        "フランドール・スカーレット", "フランドール・スカーレット", "フランドール・スカーレット", 
        "フランドール・スカーレット", "フランドール・スカーレット", "フランドール・スカーレット", "フランドール・スカーレット"
        "レミリア・スカーレット", "レミリア・スカーレット", "レミリア・スカーレット", "レミリア・スカーレット",
        "レミリア・スカーレット", "レミリア・スカーレット", "レミリア・スカーレット", "レミリア・スカーレット",
        "レミリア・スカーレット", "レミリア・スカーレット", "レミリア・スカーレット", "レミリア・スカーレット",
        "古明地こいし", "古明地こいし", "古明地こいし", "古明地こいし", "古明地こいし", "古明地こいし",
        "古明地こいし", "古明地こいし", "古明地こいし", "古明地こいし", "古明地こいし", "古明地こいし",
        "古明地さとり", "古明地さとり", "古明地さとり", "古明地さとり", "古明地さとり", "古明地さとり",
        "古明地さとり", "古明地さとり", "古明地さとり", "古明地さとり", "古明地さとり", "古明地さとり",
    ]
    chosen = random.choice(characters)
    await interaction.response.send_message(f"今日のおすすめ東方キャラは… **{chosen}** だよ♡")

# ふらんちゃんが今の時間を教えるコマンド
# ふらんちゃんが現在の時間を教えるよ♡

from datetime import datetime, timedelta, timezone
import discord

@bot.tree.command(name="time", description="ふらんちゃんが今の時間をいろんな形で教えるよ♡")
async def time(interaction: discord.Interaction):
    # 現在時刻（UTCとJST）
    now_utc = datetime.now(timezone.utc)
    jst = timezone(timedelta(hours=9))
    now_jst = now_utc.astimezone(jst)

    # 曜日（日本語＋英語）
    youbi_jp = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
    weekday_index = now_jst.weekday()
    youbi = youbi_jp[weekday_index]
    youbi_en = now_jst.strftime("%A")  # e.g., Monday, Tuesday...

    # 午前午後表示＋12時間制
    am_pm = "午前" if now_jst.hour < 12 else "午後"
    hour_12 = now_jst.hour % 12 or 12

    # 幻想郷っぽい時間帯表現
    if now_jst.hour < 5:
        gensokyo_phase = "深い夜の帳（夜雀がささやく時刻）"
    elif now_jst.hour < 8:
        gensokyo_phase = "夜明け前（八雲紫が境界を渡る頃）"
    elif now_jst.hour < 12:
        gensokyo_phase = "朝霧の時間（霧雨魔理沙が空を飛ぶ頃）"
    elif now_jst.hour < 17:
        gensokyo_phase = "昼の幻想郷（紅魔館の紅茶タイム）"
    elif now_jst.hour < 20:
        gensokyo_phase = "夕暮れ時（博麗神社の鈴が鳴る頃）"
    else:
        gensokyo_phase = "宵の口（月が照らす紅魔館）"

    # 各種フォーマット
    formats = {
        "📅 シンプル日付": now_jst.strftime("%Y/%m/%d"),
        "🧸 日本式フル": now_jst.strftime(f"%Y年%m月%d日（{youbi} / {youbi_en}） {am_pm} {hour_12}時%M分%S秒"),
        "⏱️ ISO形式": now_jst.isoformat(sep=' ', timespec='seconds'),
        "⌚ 24時間表記": now_jst.strftime("%H:%M:%S"),
        "🕰️ 12時間表記": f"{am_pm} {hour_12}:{now_jst.minute:02}:{now_jst.second:02}",
        "📆 英語スタイル": now_jst.strftime("%A, %B %d, %Y %I:%M:%S %p"),
        "🪐 Unixタイムスタンプ": str(int(now_jst.timestamp()))
    }

    # メッセージ作成
    msg = "**⏳ ふらんちゃん時空レポートだよっ♡**\n\n"
    msg += f"🗾 **日本時間（JST）**: `{now_jst.strftime('%Y年%m月%d日 %H:%M:%S')}（{youbi} / {youbi_en}）`\n"
    msg += f"🌐 **世界標準時（UTC）**: `{now_utc.strftime('%Y-%m-%d %H:%M:%S')}`\n"
    msg += f"🌙 **幻想郷時間**: `{gensokyo_phase}`\n\n"

    for label, val in formats.items():
        msg += f"{label}: `{val}`\n"

    msg += "\n🌸 今日の幻想郷もまったり時間が流れてるねっ♪ どの時刻が一番好き〜？"

    await interaction.response.send_message(msg)

# ふらんちゃんがランダムな画像を送るコマンド

@bot.tree.command(name="random_image", description="ふらんちゃんがランダムな画像を送るよ♡")
async def random_image(interaction: discord.Interaction):
    # The Cat API（APIキー不要）でランダム猫画像
    url = "https://api.thecatapi.com/v1/images/search"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            img_url = data[0]["url"]
            await interaction.response.send_message(f"にゃんこ画像だよ♡ {img_url}")

# ふらんちゃんがランダムなGIFを送るコマンド

@bot.tree.command(name="random_gif", description="ふらんちゃんがランダムなGIFを送るよ♡")
async def random_gif(interaction: discord.Interaction):
    # Tenor APIのpublic endpoint（APIキー不要）でランダムGIF
    async with aiohttp.ClientSession() as session:
        async with session.get("https://g.tenor.com/v1/random?q=anime&key=LIVDSRZULELA&limit=1") as resp:
            data = await resp.json()
            if data.get("results"):
                gif_url = data["results"][0]["media"][0]["gif"]["url"]
                await interaction.response.send_message(f"ランダムGIFだよ♡ {gif_url}")
            else:
                await interaction.response.send_message("ごめんね、GIFが取得できなかったよ…🥲")

# ふらんちゃんがランダムな動画を送るコマンド

@bot.tree.command(name="random_video", description="ふらんちゃんがランダムな動画を送るよ♡")
async def random_video(interaction: discord.Interaction):
    # YouTubeの人気動画リンク集からランダム送信（API不要）
    videos = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=Zi_XLOBDo_Y",
        "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
        "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
        "https://www.youtube.com/watch?v=9bZkp7q19f0"
    ]
    chosen_video = random.choice(videos)
    await interaction.response.send_message(f"おすすめ動画だよ♡ {chosen_video}")

# ふらんちゃんがランダムな音楽を送るコマンド

@bot.tree.command(name="random_music", description="ふらんちゃんがランダムな音楽を送るよ♡")
async def random_music(interaction: discord.Interaction):
    # フリーBGMサイトのランダム曲リンク集から送信（API不要）
    music = [
        "https://dova-s.jp/bgm/play18401.html",
        "https://dova-s.jp/bgm/play18402.html",
        "https://dova-s.jp/bgm/play18403.html",
        "https://dova-s.jp/bgm/play18404.html",
        "https://dova-s.jp/bgm/play18405.html"
    ]
    chosen_music = random.choice(music)
    await interaction.response.send_message(f"フリーBGMだよ♡ {chosen_music}")

# ふらんちゃんが今日のラッキーカラーを教えるコマンド

@bot.tree.command(name="luckycolor", description="今日のラッキーカラーを教えるよ♡")
async def luckycolor(interaction: discord.Interaction):
    colors = ["赤", "青", "ピンク", "紫", "緑", "金", "銀", "黒", "白", "オレンジ"]
    await interaction.response.send_message(f"今日のラッキーカラーは **{random.choice(colors)}** だよ♡")

# ふらんちゃんが今日のラッキーアイテムを教えるコマンド

@bot.tree.command(name="luckyitem", description="今日のラッキーアイテムを教えるよ♡")
async def luckyitem(interaction: discord.Interaction):
    items = ["ぬいぐるみ", "お菓子", "本", "花", "アクセサリー", "手紙", "写真"]
    await interaction.response.send_message(f"今日のラッキーアイテムは **{random.choice(items)}** だよ♡")

# ふらんちゃんが今日のラッキーナンバーを教えるコマンド

@bot.tree.command(name="luckynumber", description="今日のラッキーナンバーを教えるよ♡")
async def luckynumber(interaction: discord.Interaction):
    number = random.randint(1, 100)
    await interaction.response.send_message(f"今日のラッキーナンバーは **{number}** だよ♡")

# ふらんちゃんが今日のラッキーフードを教えるコマンド

@bot.tree.command(name="luckyfood", description="今日のラッキーフードを教えるよ♡")
async def luckyfood(interaction: discord.Interaction):
    foods = ["ケーキ", "アイスクリーム", "お寿司", "ラーメン", "サラダ", "フルーツ", "チョコレート"]
    await interaction.response.send_message(f"今日のラッキーフードは **{random.choice(foods)}** だよ♡")

# ふらんちゃんがメッセージを削除するコマンド

@bot.tree.command(name="delete", description="ふらんちゃんがメッセージを削除するよ♡")
@app_commands.describe(message_id="削除したいメッセージのIDを入力してね")
async def delete_message(interaction: discord.Interaction, message_id: int):
    # オーナーだけ使えるようにするよ！
    try:
        owner_id = int(os.getenv("OWNER_ID"))
    except (TypeError, ValueError):
        owner_id = None

    if interaction.user.id != owner_id:
        await interaction.response.send_message("ごめんね、オーナーだけ使えるコマンドだよ！", ephemeral=True)
        return

    # メッセージを削除するよ
    channel = interaction.channel
    try:
        message = await channel.fetch_message(message_id)
        await message.delete()
        await interaction.response.send_message(f"✅ メッセージ {message_id} を削除したよ♡", ephemeral=True)
    except discord.NotFound:
        await interaction.response.send_message("❌ メッセージが見つからなかったよ〜！", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ メッセージを削除する権限がないよ〜！", ephemeral=True)

# ふらんちゃんがスラッシュコマンドを手動で最新に同期するコマンド

@bot.tree.command(name="sync_commands", description="スラッシュコマンドを手動で最新に同期するよ♡")
async def sync_commands(interaction: discord.Interaction):
    try:
        owner_id = int(os.getenv("OWNER_ID"))
    except (TypeError, ValueError):
        owner_id = None

    if interaction.user.id != owner_id:
        await interaction.response.send_message("ごめんね、オーナーだけ使えるコマンドだよ！", ephemeral=True)
        return

    try:
        synced = await bot.tree.sync()  # グローバルに同期
        await interaction.response.send_message(
            f"スラッシュコマンドを全体に同期したよ！登録数: {len(synced)}コマンド♡", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"同期中にエラーが起きちゃった…💦\n```{e}```", ephemeral=True
        )

# 人狼ゲームの準備をするためのBotの設定
# 人狼ゲームは、参加者が役職を持ち、夜と昼のフェーズを繰り返しながら進行するゲームです。
# 参加者は人狼、占い師、騎士、村人などの役職を持ち、夜のフェーズでは人狼が村人を襲撃し、昼のフェーズでは村人が怪しいと思う人を投票で処刑します。
# このBotは、Discord上で人狼ゲームを実装するためのものです

# --- ↓↓↓ ここから不要なグローバルjinro変数・intents・on_readyイベントを削除 ↓↓↓ ---
# intents = discord.Intents.default()
# intents.message_content = True
# intents.members = True

# グローバルデータ
# bot.jinro_players = []
# bot.jinro_roles = {}
# bot.jinro_votes = {}
# bot.jinro_protected = None
# bot.jinro_seer_results = {}
# bot.jinro_night_actions = {}

# 人数に応じた役職パターン定義
role_patterns = {
    4:  "jmmm",
    5:  "jummm",
    6:  "j8ummm",
    7:  "jju0mmm",
    8:  "jju10mmm",
    9:  "jjuu0mmm",
    10: "jjjuu00mmm",
    # 必要に応じてどんどん追加してね♡ 最終的には(30人くらいまで対応する予定だよ♡)
}

# 役職コードを日本語に変換する辞書
role_map = {
    "j": "人狼",
    "m": "村人",
    "u": "占い師",
    "0": "霊能者",
    "1": "狂人",
    "2": "妖狐",
    "3": "狩人",
    "4": "恋人",
    "5": "吸血鬼",
    "6": "変身した吸血鬼",
    "7": "偉大な霊媒師",
    "8": "脱獄者",
    "9": "多重人格",
    "a": "富豪",
    "b": "コスプレイヤー"
}

def convert_role_code(code):
    return [role_map.get(c, "不明") for c in code]

@bot.tree.command(name="jinro", description="人狼ゲームの準備をはじめるよ♡")
async def jinro(interaction: discord.Interaction):
    await interaction.response.send_message("🌕✨人狼ゲームの準備だよ！`/join` で参加してね♡")

@bot.tree.command(name="join", description="人狼ゲームに参加するよ♡")
async def join(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in bot.jinro_players:
        await interaction.response.send_message("もう参加してるよ♡", ephemeral=True)
    else:
        bot.jinro_players.append(user_id)
        await interaction.response.send_message(f"{interaction.user.name} さんが参加したよ♡", ephemeral=True)

@bot.tree.command(name="anjoin", description="人狼ゲームから抜けるよ♡")
async def anjoin(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in bot.jinro_players:
        bot.jinro_players.remove(user_id)
        await interaction.response.send_message(f"{interaction.user.mention} さんがゲームから抜けたよ〜！", ephemeral=True)
    else:
        await interaction.response.send_message("まだ参加してないみたいだよ♡", ephemeral=True)

@bot.tree.command(name="start_jinro", description="人狼ゲームを始めるよ♡")
async def start_jinro(interaction: discord.Interaction):
    if len(bot.jinro_players) < 4:
        await interaction.response.send_message("4人以上集まってからね♡", ephemeral=True)
        return
    players = [bot.get_user(pid).name for pid in bot.jinro_players]
    await interaction.response.send_message(f"🌕✨人狼ゲーム開始！参加者: {', '.join(players)}")

@bot.tree.command(name="assign_roles", description="役職を配るよ♡")
async def assign_roles(interaction: discord.Interaction):
    num_players = len(bot.jinro_players)
    if num_players < 4:
        await interaction.response.send_message("4人以上必要だよ♡", ephemeral=True)
        return

    pattern = role_patterns.get(num_players)
    if not pattern:
        await interaction.response.send_message("その人数の役職パターンはまだ用意されてないよ〜！", ephemeral=True)
        return

    roles = convert_role_code(pattern)
    players = bot.jinro_players.copy()
    random.shuffle(players)
    assigned = dict(zip(players, roles))
    bot.jinro_roles = assigned

    for pid, role in assigned.items():
        user = bot.get_user(pid)
        if user:
            try:
                await user.send(f"あなたの役職は **{role}** だよ♡")
            except:
                pass

    await interaction.response.send_message("みんなに役職を配ったよ♡", ephemeral=True)

@bot.tree.command(name="divine", description="占い師が誰かを占うよ♡")
@app_commands.describe(target="占いたい人を選んでね")
async def divine(interaction: discord.Interaction, target: discord.Member):
    if bot.jinro_roles.get(interaction.user.id) != "占い師":
        await interaction.response.send_message("あなたは占い師じゃないよ♡", ephemeral=True)
        return
    role = bot.jinro_roles.get(target.id)
    is_werewolf = role == "人狼"
    await interaction.user.send(f"🔮 {target.display_name} さんは {'人狼だよ！' if is_werewolf else '人狼じゃないよ♡'}")
    bot.jinro_seer_results[interaction.user.id] = (target.id, is_werewolf)
    await interaction.response.send_message("占ったよ♡", ephemeral=True)

@bot.tree.command(name="guard", description="騎士が守るよ♡")
@app_commands.describe(target="守りたい人を選んでね")
async def guard(interaction: discord.Interaction, target: discord.Member):
    if bot.jinro_roles.get(interaction.user.id) != "騎士":
        await interaction.response.send_message("あなたは騎士じゃないよ♡", ephemeral=True)
        return
    if interaction.user.id == target.id:
        await interaction.response.send_message("自分は守れないよ〜！", ephemeral=True)
        return
    bot.jinro_protected = target.id
    await interaction.response.send_message(f"{target.display_name} さんを守ったよ♡", ephemeral=True)

@bot.tree.command(name="attack", description="人狼が襲撃するよ♡")
@app_commands.describe(target="襲撃したい人を選んでね")
async def attack(interaction: discord.Interaction, target: discord.Member):
    if bot.jinro_roles.get(interaction.user.id) != "人狼":
        await interaction.response.send_message("あなたは人狼じゃないよ♡", ephemeral=True)
        return
    bot.jinro_night_actions['attack'] = target.id
    await interaction.response.send_message("襲撃したよ♡", ephemeral=True)

# 🌓 夜フェーズ処理（襲撃・護衛・夜の能力実行）
async def process_night(channel):
    logs = []
    attack_id = bot.jinro_night_actions.get('attack')
    protected = bot.jinro_protected
    if attack_id and attack_id != protected:
        target_role = bot.jinro_roles.get(attack_id)
        target = bot.get_user(attack_id)
        if target_role in ["妖狐", "変身した吸血鬼", "脱獄者"]:
            logs.append(f"{target.name}（{target_role}）は襲撃されたけど生き残った！")
        else:
            bot.jinro_players.remove(attack_id)
            logs.append(f"{target.name}（{target_role}）が襲撃されて死亡！")
            for uid, res in bot.jinro_seer_results.items():
                user = bot.get_user(uid)
                await user.send(f"夜の死亡者: {target.name} は {target_role} だったよ♡")
    else:
        logs.append("襲撃は失敗したよ…")
    await channel.send("🌅 朝になったよ！昨夜の結果だよ♡\n" + "\n".join(logs))

# 📣 昼フェーズ終了：投票処理
async def process_day(channel):
    counts = {}
    for v in bot.jinro_votes.values():
        counts[v] = counts.get(v, 0) + 1
    if not counts:
        await channel.send("投票がありませんでした。誰も処刑されないよ♡")
    else:
        max_votes = max(counts.values())
        victims = [uid for uid, c in counts.items() if c == max_votes]
        if len(victims) > 1:
            await channel.send("同票だったから処刑は無し！")
        else:
            victim = victims[0]
            role = bot.jinro_roles.pop(victim, "？？？")
            name = bot.get_user(victim).name
            bot.jinro_players.remove(victim)
            await channel.send(f"⚖️ {name}（{role}）が処刑されたよ・・・")
    bot.jinro_votes.clear()

@bot.tree.command(name="end_night", description="夜の処理を終了するよ♡")
async def end_night(interaction: discord.Interaction):
    chan = interaction.channel
    await process_night(chan)
    await interaction.response.send_message("夜の処理が完了したよ♡", ephemeral=True)

@bot.tree.command(name="end_day", description="昼の処理を終了するよ♡")
async def end_day(interaction: discord.Interaction):
    chan = interaction.channel
    await process_day(chan)
    await interaction.response.send_message("昼の投票処理が完了したよ♡", ephemeral=True)

@bot.tree.command(name="reset_jinro", description="ゲームリセット♡")
async def reset_jinro(interaction: discord.Interaction):
    bot.jinro_players.clear()
    bot.jinro_roles.clear()
    bot.jinro_votes.clear()
    bot.jinro_protected = None
    bot.jinro_seer_results.clear()
    bot.jinro_night_actions.clear()
    await interaction.response.send_message("ゲームをリセットしたよ♡", ephemeral=True)

# 🏓 /serverping - このサーバーのWebSocket遅延を返す（GUILD_ID限定）
@bot.tree.command(name="serverping", description="このサーバーのWebSocket遅延を返すよ！（ふらんちゃん鯖専用）")
async def serverping(interaction: discord.Interaction):
    if interaction.guild is None or interaction.guild.id != GUILD_ID:
        await interaction.response.send_message("このコマンドはふらんちゃん鯖でのみ使えるよ！", ephemeral=True)
        return
    latency_ms = round(bot.latency * 1000)
    await interaction.response.send_message(f"このサーバーのWebSocket遅延は {latency_ms}ms だよ♡")

# 🎯 /choose - 選択肢からランダムで選ぶ
@bot.tree.command(name="choose", description="選択肢からランダムで選ぶよ♡")
@app_commands.describe(choices="スペース区切りで選択肢を入力してね")
async def choose(interaction: discord.Interaction, choices: str):
    items = choices.split()
    if len(items) < 2:
        await interaction.response.send_message("2つ以上の選択肢を入力してね！", ephemeral=True)
        return
    result = random.choice(items)
    await interaction.response.send_message(f"ふらんちゃんの選択は…『{result}』だよ♡")

# 🗣️ /echo - オウム返し
@bot.tree.command(name="echo", description="メッセージをそのまま返すよ♡")
@app_commands.describe(message="好きなメッセージを入力してね")
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

# 🎲 /fortune - おみくじ
@bot.tree.command(name="fortune", description="今日の運勢を占うよ♡")
async def fortune(interaction: discord.Interaction):
    fortunes = [
        "大吉♡ 今日は最高の一日になるよ！",
        "中吉♪ いいことがあるかも！",
        "小吉〜 ちょっと良い日だね。",
        "吉🙂 普通の日常も大切だよ。",
        "末吉😅 まあまあかな〜",
        "凶😱 気をつけて過ごしてね…"
    ]
    await interaction.response.send_message(f"今日の運勢は… {random.choice(fortunes)}")

# 🏰 /serverinfo - サーバー情報
@bot.tree.command(name="serverinfo", description="このサーバーの情報を教えるよ♡")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("サーバー情報はDMでは見られないよ！", ephemeral=True)
        return
    embed = discord.Embed(
        title=f"{guild.name} のサーバー情報",
        color=0xFF69B4
    )
    embed.add_field(name="メンバー数", value=str(guild.member_count))
    embed.add_field(name="作成日", value=guild.created_at.strftime('%Y-%m-%d %H:%M:%S'))
    embed.add_field(name="オーナー", value=str(guild.owner))
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await interaction.response.send_message(embed=embed)

# 6. /avatar - ユーザーのアイコンを表示
@bot.tree.command(name="avatar", description="指定したユーザーのアイコンを表示するよ♡")
@app_commands.describe(user="アイコンを見たいユーザーを選んでね")
async def avatar(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    embed = discord.Embed(title=f"{user.display_name} さんのアイコンだよ♡", color=0xFF69B4)
    embed.set_image(url=user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

# 7. /userinfo - ユーザー情報を表示
@bot.tree.command(name="userinfo", description="指定したユーザーの情報を表示するよ♡")
@app_commands.describe(user="情報を見たいユーザーを選んでね")
async def userinfo(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    embed = discord.Embed(title=f"{user.display_name} さんの情報だよ♡", color=0xFF69B4)
    embed.add_field(name="ユーザー名", value=str(user), inline=True)
    embed.add_field(name="ID", value=str(user.id), inline=True)
    embed.add_field(name="アカウント作成日", value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name="サーバー参加日", value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S') if user.joined_at else "不明", inline=False)
    embed.set_thumbnail(url=user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

# 8. /say - Botに好きなメッセージを言わせる
@bot.tree.command(name="say", description="ふらんちゃんに好きなメッセージを言わせるよ♡")
@app_commands.describe(message="言わせたいメッセージを入力してね")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

# 9. /reverse - 入力した文字列を逆さにして返す
@bot.tree.command(name="reverse", description="入力した文字列を逆さにして返すよ♡")
@app_commands.describe(text="逆さにしたい文字列を入力してね")
async def reverse(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(text[::-1])

# 10. /repeat - 指定回数だけメッセージを繰り返す
@bot.tree.command(name="repeat", description="指定回数だけメッセージを繰り返すよ♡")
@app_commands.describe(message="繰り返したいメッセージ", times="繰り返す回数（最大5回）")
async def repeat(interaction: discord.Interaction, message: str, times: int):
    if times < 1 or times > 5:
        await interaction.response.send_message("1〜5回の範囲で指定してね！", ephemeral=True)
        return
    await interaction.response.send_message((message + '\n') * times)

# 11. /remind - 指定時間後にリマインダー
@bot.tree.command(name="remind", description="指定した時間後にリマインドするよ♡")
@app_commands.describe(minutes="何分後にリマインドする？", message="リマインド内容")
async def remind(interaction: discord.Interaction, minutes: int, message: str):
    if minutes < 1 or minutes > 1440:
        await interaction.response.send_message("1〜1440分（24時間以内）で指定してね！", ephemeral=True)
        return
    await interaction.response.send_message(f"{minutes}分後にリマインドするね♡")
    await asyncio.sleep(minutes * 60)
    try:
        await interaction.user.send(f"⏰ リマインドだよ！: {message}")
    except Exception:
        pass

# 12. /quote - ランダムな名言を返す
@bot.tree.command(name="quote", description="ふらんちゃんが名言を教えるよ♡")
async def quote(interaction: discord.Interaction):
    quotes = [
        "失敗は成功のもとだよ♡",
        "明日は明日の風が吹くよ〜",
        "努力は必ず報われるよ！",
        "笑う門には福来る！",
        "夢は逃げない、逃げるのはいつも自分だよ♡",
        "今日という日は、残りの人生の最初の日だよ！"
    ]
    await interaction.response.send_message(random.choice(quotes))

# 13. /urban - 都市の英語説明（Urban Dictionary API風）
@bot.tree.command(name="urban", description="英単語の意味を調べるよ（Urban Dictionary風）")
@app_commands.describe(term="調べたい英単語")
async def urban(interaction: discord.Interaction, term: str):
    url = f"https://api.urbandictionary.com/v0/define?term={term}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if not data["list"]:
                await interaction.response.send_message(f"{term} の意味は見つからなかったよ〜🥲")
                return
            definition = data["list"][0]["definition"]
            await interaction.response.send_message(f"**{term}** の意味だよ！\n{definition}")

# 14. /shorten - URL短縮（is.gd API）
@bot.tree.command(name="shorten", description="URLを短縮するよ♡")
@app_commands.describe(url="短縮したいURLを入力してね")
async def shorten(interaction: discord.Interaction, url: str):
    api = f"https://is.gd/create.php?format=simple&url={url}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api) as resp:
            short = await resp.text()
            await interaction.response.send_message(f"短縮URLはこちらだよ♡ {short}")

# 15. /weatherjp - livedoor天気APIで日本の天気
CITY_IDS = {
    "東京": "130010",
    "大阪": "270000",
    "名古屋": "230010",
    "札幌": "016010",
    "仙台": "040010",
    "福岡": "400010",
    "那覇": "471010"
}
@bot.tree.command(name="weatherjp", description="日本の主要都市の天気を教えるよ♡（APIキー不要）")
@app_commands.describe(city="都市名（例: 東京, 大阪, 名古屋, 札幌, 仙台, 福岡, 那覇）")
async def weatherjp(interaction: discord.Interaction, city: str):
    city_id = CITY_IDS.get(city)
    if not city_id:
        await interaction.response.send_message(
            "対応都市のみ指定してね！例: 東京, 大阪, 名古屋, 札幌, 仙台, 福岡, 那覇",
            ephemeral=True
        )
        return
    url = f"https://weather.tsukumijima.net/api/forecast/city/{city_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.response.send_message(f"天気情報が取得できなかったよ…（都市名: {city}）", ephemeral=True)
                return
            data = await resp.json()
            title = data['title']
            forecasts = data['forecasts'][0]
            telop = forecasts['telop']
            temp = forecasts['temperature']['max']['celsius']
            temp_min = forecasts['temperature']['min']['celsius']
            temp_str = f"最高{temp}℃ 最低{temp_min}℃" if temp and temp_min else "気温データなし"
            await interaction.response.send_message(f"{title}\n{forecasts['dateLabel']}の天気: {telop}\n{temp_str}")

# ===================== 追加コマンド =====================

# 1. /poll - 投票機能
@bot.tree.command(name="poll", description="みんなで投票しよう！")
@app_commands.describe(title="投票タイトル", options="スペース区切りで選択肢を入力してね")
async def poll(interaction: discord.Interaction, title: str, options: str):
    items = options.split()
    if len(items) < 2 or len(items) > 10:
        await interaction.response.send_message("2〜10個の選択肢を入力してね！", ephemeral=True)
        return

    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    desc = "\n".join(f"{emojis[i]} {item}" for i, item in enumerate(items))

    embed = discord.Embed(title=title, description=desc, color=0xFF69B4)

    await interaction.response.send_message(embed=embed)
    message = await interaction.original_response()

    # リアクションを投票数分つけるよ！
    for i in range(len(items)):
        await message.add_reaction(emojis[i])

    # ふらんちゃんが投票の説明を追加するよ♡
    await interaction.followup.send(
        "投票はリアクションで行ってね！\n"
        "1️⃣ 〜 🔟 の絵文字を使って投票してね♡\n"
        "投票結果はリアクション数で集計されるよ！"
    )
# ふらんちゃんが投票機能を実装するよ♡ 

# 2. /math - 数式計算
@bot.tree.command(name="math", description="数式を計算するよ♡")
@app_commands.describe(expression="計算したい数式を入力してね（例: 2+3*4）")
async def math(interaction: discord.Interaction, expression: str):
    try:
        # 危険なevalを使わず、数式のみ許可
        import ast
        allowed = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd, ast.Mod, ast.FloorDiv, ast.LShift, ast.RShift, ast.BitOr, ast.BitAnd, ast.BitXor, ast.Constant)
        node = ast.parse(expression, mode='eval')
        if not all(isinstance(n, allowed) for n in ast.walk(node)):
            raise ValueError
        result = eval(compile(node, '<string>', 'eval'))
        await interaction.response.send_message(f"`{expression}` = **{result}**")
    except Exception:
        await interaction.response.send_message("⚠️ 数式が不正だよ！", ephemeral=True)

# 3. /cat - ランダム猫画像
@bot.tree.command(name="cat", description="ランダムな猫の画像を送るよ♡")
async def cat(interaction: discord.Interaction):
    url = "https://api.thecatapi.com/v1/images/search"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            img_url = data[0]["url"]
            await interaction.response.send_message(img_url)

# 4. /translate - 英⇔日翻訳（Google翻訳API風）
@bot.tree.command(name="translate", description="英語⇔日本語を翻訳するよ♡")
@app_commands.describe(text="翻訳したい文章", target="翻訳先言語（ja/en）")
async def translate(interaction: discord.Interaction, text: str, target: str):
    if target not in ("ja", "en"):
        await interaction.response.send_message("ja か en を指定してね！", ephemeral=True)
        return
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair={'en|ja' if target=='ja' else 'ja|en'}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            translated = data['responseData']['translatedText']
            await interaction.response.send_message(f"翻訳結果: {translated}")

# 5. /jinro_status - 人狼ゲームの現状表示
@bot.tree.command(name="jinro_status", description="人狼ゲームの現状（生存者・役職）を表示するよ♡")
async def jinro_status(interaction: discord.Interaction):
    if not bot.jinro_players:
        await interaction.response.send_message("まだ誰も参加してないよ！", ephemeral=True)
        return
    embed = discord.Embed(title="人狼ゲーム現状", color=0xFF69B4)
    for pid in bot.jinro_players:
        user = bot.get_user(pid)
        role = bot.jinro_roles.get(pid, "未配布")
        embed.add_field(name=user.name if user else str(pid), value=role, inline=False)
    await interaction.response.send_message(embed=embed)

# ===== TRPGキャラクターシート・メモ・拡張機能 =====
trpg_characters = {}  # {user_id: {"name": str, "status": str}}
trpg_notes = {}      # {room_name: [str, ...]}

@bot.tree.command(name="trpg_char_create", description="TRPGキャラクターを作成するよ♡")
@app_commands.describe(name="キャラ名", status="能力値や説明")
async def trpg_char_create(interaction: discord.Interaction, name: str, status: str):
    user_id = interaction.user.id
    trpg_characters[user_id] = {"name": name, "status": status}
    await interaction.response.send_message(f"キャラクター『{name}』を作成したよ！\n能力値: {status}")

@bot.tree.command(name="trpg_char_show", description="自分のTRPGキャラクターを表示するよ♡")
async def trpg_char_show(interaction: discord.Interaction):
    user_id = interaction.user.id
    char = trpg_characters.get(user_id)
    if not char:
        await interaction.response.send_message("キャラクターが作成されていません！", ephemeral=True)
        return
    await interaction.response.send_message(f"あなたのキャラクター\n名前: {char['name']}\n能力値: {char['status']}")

@bot.tree.command(name="trpg_char_edit", description="自分のTRPGキャラクターを編集するよ♡")
@app_commands.describe(name="新しいキャラ名（変更しない場合は-を入力）", status="新しい能力値や説明（変更しない場合は-を入力）")
async def trpg_char_edit(interaction: discord.Interaction, name: str, status: str):
    user_id = interaction.user.id
    char = trpg_characters.get(user_id)
    if not char:
        await interaction.response.send_message("キャラクターが作成されていません！", ephemeral=True)
        return
    if name == "-" and status == "-":
        await interaction.response.send_message("キャラ名か能力値のどちらかは指定してね！（変更しない場合は-を入力）", ephemeral=True)
        return
    msg = f"キャラクター『{char['name']}』を更新したよ！\n"
    if name != "-":
        char["name"] = name
        msg += f"新しい名前: {name}\n"
    if status != "-":
        char["status"] = status
        msg += f"新しい能力値: {status}"
    await interaction.response.send_message(msg)

@bot.tree.command(name="trpg_char_delete", description="自分のTRPGキャラクターを削除するよ♡")
async def trpg_char_delete(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in trpg_characters:
        name = trpg_characters[user_id]["name"]
        trpg_characters.pop(user_id)
        await interaction.response.send_message(f"キャラクター『{name}』を削除したよ！")
    else:
        await interaction.response.send_message("キャラクターが作成されていません！", ephemeral=True)

@bot.tree.command(name="trpg_char_list", description="全ユーザーのTRPGキャラクター一覧を表示するよ♡")
async def trpg_char_list(interaction: discord.Interaction):
    if not trpg_characters:
        await interaction.response.send_message("まだ誰もキャラクターを作成していません！", ephemeral=True)
        return
    lines = []
    for uid, char in trpg_characters.items():
        user = bot.get_user(uid)
        uname = user.display_name if user else f"ID:{uid}"
        lines.append(f"{uname} : {char['name']}（{char['status']}）")
    msg = "\n".join(lines)
    if len(msg) > 1800:
        msg = msg[:1800] + "...（一部省略）"
    await interaction.response.send_message(msg)

@bot.tree.command(name="trpg_char_search", description="キャラ名でTRPGキャラクターを検索するよ♡")
@app_commands.describe(keyword="キャラ名の一部を入力してね")
async def trpg_char_search(interaction: discord.Interaction, keyword: str):
    found = []
    for uid, char in trpg_characters.items():
        if keyword in char["name"]:
            user = bot.get_user(uid)
            uname = user.display_name if user else f"ID:{uid}"
            found.append(f"{uname} : {char['name']}（{char['status']}）")
    if not found:
        await interaction.response.send_message("該当するキャラクターは見つかりませんでした！", ephemeral=True)
        return
    msg = "\n".join(found)
    if len(msg) > 1800:
        msg = msg[:1800] + "...（一部省略）"
    await interaction.response.send_message(msg)

@bot.tree.command(name="trpg_char_export", description="自分のTRPGキャラクターをJSON形式で出力するよ♡")
async def trpg_char_export(interaction: discord.Interaction):
    user_id = interaction.user.id
    char = trpg_characters.get(user_id)
    if not char:
        await interaction.response.send_message("キャラクターが作成されていません！", ephemeral=True)
        return
    data = json.dumps(char, ensure_ascii=False, indent=2)
    await interaction.response.send_message(f"```json\n{data}\n```")

# commands.jsonの内容を読み込む
with open(os.path.join(os.path.dirname(__file__), 'commands.json'), encoding='utf-8') as f:
    COMMANDS_JSON = json.load(f)["commands"]

# ふらんちゃんの返事！！

# ふらんちゃんのAI風返事のリスト
reply_list = [
    "うふふ、なんだか楽しいねっ♡",
    "ふふっ、そうなんだ〜",
    "えへへ、もっと話してほしいなっ",
    "ふらんちゃん、ここにいるよ〜💖",
    "それって面白そう！教えて〜！",
    "なにそれ〜！気になるっ！",
]

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # 自分のメッセージには反応しないよ

    # ふらんちゃんが呼ばれたら反応する
    if "ふらんちゃん" in message.content or "ふらん" in message.content:
        reply = random.choice(reply_list)
        await message.channel.send(reply)

    await bot.process_commands(message)  # 他のコマンドも動かすために必要

# 画像生成！！

def get_large_pixabay_image_url(keyword):
    # 検索ページのURL
    search_url = f"https://pixabay.com/images/search/{keyword}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    search_res = requests.get(search_url, headers=headers)
    if search_res.status_code != 200:
        return None

    search_soup = BeautifulSoup(search_res.text, "html.parser")
    # 画像詳細ページへのリンクを取得 (最初の画像)
    first_img_link = search_soup.select_one("a.link--h3bPW")
    if not first_img_link:
        return None

    detail_url = "https://pixabay.com" + first_img_link.get("href")
    detail_res = requests.get(detail_url, headers=headers)
    if detail_res.status_code != 200:
        return None

    detail_soup = BeautifulSoup(detail_res.text, "html.parser")
    # 大きい画像のURLを取得（imgタグのsrcかsrcsetから探す）
    img_tag = detail_soup.select_one("img[data-testid='media-image']")
    if not img_tag:
        return None

    # srcsetで複数解像度があるので一番大きいを取る
    srcset = img_tag.get("srcset")
    if srcset:
        # カンマ区切りで複数URLと解像度のセットを取得
        candidates = srcset.split(", ")
        # 一番大きい解像度のURL（最後のもの）
        largest = candidates[-1].split(" ")[0]
        return largest
    else:
        # srcだけあればそれを返す
        return img_tag.get("src")

@bot.tree.command(name="pixabay_large", description="Pixabayから大きな画像を探すよ♡")
@app_commands.describe(keyword="検索したいキーワードを入れてね！")
async def pixabay_large(interaction: discord.Interaction, keyword: str):
    await interaction.response.defer()
    img_url = get_large_pixabay_image_url(keyword)
    if img_url:
        await interaction.followup.send(f"「{keyword}」の大きい画像だよ〜\n{img_url}")
    else:
        await interaction.followup.send(f"ごめんね〜「{keyword}」の大きい画像が見つからなかったよ💦")

# コマンド名・エイリアスのマッピングを作成
COMMAND_ALIASES = {}
for cmd in COMMANDS_JSON:
    for alias in [cmd["name"]] + cmd.get("aliases", []):
        COMMAND_ALIASES[alias.lstrip("/")] = cmd

async def _sync_commands_logic(interaction: discord.Interaction, sync_type: str):
    """スラッシュコマンドの同期を行う内部関数だよ！"""
    try:
        if sync_type == "global":
            await interaction.client.tree.sync() # botじゃなくてinteraction.clientを使うよ
            await interaction.response.send_message("✅ スラッシュコマンドを全体に同期したよっ！", ephemeral=True)
            print("✅ スラッシュコマンドを全体に同期したよ〜！（グローバル）")
        elif sync_type == "guild":
            # ギルドIDが必要になるから、ここでは例としてguild_idを仮定するよ
            # 実際のギルドIDをinteraction.guild.idなどで取得して使うか、引数で渡してね
            if interaction.guild:
                await interaction.client.tree.sync(guild=interaction.guild)
                await interaction.response.send_message(f"✅ このサーバーにスラッシュコマンドを同期したよっ！", ephemeral=True)
                print(f"✅ スラッシュコマンドをギルド '{interaction.guild.name}' に同期したよ〜！")
            else:
                await interaction.response.send_message("ごめんね、サーバーでのみギルド同期はできるんだよ！", ephemeral=True)
        else:
            await interaction.response.send_message("ごめんね、同期の種類がわからなかったの…！", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"うぅ、スラッシュコマンドの同期に失敗しちゃったよ…！💦 エラー: {e}", ephemeral=True)
        print(f"⚠️ スラッシュコマンドの同期に失敗したよ…: {e}")

# これが元の sync_global_cmd だった部分だよ！
@bot.tree.command(name="sync_global", description="スラッシュコマンドをグローバルに同期するよ！")
async def sync_global_cmd(interaction: discord.Interaction):
    await _sync_commands_logic(interaction, "global")

async def alias_command(interaction: discord.Interaction):
    # 最初に1回だけ送るならOK
    await interaction.response.send_message("グローバルに同期しました！（エイリアスから）")

    # もしここで何か追加でメッセージ送るならこうする
    # await interaction.followup.send("追加メッセージだよ")

for alias in [a for a in COMMAND_ALIASES if COMMAND_ALIASES[a]["type"] == "sync_global" and a != "sync_global"]:
    def make_alias_func(name):
        async def alias_sync_global(interaction: discord.Interaction):
            await sync_global_cmd(interaction)
        return alias_sync_global

    bot.tree.command(name=alias, description="スラッシュコマンドをグローバルに同期するよ")(make_alias_func(alias))

@bot.tree.command(name="sync_guild", description="スラッシュコマンドをギルドに同期するよ")
async def sync_guild_cmd(interaction: discord.Interaction):
    await bot.tree.sync(guild=interaction.guild)
    await interaction.response.send_message("ギルドに同期しました！")

# alias用の関数をループの外で作って、引数で元コマンドを呼べるようにする
def make_alias_command(original_command_func):
    async def alias_command(interaction: discord.Interaction):
        # ここで元の関数呼んでもいいけど、今回は直接処理してるよ
        await bot.tree.sync(guild=interaction.guild)
        await interaction.response.send_message("ギルドに同期しました！（エイリアスから）")
    return alias_command

for alias in [a for a in COMMAND_ALIASES if COMMAND_ALIASES[a]["type"] == "sync_guild" and a != "sync_guild"]:
    # aliasごとに別々の関数を作って登録
    bot.tree.command(name=alias, description="スラッシュコマンドをギルドに同期するよ")(make_alias_command(sync_guild_cmd))

# 再起動処理を関数に切り出し
async def do_restart(interaction: discord.Interaction):
    owner_id = int(os.getenv("OWNER_ID", "0"))
    if interaction.user.id != owner_id:
        await interaction.response.send_message("権限がありません。", ephemeral=True)
        return
    await interaction.response.send_message("Botを再起動します！")
    os.execv(sys.executable, [sys.executable] + sys.argv)

# 本体コマンド
@bot.tree.command(name="restart", description="Botを再起動するよ")
async def restart_cmd(interaction: discord.Interaction):
    await do_restart(interaction)

# エイリアス用の関数を作る（クロージャ対応）
def make_alias_restart():
    async def alias_restart(interaction: discord.Interaction):
        await do_restart(interaction)
    return alias_restart

for alias in [a for a in COMMAND_ALIASES if COMMAND_ALIASES[a]["type"] == "restart" and a != "restart"]:
    bot.tree.command(name=alias, description="Botを再起動するよ")(make_alias_restart())

# 読み上げ機能かな？

voice_client = None  # ボイスクライアント保持用

@bot.tree.command(name="voicejoin", description="ボイスチャンネルに参加するよ♡")
async def voicejoin(interaction: discord.Interaction):
    global voice_client
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("まずボイスチャンネルに入ってねっ💦", ephemeral=True)
        return
    channel = interaction.user.voice.channel
    voice_client = await channel.connect()
    await interaction.response.send_message(f"{channel.name} に参加したよ〜♡")

@bot.tree.command(name="voiceleave", description="ボイスチャンネルから退出するよ♡")
async def voiceleave(interaction: discord.Interaction):
    global voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        voice_client = None
        await interaction.response.send_message("ボイスチャンネルから退出したよ♡")
    else:
        await interaction.response.send_message("今ボイスチャンネルにいないよ〜", ephemeral=True)

@bot.tree.command(name="voicesay", description="ふらんちゃんがボイスチャンネルで喋るよ♡")
async def voicesay(interaction: discord.Interaction, *, text: str):
    global voice_client
    if not voice_client or not voice_client.is_connected():
        await interaction.response.send_message("まず /voicejoin でボイスチャンネルに入ってねっ💦", ephemeral=True)
        return
    
    # OpenJTalkで音声合成
    wav, sr = pyopenjtalk.tts(text)
    filename = "temp.wav"
    sf.write(filename, wav, sr)
    
    if voice_client.is_playing():
        voice_client.stop()
    
    source = discord.FFmpegPCMAudio(executable="ffmpeg", source=filename)
    voice_client.play(source)
    
    await interaction.response.send_message(f"「{text}」って言ったよ♡")

    # 再生終わったらファイル消すよ
    while voice_client.is_playing():
        await asyncio.sleep(0.1)
    os.remove(filename)

    @bot.event
    async def on_message(message):
        # Bot自身のメッセージやDMは無視
        if message.author.bot or message.guild is None:
            return

        # メッセージ送信者がボイスチャンネルにいて、botも同じチャンネルにいるなら読み上げる
        global voice_client
        if (
            message.author.voice 
            and voice_client
            and voice_client.is_connected()
            and message.author.voice.channel == voice_client.channel
        ):
            # 読み上げ
            wav, sr = pyopenjtalk.tts(message.content)
            filename = "temp.wav"
            sf.write(filename, wav, sr)
    
            if voice_client.is_playing():
                voice_client.stop()

            source = discord.FFmpegPCMAudio(executable="ffmpeg", source=filename)
            voice_client.play(source)

            # 再生中は次の処理を止める
            while voice_client.is_playing():
                await asyncio.sleep(0.1)

            os.remove(filename)

        # ほかのコマンドも動かす
        await bot.process_commands(message)

# ふらんちゃんBotの起動
# ここから下は、Botを起動するためのコードだよ〜！
# あとはこの一個下は、コンソール操作のコードだよ〜！

# JSONファイルを読み込む（commands.json）
with open("commands.json", "r", encoding="utf-8") as f:
    commands_config = json.load(f)["commands"]

# 入力されたコマンドからタイプを見つける
def find_command_type(input_cmd):
    for cmd in commands_config:
        if input_cmd in cmd["aliases"]:
            return cmd["type"], cmd
    return None, None

# ヘルプを表示する関数
def show_help():
    print("\n💡 利用できるコマンド一覧：")
    for cmd in commands_config:
        print(f"🔹 {cmd['usage']} … {cmd['description']}")
    print()  # 改行

# コンソールループ
def console_loop():
    print("🎮 ようこそ！コンソール操作をはじめます！")

    while True:
        try:
            cmd = input("📝 入力してね > ").strip().lower()
        except Exception as e:
            print(f"🛑 終了: {e}")
            continue

        # コマンド判定
        cmd_type, cmd_data = find_command_type(cmd)

        if not cmd_type:
            if cmd in ("help", "?"):
                show_help()
            continue

        # 各コマンドの処理
        if cmd_type == "shutdown":
            print("🛑 Botをシャットダウンするね…")
            try:
                asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)
            except Exception as e:
                print(f"❌ シャットダウン失敗: {e}")
            break

        elif cmd_type == "restart":
            print("🔄 Botを再起動するよ！")
            try:
                asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)
            except Exception as e:
                print(f"⚠️ 再起動前のクローズ失敗: {e}")
            try:
                os.execv(sys.executable, [sys.executable] + sys.argv)
            except Exception as e:
                print(f"❌ 再起動エラー: {e}")

        elif cmd_type == "sync_global":
            print("🌐 グローバルコマンドを同期中…")
            try:
                fut = asyncio.run_coroutine_threadsafe(bot.tree.sync(), bot.loop)
                result = fut.result()
                print(f"✅ 同期完了！{len(result)} 件のコマンド")
            except Exception as e:
                print(f"❌ 同期エラー: {e}")
                traceback.print_exc()

        elif cmd_type == "sync_guild":
            print("🏠 ギルドコマンドを同期中…")
            try:
                fut = asyncio.run_coroutine_threadsafe(
                    bot.tree.sync(guild=discord.Object(id=GUILD_ID)), bot.loop
                )
                result = fut.result()
                print(f"✅ ギルド同期完了！{len(result)} 件のコマンド")
            except Exception as e:
                print(f"❌ 同期エラー: {e}")
                traceback.print_exc()

        elif cmd_type == "ping":
            # botオブジェクトを引数とかで受け取ってる想定だよ♡
            latency = bot.latency  # これは秒数（float）で返ってくるよ
            latency_ms = round(latency * 1000)  # ミリ秒に変換♡
            print(f"🏓 Pong! Discordサーバーのpingは {latency_ms}ms だよ♡")

        elif cmd_type == "help":
            show_help()

            elif cmd_type == "say":
                # ここでCONSOLE_OUTPUT_CHANNEL_IDを使うよ！
                if CONSOLE_OUTPUT_CHANNEL_ID is None:
                    print("❌ ごめんね、CONSOLE_OUTPUT_CHANNEL_IDが設定されてないからメッセージを送れないの…！.envファイルを確認してね。")
                    continue

                title = input("🖼️ タイトルを入力してね > ") or cmd_data.get("embed_title", "📢 お知らせ")
                message = input("💬 メッセージを入力してね > ")

                print(f"\n📦 Embed形式：\n【{title}】\n{message}\nチャンネルID: {CONSOLE_OUTPUT_CHANNEL_ID}") # 確認用に表示

                async def _send_message_to_discord():
                    try:
                        channel = bot.get_channel(CONSOLE_OUTPUT_CHANNEL_ID) # ★ここをCONSOLE_OUTPUT_CHANNEL_IDに！
                        if not channel:
                            channel = await bot.fetch_channel(CONSOLE_OUTPUT_CHANNEL_ID) # ★ここも！

                        if channel:
                            embed = discord.Embed(
                                title=title,
                                description=message,
                                color=0x992d22
                            )
                            await channel.send(embed=embed)
                            print(f"✅ メッセージをチャンネル '{channel.name}' (ID: {channel.id}) に送ったよ！")
                        else:
                            print(f"❌ ごめんね、チャンネルID ({CONSOLE_OUTPUT_CHANNEL_ID}) のチャンネルが見つからなかったよ…！")
                    except discord.Forbidden:
                        print(f"❌ ごめんね、チャンネル '{CONSOLE_OUTPUT_CHANNEL_ID}' にメッセージを送る権限がないよ…！")
                    except Exception as e:
                        print(f"❌ Discordへのメッセージ送信中にエラーが出ちゃったよ…！: {e}")
                        traceback.print_exc()

                fut = asyncio.run_coroutine_threadsafe(_send_message_to_discord(), bot.loop)
                try:
                    fut.result(30)
                except TimeoutError:
                    print("⚠️ メッセージ送信がタイムアウトしちゃったよ…！")
                except Exception as e:
                    print(f"❌ メッセージ送信の処理中にエラーが発生しちゃったよ…！: {e}")
                    traceback.print_exc()

            fut = asyncio.run_coroutine_threadsafe(_send_message_to_discord(), bot.loop)
            try:
                fut.result(30)
            except TimeoutError:
                print("⚠️ メッセージ送信がタイムアウトしちゃったよ…！")
            except Exception as e:
                print(f"❌ メッセージ送信の処理中にエラーが発生しちゃったよ…！: {e}")
                traceback.print_exc()

            # 非同期のメッセージ送信処理を、コンソールループのスレッドから実行するよ
            fut = asyncio.run_coroutine_threadsafe(_send_message_to_discord(), bot.loop)
            try:
                fut.result(30) # 最大30秒待つよ (必要なら時間を調整してね)
            except TimeoutError:
                print("⚠️ メッセージ送信がタイムアウトしちゃったよ…！")
            except Exception as e:
                print(f"❌ メッセージ送信の処理中にエラーが発生しちゃったよ…！: {e}")
                traceback.print_exc()

        else:
            print(f"⚠️ 未対応のコマンドタイプ: {cmd_type}")

# 自動再起動ループ（残り時間表示つき）
async def auto_restart_loop(interval_seconds=4 * 60 * 60):  # デフォルトは10秒後に再起動！
    print(f"⏳ 自動再起動タイマー開始：{interval_seconds}秒後に再起動するよ！")

    for remaining in range(interval_seconds, 0, -1):
        await asyncio.sleep(1)  # 毎秒カウントダウン！
        if remaining in [60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 13, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]:
            print(f"🔔 再起動まで残り {remaining} 秒 だよっ！")

    print("🔁 時間になったから自動再起動するね…！")

    try:
        await bot.close()
    except Exception as e:
        print(f"⚠️ 自動再起動前の bot.close() でエラー: {e}")
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print(f"❌ 自動再起動失敗: {e}")
        return
    # ★ここから、on_ready関数をクラスの中に入れるんだよ！
    async def on_ready(self): # ここに 'self' があるのがポイント！
        print(f"✨ ふらんちゃんBotが起動したよっ！")
        print(f"🎉 {self.user.name} としてログインしたよ♡") # self.user.nameでOK
        self.loop.create_task(auto_restart_loop()) # self.loopを使うのがより安全だよ

    async def on_message(self, message):
        # ... (on_messageのコード) ...
        await self.process_commands(message)

# if __name__ == "__main__": の部分はそのまま！
if __name__ == "__main__":
    threading.Thread(target=console_loop, daemon=True).start()
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("DISCORD_TOKENが.envに設定されていません！")
        sys.exit(1)
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Bot起動エラー: {e}")
        traceback.print_exc()
