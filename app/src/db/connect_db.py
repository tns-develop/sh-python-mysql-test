from ..utils import const
import mysql.connector

class ConnectDb:
  def __init__(self, connect_info, user=const.DB_USER, password=const.DB_PASSWORD, database=const.CONNECT_DB):
      # "host:port"形式と仮定
      host, port = connect_info.split(':')

      self._host = host
      self._port = port
      self._user = user
      self._password = password
      self._database = database
      self._connection = None

  def connect(self):
      self._connection = mysql.connector.connect(
          host=self._host,
          user=self._user,
          password=self._password,
          database=self._database
      )

  def query(self, sql, params=None):
      cursor = self._connection.cursor()
      cursor.execute(sql, params)
      result = cursor.fetchall()
      return result

  def close(self):
      if self._connection:
          self._connection.close()

  def __del__(self):
    if self._connection:
      self._connection.close()
