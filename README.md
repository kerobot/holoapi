# ホロAPI

MongoDB へ登録したホロジュールのホロライブスケジュールと Youtube の動画情報を取得します。

## 環境

* Windows 11 Pro 22H2
* Python 3.11.1
* PowerShell 7.3.1
* Visual Studio Code 1.74.3
* Git for Windows 2.39.1.windows.1
* MongoDB 6.0.3 / Mongosh 1.6.0

## Poetry と pyenv の確認

```powershell
> poetry --version
Poetry version 1.3.2

> pyenv --version
pyenv 3.1.1
```

## MongoDB の確認

```powershell
> mongosh --version
1.6.0
```

## Python 環境設定

```powershell
> pyenv versions
> pyenv install 3.11.1
> pyenv local 3.11.1
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
> mongosh localhost:27017/admin -u admin -p
> use holoduledb
switched to db holoduledb
> show collections
holodules
> db.createCollection("users");
{ "ok" : 1 }
> db.users.insertOne( {"id":"1", "username":"user01", "password":"dummy", "firstname": "taro", "lastname": "tokyo"} );
{
  acknowledged: true,
  insertedId: ObjectId("63d1dfafcec12c32af27ec11")
}
> db.users.find();
[
  {
    _id: ObjectId("63d1dfafcec12c32af27ec11"),
    id: '1',
    username: 'user01',
    password: 'dummy',
    firstname: 'taro',
    lastname: 'tokyo'
  }
]
```

## プログラムの実行

```powershell
> poetry run python app.py
```

## JWTトークンの取得

```powershell
> curl "http://127.0.0.1:5000/login" -X POST -H "Content-Type: application/json" -d '"{ \"username\": \"user01\", \"password\": \"dummy\" }"'
```

## データの取得

```powershell
> curl "http://localhost:5000/holodules/20230126" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzcwMzcyMzYsImlhdCI6MTYzNzAzNjkzNiwibmJmIjoxNjM3MDM2OTM2LCJpZGVudGl0eSI6InVzZXIwMSJ9.H7u5aoWcDEDKsXM-x9u4uPo2sdfwaQeG7nm9LCPTy_s"
```
