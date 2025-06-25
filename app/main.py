from fastapi import FastAPI 
from app.routes import predict_routes 

app = FastAPI(title="API Estimation Prix au m_2")

app.include_router(predict_routes.router)