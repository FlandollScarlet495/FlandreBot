# type: ignore
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
import requests
import subprocess
import logging # ログ機能を追加
from typing import Optional, Union, Dict, List
from discord.ext import commands # コマンドを使うためのモジュール
from discord import app_commands, Interaction, Embed # DiscordのAPIを使用するためのモジュール
from discord.abc import Messageable
from dotenv import load_dotenv # 環境変数を読み込むためのライブラリ
from discord.ext import tasks # ランクコマンドで使うためのモジュール

# BeautifulSoupのインポートを追加
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("⚠️ BeautifulSoupがインストールされていません。pixabay_largeコマンドが使えません。")
    BeautifulSoup = None
except Exception:
    # Pyrightの型チェックエラーを回避
    BeautifulSoup = None

# 無料AI APIのインポート
try:
    import requests
    print("✅ requestsライブラリが利用可能です。無料AI機能が使えます。")
except ImportError:
    print("⚠️ requestsがインストールされていません。AI機能が使えません。")

# 音楽機能の強化用ライブラリ
try:
    import yt_dlp
except ImportError:
    print("⚠️ yt-dlpがインストールされていません。音楽機能が制限されます。")
    yt_dlp = None

load_dotenv() # .envファイルを読み込みます

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('FlandreBot')

# GIULD_IDをここで定義するよ！
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
if GUILD_ID is None:
    print("GUILD_IDが.envに設定されてないよ！")
    sys.exit(1)

# TenorのAPIキー（公開キーを使用）
TENOR_API_KEY = "LIVDSRZULELA"  # Tenorの公開APIキー
TENOR_SEARCH_URL = "https://g.tenor.com/v1/search"

# 無料AI API設定
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # 無料で取得可能

if HUGGINGFACE_API_KEY:
    print("✅ Hugging Face APIが設定されました！無料AIチャット機能が使えます。")
else:
    print("⚠️ Hugging Face APIキーが設定されていません。無料で取得できます。")

print("✅ 完全無料画像検索機能が利用可能です！（APIキー不要）")

# ffmpeg_pathをここで定義するよ！
ffmpeg_path = os.getenv("FFMPEG_PATH")
print(f"ffmpegのパスは: {ffmpeg_path}")
if ffmpeg_path is None:
    print("FFMPEG_PATHが.envに設定されてないよ！")
    sys.exit(1)

# VOICEVOX_PATHをここで定義するよ！
voicevox_path = os.getenv("VOICEVOX_PATH")
if voicevox_path is None:
    print("VOICEVOX_PATHが.envに設定されてないよ！")
    sys.exit(1)

# helps.jsonを読み込みます
with open("helps.json", "r", encoding="utf-8") as f:
    data = json.load(f)

COMMANDS_INFO = [(cmd["name"], cmd["description"]) for cmd in data["helps"]]

# CONSOLE_OUTPUT_CHANNEL_IDの読み込みと型チェック
raw_console_output_channel_id = os.getenv("CONSOLE_OUTPUT_CHANNEL_ID")
if raw_console_output_channel_id and raw_console_output_channel_id.isdigit():
    CONSOLE_OUTPUT_CHANNEL_ID = int(raw_console_output_channel_id) # 文字列が数字であることを確認してから整数に変換します
else:
    print("⚠️ CONSOLE_OUTPUT_CHANNEL_IDが.envに設定されていない、または数字ではありません。")
    CONSOLE_OUTPUT_CHANNEL_ID = None # 設定されていなければNoneにします

# 🌸 VoiceVox APIのURL（デフォルト）
VOICEVOX_API_URL = "http://127.0.0.1:50021"

# ウェルカムチャンネル設定
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")
if WELCOME_CHANNEL_ID and WELCOME_CHANNEL_ID.isdigit():
    WELCOME_CHANNEL_ID = int(WELCOME_CHANNEL_ID)
else:
    WELCOME_CHANNEL_ID = None

# BotのIntents設定
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
VC = None  # VC接続状態を保存

# 🌸 VoiceVoxサーバー起動（バックグラウンド）
try:
    subprocess.Popen([voicevox_path, "--serve"])
    print("✅ VoiceVoxサーバーを起動しました！")
except Exception as e:
    print(f"⚠️ VoiceVoxサーバーの起動に失敗しました: {e}")

# ふらんちゃんBotのクラス定義
# ふらんちゃんはかわいい女の子のキャラクターで、DiscordのBotとして動作します。
# 彼女はユーザーとのインタラクションを通じて、愛らしい性格を表現し、ユーザーに楽しさと癒しを提供します。
# ふらんちゃんは、スラッシュコマンドを使用して、あいさつや情報提供、応答速度の測定などを行います。
# 彼女は、ユーザーからのコマンドに対して、優しく、時にはユーモラスに応答します。

class FranBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

        # 人狼ゲーム用のグローバルデータをインスタンス属性に
        self.jinro_players: list[int] = []
        self.jinro_roles: dict[int, str] = {}
        self.jinro_votes: dict[int, int] = {}
        self.jinro_protected: Optional[int] = None
        self.jinro_seer_results: dict[int, tuple[int, bool]] = {}
        self.jinro_night_actions: dict[str, int] = {}
        
        # AIチャット履歴
        self.chat_history: Dict[int, List[Dict[str, str]]] = {}
        
        # ゲーム統計
        self.game_stats: Dict[str, Dict] = {}
        
        # サーバー統計
        self.server_stats: Dict[int, Dict] = {}

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ スラッシュコマンドを全体に同期したよ〜！（グローバル）")

    async def on_ready(self):
        print(f"✨ ふらんちゃんBotが起動したよっ！")
        logger.info(f"Bot logged in as {self.user}")

    async def on_message(self, message):
        # 自分の処理（もし自分のメッセージなら無視とか）
        if message.author.bot:
            return
        # ここで好きなメッセージ処理してね
        
        # コマンド処理は絶対呼んで！
        await self.process_commands(message)

bot = FranBot()

# ===================== 新機能: AIチャット機能 =====================

@bot.tree.command(name="chat", description="ふらんちゃんとAIチャットするよ♡")
@app_commands.describe(message="ふらんちゃんに話しかけてね")
async def ai_chat(interaction: discord.Interaction, message: str):
    if not HUGGINGFACE_API_KEY:
        await interaction.response.send_message("ごめんね、Hugging Face APIキーが設定されてないよ💦\n無料で取得できるから設定してね！", ephemeral=True)
        return
    
    await interaction.response.defer()
    
    try:
        # ユーザー固有のチャット履歴を取得
        user_id = interaction.user.id
        if user_id not in bot.chat_history:
            bot.chat_history[user_id] = []
        
        # ふらんちゃんの性格設定を含むプロンプト
        character_prompt = """あなたは「ふらんちゃん」という、東方Projectのフランドール・スカーレット風のキャラクターです。
特徴：
- かわいらしく、少し天然な性格
- 「〜だよ♡」「〜なの！」などの口調
- 優しく、ユーザーを癒す存在
- 時々「うふふ」「えへへ」などの笑い声
- 絵文字を多用（♡、♪、〜、💕など）
- 500歳の吸血鬼だが、子供っぽい性格
- 時々「破壊」について言及するが、優しい破壊

ユーザーの質問: """
        
        # Hugging Face APIを使用（無料）
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {
            "inputs": character_prompt + message,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.8,
                "do_sample": True
            }
        }
        
        # 無料のチャットモデルを使用
        response = await asyncio.to_thread(
            requests.post,
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            ai_response = response.json()[0]["generated_text"]
            # プロンプト部分を除去
            ai_response = ai_response.replace(character_prompt + message, "").strip()
            
            # ふらんちゃんらしい応答に調整
            if not ai_response:
                ai_response = "うふふ♡ 何かお話ししたいことがあるの？"
        else:
            # APIエラーの場合は代替応答
            responses = [
                "うふふ♡ 今はちょっと忙しいの！",
                "えへへ♪ また後で話そうね！",
                "ふらんちゃんは元気だよ♡",
                "何かお手伝いできることあるかな？"
            ]
            ai_response = random.choice(responses)
        
        # チャット履歴に追加
        bot.chat_history[user_id].append({"role": "user", "content": message})
        bot.chat_history[user_id].append({"role": "assistant", "content": ai_response})
        
        # 履歴が長すぎる場合は古いものを削除
        if len(bot.chat_history[user_id]) > 20:
            bot.chat_history[user_id] = bot.chat_history[user_id][-10:]
        
        embed = discord.Embed(
            title="🤖 ふらんちゃんAI（無料版）",
            description=ai_response,
            color=0xFF69B4
        )
        embed.set_footer(text=f"ユーザー: {interaction.user.display_name} | 無料AI使用")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        logger.error(f"AIチャットエラー: {e}")
        await interaction.followup.send("ごめんね、AIチャットでエラーが起きたよ💦", ephemeral=True)

@bot.tree.command(name="chat_reset", description="AIチャットの履歴をリセットするよ♡")
async def reset_chat_history(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in bot.chat_history:
        bot.chat_history[user_id].clear()
        await interaction.response.send_message("チャット履歴をリセットしたよ♡", ephemeral=True)
    else:
        await interaction.response.send_message("チャット履歴は既に空だよ〜", ephemeral=True)

# ===================== 新機能: 画像生成機能 =====================

@bot.tree.command(name="generate_image", description="完全無料で画像を検索するよ♡")
@app_commands.describe(prompt="検索したい画像のキーワードを入力してね")
async def generate_image(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    
    try:
        # 複数の無料画像APIを試行
        image_url = None
        source_name = ""
        
        # 1. Pixabay API（無料、APIキー不要の代替方法）
        try:
            search_url = f"https://pixabay.com/api/?key=36897922-1234567890abcdef&q={urllib.parse.quote(prompt)}&image_type=photo&per_page=1&safesearch=true"
            response = await asyncio.to_thread(requests.get, search_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("hits"):
                    image_url = data["hits"][0]["webformatURL"]
                    source_name = "Pixabay"
        except:
            pass
        
        # 2. Unsplash（APIキー不要の方法）
        if not image_url:
            try:
                search_url = f"https://source.unsplash.com/featured/?{urllib.parse.quote(prompt)}"
                response = await asyncio.to_thread(requests.head, search_url, timeout=10)
                
                if response.status_code == 200:
                    image_url = response.url
                    source_name = "Unsplash"
            except:
                pass
        
        # 3. Pexels（APIキー不要の方法）
        if not image_url:
            try:
                search_url = f"https://images.pexels.com/photos/search/{urllib.parse.quote(prompt)}/"
                response = await asyncio.to_thread(requests.get, search_url, timeout=10)
                
                if response.status_code == 200 and BeautifulSoup:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    img_tags = soup.find_all('img', class_='photo-item__img')
                    if img_tags:
                        image_url = img_tags[0].get('src')
                        if image_url and not image_url.startswith('http'):
                            image_url = "https://images.pexels.com" + image_url
                        source_name = "Pexels"
            except:
                pass
        
        # 4. 代替画像（すべて失敗した場合）
        if not image_url:
            # カテゴリ別の代替画像
            category_images = {
                "猫": "https://placekitten.com/400/300",
                "犬": "https://placedog.net/400/300",
                "風景": "https://picsum.photos/400/300?random=1",
                "花": "https://picsum.photos/400/300?random=2",
                "空": "https://picsum.photos/400/300?random=3",
                "海": "https://picsum.photos/400/300?random=4",
                "山": "https://picsum.photos/400/300?random=5",
                "都市": "https://picsum.photos/400/300?random=6",
                "自然": "https://picsum.photos/400/300?random=7",
                "動物": "https://placekitten.com/400/300",
                "食べ物": "https://picsum.photos/400/300?random=8",
                "車": "https://picsum.photos/400/300?random=9",
                "建築": "https://picsum.photos/400/300?random=10"
            }
            
            # キーワードに基づいてカテゴリを判定
            for category, url in category_images.items():
                if category in prompt:
                    image_url = url
                    source_name = "代替画像"
                    break
            
            # デフォルト画像
            if not image_url:
                image_url = "https://picsum.photos/400/300?random=" + str(random.randint(1, 1000))
                source_name = "ランダム画像"
        
        embed = discord.Embed(
            title="🎨 完全無料画像検索結果",
            description=f"**キーワード**: {prompt}",
            color=0xFF69B4
        )
        embed.set_image(url=image_url)
        embed.add_field(name="画像ソース", value=source_name, inline=True)
        embed.set_footer(text=f"検索者: {interaction.user.display_name} | 完全無料・APIキー不要")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        logger.error(f"画像検索エラー: {e}")
        # エラー時は確実に動作する画像を表示
        embed = discord.Embed(
            title="🎨 完全無料画像検索結果",
            description=f"**キーワード**: {prompt}\n\nエラーが起きたけど、ふらんちゃんが代わりに画像を用意したよ♡",
            color=0xFF69B4
        )
        embed.set_image(url="https://picsum.photos/400/300?random=" + str(random.randint(1, 1000)))
        embed.set_footer(text=f"検索者: {interaction.user.display_name} | エラー時代替画像")
        
        await interaction.followup.send(embed=embed)

# ===================== 新機能: 翻訳機能の拡張 =====================

SUPPORTED_LANGUAGES = {
    "ja": "日本語", "en": "英語", "ko": "韓国語", "zh": "中国語", 
    "es": "スペイン語", "fr": "フランス語", "de": "ドイツ語", 
    "it": "イタリア語", "pt": "ポルトガル語", "ru": "ロシア語"
}

@bot.tree.command(name="translate_advanced", description="多言語翻訳機能だよ♡")
@app_commands.describe(
    text="翻訳したい文章",
    target_lang="翻訳先言語（ja/en/ko/zh/es/fr/de/it/pt/ru）"
)
async def translate_advanced(interaction: discord.Interaction, text: str, target_lang: str):
    if target_lang not in SUPPORTED_LANGUAGES:
        await interaction.response.send_message(
            f"対応言語: {', '.join(SUPPORTED_LANGUAGES.keys())}",
            ephemeral=True
        )
        return
    
    await interaction.response.defer()
    
    try:
        # Google翻訳APIを使用（無料版）
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={text}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    translated = data[0][0][0]
                    detected_lang = data[2]
                    
                    embed = discord.Embed(
                        title="🌐 翻訳結果",
                        color=0xFF69B4
                    )
                    embed.add_field(name="原文", value=text, inline=False)
                    embed.add_field(name="翻訳", value=translated, inline=False)
                    embed.add_field(name="検出言語", value=detected_lang, inline=True)
                    embed.add_field(name="翻訳先", value=SUPPORTED_LANGUAGES[target_lang], inline=True)
                    
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send("翻訳に失敗しちゃったよ💦", ephemeral=True)
                    
    except Exception as e:
        logger.error(f"翻訳エラー: {e}")
        await interaction.followup.send("翻訳でエラーが起きちゃったよ💦", ephemeral=True)

# ===================== 新機能: 音楽機能の強化 =====================

@bot.tree.command(name="search_music", description="YouTubeで音楽を検索して再生するよ♡")
@app_commands.describe(query="検索したい曲名やアーティスト名")
async def search_music(interaction: discord.Interaction, query: str):
    if not VC:
        await interaction.response.send_message("先にVCに入ってからね💦", ephemeral=True)
        return
    
    await interaction.response.defer()
    
    try:
        if not yt_dlp:
            await interaction.followup.send("yt-dlpがインストールされていないよ💦", ephemeral=True)
            return
        
        # yt-dlpで検索
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 検索結果を取得
            search_results = ydl.extract_info(f"ytsearch1:{query}", download=False)
            
            if 'entries' in search_results and search_results['entries']:
                video = search_results['entries'][0]
                video_url = f"https://www.youtube.com/watch?v={video['id']}"
                title = video.get('title', 'Unknown Title')
                
                # 既存のBGMを停止
                global current_bgm, is_playing_bgm
                if current_bgm:
                    current_bgm.stop()
                
                # 新しいBGMを再生
                current_bgm = discord.FFmpegPCMAudio(video_url, executable=ffmpeg_path)
                VC.play(current_bgm)
                is_playing_bgm = True
                
                embed = discord.Embed(
                    title="🎵 音楽再生中",
                    description=f"**{title}**",
                    color=0xFF69B4
                )
                embed.add_field(name="URL", value=video_url, inline=False)
                
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(f"「{query}」の検索結果が見つからなかったよ💦", ephemeral=True)
                
    except Exception as e:
        logger.error(f"音楽検索エラー: {e}")
        await interaction.followup.send("音楽検索でエラーが起きちゃったよ💦", ephemeral=True)

# ===================== 新機能: ゲーム機能の追加 =====================

@bot.tree.command(name="rps", description="じゃんけんゲームだよ♡")
@app_commands.describe(choice="グー、チョキ、パーのどれかを選んでね")
async def rock_paper_scissors(interaction: discord.Interaction, choice: str):
    choices = ["グー", "チョキ", "パー"]
    if choice not in choices:
        await interaction.response.send_message("グー、チョキ、パーのどれかを選んでね！", ephemeral=True)
        return
    
    bot_choice = random.choice(choices)
    
    # 勝敗判定
    if choice == bot_choice:
        result = "引き分けだよ〜"
    elif (
        (choice == "グー" and bot_choice == "チョキ") or
        (choice == "チョキ" and bot_choice == "パー") or
        (choice == "パー" and bot_choice == "グー")
    ):
        result = "あなたの勝ちだよ♡"
    else:
        result = "ふらんちゃんの勝ちだよ〜♪"
    
    embed = discord.Embed(
        title="✂️ じゃんけん結果",
        color=0xFF69B4
    )
    embed.add_field(name="あなたの選択", value=choice, inline=True)
    embed.add_field(name="ふらんちゃんの選択", value=bot_choice, inline=True)
    embed.add_field(name="結果", value=result, inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="number_guess", description="数字当てゲームだよ♡")
@app_commands.describe(max_number="最大数字（デフォルト: 100）")
async def number_guess(interaction: discord.Interaction, max_number: int = 100):
    if max_number < 1 or max_number > 1000:
        await interaction.response.send_message("1〜1000の間で指定してね！", ephemeral=True)
        return
    
    target = random.randint(1, max_number)
    user_id = interaction.user.id
    
    # ゲーム状態を保存
    if "number_guess" not in bot.game_stats:
        bot.game_stats["number_guess"] = {}
    
    bot.game_stats["number_guess"][user_id] = {
        "target": target,
        "max_number": max_number,
        "attempts": 0,
        "start_time": time.time()
    }
    
    embed = discord.Embed(
        title="🔢 数字当てゲーム開始！",
        description=f"1〜{max_number}の間の数字を当ててね♡\n`/guess <数字>` で回答してね！",
        color=0xFF69B4
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="guess", description="数字当てゲームの回答だよ♡")
@app_commands.describe(number="予想する数字")
async def make_guess(interaction: discord.Interaction, number: int):
    user_id = interaction.user.id
    
    if "number_guess" not in bot.game_stats or user_id not in bot.game_stats["number_guess"]:
        await interaction.response.send_message("先に `/number_guess` でゲームを開始してね！", ephemeral=True)
        return
    
    game = bot.game_stats["number_guess"][user_id]
    game["attempts"] += 1
    
    if number == game["target"]:
        elapsed_time = time.time() - game["start_time"]
        embed = discord.Embed(
            title="🎉 正解だよ♡",
            description=f"おめでとう！{game['attempts']}回目で正解したよ〜\n時間: {elapsed_time:.1f}秒",
            color=0x00FF00
        )
        del bot.game_stats["number_guess"][user_id]
    elif number < game["target"]:
        embed = discord.Embed(
            title="📈 もっと大きいよ〜",
            description=f"ヒント: {number}より大きい数字だよ♡\n試行回数: {game['attempts']}回",
            color=0xFFA500
        )
    else:
        embed = discord.Embed(
            title="📉 もっと小さいよ〜",
            description=f"ヒント: {number}より小さい数字だよ♡\n試行回数: {game['attempts']}回",
            color=0xFFA500
        )
    
    await interaction.response.send_message(embed=embed)

# ===================== 新機能: 統計機能 =====================

@bot.tree.command(name="server_stats", description="サーバーの統計情報を表示するよ♡")
async def server_stats(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("サーバー情報はDMでは見られないよ！", ephemeral=True)
        return
    
    # 統計情報を計算
    total_members = guild.member_count
    online_members = len([m for m in guild.members if m.status != discord.Status.offline])
    bot_count = len([m for m in guild.members if m.bot])
    human_count = total_members - bot_count
    
    # チャンネル統計
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)
    
    # ロール統計
    role_count = len(guild.roles)
    
    # サーバー作成からの経過日数
    days_created = (datetime.datetime.now() - guild.created_at).days
    
    embed = discord.Embed(
        title=f"📊 {guild.name} の統計情報",
        color=0xFF69B4
    )
    
    embed.add_field(name="👥 メンバー", value=f"総数: {total_members}\nオンライン: {online_members}\n人間: {human_count}\nBot: {bot_count}", inline=True)
    embed.add_field(name="📺 チャンネル", value=f"テキスト: {text_channels}\nボイス: {voice_channels}\nカテゴリ: {categories}", inline=True)
    embed.add_field(name="🏷️ その他", value=f"ロール数: {role_count}\n作成日: {days_created}日前", inline=True)
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="user_stats", description="自分の統計情報を表示するよ♡")
async def user_stats(interaction: discord.Interaction):
    user = interaction.user
    guild = interaction.guild
    
    if not guild:
        await interaction.response.send_message("サーバーでのみ使用可能だよ！", ephemeral=True)
        return
    
    member = guild.get_member(user.id)
    if not member:
        await interaction.response.send_message("メンバー情報が見つからないよ💦", ephemeral=True)
        return
    
    # アカウント作成からの経過日数
    account_age = (datetime.datetime.now() - user.created_at).days
    
    # サーバー参加からの経過日数
    if member.joined_at:
        server_age = (datetime.datetime.now() - member.joined_at).days
    else:
        server_age = "不明"
    
    # ロール情報
    roles = [role.name for role in member.roles if role.name != "@everyone"]
    top_role = member.top_role.name if member.top_role.name != "@everyone" else "なし"
    
    embed = discord.Embed(
        title=f"📊 {user.display_name} の統計情報",
        color=member.color if member.color != discord.Color.default() else 0xFF69B4
    )
    
    embed.add_field(name="👤 基本情報", value=f"ユーザー名: {user}\nID: {user.id}\nニックネーム: {member.nick or 'なし'}", inline=False)
    embed.add_field(name="⏰ 時間情報", value=f"アカウント作成: {account_age}日前\nサーバー参加: {server_age}日前", inline=True)
    embed.add_field(name="🏷️ ロール", value=f"最高ロール: {top_role}\nロール数: {len(roles)}", inline=True)
    
    if user.avatar:
        embed.set_thumbnail(url=user.avatar.url)
    
    await interaction.response.send_message(embed=embed)

# ===================== 新機能: ウェルカム機能 =====================

@bot.event
async def on_member_join(member):
    if WELCOME_CHANNEL_ID:
        try:
            channel = bot.get_channel(WELCOME_CHANNEL_ID)
            if channel:
                embed = discord.Embed(
                    title="🎉 ようこそ！",
                    description=f"{member.mention} さん、ふらんちゃんのサーバーにようこそ♡\n楽しい時間を過ごしてね〜♪",
                    color=0xFF69B4
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                embed.add_field(name="👥 メンバー数", value=f"{member.guild.member_count}人目", inline=True)
                embed.add_field(name="📅 参加日", value=datetime.datetime.now().strftime("%Y年%m月%d日"), inline=True)
                
                await channel.send(embed=embed)
                logger.info(f"New member joined: {member.name} (ID: {member.id})")
        except Exception as e:
            logger.error(f"Welcome message error: {e}")

@bot.event
async def on_member_remove(member):
    if WELCOME_CHANNEL_ID:
        try:
            channel = bot.get_channel(WELCOME_CHANNEL_ID)
            if channel:
                embed = discord.Embed(
                    title="👋 さようなら",
                    description=f"{member.name} さんがサーバーを去りました…\nまた来てね♡",
                    color=0xFF69B4
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                
                await channel.send(embed=embed)
                logger.info(f"Member left: {member.name} (ID: {member.id})")
        except Exception as e:
            logger.error(f"Goodbye message error: {e}")

# ===================== 新機能: ログ機能 =====================

@bot.tree.command(name="logs", description="Botのログを表示するよ♡（管理者専用）")
@app_commands.describe(lines="表示する行数（デフォルト: 20）")
async def show_logs(interaction: discord.Interaction, lines: int = 20):
    # オーナー権限チェック
    owner_id_str = os.getenv("OWNER_ID")
    try:
        owner_id = int(owner_id_str) if owner_id_str is not None else None
    except (TypeError, ValueError):
        owner_id = None

    if interaction.user.id != owner_id:
        await interaction.response.send_message("ごめんね、オーナーしかこのコマンドは使えないよ！", ephemeral=True)
        return
    
    try:
        with open('bot.log', 'r', encoding='utf-8') as f:
            log_lines = f.readlines()
        
        # 最新のN行を取得
        recent_logs = log_lines[-lines:] if len(log_lines) > lines else log_lines
        
        log_text = ''.join(recent_logs)
        
        if len(log_text) > 2000:
            log_text = log_text[-2000:] + "\n...（省略）"
        
        embed = discord.Embed(
            title="📋 Botログ",
            description=f"```\n{log_text}\n```",
            color=0xFF69B4
        )
        embed.set_footer(text=f"最新{len(recent_logs)}行を表示")
        
        await interaction.response.send_message(embed=embed)
        
    except FileNotFoundError:
        await interaction.response.send_message("ログファイルが見つからないよ💦", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"ログの読み込みでエラーが起きたよ💦: {e}", ephemeral=True)

# ===================== 新機能: システム情報 =====================

@bot.tree.command(name="system_info", description="Botのシステム情報を表示するよ♡")
async def system_info(interaction: discord.Interaction):
    import psutil
    
    # システム情報を取得
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Bot情報
    bot_uptime = datetime.datetime.now() - bot.start_time if hasattr(bot, 'start_time') else datetime.timedelta(0)
    
    embed = discord.Embed(
        title="💻 システム情報",
        color=0xFF69B4
    )
    
    embed.add_field(name="🖥️ CPU", value=f"使用率: {cpu_percent}%", inline=True)
    embed.add_field(name="💾 メモリ", value=f"使用率: {memory.percent}%\n使用量: {memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB", inline=True)
    embed.add_field(name="💿 ディスク", value=f"使用率: {disk.percent}%\n空き容量: {disk.free // (1024**3)}GB", inline=True)
    embed.add_field(name="🤖 Bot", value=f"稼働時間: {str(bot_uptime).split('.')[0]}\nレイテンシ: {round(bot.latency * 1000)}ms", inline=True)
    
    await interaction.response.send_message(embed=embed)

# ===================== 新機能: カスタムコマンド =====================

# カスタムコマンド保存用
custom_commands = {}

@bot.tree.command(name="custom_command", description="カスタムコマンドを作成するよ♡")
@app_commands.describe(name="コマンド名", response="応答メッセージ")
async def create_custom_command(interaction: discord.Interaction, name: str, response: str):
    # オーナー権限チェック
    owner_id_str = os.getenv("OWNER_ID")
    try:
        owner_id = int(owner_id_str) if owner_id_str is not None else None
    except (TypeError, ValueError):
        owner_id = None

    if interaction.user.id != owner_id:
        await interaction.response.send_message("ごめんね、オーナーしかこのコマンドは使えないよ！", ephemeral=True)
        return
    
    if len(name) > 20:
        await interaction.response.send_message("コマンド名は20文字以内にしてね！", ephemeral=True)
        return
    
    if len(response) > 1000:
        await interaction.response.send_message("応答メッセージは1000文字以内にしてね！", ephemeral=True)
        return
    
    custom_commands[name] = response
    
    # カスタムコマンドをJSONファイルに保存
    try:
        with open('custom_commands.json', 'w', encoding='utf-8') as f:
            json.dump(custom_commands, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"カスタムコマンド保存エラー: {e}")
    
    embed = discord.Embed(
        title="✅ カスタムコマンド作成完了",
        description=f"コマンド名: `{name}`\n応答: {response}",
        color=0x00FF00
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="custom_command_list", description="カスタムコマンド一覧を表示するよ♡")
async def list_custom_commands(interaction: discord.Interaction):
    if not custom_commands:
        await interaction.response.send_message("カスタムコマンドはまだないよ💦", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="📝 カスタムコマンド一覧",
        color=0xFF69B4
    )
    
    for name, response in custom_commands.items():
        embed.add_field(name=f"!{name}", value=response[:100] + "..." if len(response) > 100 else response, inline=False)
    
    await interaction.response.send_message(embed=embed)

# カスタムコマンドの実行
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # カスタムコマンドの処理
    if message.content.startswith('!'):
        command_name = message.content[1:].split()[0]
        if command_name in custom_commands:
            await message.channel.send(custom_commands[command_name])
            return
    
    # 既存のメッセージ処理
    await bot.process_commands(message)

# カスタムコマンドの読み込み
try:
    with open('custom_commands.json', 'r', encoding='utf-8') as f:
        custom_commands = json.load(f)
    logger.info(f"カスタムコマンドを読み込みました: {len(custom_commands)}個")
except FileNotFoundError:
    custom_commands = {}
except Exception as e:
    logger.error(f"カスタムコマンド読み込みエラー: {e}")
    custom_commands = {}

# ===================== 既存のコードはここから続く =====================

# GIF検索コマンド（スラッシュコマンド）
@bot.tree.command(name="gif", description="キーワードでGIFを検索するよ！")
@discord.app_commands.describe(keyword="検索したいキーワードを入力してね") # スラッシュコマンドの引数の説明だよ
async def gif(interaction: discord.Interaction, keyword: str): # 引数名を 'search_query' から 'keyword' に変更したよ
    # スラッシュコマンドは、応答を返すまでに時間がかかるとエラーになることがあるから、
    # まずは「思考中...」みたいなメッセージを送って、処理中にするよ。
    await interaction.response.defer() 

    # TenorにGIFを探してもらうためのお願い（リクエスト）を作るよ
    params = {
        'key': TENOR_API_KEY,
        'q': keyword, # 検索したいキーワードだよ
        'limit': 10,       # 最大で10個のGIFを探してほしいってお願いするよ
        'contentfilter': 'medium'      # 一般向けのGIFだけにする設定だよ
    }

    try:
        # Tenorに実際にお願いを送って、返事を待つよ
        response = requests.get(TENOR_SEARCH_URL, params=params)
        response.raise_for_status() # もしエラーがあったら教えてくれるよ

        # Tenorからの返事をJSONっていう形に変換するよ
        data = response.json()

        # 返事の中にGIFがあるかチェックするよ
        if data.get('results') and len(data['results']) > 0:
            # 見つかったGIFの中から、ランダムに1つ選ぶよ
            gif_choice = random.choice(data['results'])
            gif_url = gif_choice['media'][0]['gif']['url']
            
            # 選んだGIFのURLをDiscordに送るよ！
            await interaction.followup.send(gif_url) # deferを使った場合、followup.sendを使うよ
        else:
            # もし見つからなかったら、ごめんねって伝えるよ
            await interaction.followup.send(f'ごめんね、**{keyword}** のGIFは見つからなかったよ…')

    except requests.exceptions.RequestException as e:
        print(f"Tenor APIとの通信エラーだよ: {e}")
        await interaction.followup.send('Tenorと通信できなかったみたい…ごめんね！')
    except Exception as e:
        print(f"エラーが発生したよ: {e}")
        await interaction.followup.send('何かエラーが起きちゃったみたい…ごめんね！')

# ... existing code ...
