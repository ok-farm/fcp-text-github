#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Cut Pro テロップ抽出ツール - Web版
GitHub Pages/Webアプリケーション対応
"""

import os
import csv
import xml.etree.ElementTree as ET
import tempfile
import zipfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

class FCPParser:
    """Final Cut Pro XML解析クラス - Web版"""
    
    def __init__(self):
        self.subtitles = []
    
    def parse_fcpxml_content(self, xml_content):
        """
        XMLコンテンツを解析してテロップ情報を抽出
        """
        try:
            root = ET.fromstring(xml_content)
            self.subtitles = []
            
            print(f"XML解析開始 - ルート要素: {root.tag}")
            
            # タイムライン上の要素を順次処理
            title_data = []
            
            for project in root.iter('project'):
                for sequence in project.iter('sequence'):
                    for spine in sequence.iter('spine'):
                        for element in spine:
                            if element.tag == 'asset-clip':
                                # asset-clipの位置情報を取得
                                clip_offset = element.get('offset', '0s')
                                clip_start = element.get('start', '0s')
                                
                                clip_offset_seconds = self.convert_time_to_seconds(clip_offset)
                                clip_start_seconds = self.convert_time_to_seconds(clip_start)
                                
                                # このasset-clip内のtitle要素を処理
                                for title in element.iter('title'):
                                    title_offset = title.get('offset', '0s')
                                    title_offset_seconds = self.convert_time_to_seconds(title_offset)
                                    
                                    # 正しいタイムライン位置の計算
                                    timeline_position = clip_offset_seconds + (title_offset_seconds - clip_start_seconds)
                                    title_data.append((timeline_position, title))
            
            # タイムライン位置でソート
            title_data.sort(key=lambda x: x[0])
            
            print(f"プロジェクト内で {len(title_data)} 個のtitle要素を発見（タイムラインソート済み）")
            
            # 最初のテロップを基準点として使用
            if title_data:
                first_position = title_data[0][0]
                print(f"最初のテロップのタイムライン位置: {first_position:.2f}秒")
                
                for i, (timeline_position, title) in enumerate(title_data):
                    # 最初のテロップを0秒開始にするための調整
                    adjusted_position = timeline_position - first_position
                    subtitle_info = self.extract_title_with_position(title, adjusted_position)
                    if subtitle_info:
                        self.subtitles.append(subtitle_info)
                        print(f"テロップ {i+1}: {subtitle_info['text'][:30]} ({subtitle_info['start_timecode']} - {subtitle_info['end_timecode']}) [adjusted: {adjusted_position:.2f}s]")
            
            print(f"最終的に {len(self.subtitles)} 個のテロップを抽出")
            return self.subtitles
            
        except Exception as e:
            raise Exception(f"XML解析エラー: {str(e)}")
    
    def extract_title_with_position(self, title_element, start_seconds):
        """
        指定された開始位置でテロップ情報を抽出（正確な継続時間付き）
        """
        try:
            # テキスト内容を取得
            text_content = ""
            
            # text要素内のtext-style要素からテキストを抽出
            for text_elem in title_element.iter('text'):
                for text_style in text_elem.iter('text-style'):
                    if text_style.text and text_style.text.strip():
                        text_content += text_style.text.strip()
            
            if text_content.strip():
                # 実際の継続時間を取得
                duration_str = title_element.get('duration', '7s')
                duration_seconds = self.convert_time_to_seconds(duration_str)
                
                end_seconds = start_seconds + duration_seconds
                
                start_tc = self.convert_seconds_to_timecode(start_seconds)
                end_tc = self.convert_seconds_to_timecode(end_seconds)
                
                return {
                    'start_timecode': start_tc,
                    'end_timecode': end_tc,
                    'text': text_content.strip()
                }
            
        except Exception as e:
            print(f"位置指定抽出エラー: {e}")
        
        return None
    
    def convert_time_to_seconds(self, time_str):
        """
        FCP時間形式を秒数に変換
        """
        try:
            if time_str.endswith('s'):
                time_value = time_str[:-1]
                
                if '/' in time_value:
                    numerator, denominator = time_value.split('/')
                    return float(numerator) / float(denominator)
                else:
                    return float(time_value)
        except:
            return 0.0
        return 0.0
    
    def convert_seconds_to_timecode(self, seconds):
        """
        秒数をタイムコードに変換 - Final Cut Pro 60fps対応
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        frames = int((seconds % 1) * 60)  # 60fps（Final Cut Pro標準）
        return f"{hours:02d}:{minutes:02d}:{secs:02d}:{frames:02d}"


def process_uploaded_file(file):
    """
    アップロードされたファイルを処理
    """
    try:
        parser = FCPParser()
        
        # ファイル拡張子をチェック
        filename = secure_filename(file.filename)
        
        if filename.endswith('.fcpxml'):
            # 単体XMLファイルの場合
            xml_content = file.read().decode('utf-8')
            return parser.parse_fcpxml_content(xml_content)
        
        elif filename.endswith(('.fcpbundle', '.fcpxmld')):
            # ZIPとして扱われたバンドルファイルの場合
            with tempfile.TemporaryDirectory() as temp_dir:
                # ZIPファイルとして展開を試行
                try:
                    with zipfile.ZipFile(file, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                    
                    # Info.fcpxml または *.fcpxml ファイルを探す
                    temp_path = Path(temp_dir)
                    xml_file = None
                    
                    # Info.fcpxml を優先して検索
                    info_xml = temp_path / 'Info.fcpxml'
                    if info_xml.exists():
                        xml_file = info_xml
                    else:
                        # 他の.fcpxmlファイルを検索
                        for xml_path in temp_path.rglob("*.fcpxml"):
                            xml_file = xml_path
                            break
                    
                    if xml_file:
                        xml_content = xml_file.read_text(encoding='utf-8')
                        return parser.parse_fcpxml_content(xml_content)
                    else:
                        raise FileNotFoundError("バンドル内にFCPXMLファイルが見つかりません")
                
                except zipfile.BadZipFile:
                    raise ValueError("不正なファイル形式です")
        
        else:
            raise ValueError("サポートされていないファイル形式です。.fcpxml、.fcpbundle、または.fcpxmldファイルをアップロードしてください")
    
    except Exception as e:
        raise Exception(f"ファイル処理エラー: {str(e)}")


def generate_csv_content(subtitles):
    """
    テロップデータからCSVコンテンツを生成
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # ヘッダー書き込み
    writer.writerow(['開始タイムコード', '終了タイムコード', 'テロップ内容'])
    
    # データ書き込み
    for subtitle in subtitles:
        writer.writerow([
            subtitle['start_timecode'],
            subtitle['end_timecode'], 
            subtitle['text']
        ])
    
    return output.getvalue()


@app.route('/')
def index():
    """
    メインページ
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    ファイルアップロード処理
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        # ファイル処理
        subtitles = process_uploaded_file(file)
        
        if not subtitles:
            return jsonify({'error': 'テロップが見つかりませんでした'}), 400
        
        return jsonify({
            'success': True,
            'count': len(subtitles),
            'subtitles': subtitles
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_csv():
    """
    CSVファイルダウンロード
    """
    try:
        subtitles = request.json.get('subtitles', [])
        
        if not subtitles:
            return jsonify({'error': 'ダウンロードするデータがありません'}), 400
        
        # CSV内容生成
        csv_content = generate_csv_content(subtitles)
        
        # BytesIOオブジェクトを作成してUTF-8 BOMを追加
        csv_bytes = io.BytesIO()
        csv_bytes.write('\ufeff'.encode('utf-8'))  # BOM
        csv_bytes.write(csv_content.encode('utf-8'))
        csv_bytes.seek(0)
        
        return send_file(
            csv_bytes,
            mimetype='text/csv',
            as_attachment=True,
            download_name='subtitles.csv'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)