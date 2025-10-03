# Python 3.11ベースイメージを使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新とPoetryのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN pip install poetry

# Poetryの設定（仮想環境をコンテナ内に作らない）
RUN poetry config virtualenvs.create false

# 依存関係ファイルをコピー
COPY pyproject.toml /app/

# 依存関係をインストール（エラー時でも継続するよう変更）
RUN poetry install --no-root --only main || \
    poetry install --no-root --without dev || \
    pip install fastapi uvicorn sqlalchemy asyncpg alembic python-jose passlib python-multipart pydantic pydantic-settings python-dotenv jinja2

# アプリケーションのソースコードをコピー
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/

# ポート8000を公開
EXPOSE 8000

# アプリケーション起動コマンド
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]