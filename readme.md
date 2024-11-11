# fib_api 仕様

## 各ファイルの役割
- main.py：実際のAPIを実装
- make_db.py：アクセスログを残すためのデータベースを初期化
  - webサーバー上で1回のみ実行するとよい
- unit_test.py：ユニットテストの実行
- validation_test.csv：テストデータと期待される出力を格納
  - 列の説明：左から「入力、期待される結果、期待されるステータスコード」

## 使用したpythonライブラリとその役割
- fastapi：APIの実装
- uvicorn：fastapiアプリケーションの実行
- requests：pythonコードからhttpリクエストの送信
- pytest：ユニットテストの実行
- httpx：python用のhttpクライアントライブラリ、pytestを動かすために使用

## APIアプリの概要
- httpメゾット：GET
- URI：http://54.64.165.29:8000/fib/?n={n}
  - {n}に入力したい数字を入力
- HTTPステータスコード（処理が成功した場合）：200
- リクエスト例：http://54.64.165.29:8000/fib/?n=99
  - 出力：`{"result":218922995834555169026}`
  - json形式で出力する
- HTTPステータスコード（処理が失敗した場合）：400
- 処理が失敗する例
  - 非負の整数を入力
  - 少数を入力
  - 文字列を入力
  - 空文字""を入力
- リクエスト例（非負）：http://54.64.165.29:8000/fib/?n=-1
  - 出力：`{"status":400,"result":"Input must be a non-negative integer."}`
- リクエスト例（文字列）：http://54.64.165.29:8000/fib/?n=abc
  - 出力：`{"status":400,"result":"Input must be an integer."}`
  - 少数を入力しても、Resultには同じエラー文が返ってくる
- リクエスト例（空文字）：リクエスト例（非負）：http://54.64.165.29:8000/fib/?n=
  - 出力：`{"status":400,"result":"There is no input."}`
- その他の仕様
  - アクセルがあるごとに、ログをデータベース(fib_log.db)に記入

## ユニットテストのやり方
- python version：3.12.4
- 使用ライブラリ：requests, pytest, httpx
  - `pip install requests pytest httpx`等でインストールしておく
- validation_test.csvをunit_test.pyと同じ実行フォルダにおいておく
- ターミナルで`pytest unit_test.py -v`を実行
  - 以下のように出力できれば成功
```shell
=================================== test session starts ===================================
platform win32 -- Python 3.12.4, pytest-8.3.3, pluggy-1.5.0 -- c:\Users\kato0\Documents\program_file\Speee\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\kato0\Documents\program_file\Speee
plugins: anyio-4.6.2.post1, cov-6.0.0
collected 8 items
unit_test.py::test_validate_input[0-0-200] PASSED                                    [ 25%]
unit_test.py::test_validate_input[9-34-200] PASSED                                   [ 37%]
unit_test.py::test_validate_input[-1-Input must be a non-negative integer.-400] PASSED [ 50%]
unit_test.py::test_validate_input[abc-Input must be an integer.-400] PASSED          [ 62%]
unit_test.py::test_validate_input[33 a-Input must be an integer.-400] PASSED         [ 75%]
unit_test.py::test_validate_input[-There is no input.-400] PASSED                    [ 87%]
unit_test.py::test_api_null_input PASSED                                             [100%]

==================================== 8 passed in 1.34s ====================================
```
