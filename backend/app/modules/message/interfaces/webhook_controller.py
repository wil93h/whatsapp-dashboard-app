from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from app.modules.message.application.process_message import ProcessMessageUseCase

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    try:
        form = await request.form()

        mensaje = form.get("Body")
        numero = form.get("From")

        use_case = ProcessMessageUseCase()
        use_case.execute(mensaje, numero)

        return PlainTextResponse("Procesado ✅")

    except Exception as e:
        print("Error:", e)
        return PlainTextResponse("Error", status_code=500)