import json
from app.modules.message.infrastructure.repository import MessageRepository
from app.modules.message.infrastructure.ai_service import analizar_mensaje
from app.modules.message.schemas.message_schema import AIResponse

class ProcessMessageUseCase:

    def __init__(self):
        self.repo = MessageRepository()

    def execute(self, texto: str, numero: str):

        # 1. Guardar mensaje
        message_id = self.repo.create(texto, numero)
        print("AI message_id:", message_id)
        # 2. IA
        ai_raw = analizar_mensaje(texto)
        print("AI RAW:", ai_raw)
        # 3. Parsear JSON
        ai_json = json.loads(ai_raw)
        print("ai_json RAW:", ai_json)

        # 4. Validar
        ai_data = AIResponse(**ai_json)
        print("ai_data RAW:", ai_data)

        # 5. Actualizar
        self.repo.update_analysis(message_id, ai_data.dict())

        return {"status": "processed"}