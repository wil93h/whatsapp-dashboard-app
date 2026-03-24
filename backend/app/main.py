from fastapi import FastAPI
from app.modules.message.interfaces.webhook_controller import router as webhook_router
from app.modules.message.interfaces.api_controller import router as api_router

app = FastAPI()

app.include_router(webhook_router)
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "API funcionando 🚀"}