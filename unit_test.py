# APIのユニットテストを行うスクリプト
import requests
import pytest
import csv

BASE_URL = "127.0.0.1:8000"  # 実際のAPIのURL

STATUS_BAD_REQUEST = 400
STATUS_SUCCESS = 200

ERROR_MESSAGES = {
    "negative": "Input must be a non-negative integer.",
    "invalid": "Input must be an integer.",
    "null": "There is no input."
}

with open("validation_test.csv") as f:
    test_case = csv.reader(f)
    test_case = list(test_case)

def test_validate_input():
    for n, expected in test_case:
        if n == "input_parameter":
            continue
        try:
            result = requests.get(f"{BASE_URL}/fib/?n={n}")
            assert result.status_code == STATUS_SUCCESS
            data = result.json()
            assert data["result"] == int(expected)
        except ValueError as e:
            assert str(e) == expected

def test_api_null_input():
    response = requests.get(f"{BASE_URL}/fib/")
    assert response.status_code == 422  # FastAPIのバリデーションエラー

if __name__ == "__main__":
    pytest.main([__file__, "-v"])