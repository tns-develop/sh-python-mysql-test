#!/bin/bash
echo "接続先: $1"
echo "実行日: $2"

connectInfo=$1
targetDate=$2

# シェルの実行ディレクトリ取得
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 並列実行を想定。直列実行する場合は末尾の「&」を取り除いてください。
# python3 -m ${dir}/../logic/create_orders.py ${connectInfo} ${connectInfo} &
# python3 ../logic/create_products.py ${connectInfo} ${connectInfo} &
python3 -m src.logic.create_orders ${connectInfo} ${targetDate} &
python3 -m src.logic.create_products ${connectInfo} ${targetDate} &

# 全ての処理の終了を待つ
wait