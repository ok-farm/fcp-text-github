# デプロイ手順

このアプリケーションは複数のクラウドプラットフォームでデプロイできるよう設定されています。

## 🚀 推奨デプロイ方法

### 1. Railway (推奨)

1. [Railway.app](https://railway.app/) にアクセス
2. GitHubアカウントでログイン
3. "New Project" → "Deploy from GitHub repo"
4. `fcp-text-github` リポジトリを選択
5. 自動でビルドとデプロイが開始されます

**料金**: 月500時間まで無料

### 2. Render (推奨)

1. [Render.com](https://render.com/) にアクセス
2. GitHubアカウントでログイン
3. "New" → "Web Service"
4. リポジトリを接続: `https://github.com/ok-farm/fcp-text-github`
5. 設定:
   - **Name**: `fcp-text-github`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --config gunicorn.conf.py app:app`
6. "Create Web Service" をクリック

**料金**: 無料プランあり（月750時間）

### 3. Vercel

1. [Vercel.com](https://vercel.com/) にアクセス
2. GitHubアカウントでログイン
3. "Import Project" 
4. リポジトリURL: `https://github.com/ok-farm/fcp-text-github`
5. Framework Preset: "Other"
6. Deploy

**料金**: 個人利用無料

### 4. Heroku

```bash
# Heroku CLI使用
heroku create your-app-name
git push heroku main
```

**料金**: 有料のみ（月$7〜）

### 5. DigitalOcean App Platform

1. [DigitalOcean](https://www.digitalocean.com/) にアクセス
2. "Create" → "Apps"
3. GitHubリポジトリを接続
4. 自動検出された設定を確認してデプロイ

## ⚙️ 環境変数設定

デプロイ時に以下の環境変数を設定（オプション）:

- `FLASK_ENV`: `production` (本番環境)
- `SECRET_KEY`: ランダムな文字列
- `WEB_CONCURRENCY`: `1` (ワーカー数)

## 🔍 デプロイ後の確認

デプロイ完了後、以下をテスト:

1. ✅ ホームページが表示される
2. ✅ ファイルアップロード機能が動作する  
3. ✅ CSVダウンロードが正常に動作する

## 🐛 トラブルシューティング

### よくある問題

**Q: ファイルアップロードが失敗する**
- A: プラットフォームのファイルサイズ制限を確認（通常10-100MB）

**Q: タイムアウトエラーが発生**
- A: 大きなファイルの場合、処理に時間がかかります

**Q: メモリエラー**  
- A: 無料プランのメモリ制限（512MB程度）を超えている可能性

## 🔗 デプロイされたアプリの例

デプロイが完了すると以下のようなURLでアクセスできます:

- Railway: `https://your-app.railway.app`
- Render: `https://your-app.onrender.com`  
- Vercel: `https://your-app.vercel.app`

---

**注意**: 無料プランでは制限があります（CPU時間、メモリ、ストレージなど）