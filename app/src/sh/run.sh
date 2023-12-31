#!/bin/bash
echo "接続先: $1"
echo "実行日: $2"
echo "ログファイル名: $3"

connectInfo=$1
targetDate=$2
targetLog=$3

# シェルの実行ディレクトリ取得
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 並列実行を想定。直列実行する場合は末尾の「&」を取り除いてください。
python3 -m src.logic.create_orders ${connectInfo} ${targetDate} &
python3 -m src.logic.create_products ${connectInfo} ${targetDate} &
python3 -m src.logic.create_browsing_infos ${connectInfo} ${targetDate} ${targetLog} &

# 全ての処理の終了を待つ
wait