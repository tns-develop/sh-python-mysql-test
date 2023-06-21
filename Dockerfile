# Ubuntu 20.04をベースイメージとして使用
FROM ubuntu:20.04

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Pythonのライブラリをアップグレード
RUN python3 -m pip install --upgrade pip

# アプリケーションディレクトリを作成
WORKDIR /app

# 必要なPythonのライブラリをrequirements.txtからインストール
COPY app/requirements.txt /app/
RUN python3 -m pip install -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . /app/
