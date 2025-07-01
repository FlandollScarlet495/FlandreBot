import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
import datetime
import threading
import time
from functools import wraps
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'flandre_bot_dashboard_secret_key'

# 管理者認証
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "flandre123"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Bot状態の取得
    bot_status = get_bot_status()
    return render_template('dashboard.html', bot_status=bot_status)

@app.route('/commands')
@login_required
def commands():
    try:
        with open('helps.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            commands_list = data.get('helps', [])
    except:
        commands_list = []
    # カテゴリごとにまとめる
    category_commands = defaultdict(list)
    for cmd in commands_list:
        cat = cmd.get('category', 'その他')
        category_commands[cat].append(cmd)
    # README自動生成用の全コマンドリストも渡す
    all_commands = [cmd for cmds in category_commands.values() for cmd in cmds]
    return render_template('commands.html', category_commands=category_commands, all_commands=all_commands)

@app.route('/settings')
@login_required
def settings():
    # 設定の取得
    settings_data = get_settings()
    return render_template('settings.html', settings=settings_data)

@app.route('/logs')
@login_required
def logs():
    # ログの取得
    log_data = get_logs()
    return render_template('logs.html', logs=log_data)

@app.route('/api/bot_status')
@login_required
def api_bot_status():
    return jsonify(get_bot_status())

@app.route('/api/logs')
@login_required
def api_logs():
    return jsonify(get_logs())

@app.route('/api/commands')
@login_required
def api_commands():
    try:
        with open('helps.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return jsonify(data.get('helps', []))
    except:
        return jsonify([])

def get_bot_status():
    # Bot状態の取得（bot_status.jsonから取得）
    try:
        with open('bot_status.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {
            'status': '不明',
            'uptime': '-',
            'servers': '-',
            'users': '-',
            'commands_used': '-',
            'memory_usage': '-',
            'cpu_usage': '-'
        }

def get_commands_list():
    # コマンド一覧の取得
    try:
        with open('commands.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('commands', [])
    except:
        return []

def get_settings():
    # 設定の取得
    try:
        with open('env.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "設定ファイルが見つかりません"

def get_logs():
    # ログの取得
    try:
        with open('bot.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return lines[-50:]  # 最新50行
    except:
        return ["ログファイルが見つかりません"]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 