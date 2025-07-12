from fastapi import FastAPI
from api.routes import router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="API Educacional IA")

app.include_router(router, prefix="/api")
