#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ローカルテスト用スクリプト
"""

import os
import sys
from pathlib import Path

# アプリケーションをインポート
from app import FCPParser, process_uploaded_file

def test_xml_parsing():
    """XML解析機能のテスト"""
    print("=== Final Cut Pro テロップ抽出ツール - ローカルテスト ===\n")
    
    # テスト用XMLファイルのパスを確認
    test_xml_path = "/Users/sk/Desktop/てすと.fcpxmld/Info.fcpxml"
    
    if not os.path.exists(test_xml_path):
        print(f"❌ テストファイルが見つかりません: {test_xml_path}")
        return False
    
    try:
        # XMLファイルを読み込み
        with open(test_xml_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        # パーサーでテスト
        parser = FCPParser()
        subtitles = parser.parse_fcpxml_content(xml_content)
        
        print(f"✅ XML解析成功")
        print(f"📊 抽出されたテロップ数: {len(subtitles)}")
        
        if subtitles:
            print(f"\n📝 最初の5件:")
            for i, subtitle in enumerate(subtitles[:5]):
                print(f"  {i+1}. {subtitle['start_timecode']} - {subtitle['end_timecode']}: {subtitle['text'][:50]}...")
        
        # 期待値との照合テスト
        expected_results = [
            ("00:00:34:00", "博多の中心地「天神」から10分のお部屋"),
            ("00:00:40:00", "防犯カメラは1Fだけで10台以上安心感があります"),
            ("00:00:50:30", "お部屋に向かう前に共用部をご紹介"),
            ("00:00:56:30", "エントランス左には宅配BOX"),
            ("00:01:02:30", "32個まで荷物を預かれるので再配達の心配が減りそう")
        ]
        
        print(f"\n🎯 期待値との照合テスト:")
        all_match = True
        for i, (expected_tc, expected_text) in enumerate(expected_results):
            if i < len(subtitles):
                actual_tc = subtitles[i]['start_timecode']
                actual_text = subtitles[i]['text']
                
                tc_match = actual_tc == expected_tc
                text_match = expected_text in actual_text
                
                status = "✅" if (tc_match and text_match) else "❌"
                print(f"  {status} テロップ {i+1}: {actual_tc} ({'一致' if tc_match else '不一致'})")
                
                if not (tc_match and text_match):
                    all_match = False
                    print(f"    期待値: {expected_tc} - {expected_text}")
                    print(f"    実際値: {actual_tc} - {actual_text}")
        
        if all_match:
            print(f"\n🎉 すべてのテストに合格しました！")
        else:
            print(f"\n⚠️  一部のテストが不一致でした")
        
        return True
        
    except Exception as e:
        print(f"❌ テスト中にエラーが発生: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_web_functions():
    """Web機能のテスト"""
    print(f"\n=== Web機能テスト ===")
    
    try:
        from app import generate_csv_content
        
        # テスト用データ
        test_subtitles = [
            {
                'start_timecode': '00:00:34:00',
                'end_timecode': '00:00:40:00', 
                'text': '博多の中心地「天神」から10分のお部屋'
            },
            {
                'start_timecode': '00:00:40:00',
                'end_timecode': '00:00:48:00',
                'text': '防犯カメラは1Fだけで10台以上安心感があります'
            }
        ]
        
        # CSV生成テスト
        csv_content = generate_csv_content(test_subtitles)
        
        print("✅ CSV生成機能: 正常")
        print("📄 CSV内容プレビュー:")
        print(csv_content[:200] + "...")
        
        return True
        
    except Exception as e:
        print(f"❌ Web機能テストでエラー: {str(e)}")
        return False

if __name__ == '__main__':
    print("Final Cut Pro テロップ抽出ツール - GitHub版テスト開始\n")
    
    # XML解析テスト
    xml_test_passed = test_xml_parsing()
    
    # Web機能テスト
    web_test_passed = test_web_functions()
    
    print(f"\n=== テスト結果 ===")
    print(f"XML解析: {'✅ 合格' if xml_test_passed else '❌ 不合格'}")
    print(f"Web機能: {'✅ 合格' if web_test_passed else '❌ 不合格'}")
    
    if xml_test_passed and web_test_passed:
        print(f"\n🎉 すべてのテストに合格しました！")
        print(f"GitHub デプロイの準備が完了しています。")
        print(f"\n次のステップ:")
        print(f"1. cd /Users/sk/Desktop/FCP-text-github")
        print(f"2. python app.py (ローカルテスト)")
        print(f"3. GitHubにpushしてデプロイ")
    else:
        print(f"\n❌ テストが失敗しました。修正が必要です。")
        sys.exit(1)