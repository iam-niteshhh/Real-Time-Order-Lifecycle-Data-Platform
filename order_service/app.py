from fastapi import fastapi
from service import create_order

app = FastAPI()

@app.post("/order")
def order_endpoint(payload: dict):
    return create_order(payload)
