from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sqlite3
import datetime

STATUS_BAD_REQUEST = 400
STATUS_SUCCESS = 200

ERROR_MESSAGES = {
    "negative": "Input must be a non-negative integer.",
    "invalid": "Input must be an integer.",
    "null": "There is no input."
}

def save_result(n, status: int):
    query = "INSERT INTO fib_log (id, access_time, input_parameter, status_code) VALUES (?, ?, ?, ?)"

    conn = sqlite3.connect('fib_log.db')
    cur = conn.cursor()
    
    id = cur.execute("SELECT COUNT(*) FROM fib_log").fetchone()[0] + 1

    cur.execute(query, (id, datetime.datetime.now().isoformat(), n, status))
    
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

def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        res = a + b
        a, b = b, res
    return b

app = FastAPI()

@app.get("/fib/")
def get_fibonacci(n: str):
    try:
        valid_input = validate_input(n)
        result = fibonacci(valid_input)
        save_result(valid_input, STATUS_SUCCESS)
        return JSONResponse(
            status_code=STATUS_SUCCESS,
            content={"result": result}
        )
    except ValueError as e:
        return JSONResponse(
            status_code=STATUS_BAD_REQUEST,
            content={"status": STATUS_BAD_REQUEST, "result": str(e)}
        )