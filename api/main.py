from fastapi import FastAPI
from api.routes.metrics import router as metrics_router
from api.routes.order import router as order_router

app = FastAPI()

app.include_router(metrics_router)
app.include_router(order_router)
