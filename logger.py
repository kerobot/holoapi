"""
ログ出力の設定とロガーインスタンスの生成
"""

import json
import datetime
import inspect
from os.path import join
from functools import wraps
from logging import config, getLogger, Filter

class CustomFilter(Filter):
    def filter(self, record):
        record.real_filename = getattr(record, 'real_filename', record.filename)
        record.real_funcName = getattr(record, 'real_funcName', record.funcName)
        record.real_lineno = getattr(record, 'real_lineno', record.lineno)
        return True

def get_logger(log_dir, json_path, verbose):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            log_config = json.load(f)
    except FileNotFoundError:
        print(f"設定ファイル {json_path} が見つかりません。")
        return None
    except json.JSONDecodeError:
        print(f"設定ファイル {json_path} の形式が正しくありません。")
        return None

    # ログファイル名を日付とする
    log_path = join(log_dir, f"{datetime.datetime.now().strftime('%Y%m%d')}.log")
    log_config["handlers"]["rotateFileHandler"]["filename"] = log_path

    # verbose引数が True の場合、レベルをINFOからDEBUGに置換
    if verbose:
        log_config["root"]["level"] = "DEBUG"
        log_config["handlers"]["consoleHandler"]["level"] = "DEBUG"
        log_config["handlers"]["rotateFileHandler"]["level"] = "DEBUG"

    try:
        # ロギングの設定を適用
        config.dictConfig(log_config)
    except ValueError as e:
        print(f"ログ設定の適用に失敗しました：{e}")
        return None

    # ロガーを取得
    logger = getLogger(__name__)
    logger.addFilter(CustomFilter())
    return logger

def log(logger):
    def _decorator(func):
        # funcのメタデータを引き継ぐ
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            extra = {
                'real_filename': inspect.getfile(func),
                'real_funcName': func_name,
                'real_lineno': inspect.currentframe().f_back.f_lineno
            }
            # funcの開始
            logger.info(f'[START] {func_name}', extra=extra)
            try:
                # funcの実行
                return func(*args, **kwargs)
            except Exception as err:
                # funcのエラーハンドリング
                logger.error(err, exc_info=True, extra=extra)
            finally:
                # funcの終了
                logger.info(f'[END] {func_name}', extra=extra)
        return wrapper
    return _decorator
