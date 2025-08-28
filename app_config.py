#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
アプリケーション設定ファイル
"""

import os

class Config:
    # Flask設定
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # ファイルアップロード設定
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    UPLOAD_EXTENSIONS = ['.fcpxml', '.fcpbundle', '.fcpxmld']
    
    # デバッグモード (本番環境では False に設定)
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # ポート設定 (Heroku対応)
    PORT = int(os.environ.get('PORT', 5000))