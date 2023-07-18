import sys
import os
import csv
import time
import re
from collections import defaultdict
from urllib.parse import urlparse
from ..db import ConnectDb
from ..utils import Logger
from ..utils import const

def main():
    # 初期処理
    connect_info = sys.argv[1]
    target_date = sys.argv[2]
    target_log = sys.argv[3]
    start_time = time.time()

    # 取得対象情報
    process_name = '閲覧情報出力処理'
    sql_file = f'{const.SQL_FILE_DIR}/get_browsing_infos.sql'
    output_file = f'{const.CSV_OUTPUT_DIR}/output_browsing_infos_{target_date}.csv'
    log_file = f'{const.LOG_OUTPUT_DIR}/output_browsing_infos_{target_date}.log'
    output_dir = os.path.dirname(output_file)
    log_dir = os.path.dirname(log_file)

    # ディレクトリが存在しなければ作成する
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 処理開始
    logger = Logger(__name__, log_file)
    logger.info(f'{process_name} 開始 接続先：「{connect_info}」 対象日：「{target_date}」')

    # DB接続
    db = ConnectDb(connect_info)
    try:
        db.connect()
    except Exception as e:
        logger.error(f'データベースの接続に失敗しました。: {e}')
        return

    # SQL実行して閲覧情報テーブルのデータ取得
    browsing_info_dict = {}
    try:
        with open(sql_file, 'r') as file:
            query = file.read()
        
        results = db.query(query)

        # 取得した情報をキー:URL、値:情報詳細の辞書に変換
        for result in results:
            browsing_info_dict[result[0]] = result[1:]
    except Exception as e:
        logger.error(f'閲覧情報テーブルのデータ取得に失敗しました。: {e}')
        return
    finally:
        db.close()
    
    # ログファイルの解析
    log_data = {}
    try:
        # browsing_info_dictのキーをリストに変換
        url_list = list(browsing_info_dict.keys())
        log_data = parse_log_file(target_log, url_list)
    except Exception as e:
        logger.error(f'ログファイルの解析に失敗しました。: {e}')
        return

    # ファイル出力
    try:
        num_results = len(log_data)

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(log_data)

        # 処理終了時間を取得し、処理時間を計算
        end_time = time.time()
        elapsed_time = end_time - start_time

        logger.info(f'{process_name} 正常終了  ファイル出力件数：{num_results}件 計算時間：{elapsed_time:.3f}秒', )
    except Exception as e:
        logger.error(f'{process_name} 異常終了  エラー情報: {e}', )

def parse_log_file(log_file_path, url_list):
    """ログファイルをパースして、IPアドレス、アクセス日時、アクセスURLの組み合わせごとのアクセス回数を集計する
    
    Args:
        log_file_path (str): ログファイルのパス
        url_list (list): 閲覧情報テーブルのURLリスト
    
    Returns:
        dict: IPアドレス、アクセス日時、アクセスURLの組み合わせごとのアクセス回数
    """
    
    # ログファイルのパースに使用する正規表現
    pattern = re.compile(
        r"(?P<ip>\d+\.\d+\.\d+\.\d+)"  # IPアドレス
        r".*?"  # （不要な部分をスキップ）
        r"\[(?P<datetime>.+?)\]"  # アクセス日時
        r".*?"  # （不要な部分をスキップ）
        r"\"GET (?P<url>.*?) "  # アクセスURL
    )

    data = defaultdict(int)
    with open(log_file_path, "r") as file:
        for line in file:
            match = pattern.match(line)
            if match is not None:
                # urlからurlparseを使用してパスの最後の部分を取得
                url_path = urlparse(match.group("url")).path.split('/')[-1]
                # url_pathがurl_listに含まれている場合のみ集計対象とする
                if url_path in url_list:
                    data[match.group("ip"), match.group("datetime"), match.group("url")] += 1

    return data

if __name__ == "__main__":
    main()
