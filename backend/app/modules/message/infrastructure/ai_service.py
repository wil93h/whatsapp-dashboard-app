import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def analizar_mensaje(texto: str):
    prompt = f"""
Analiza el siguiente mensaje de un cliente de una cafetería.

Responde SOLO en JSON con esta estructura exacta:

{{
  "sentimiento": "positivo | negativo | neutro",
  "tema": "Servicio al Cliente | Calidad del Producto | Precio | Limpieza | Otro",
  "resumen": "Resumen corto del mensaje"
}}

Mensaje:
"{texto}"
"""

    try:
        response = model.generate_content(
            f"""Eres un analista de sentimiento. Responde únicamente en JSON válido.
            
            IMPORTANTE:
            - Responde SOLO JSON válido
            - NO uses markdown
            - NO uses ```json
            - NO agregues texto adicional

            \n{prompt}"""
        )

        return response.text

    except Exception as e:
        print("Error IA:", e)

        return json.dumps({
            "sentimiento": "neutro",
            "tema": "Otro",
            "resumen": "Error al procesar"
        })