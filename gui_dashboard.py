import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import threading
import time
import datetime
from collections import defaultdict
import webbrowser
import subprocess
import sys
import requests
import psutil # psutilを追加

class FlandreBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 ふらんちゃんBot ダッシュボード")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f5f5f5')

        # アイコン設定（Windowsの場合）
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

        # データ保存用
        self.bot_status = {}
        self.commands_data = []
        self.logs_data = []

        # GUI構築
        self.setup_gui()

        # 自動更新開始
        self.start_auto_refresh()

    def setup_gui(self):
        # メインフレーム
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # タイトル
        title_label = tk.Label(main_frame, text="🌸 ふらんちゃんBot ダッシュボード",
                              font=("Arial", 20, "bold"), fg="#ff69b4", bg="#f5f5f5")
        title_label.pack(pady=(0, 20))

        # ノートブック（タブ）作成
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 各タブを作成
        self.create_dashboard_tab()
        self.create_commands_tab()
        self.create_logs_tab()
        self.create_settings_tab()
        self.create_control_tab()

    def create_dashboard_tab(self):
        """ダッシュボードタブ"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 ダッシュボード")

        # ステータス表示エリア
        status_frame = ttk.LabelFrame(dashboard_frame, text="Bot状態", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=5)

        # ステータスグリッド
        self.status_vars = {}
        status_items = [
            ("status", "Bot状態", "不明"),
            ("uptime", "稼働時間", "-"),
            ("servers", "サーバー数", "0"),
            ("users", "ユーザー数", "0"),
            ("commands_used", "コマンド使用回数", "0"),
            ("memory_usage", "Botメモリ", "-"), # ラベル変更
            ("cpu_usage", "Bot CPU", "-"), # ラベル変更
            ("latency", "レイテンシ", "-"),
            ("system_cpu", "システムCPU", "-"),
            ("system_memory", "システムメモリ", "-"),
            ("system_disk", "システムディスク", "-"),
            ("system_time", "現在時刻", "-")
        ]

        for i, (key, label, default) in enumerate(status_items):
            row = i // 2
            col = i % 2

            frame = ttk.Frame(status_frame)
            frame.grid(row=row, column=col, sticky="ew", padx=5, pady=5)

            ttk.Label(frame, text=f"{label}:", font=("Arial", 10, "bold")).pack(anchor="w")
            var = tk.StringVar(value=default)
            self.status_vars[key] = var
            ttk.Label(frame, textvariable=var, font=("Arial", 12)).pack(anchor="w")

        # プログレスバー
        progress_frame = ttk.LabelFrame(dashboard_frame, text="リソース使用率", padding=10)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)

        # Bot メモリ使用率
        ttk.Label(progress_frame, text="Bot メモリ使用率:").pack(anchor="w")
        self.memory_value_label = ttk.Label(progress_frame, text="0%", font=("Arial", 14, "bold"), foreground="#007acc")
        self.memory_value_label.pack(anchor="w")
        self.memory_progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.memory_progress.pack(fill=tk.X, pady=2)

        # Bot CPU使用率
        ttk.Label(progress_frame, text="Bot CPU使用率:").pack(anchor="w")
        self.cpu_value_label = ttk.Label(progress_frame, text="0%", font=("Arial", 14, "bold"), foreground="#007acc")
        self.cpu_value_label.pack(anchor="w")
        self.cpu_progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.cpu_progress.pack(fill=tk.X, pady=2)

        # システムCPU使用率
        ttk.Label(progress_frame, text="システムCPU使用率:").pack(anchor="w")
        self.system_cpu_value_label = ttk.Label(progress_frame, text="0%", font=("Arial", 14, "bold"), foreground="#007acc")
        self.system_cpu_value_label.pack(anchor="w")
        self.system_cpu_progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.system_cpu_progress.pack(fill=tk.X, pady=2)

        # システムメモリ使用率
        ttk.Label(progress_frame, text="システムメモリ使用率:").pack(anchor="w")
        self.system_memory_value_label = ttk.Label(progress_frame, text="0%", font=("Arial", 14, "bold"), foreground="#007acc")
        self.system_memory_value_label.pack(anchor="w")
        self.system_memory_progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.system_memory_progress.pack(fill=tk.X, pady=2)

        # システムディスク使用率
        ttk.Label(progress_frame, text="システムディスク使用率:").pack(anchor="w")
        self.system_disk_value_label = ttk.Label(progress_frame, text="0%", font=("Arial", 14, "bold"), foreground="#007acc")
        self.system_disk_value_label.pack(anchor="w")
        self.system_disk_progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.system_disk_progress.pack(fill=tk.X, pady=2)

        # ====== 自動更新間隔選択UIを追加 ======
        interval_frame = ttk.Frame(dashboard_frame)
        interval_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        ttk.Label(interval_frame, text="⏱️ 自動更新間隔:").pack(side=tk.LEFT)
        self.refresh_interval_var = tk.IntVar(value=5)
        interval_options = [("1秒ごと", 1), ("5秒ごと", 5), ("10秒ごと", 10), ("30秒ごと", 30), ("60秒ごと", 60)] # オプション追加
        for label, val in interval_options:
            ttk.Radiobutton(interval_frame, text=label, variable=self.refresh_interval_var, value=val, command=self.on_refresh_interval_change).pack(side=tk.LEFT, padx=5)
        # =====================================

        # 更新ボタン
        button_frame = ttk.Frame(dashboard_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(button_frame, text="🔄 更新", command=self.refresh_dashboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📊 詳細統計", command=self.show_detailed_stats).pack(side=tk.LEFT, padx=5)

    def create_commands_tab(self):
        """コマンド一覧タブ"""
        commands_frame = ttk.Frame(self.notebook)
        self.notebook.add(commands_frame, text="📝 コマンド")

        # 検索フレーム
        search_frame = ttk.Frame(commands_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="検索:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_commands)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        # カテゴリフィルター
        ttk.Label(search_frame, text="カテゴリ:").pack(side=tk.LEFT, padx=(20, 5))
        self.category_var = tk.StringVar(value="すべて")
        self.category_combo = ttk.Combobox(search_frame, textvariable=self.category_var,
                                     values=["すべて"], state="readonly", width=15)
        self.category_combo.pack(side=tk.LEFT, padx=5)
        self.category_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_commands())

        # コマンドリスト
        list_frame = ttk.Frame(commands_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Treeview（テーブル形式）
        columns = ("コマンド", "説明", "使い方", "カテゴリ")
        self.commands_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.commands_tree.heading(col, text=col)
            self.commands_tree.column(col, width=200)

        # スクロールバー
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.commands_tree.yview)
        self.commands_tree.configure(yscrollcommand=scrollbar.set)

        self.commands_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 詳細表示
        detail_frame = ttk.LabelFrame(commands_frame, text="コマンド詳細", padding=10)
        detail_frame.pack(fill=tk.X, padx=10, pady=5)

        self.detail_text = scrolledtext.ScrolledText(detail_frame, height=8, wrap=tk.WORD)
        self.detail_text.pack(fill=tk.BOTH, expand=True)

        # イベントバインド
        self.commands_tree.bind('<<TreeviewSelect>>', self.show_command_detail)

        # ボタン
        button_frame = ttk.Frame(commands_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(button_frame, text="🔄 更新", command=self.refresh_commands).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📋 コピー", command=self.copy_command).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📄 エクスポート", command=self.export_commands).pack(side=tk.LEFT, padx=5)

    def create_logs_tab(self):
        """ログ表示タブ"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="📋 ログ")

        # ログ表示エリア
        log_frame = ttk.LabelFrame(logs_frame, text="Botログ", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # ログレベルフィルター
        filter_frame = ttk.Frame(logs_frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(filter_frame, text="ログレベル:").pack(side=tk.LEFT)
        self.log_level_var = tk.StringVar(value="すべて")
        log_level_combo = ttk.Combobox(filter_frame, textvariable=self.log_level_var,
                                      values=["すべて", "ERROR", "WARNING", "INFO", "DEBUG"],
                                      state="readonly", width=10)
        log_level_combo.pack(side=tk.LEFT, padx=5)
        log_level_combo.bind('<<ComboboxSelected>>', self.filter_logs)

        # 行数制限
        ttk.Label(filter_frame, text="表示行数:").pack(side=tk.LEFT, padx=(20, 5))
        self.log_lines_var = tk.StringVar(value="100")
        log_lines_combo = ttk.Combobox(filter_frame, textvariable=self.log_lines_var,
                                      values=["50", "100", "200", "500", "1000"],
                                      state="readonly", width=8)
        log_lines_combo.pack(side=tk.LEFT, padx=5)
        log_lines_combo.bind('<<ComboboxSelected>>', self.refresh_logs) # フィルターではなくrefresh_logsを呼ぶ

        # ボタン
        button_frame = ttk.Frame(logs_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(button_frame, text="🔄 更新", command=self.refresh_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ クリア", command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 保存", command=self.save_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📄 エクスポート", command=self.export_logs).pack(side=tk.LEFT, padx=5)

    def create_settings_tab(self):
        """設定タブ"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ 設定")

        # 設定表示エリア
        settings_display_frame = ttk.LabelFrame(settings_frame, text="現在の設定", padding=10)
        settings_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.settings_text = scrolledtext.ScrolledText(settings_display_frame, wrap=tk.WORD, font=("Consolas", 9))
        self.settings_text.pack(fill=tk.BOTH, expand=True)

        # ボタン
        button_frame = ttk.Frame(settings_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(button_frame, text="🔄 更新", command=self.refresh_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📝 編集", command=self.edit_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 保存", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📄 エクスポート", command=self.export_settings).pack(side=tk.LEFT, padx=5)

    def create_control_tab(self):
        """制御タブ"""
        control_frame = ttk.Frame(self.notebook)
        self.notebook.add(control_frame, text="🎮 制御")

        # Bot制御
        control_group = ttk.LabelFrame(control_frame, text="Bot制御", padding=10)
        control_group.pack(fill=tk.X, padx=10, pady=5)

        # 起動/停止ボタン
        self.bot_status_var = tk.StringVar(value="停止中")
        status_label = ttk.Label(control_group, textvariable=self.bot_status_var,
                                font=("Arial", 12, "bold"))
        status_label.pack(pady=5)

        button_frame = ttk.Frame(control_group)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="🚀 起動", command=self.start_bot).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🛑 停止", command=self.stop_bot).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 再起動", command=self.restart_bot).pack(side=tk.LEFT, padx=5)

        # ファイル管理
        file_group = ttk.LabelFrame(control_frame, text="ファイル管理", padding=10)
        file_group.pack(fill=tk.X, padx=10, pady=5)

        file_button_frame = ttk.Frame(file_group)
        file_button_frame.pack(pady=5)

        ttk.Button(file_button_frame, text="📁 フォルダを開く", command=self.open_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_button_frame, text="📄 ログファイル", command=self.open_log_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_button_frame, text="⚙️ 設定ファイル", command=self.open_config_file).pack(side=tk.LEFT, padx=5)

        # システム情報
        system_group = ttk.LabelFrame(control_frame, text="システム情報", padding=10)
        system_group.pack(fill=tk.X, padx=10, pady=5)

        # --- 追加: システムリソースのプログレスバー＋ラベル ---
        sysres_frame = ttk.Frame(system_group)
        sysres_frame.pack(fill=tk.X, pady=5)
        # CPU
        ttk.Label(sysres_frame, text="システムCPU使用率:").pack(anchor="w") # ラベル追加
        self.ctrl_sys_cpu_value_label = ttk.Label(sysres_frame, text="0%", font=("Arial", 14, "bold"), foreground="#007acc")
        self.ctrl_sys_cpu_value_label.pack(anchor="w")
        self.ctrl_sys_cpu_progress = ttk.Progressbar(sysres_frame, length=400, mode='determinate')
        self.ctrl_sys_cpu_progress.pack(fill=tk.X, pady=2)
        # MEM
        ttk.Label(sysres_frame, text="システムメモリ使用率:").pack(anchor="w") # ラベル追加
        self.ctrl_sys_mem_value_label = ttk.Label(sysres_frame, text="0%", font=("Arial", 14, "bold"), foreground="#007acc")
        self.ctrl_sys_mem_value_label.pack(anchor="w")
        self.ctrl_sys_mem_progress = ttk.Progressbar(sysres_frame, length=400, mode='determinate')
        self.ctrl_sys_mem_progress.pack(fill=tk.X, pady=2)
        # DISK
        ttk.Label(sysres_frame, text="システムディスク使用率:").pack(anchor="w") # ラベル追加
        self.ctrl_sys_disk_value_label = ttk.Label(sysres_frame, text="0%", font=("Arial", 14, "bold"), foreground="#007acc")
        self.ctrl_sys_disk_value_label.pack(anchor="w")
        self.ctrl_sys_disk_progress = ttk.Progressbar(sysres_frame, length=400, mode='determinate')
        self.ctrl_sys_disk_progress.pack(fill=tk.X, pady=2)
        # --- ここまで追加 ---

        self.system_text = scrolledtext.ScrolledText(system_group, height=8, wrap=tk.WORD, font=("Consolas", 9))
        self.system_text.pack(fill=tk.BOTH, expand=True)

        # システム情報更新ボタン
        ttk.Button(system_group, text="🔄 システム情報更新", command=self.refresh_system_info).pack(pady=5)

    def start_auto_refresh(self):
        """自動更新開始（after方式）"""
        self._auto_refresh_running = True
        self.auto_refresh_loop()

    def auto_refresh_loop(self):
        if not self._auto_refresh_running:
            return
        try:
            # 各タブの更新メソッドを呼び出す
            self.refresh_dashboard()
            self.refresh_commands() # コマンド一覧も定期更新
            self.refresh_logs() # ログも定期更新
            self.refresh_system_info() # システム情報も定期更新
        except Exception as e:
            print(f"自動更新エラー: {e}")
            # エラー発生時は少し待って再試行
            interval = 60000 # 1分
        else:
            # 正常時は設定された間隔で更新
            interval = self.refresh_interval_var.get() * 1000 if hasattr(self, 'refresh_interval_var') else 5000 # デフォルト5秒
        self.root.after(interval, self.auto_refresh_loop)

    def on_refresh_interval_change(self):
        # 自動更新間隔が変更されたときに呼ばれる
        # after方式では、次のauto_refresh_loop呼び出しで新しい間隔が使われるため、特別な処理は不要
        pass

    def refresh_dashboard(self):
        """ダッシュボード更新"""
        try:
            # bot_status.jsonの代わりにAPIから取得
            # Bot本体 (flandre_bot.py) が http://localhost:5005/status で状態を返すAPIを提供している必要があります
            try:
                res = requests.get('http://localhost:5005/status', timeout=2)
                res.raise_for_status() # HTTPエラーがあれば例外発生
                self.bot_status = res.json()
                self.bot_status_var.set("オンライン") # Bot状態をオンラインに設定
            except requests.exceptions.RequestException as e:
                print(f"Bot状態取得エラー (API): {e}")
                self.bot_status = {} # 取得失敗時は空にする
                self.bot_status_var.set("オフライン") # Bot状態をオフラインに設定

            # ステータス更新
            for key, var in self.status_vars.items():
                if key in self.bot_status:
                    var.set(str(self.bot_status[key]))
                elif key in ['status', 'uptime', 'servers', 'users', 'commands_used', 'memory_usage', 'cpu_usage', 'latency']:
                     # APIから取得できなかったBot関連の項目はデフォルト値に戻す
                    var.set("-")
                    if key == 'status':
                         var.set("オフライン")


            # プログレスバー更新 (Bot関連)
            try:
                # Botメモリ使用率 (MB表示からパーセント表示に変換が必要な場合)
                if 'memory_usage' in self.bot_status:
                    mem_str = self.bot_status['memory_usage'].replace(' MB', '').strip()
                    try:
                        mem_mb = float(mem_str)
                        # システム全体のメモリ容量を取得してパーセントを計算 (簡易的)
                        total_memory_gb = psutil.virtual_memory().total / (1024**3)
                        total_memory_mb = total_memory_gb * 1024
                        if total_memory_mb > 0:
                             memory_percent = (mem_mb / total_memory_mb) * 100
                             self.memory_progress['value'] = memory_percent
                             self.memory_value_label['text'] = f"{memory_percent:.1f}% ({mem_str} MB)"
                        else:
                             self.memory_progress['value'] = 0
                             self.memory_value_label['text'] = f"- ({mem_str} MB)"
                    except ValueError:
                         self.memory_progress['value'] = 0
                         self.memory_value_label['text'] = f"- ({mem_str})"
                else:
                    self.memory_progress['value'] = 0
                    self.memory_value_label['text'] = "-"

                # Bot CPU使用率 (パーセント表示を期待)
                if 'cpu_usage' in self.bot_status:
                    cpu_str = self.bot_status['cpu_usage'].replace('%', '').strip()
                    try:
                        cpu_percent = float(cpu_str)
                        self.cpu_progress['value'] = cpu_percent
                        self.cpu_value_label['text'] = f"{cpu_percent:.1f}%"
                    except ValueError:
                        self.cpu_progress['value'] = 0
                        self.cpu_value_label['text'] = f"- ({cpu_str})"
                else:
                    self.cpu_progress['value'] = 0
                    self.cpu_value_label['text'] = "-"

            except Exception as e:
                print(f"Botリソース表示エラー: {e}")
                self.memory_progress['value'] = 0
                self.memory_value_label['text'] = "エラー"
                self.cpu_progress['value'] = 0
                self.cpu_value_label['text'] = "エラー"


            # システム情報を更新
            self.update_system_status()

        except Exception as e:
            print(f"ダッシュボード更新エラー: {e}")

    def update_system_status(self):
        """システム情報を更新 (ダッシュボード用)"""
        try:
            # psutilがインストールされているか確認
            if 'psutil' not in sys.modules:
                 print("psutilがインストールされていません。システム情報は表示できません。")
                 return

            # システム情報を取得
            cpu_percent = psutil.cpu_percent(interval=0.5) # 短い間隔で取得
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            current_time = datetime.datetime.now().strftime('%H:%M:%S')

            # ステータス変数に設定
            if 'system_cpu' in self.status_vars:
                self.status_vars['system_cpu'].set(f"{cpu_percent:.1f}%")
            if 'system_memory' in self.status_vars:
                self.status_vars['system_memory'].set(f"{memory.percent:.1f}%")
            if 'system_disk' in self.status_vars:
                self.status_vars['system_disk'].set(f"{disk.percent:.1f}%")
            if 'system_time' in self.status_vars:
                self.status_vars['system_time'].set(current_time)

            # プログレスバーも更新 (ダッシュボードタブ)
            try:
                self.system_cpu_progress['value'] = cpu_percent
                self.system_cpu_value_label['text'] = f"{cpu_percent:.1f}%"

                self.system_memory_progress['value'] = memory.percent
                self.system_memory_value_label['text'] = f"{memory.percent:.1f}%"

                self.system_disk_progress['value'] = disk.percent
                self.system_disk_value_label['text'] = f"{disk.percent:.1f}%"
            except Exception as e:
                 print(f"システムリソースプログレスバー更新エラー (ダッシュボード): {e}")


        except Exception as e:
            print(f"システム情報更新エラー: {e}")

    def refresh_commands(self):
        """コマンド一覧更新"""
        try:
            # helps.jsonから読み込み
            if os.path.exists('helps.json'):
                with open('helps.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.commands_data = data.get('helps', [])

                # Treeviewクリア
                for item in self.commands_tree.get_children():
                    self.commands_tree.delete(item)

                # カテゴリリスト更新
                categories = sorted(list(set(cmd.get('category', 'その他') for cmd in self.commands_data)))
                categories.insert(0, "すべて") # 「すべて」を先頭に追加
                if hasattr(self, 'category_combo'):
                    current_category = self.category_var.get()
                    self.category_combo['values'] = categories
                    if current_category not in categories:
                         self.category_var.set("すべて") # 現在のカテゴリがなくなったら「すべて」に戻す

                # コマンド追加 (フィルターはfilter_commandsで行う)
                # ここでは全データを読み込むだけ
                self.filter_commands() # 読み込み後にフィルターを適用して表示

        except Exception as e:
            print(f"コマンド更新エラー: {e}")
            messagebox.showerror("エラー", f"コマンド一覧の読み込みに失敗しました: {e}")


    def refresh_logs(self):
        """ログ更新"""
        try:
            if os.path.exists('bot.log'):
                with open('bot.log', 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                self.logs_data = lines # 全ログデータを保持

                # テキスト更新 (フィルターと行数制限を適用して表示)
                self.filter_logs()

        except Exception as e:
            print(f"ログ更新エラー: {e}")
            messagebox.showerror("エラー", f"ログファイルの読み込みに失敗しました: {e}")


    def refresh_settings(self):
        """設定更新"""
        try:
            # env.txtまたは.envから読み込み
            config_file = None
            for file in ['env.txt', '.env']:
                if os.path.exists(file):
                    config_file = file
                    break

            if config_file:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                self.settings_text.delete(1.0, tk.END)
                self.settings_text.insert(1.0, content)
            else:
                self.settings_text.delete(1.0, tk.END)
                self.settings_text.insert(1.0, "設定ファイルが見つかりません")
        except Exception as e:
            print(f"設定更新エラー: {e}")
            messagebox.showerror("エラー", f"設定ファイルの読み込みに失敗しました: {e}")


    def filter_commands(self, *args):
        """コマンドフィルター"""
        search_term = self.search_var.get().lower()
        category = self.category_var.get()

        # Treeviewクリア
        for item in self.commands_tree.get_children():
            self.commands_tree.delete(item)

        # フィルター適用
        for cmd in self.commands_data:
            # 検索フィルター
            if search_term:
                if not (search_term in cmd.get('name', '').lower() or
                       search_term in cmd.get('description', '').lower() or
                       search_term in cmd.get('usage', '').lower() or # 使い方にも検索を適用
                       any(search_term in alias.lower() for alias in cmd.get('aliases', [])) # エイリアスにも検索を適用
                       ):
                    continue

            # カテゴリフィルター
            if category != "すべて" and cmd.get('category', 'その他') != category:
                continue

            self.commands_tree.insert('', 'end', values=(
                cmd.get('name', ''),
                cmd.get('description', ''),
                cmd.get('usage', ''),
                cmd.get('category', 'その他')
            ))

    def filter_logs(self, *args):
        """ログフィルター"""
        try:
            lines = self.logs_data # 全ログデータを使用

            # ログレベルフィルター
            log_level = self.log_level_var.get()
            if log_level != "すべて":
                lines = [line for line in lines if f" - {log_level} -" in line] # ログフォーマットに合わせて修正

            # 行数制限
            try:
                max_lines = int(self.log_lines_var.get())
                lines = lines[-max_lines:]
            except:
                lines = lines[-100:] # デフォルト100行

            # テキスト更新
            self.log_text.delete(1.0, tk.END)
            for line in lines:
                self.log_text.insert(tk.END, line)

            # 最新行にスクロール
            self.log_text.see(tk.END)

        except Exception as e:
            print(f"ログフィルターエラー: {e}")
            # エラー時はログ表示をクリア
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(1.0, f"ログのフィルターまたは表示に失敗しました: {e}")


    def show_command_detail(self, event):
        """コマンド詳細表示"""
        selection = self.commands_tree.selection()
        if selection:
            item = self.commands_tree.item(selection[0])
            values = item['values']

            # 詳細情報を検索 (表示されているコマンド名で検索)
            command_name = values[0]
            found_cmd = next((cmd for cmd in self.commands_data if cmd.get('name') == command_name), None)

            if found_cmd:
                detail = f"コマンド名: {found_cmd.get('name', '')}\n"
                detail += f"説明: {found_cmd.get('description', '')}\n"
                detail += f"使い方: {found_cmd.get('usage', '')}\n"
                detail += f"エイリアス: {', '.join(found_cmd.get('aliases', []))}\n"
                detail += f"カテゴリ: {found_cmd.get('category', 'その他')}\n"

                self.detail_text.delete(1.0, tk.END)
                self.detail_text.insert(1.0, detail)
            else:
                 self.detail_text.delete(1.0, tk.END)
                 self.detail_text.insert(1.0, "コマンド詳細が見つかりません。")


    def show_detailed_stats(self):
        """詳細統計表示"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("詳細統計")
        stats_window.geometry("600x400")

        text = scrolledtext.ScrolledText(stats_window, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        stats_text = "=== ふらんちゃんBot 詳細統計 ===\n\n"
        if self.bot_status:
            for key, value in self.bot_status.items():
                stats_text += f"{key}: {value}\n"
        else:
            stats_text += "Bot状態が取得できませんでした。\n"

        # システム情報も追加
        try:
            import psutil
            stats_text += "\n=== システム情報 ===\n\n"
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            current_time = datetime.datetime.now()

            stats_text += f"  Python バージョン: {sys.version.split()[0]}\n"
            stats_text += f"  OS: {os.name} ({sys.platform})\n"
            stats_text += f"  現在時刻: {current_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

            stats_text += f"💻 CPU情報:\n"
            stats_text += f"  システムCPU使用率: {cpu_percent:.1f}%\n"
            stats_text += f"  CPUコア数: {psutil.cpu_count()}\n"
            try:
                 stats_text += f"  CPU周波数: {psutil.cpu_freq().current:.0f}MHz\n\n"
            except:
                 stats_text += "  CPU周波数: 取得できませんでした\n\n"


            stats_text += f"💾 メモリ情報:\n"
            stats_text += f"  システムメモリ使用率: {memory.percent:.1f}%\n"
            stats_text += f"  使用量: {memory.used // (1024**3):.1f}GB / {memory.total // (1024**3):.1f}GB\n"
            stats_text += f"  空き容量: {memory.available // (1024**3):.1f}GB\n\n"

            stats_text += f"💿 ディスク情報:\n"
            stats_text += f"  ディスク使用率: {disk.percent:.1f}%\n"
            stats_text += f"  使用量: {disk.used // (1024**3):.1f}GB / {disk.total // (1024**3):.1f}GB\n"
            stats_text += f"  空き容量: {disk.free // (1024**3):.1f}GB\n\n"

            # プロセス情報 (GUI自身の情報)
            try:
                process = psutil.Process(os.getpid())
                process_memory = process.memory_info().rss / (1024 * 1024)  # MB
                process_cpu = process.cpu_percent()
                stats_text += f"📊 GUIプロセス情報:\n"
                stats_text += f"  プロセスID: {process.pid}\n"
                stats_text += f"  メモリ使用量: {process_memory:.1f}MB\n"
                stats_text += f"  CPU使用率: {process_cpu:.1f}%\n"
                stats_text += f"  起動時刻: {datetime.datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            except Exception as e:
                 stats_text += f"📊 GUIプロセス情報: 取得できませんでした ({e})\n\n"


        except Exception as e:
            stats_text += f"\nシステム情報の取得に失敗しました: {e}\n"


        text.insert(1.0, stats_text)
        text.configure(state='disabled') # 編集不可にする


    def copy_command(self):
        """コマンドコピー"""
        selection = self.commands_tree.selection()
        if selection:
            item = self.commands_tree.item(selection[0])
            values = item['values']
            command = values[0]

            self.root.clipboard_clear()
            self.root.clipboard_append(command)
            messagebox.showinfo("コピー完了", f"コマンド '{command}' をクリップボードにコピーしました")
        else:
             messagebox.showwarning("警告", "コピーするコマンドを選択してください。")


    def export_commands(self):
        """コマンドエクスポート"""
        try:
            filename = f"commands_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== ふらんちゃんBot コマンド一覧 ===\n\n")
                # 表示されているコマンドのみをエクスポート
                for item_id in self.commands_tree.get_children():
                    values = self.commands_tree.item(item_id)['values']
                    # commands_dataから詳細情報を取得
                    cmd = next((c for c in self.commands_data if c.get('name') == values[0]), None)
                    if cmd:
                        f.write(f"コマンド: {cmd.get('name', '')}\n")
                        f.write(f"説明: {cmd.get('description', '')}\n")
                        f.write(f"使い方: {cmd.get('usage', '')}\n")
                        f.write(f"エイリアス: {', '.join(cmd.get('aliases', []))}\n")
                        f.write(f"カテゴリ: {cmd.get('category', 'その他')}\n")
                        f.write("-" * 50 + "\n")

            messagebox.showinfo("エクスポート完了", f"コマンド一覧を {filename} に保存しました")
        except Exception as e:
            messagebox.showerror("エラー", f"エクスポートに失敗しました: {e}")

    def clear_logs(self):
        """ログクリア"""
        if messagebox.askyesno("確認", "ログ表示をクリアしますか？\n(ファイルの内容は消えません)"):
            self.log_text.delete(1.0, tk.END)
            self.logs_data = [] # 表示データもクリア


    def save_logs(self):
        """ログ保存 (バックアップ)"""
        try:
            filename = f"logs_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            # 現在表示されているログではなく、読み込んだ全ログデータを保存
            with open(filename, 'w', encoding='utf-8') as f:
                f.writelines(self.logs_data)

            messagebox.showinfo("保存完了", f"ログを {filename} に保存しました")
        except Exception as e:
            messagebox.showerror("エラー", f"保存に失敗しました: {e}")

    def export_logs(self):
        """ログエクスポート (保存と同じ処理)"""
        self.save_logs()

    def edit_settings(self):
        """設定編集"""
        # 設定ファイルを開く処理を呼び出す
        self.open_config_file()
        messagebox.showinfo("情報", "設定の編集は開いたファイルを直接編集してください。\n編集後に「更新」ボタンを押すと内容が反映されます。")


    def save_settings(self):
        """設定保存"""
        try:
            content = self.settings_text.get(1.0, tk.END).strip() # 末尾の改行を削除
            # env.txtまたは.envに保存
            config_file = None
            for file in ['env.txt', '.env']:
                if os.path.exists(file):
                    config_file = file
                    break
            # ファイルが見つからない場合はenv.txtに新規作成
            if config_file is None:
                 config_file = 'env.txt'

            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(content)

            messagebox.showinfo("保存完了", f"設定を {config_file} に保存しました")
        except Exception as e:
            messagebox.showerror("エラー", f"保存に失敗しました: {e}")

    def export_settings(self):
        """設定エクスポート (バックアップ)"""
        try:
            filename = f"settings_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            content = self.settings_text.get(1.0, tk.END).strip()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

            messagebox.showinfo("エクスポート完了", f"設定を {filename} に保存しました")
        except Exception as e:
            messagebox.showerror("エラー", f"エクスポートに失敗しました: {e}")

    def start_bot(self):
        """Bot起動"""
        try:
            # start_gui_dashboard.bat と同じディレクトリにある Start.bat を実行
            bot_start_script = os.path.join(os.path.dirname(__file__), 'Start.bat')
            if os.path.exists(bot_start_script):
                # 新しいコンソールウィンドウで実行
                subprocess.Popen([bot_start_script], cwd=os.path.dirname(__file__), creationflags=subprocess.CREATE_NEW_CONSOLE)
                messagebox.showinfo("起動", "Botを起動しました。\n新しいコンソールウィンドウを確認してください。")
                self.bot_status_var.set("起動中 (確認中)") # 起動中だが状態はAPIで確認
            else:
                 messagebox.showwarning("警告", "Bot起動用の Start.bat ファイルが見つかりません。")

        except Exception as e:
            messagebox.showerror("エラー", f"Botの起動に失敗しました: {e}")

    def stop_bot(self):
        """Bot停止"""
        if messagebox.askyesno("確認", "Botを停止しますか？\n(Botプロセスを強制終了します)"):
            try:
                # Bot本体にAPIで停止を指示する方が安全ですが、簡易的にpythonプロセスを終了
                # 注意: これだと他のpythonプロセスも終了する可能性があります
                # より安全な方法は、Bot本体に停止APIを実装し、それを呼び出すことです。
                os.system("taskkill /f /im python.exe 2>nul")
                messagebox.showinfo("停止", "Botを停止しました。\n関連するコンソールウィンドウが閉じたか確認してください。")
                self.bot_status_var.set("停止中")
            except Exception as e:
                messagebox.showerror("エラー", f"Botの停止に失敗しました: {e}")

    def restart_bot(self):
        """Bot再起動"""
        if messagebox.askyesno("確認", "Botを再起動しますか？"):
            self.stop_bot()
            # 停止処理が完了するまで少し待つ
            self.root.after(2000, self.start_bot) # 2秒後に起動処理を呼び出す
            self.bot_status_var.set("再起動中...")


    def open_folder(self):
        """フォルダを開く"""
        try:
            # 現在のスクリプトがあるディレクトリを開く
            folder_path = os.path.dirname(__file__)
            os.startfile(folder_path)
        except Exception as e:
            messagebox.showerror("エラー", f"フォルダを開けませんでした: {e}")

    def open_log_file(self):
        """ログファイルを開く"""
        try:
            log_file_path = os.path.join(os.path.dirname(__file__), 'bot.log')
            if os.path.exists(log_file_path):
                os.startfile(log_file_path)
            else:
                messagebox.showwarning("警告", "ログファイルが見つかりません")
        except Exception as e:
            messagebox.showerror("エラー", f"ログファイルを開けませんでした: {e}")

    def open_config_file(self):
        """設定ファイルを開く"""
        try:
            config_file_path = None
            for file in ['env.txt', '.env']:
                full_path = os.path.join(os.path.dirname(__file__), file)
                if os.path.exists(full_path):
                    config_file_path = full_path
                    break

            if config_file_path:
                os.startfile(config_file_path)
            else:
                messagebox.showwarning("警告", "設定ファイルが見つかりません (env.txt または .env)")
        except Exception as e:
            messagebox.showerror("エラー", f"設定ファイルを開けませんでした: {e}")

    def refresh_system_info(self):
        """システム情報更新 (制御タブ用)"""
        try:
            # psutilがインストールされているか確認
            if 'psutil' not in sys.modules:
                 info = "psutilがインストールされていません。\nシステム情報は表示できません。\n(pip install psutil でインストールしてください)"
                 self.system_text.delete(1.0, tk.END)
                 self.system_text.insert(1.0, info)
                 # プログレスバーもリセット
                 self.ctrl_sys_cpu_progress['value'] = 0
                 self.ctrl_sys_cpu_value_label['text'] = "-"
                 self.ctrl_sys_mem_progress['value'] = 0
                 self.ctrl_sys_mem_value_label['text'] = "-"
                 self.ctrl_sys_disk_progress['value'] = 0
                 self.ctrl_sys_disk_value_label['text'] = "-"
                 return

            # 詳細なシステム情報を取得
            cpu_percent = psutil.cpu_percent(interval=0.1) # 短い間隔で取得
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            current_time = datetime.datetime.now()

            # --- 追加: プログレスバー＋ラベル更新 (制御タブ) ---
            self.ctrl_sys_cpu_progress['value'] = cpu_percent
            self.ctrl_sys_cpu_value_label['text'] = f"{cpu_percent:.1f}%"
            self.ctrl_sys_mem_progress['value'] = memory.percent
            self.ctrl_sys_mem_value_label['text'] = f"{memory.percent:.1f}%"
            self.ctrl_sys_disk_progress['value'] = disk.percent
            self.ctrl_sys_disk_value_label['text'] = f"{disk.percent:.1f}%"
            # --- ここまで追加 ---

            # ネットワーク情報
            network = psutil.net_io_counters()

            # プロセス情報 (GUI自身の情報)
            try:
                process = psutil.Process(os.getpid())
                process_memory = process.memory_info().rss / (1024 * 1024)  # MB
                process_cpu = process.cpu_percent()
                process_create_time = datetime.datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                 process = None
                 process_memory = "取得失敗"
                 process_cpu = "取得失敗"
                 process_create_time = "取得失敗"
                 print(f"GUIプロセス情報取得エラー: {e}")


            info = "=== システム情報 ===\n\n"
            info += f"🖥️ 基本情報:\n"
            info += f"  Python バージョン: {sys.version.split()[0]}\n"
            info += f"  OS: {os.name} ({sys.platform})\n"
            info += f"  現在時刻: {current_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

            info += f"💻 CPU情報:\n"
            info += f"  システムCPU使用率: {cpu_percent:.1f}%\n"
            info += f"  CPUコア数: {psutil.cpu_count()}\n"
            try:
                 info += f"  CPU周波数: {psutil.cpu_freq().current:.0f}MHz\n\n"
            except:
                 info += "  CPU周波数: 取得できませんでした\n\n"


            info += f"💾 メモリ情報:\n"
            info += f"  システムメモリ使用率: {memory.percent:.1f}%\n"
            info += f"  使用量: {memory.used // (1024**3):.1f}GB / {memory.total // (1024**3):.1f}GB\n"
            info += f"  空き容量: {memory.available // (1024**3):.1f}GB\n\n"

            info += f"💿 ディスク情報:\n"
            info += f"  ディスク使用率: {disk.percent:.1f}%\n"
            info += f"  使用量: {disk.used // (1024**3):.1f}GB / {disk.total // (1024**3):.1f}GB\n"
            info += f"  空き容量: {disk.free // (1024**3):.1f}GB\n\n"

            info += f"🌐 ネットワーク情報:\n"
            info += f"  送信: {network.bytes_sent // (1024**2):.1f}MB\n"
            info += f"  受信: {network.bytes_recv // (1024**2):.1f}MB\n\n"

            info += f"📊 GUIプロセス情報:\n"
            info += f"  プロセスID: {os.getpid()}\n" # GUI自身のPID
            info += f"  メモリ使用量: {process_memory:.1f}MB\n" if isinstance(process_memory, (int, float)) else f"  メモリ使用量: {process_memory}\n"
            info += f"  CPU使用率: {process_cpu:.1f}%\n" if isinstance(process_cpu, (int, float)) else f"  CPU使用率: {process_cpu}\n"
            info += f"  起動時刻: {process_create_time}\n\n"


            info += f"🔄 自動更新間隔: {self.refresh_interval_var.get()}秒\n"
            info += f"最終更新: {current_time.strftime('%H:%M:%S')}\n"

            self.system_text.delete(1.0, tk.END)
            self.system_text.insert(1.0, info)
        except Exception as e:
            self.system_text.delete(1.0, tk.END)
            self.system_text.insert(1.0, f"システム情報の取得に失敗しました: {e}")


def main():

    root = tk.Tk()
    app = FlandreBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    # psutilがインストールされているかチェック
    try:
        import psutil
    except ImportError:
        print("psutilライブラリが見つかりません。")
        print("システムリソース情報（CPU, メモリ, ディスク）を表示するには、")
        print("コマンドプロンプトで 'pip install psutil' を実行してください。")
        # psutilがない場合でもGUIは起動できるようにする

    # requestsがインストールされているかチェック
    try:
        import requests
    except ImportError:
        print("requestsライブラリが見つかりません。")
        print("Bot状態をAPIで取得するには、")
        print("コマンドプロンプトで 'pip install requests' を実行してください。")
        # requestsがない場合でもGUIは起動できるようにする

    main()