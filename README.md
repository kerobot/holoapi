# ホロAPI

MongoDB へ登録したホロジュールのホロライブスケジュールと Youtube の動画情報を取得します。

## 環境

* Windows 10 Pro 1909 x64
* Python 3.8.5 x64
* PowerShell 7.1 x64
* Visual Studio Code 1.51.1 x64
* Git for Windows 2.27.0 x64
* MongoDB 4.4.1 x64

## Poetry と pyenv の確認

```powershell
> poetry --version
Poetry version 1.1.0

> pyenv --version
pyenv 2.64.2
```

## MongoDB の確認

```powershell
> mongo --version
MongoDB shell version v4.4.1
```

## Python 環境設定

```powershell
> pyenv versions
> pyenv install 3.8.5
> pyenv local 3.8.5
```

## パッケージのインストール

```powershell
> poetry install
```

## .env の作成

* .envファイルを作成する
* .env.sampleを参考にURLやAPIキーを設定する

## lounch.json の作成

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}
```

## MongoDB

```powershell
> mongo localhost:27017/admin -u admin -p
> use holoduledb
switched to db holoduledb
> show collections
holodules
> db.createCollection("users");
{ "ok" : 1 }
> db.users.save( {"id":"1", "username":"user01", "password":"dummy", "firstname": "taro", "lastname": "tokyo"} );
WriteResult({ "nInserted" : 1 })
> db.users.find();
{ "_id" : ObjectId("5fe1aca6d53eaa62c5f8c75b"), "id" : "1", "username" : "user01", "password" : "dummy", "firstname" : "taro", "lastname" : "tokyo" }
```

## プログラムの実行

```powershell
> poetry run python app.py
```

## JWTトークンの取得

```powershell
> curl "http://127.0.0.1:5000/auth" -X POST -H "Content-Type: application/json" -d '"{ \"username\": \"user01\", \"password\": \"dummy\" }"'
```

## データの取得

```powershell
> curl "http://localhost:5000/holodules/20201209" -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzcwMzcyMzYsImlhdCI6MTYzNzAzNjkzNiwibmJmIjoxNjM3MDM2OTM2LCJpZGVudGl0eSI6InVzZXIwMSJ9.H7u5aoWcDEDKsXM-x9u4uPo2sdfwaQeG7nm9LCPTy_s"
```
