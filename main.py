from fastapi import FastAPI
from fastapi.responses import JSONResponse
from utils import STATUS_BAD_REQUEST, STATUS_SUCCESS, save_result, validate_input, fibonacci

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