import os
import urllib.request
from dotenv import load_dotenv

class Settings:
    def __init__(self, envpath):
        # .env ファイルを明示的に指定して環境変数として読み込む
        self.__dotenv_path = envpath
        load_dotenv(self.__dotenv_path)
        # 環境変数から設定値を取得
        self.__mongodb_user = os.environ.get("MONGODB_USER")
        self.__mongodb_password = os.environ.get("MONGODB_PASSWORD")
        self.__mongodb_host = os.environ.get("MONGODB_HOST")

    # mongodb の ユーザー
    @property
    def mongodb_user(self):
        return self.__mongodb_user

    # mongodb の パスワード
    @property
    def mongodb_password(self):
        return self.__mongodb_password

    # mongodb の ホスト:ポート
    @property
    def mongodb_host(self):
        return self.__mongodb_host

    # 指定したURLにアクセスできるかをチェック
    def __check_url(self, url):
        try:
            with urllib.request.urlopen(url):
                return True
        except urllib.request.HTTPError:
            return False