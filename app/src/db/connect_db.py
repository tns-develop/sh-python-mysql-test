from ..utils import const
import mysql.connector

class ConnectDb:
    """DB接続クラス
    """

    def __init__(self, connect_info, user=const.DB_USER, password=const.DB_PASSWORD, database=const.CONNECT_DB):
        """接続先の情報を保持

        Args:
            connect_info (str): 接続先情報
            user (str, optional): DBユーザー. Defaults to const.DB_USER.
            password (str, optional): DBパスワード. Defaults to const.DB_PASSWORD.
            database (str, optional): DB名. Defaults to const.CONNECT_DB.
        """
        # "host:port"形式と仮定
        host, port = connect_info.split(':')

        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database
        self._connection = None

    def connect(self):
        """DB接続
        """
        # mysqlのDBに接続
        self._connection = mysql.connector.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database,
        )

    def query(self, sql, params=None):
        """SQLを実行して結果を返す
        """
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchall()
        return result

    def close(self):
        """DB接続を閉じる
        """
        if self._connection:
            self._connection.close()

    def __del__(self):
        """デストラクタ
        """
        if self._connection:
            self._connection.close()
