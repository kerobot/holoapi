from flask import Flask, jsonify, request, abort, make_response
from pymongo import MongoClient
from os.path import join, dirname
import json
from urllib.parse import quote_plus
from models.holodule import Holodule
from settings import Settings
from logger import log, get_logger

# ロギングの設定
json_path = join(dirname(__file__), "config/logger.json")
log_dir = join(dirname(__file__), "log")
logger = get_logger(log_dir, json_path, False)

# Settings インスタンス
settings = Settings(join(dirname(__file__), '.env'))

# MongoDB 接続情報
mongodb_user = quote_plus(settings.mongodb_user)
mongodb_password = quote_plus(settings.mongodb_password)
mongodb_host = "mongodb://%s/" % (settings.mongodb_host)

# MongoDB 接続認証
client = MongoClient(mongodb_host)
db = client.holoduledb
db.authenticate(name=mongodb_user,password=mongodb_password)

# Flask
app = Flask(__name__)
# JSONのソートを抑止
app.config['JSON_SORT_KEYS'] = False

@log(logger)
@app.route('/')
def index():
    logger.info(f"holoapi")
    return 'holoapi'

# ホロジュール配信予定の取得
@log(logger)
@app.route('/Holodules/<string:date>', methods=['GET'])
def get_Holodules(date):
    logger.info(f"Holodules/{date}")
    if len(date) != 8:
        abort(500)

    # MongoDB から年月日を条件にホロジュール配信予定を取得してリストに格納
    holodule_list = []
    for doc in db.holodules.find({"datetime": {'$regex':'^'+date}}).sort("datetime", -1):
        holodule = Holodule.from_doc(doc)
        holodule_list.append(holodule)

    if len(holodule_list) == 0:
        abort(404)

    # オブジェクトをもとに辞書を構築してJSONとして返却
    data = {}
    for holodule in holodule_list:
        doc = holodule.to_doc()
        data[doc['key']] = doc
    result = {
        "result":len(holodule_list),
        "data":data
    }
    # UTF-8コード、Content-Type は application/json
    return make_response(jsonify(result))
    # UTF-8文字、Content-Type は text/html; charset=utf-8
    # return make_response(json.dumps(result, ensure_ascii=False))

# エラーハンドラ：404
@log(logger)
@app.errorhandler(404)
def not_found(error):
    logger.error(f"{error}")
    return make_response(jsonify({'error': 'Not found'}), 404)

# エラーハンドラ：500
@log(logger)
@app.errorhandler(500)
def internal_server_error(error):
    logger.error(f"{error}")
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

if __name__ == "__main__":
    app.run()
