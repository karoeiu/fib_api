# APIのユニットテストを行うスクリプト
import requests
import pytest
import csv

BASE_URL = "http://54.64.165.29:8000"  # 実際のAPIのURL

STATUS_BAD_REQUEST = 400
STATUS_SUCCESS = 200

ERROR_MESSAGES = {
    "negative": "Input must be a non-negative integer.",
    "invalid": "Input must be an integer.",
    "null": "There is no input."
}

def read_test_cases():
    with open("validation_test.csv") as f:
        reader = csv.reader(f)
        test_cases = list(reader)
    return test_cases

# テストケースを読み込んで、レスポンスの検証
@pytest.mark.parametrize("n, expected, status", read_test_cases())
def test_validate_input(n, expected, status):
    response = requests.get(f"{BASE_URL}/fib/?n={n}")
    assert response.status_code == int(status)
    
    if int(status) == STATUS_SUCCESS:
        assert response.json()["result"] == int(expected)
    else:
        assert response.json()["result"] == expected

# /fib/ 以降に何も入力がない場合のテスト
def test_api_null_input():
    response = requests.get(f"{BASE_URL}/fib/")
    assert response.status_code == 422  # FastAPIのバリデーションエラー

if __name__ == "__main__":
    pytest.main([__file__, "-v"])