import json
from flask import Flask, jsonify, request, abort, make_response, current_app
from flask import jsonify, request, Flask
from flask_jwt_extended import jwt_required, create_access_token, JWTManager, get_jwt_identity
from flask_cors import CORS
from pymongo import MongoClient
from os.path import join, dirname
from urllib.parse import quote_plus
from datetime import timedelta
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

# Flask
app = Flask(__name__)
app.url_map.strict_slashes = False

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

# JWT の認証エラーハンドラ
@log(logger)
def jwt_unauthorized_loader_handler(reason):
    logger.error(f"{reason}")
    return make_response(jsonify({'error': 'Unauthorized'}), 401)

# JWT
jwt = JWTManager(app)
jwt.unauthorized_loader(jwt_unauthorized_loader_handler)

# レスポンスにCORS許可のヘッダーを付与
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

# ログインしてトークンを返却
@log(logger)
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        abort(400)

    request_body = request.get_json()
    if request_body is None:
        abort(400)

    whitelist = {'username', 'password'}
    if not request_body.keys() <= whitelist:
        abort(400)

    u = request_body['username']
    p = request_body['password']

    user = User.from_doc(db.users.find_one({"username": request_body['username']}))
    authenticated = True if user is not None and user.password == request_body['password'] else False
    auth_user = user if authenticated else None

    if auth_user is None:
        abort(401)

    access_token = create_access_token(identity=auth_user.username)
    response_body = {'access_token': access_token}
    return make_response(jsonify(response_body), 200)

# ホロジュール配信予定を取得
@log(logger)
@app.route('/holodules/<string:date>', methods=['GET'])
@jwt_required()
def holodules(date):
    identity = get_jwt_identity()
    if identity == None:
        abort(500)

    if len(date) != 8:
        abort(500)

    logger.info(f"username: {identity} date: {date}")

    # MongoDB から年月日を条件にホロジュール配信予定を取得してリストに格納
    holodule_list = []
    for holodule in db.holodules.find({"datetime": {'$regex':'^'+date}}).sort("datetime", -1):
        holodule_list.append(Holodule.from_doc(holodule))

    # オブジェクトリストをJSON配列に変換
    holodules = []
    for holodule in holodule_list:
        holodules.append(holodule.to_doc())

    # UTF-8コードの application/json として返却
    return make_response(jsonify(holodules), 200)

# エラーハンドラ：400
@log(logger)
@app.errorhandler(400)
def bad_request(error):
    logger.error(f"{error}")
    return make_response(jsonify({'error': 'Bad request'}), 400)

# エラーハンドラ：401
@log(logger)
@app.errorhandler(401)
def Unauthorized(error):
    logger.error(f"{error}")
    return make_response(jsonify({'error': 'Unauthorized'}), 401)

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
