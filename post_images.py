import os
from os.path import join, dirname  # ファイルのパスを取得するために使用
from dotenv import load_dotenv  # 環境変数の読み込みに使用

# .envファイルのパスを指定
dotenv_path = join(dirname(__file__), '.env')
# .envファイルの内容を読み込む
load_dotenv(dotenv_path)

BOT_TOKEN =os.environ.get("TOKEN")



