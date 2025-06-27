from fastapi import FastAPI
from app.routes import predict_routes

app = FastAPI(title="API Prédiction Immobilier")

app.include_router(predict_routes.router)
