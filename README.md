# Final Cut Pro テロップ抽出ツール - Web版

Final Cut Pro プロジェクトファイル（.fcpxml、.fcpbundle、.fcpxmld）からテロップ情報を抽出してCSVファイルで出力するWebアプリケーションです。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 主な機能

- **正確なタイムコード抽出**: Final Cut Pro の60fpsタイムコードに完全対応
- **複数形式対応**: .fcpxml、.fcpbundle、.fcpxmld ファイルをサポート
- **Webインターフェース**: ドラッグ&ドロップでファイルアップロード
- **CSV出力**: Excel対応のUTF-8 BOM付きCSV形式で出力
- **リアルタイムプレビュー**: 抽出結果をその場で確認

## 📋 対応形式

| 形式 | 説明 |
|------|------|
| `.fcpxml` | Final Cut Pro XML単体ファイル |
| `.fcpbundle` | Final Cut Pro バンドルプロジェクト |
| `.fcpxmld` | Final Cut Pro XMLディレクトリ |

## 🚀 クイックスタート

### 必要環境

- Python 3.8 以上
- Flask 3.0.0 以上

### インストール

1. リポジトリをクローン
```bash
git clone https://github.com/your-username/fcp-text-github.git
cd fcp-text-github
```

2. 依存関係をインストール
```bash
pip install -r requirements.txt
```

3. アプリケーションを起動
```bash
python app.py
```

4. ブラウザで http://localhost:5000 を開く

## 📱 使用方法

1. **ファイル選択**: Final Cut Pro プロジェクトファイルをドラッグ&ドロップまたはクリックで選択
2. **自動処理**: アップロードされたファイルが自動的に解析されます
3. **結果確認**: 抽出されたテロップの一覧を確認
4. **CSV出力**: 「CSVファイルをダウンロード」ボタンでファイルをダウンロード

## 🎬 出力形式

CSVファイルは以下の形式で出力されます：

| 開始タイムコード | 終了タイムコード | テロップ内容 |
|------------------|------------------|--------------|
| 00:00:34:00 | 00:00:40:00 | 博多の中心地「天神」から10分のお部屋 |
| 00:00:40:00 | 00:00:48:00 | 防犯カメラは1Fだけで10台以上安心感があります |
| 00:00:50:30 | 00:00:56:30 | お部屋に向かう前に共用部をご紹介 |

## ⚙️ API エンドポイント

### POST /upload
ファイルアップロード処理

**パラメータ:**
- `file`: Final Cut Pro プロジェクトファイル

**レスポンス:**
```json
{
  "success": true,
  "count": 143,
  "subtitles": [
    {
      "start_timecode": "00:00:34:00",
      "end_timecode": "00:00:40:00", 
      "text": "博多の中心地「天神」から10分のお部屋"
    }
  ]
}
```

### POST /download
CSVファイルダウンロード

**パラメータ:**
```json
{
  "subtitles": [...]
}
```

## 🔧 技術仕様

### タイムコード計算

Final Cut Pro の複雑なタイムライン構造を正確に解析：

```python
timeline_position = asset_clip_offset + (title_offset - asset_clip_start)
```

### 60fps タイムコード対応

Final Cut Pro 標準の60fpsタイムコードに対応：

```python
frames = int((seconds % 1) * 60)  # 60fps
timecode = f"{hours:02d}:{minutes:02d}:{secs:02d}:{frames:02d}"
```

## 📂 プロジェクト構成

```
fcp-text-github/
├── app.py              # メインアプリケーション
├── templates/
│   └── index.html      # Webインターフェース
├── requirements.txt    # Python依存関係
├── README.md          # このファイル
├── .gitignore         # Git無視ファイル
└── runtime.txt        # Python バージョン指定
```

## 🐛 トラブルシューティング

### よくある問題

**Q: ファイルアップロードでエラーが発生する**
- A: ファイルサイズが100MBを超えていないか確認してください

**Q: テロップが抽出されない**
- A: Final Cut Pro プロジェクト内にtitle要素が含まれているか確認してください

**Q: タイムコードがずれている**
- A: プロジェクトのフレームレート設定を確認してください（60fps推奨）

## 🤝 貢献

プルリクエストやIssueでの貢献を歓迎します。

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🙏 謝辞

- Final Cut Pro XML形式の解析技術
- Flask Webフレームワーク
- Bootstrap UI コンポーネント

---

**作成者**: Claude Code  
**最終更新**: 2025年8月28日