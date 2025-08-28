#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gunicorn設定ファイル (本番環境用)
"""

import os

# バインドアドレス
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"

# ワーカー数
workers = int(os.environ.get('WEB_CONCURRENCY', 1))

# ワーカークラス
worker_class = 'sync'

# タイムアウト
timeout = 120

# Keep-alive
keepalive = 5

# 最大リクエストサイズ (100MB)
max_request_size = 104857600

# ログレベル
loglevel = 'info'

# アクセスログ
accesslog = '-'

# エラーログ
errorlog = '-'

# プリロード
preload_app = True