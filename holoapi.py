from flask import Flask, jsonify, request, abort, make_response
from os.path import join, dirname
from pymongo import MongoClient
import json
from urllib.parse import quote_plus
from app.settings import Settings
from app.holodule import Holodule

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
api = Flask(__name__)
# JSONのソートを抑止
api.config['JSON_SORT_KEYS'] = False

# ホロジュール配信予定の取得
@api.route('/Holodules/<string:date>', methods=['GET'])
def get_Holodules(date):
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
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# エラーハンドラ：500
@api.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

if __name__ == "__main__":
    api.run(port=8888)
