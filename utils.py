import sqlite3
import datetime
import numpy as np

STATUS_BAD_REQUEST = 400
STATUS_SUCCESS = 200

ERROR_MESSAGES = {
    "negative": "Input must be a non-negative integer.",
    "invalid": "Input must be an integer.",
    "null": "There is no input."
}

def save_result(n, result: int):
    query = "INSERT INTO fib_log (id, access_time, input_parameter, result) VALUES (?, ?, ?, ?)"

    conn = sqlite3.connect('fib_log.db')
    cur = conn.cursor()
    
    id = cur.execute("SELECT COUNT(*) FROM fib_log").fetchone()[0] + 1

    cur.execute(query, (id, datetime.datetime.now().isoformat(), n, result))
    
    conn.commit()
    conn.close()

def validate_input(n: str) -> int:
    try:
        if n == "":
            raise ValueError(ERROR_MESSAGES["null"])
        
        n = int(n)
        if n < 0:
            raise ValueError(ERROR_MESSAGES["negative"])
        
        return n
    
    except ValueError as e:
        if str(e) == ERROR_MESSAGES["null"]:
            save_result("", ERROR_MESSAGES["null"])
            raise ValueError(ERROR_MESSAGES["null"])
        
        elif str(e) == ERROR_MESSAGES["negative"]:
            save_result(0, ERROR_MESSAGES["negative"])
            raise ValueError(ERROR_MESSAGES["negative"])
        
        else:
            save_result(0, ERROR_MESSAGES["invalid"])
            raise ValueError(ERROR_MESSAGES["invalid"])

def mat_pow(mat, n):
    result = [[1, 0], [0, 1]]
    base = mat

    while n > 0:
        if n % 2 == 1:
            result = np.dot(result, base)
        base = np.dot(base, base)
        n //= 2

    return result

# 第0項は0とする。
def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    mat = [[1, 1], [1, 0]]

    mat = mat_pow(mat, n)
    return mat[1][0]