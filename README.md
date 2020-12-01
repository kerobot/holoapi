# ホロAPI

MongoDB へ登録したホロジュールのホロライブスケジュールと Youtube の動画情報を取得します。

## 環境

* Windows 10 Pro 1909 x64
* Python 3.8.5 x64
* PowerShell 7.1 x64
* Visual Studio Code 1.51.1 x64
* Git for Windows 2.27.0 x64

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

## プログラムの実行

```powershell
> poetry run python holoapi.py
```
