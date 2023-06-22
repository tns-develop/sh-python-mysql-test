import sys
import os
import csv
from ..db import ConnectDb  # 先程定義したDatabaseクラスをインポート
from ..utils import Logger  # 先程定義したLoggerクラスをインポート
from ..utils import const

def main():
    # 初期処理
    connect_info = sys.argv[1]
    target_date = sys.argv[2]
    process_name = '注文情報出力処理'
    sql_file = f'{const.SQL_FILE_DIR}/getOrders.sql'
    output_file = f'{const.CSV_OUTPUT_DIR}/outputOrders_{target_date}.csv'
    output_dir = os.path.dirname(output_file)
    log_file = f'{const.LOG_OUTPUT_DIR}/outputOrders_{target_date}.log'

    # ディレクトリが存在しなければ作成する
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 処理開始
    logger = Logger(__name__, log_file)
    logger.info(f'{process_name} 開始 接続先=「{connect_info}」 対象日：「{target_date}」')

    # DB接続
    db = ConnectDb(connect_info)
    try:
        db.connect()
    except Exception as e:
        logger.error(f'データベースの接続に失敗しました。: {e}')
        return

    # SQL実行してファイル出力
    try:
        with open(sql_file, 'r') as file:
            query = file.read().replace('{target_date}', target_date)

        results = db.query(query)
        num_results = len(results)

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(results)

        logger.info(f'{process_name} 正常終了  ファイル出力件数={num_results}件', )
    except Exception as e:
        logger.error(f'{process_name} 異常終了  エラー情報: {e}', )
    finally:
        db.close()

if __name__ == "__main__":
    main()
