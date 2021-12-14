import json
from flask import Flask, jsonify, request, abort, make_response, current_app
from flask_jwt import jwt_required, current_identity, JWT
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from os.path import join, dirname
from urllib.parse import quote_plus
from datetime import timedelta, datetime
from models.holodule import Holodule
from models.user import User
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

# ユーザー名とパスワードを用いて認証情報を検証するコールバック関数
def authoricate(username, password):
    user = User.from_doc(db.users.find_one({"username": username}))
    authenticated = True if user is not None and user.password == password else False
    return user if authenticated else None

# JWTペイロードをもとにユーザー情報を取得するコールバック関数
def identity(payload):
    # @jwt.jwt_payload_handler でJWTペイロードをカスタマイズし、identity をユーザー名にしている
    username = payload['identity']
    user = User.from_doc(db.users.find_one({"username": username}))
    return user

# Flask
app = Flask(__name__)
# CORS
CORS(app)
# JSONのソートを抑止
app.config['JSON_SORT_KEYS'] = False
# Flask JWT
app.config['JWT_SECRET_KEY'] = settings.jwt_secret_key      # JWTに署名する際の秘密鍵
app.config['JWT_ALGORITHM'] = 'HS256'                       # 暗号化署名のアルゴリズム
app.config['JWT_LEEWAY'] = 0                                # 有効期限に対する余裕時間
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=300) # トークンの有効期間
app.config['JWT_NOT_BEFORE_DELTA'] = timedelta(seconds=0)   # トークンの使用を開始する相対時間
app.config['JWT_AUTH_URL_RULE'] = '/auth'                   # 認証エンドポイントURL
jwt = JWT(app, authoricate, identity)                       # ここで上記2つの関数を指定

# レスポンスにCORS許可のヘッダーを付与
@app.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# JWTペイロードのカスタマイズ
@jwt.jwt_payload_handler
def make_payload(identity):
    iat = datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA') 
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
    identity = getattr(identity, 'username')
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}

# ホロジュール配信予定の取得
@log(logger)
@app.route('/holodules/<string:date>', methods=['GET'])
@jwt_required()
def get_Holodules(date):
    logger.info(f"{getattr(current_identity, 'username')}")
    logger.info(f"holodules/{date}")
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
    holodules = []
    for holodule in holodule_list:
        doc = holodule.to_doc()
        holodules.append(doc)
    result = {
        "result":len(holodule_list),
        "holodules":holodules
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
