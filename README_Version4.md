# シンプルガチャBot（Koyeb/Discloud用）

- main.py：Bot本体（コマンドは/ガチャ, /残高）
- requirements.txt：discord.pyのみ
- free_gacha_animation.gif：ガチャ演出画像（ダミー。ご自身で差し替え）

## Koyeb設定
1. ファイルをGitHubリポジトリにアップロード
2. Koyebでサービス作成、スタートコマンド`python main.py`
3. 環境変数`DISCORD_BOT_TOKEN`を設定

## 注意
- SQLite(DB)は一時保存。永続化必要なら外部DB推奨