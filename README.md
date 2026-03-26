
# Dashboard de feedback del Cliente – Café de El Salvador
Sistema end‑to‑end que permite a los clientes enviar feedback por WhatsApp, almacenarlo en MongoDB y analizarlo automáticamente con IA (Google Gemini) para mostrar en tiempo real el sentimiento, los temas principales y las tendencias en un dashboard interactivo.
## Tecnologías utilizadas
| Área | Tecnología |
|------|------------|
| **Backend** | Python, FastAPI, MongoDB (PyMongo), Google Gemini AI |
| **Frontend** | React, TypeScript, Vite, Recharts |
| **Mensajería** | Twilio WhatsApp Sandbox |
| **Infraestructura** | Docker, Docker Compose, MongoDB Atlas, ngrok |
## Requisitos y configuración local
### 1. Clonar el repositorio
```bash
git clone https://github.com/wil93h/whatsapp-dashboard-app
```

### 2. Levantar el proyecto con Docker Compose

Asegúrate de tener Docker instalado en tu máquina.

-   En la raíz del proyecto, crea un archivo `.env` dentro de la carpeta `backend/` con las siguientes variables:
    

```bash
cd backend
echo "GOOGLE_API_KEY=tu_api_key_de_gemini" >> .env
echo "MONGODB_URI=mongodb://mongo:27017" >> .env
cd ..
```
-   Construye y levanta los contenedores:
    

```bash
docker-compose up --build
```
-   El backend estará disponible en `http://localhost:8000` y el frontend en `http://localhost:5173`.
    
-   MongoDB se ejecutará en el puerto `27017` dentro del contenedor, pero solo es accesible desde el backend (no exponemos el puerto a menos que lo necesites).
 

### 3. Exponer el webhook con ngrok (para Twilio)

Twilio necesita una URL pública para enviar los mensajes. Usamos ngrok para crear un túnel hacia nuestro backend local.

-   Descarga e instala ngrok desde [ngrok.com](https://ngrok.com/).
    
-   Ejecuta el siguiente comando para exponer el puerto `8000`:
    

```bash
ngrok http 8000
```
-   Copia la URL pública que te proporciona ngrok (ej. `https://abc123.ngrok.io`).
    
-   En el panel de Twilio (WhatsApp Sandbox), configura la URL del webhook apuntando a `https://tu-url-ngrok.io/webhook`.
    
-   Asegúrate de que el método sea `POST`.
    

### 4. Verificar que todo funciona

-   Envía un mensaje de WhatsApp al número de prueba que proporciona Twilio.
    
-   Revisa los logs del backend (`docker-compose logs backend`) para confirmar que el mensaje se recibe y procesa.
    
-   Abre el dashboard en `http://localhost:5173` y observa los gráficos actualizarse.
    
### 5. Justificación Técnica

#### Matriz de Decisión: MongoDB (NoSQL) vs SQL
La elección de MongoDB frente a una base de datos relacional se basó en los siguientes criterios:

| Criterio | MongoDB (NoSQL) | SQL (PostgreSQL/MySQL) | Decisión |
| :--- | :--- | :--- | :--- |
| **Esquema de datos** | Flexible, permite documentos con campos variables. Ideal para mensajes que se enriquecen después con análisis de IA. | Esquema rígido; requiere migraciones al añadir campos como `sentimiento`, `tema`, etc. | ✅ **MongoDB**: permite evolucionar el esquema sin downtime. |
| **Escalabilidad** | Escala horizontalmente (sharding) de forma nativa, adecuado para alto volumen de mensajes. | Escala verticalmente; el sharding es complejo y menos común en implementaciones pequeñas. | ✅ **MongoDB**: mejor preparado para crecimiento futuro. |
| **Consultas analíticas** | Agregaciones (pipeline) potentes para cálculos de sentimientos y temas. | SQL también permite agregaciones, pero requiere un esquema normalizado. | ⚖️ **Empate**: ambos pueden realizar las consultas necesarias. |
| **Operaciones de actualización** | Actualizaciones atómicas de campos (ej. añadir análisis a un mensaje existente). | Requiere `UPDATE` sobre columnas fijas. | ✅ **MongoDB**: más natural para enriquecer documentos. |
| **Ecosistema y facilidad** | Integración sencilla con Python (PyMongo), ideal para prototipos rápidos. | También buena integración con SQLAlchemy, pero requiere definir modelos. | ⚖️ Ambos válidos, pero MongoDB acelera el desarrollo inicial. |


> **Conclusión:** MongoDB se eligió por su flexibilidad de esquema, facilidad para manejar documentos semiestructurados (mensajes + análisis) y su capacidad de escalado horizontal, alineándose con la naturaleza evolutiva del proyecto.

---

### Estrategia de Prompts

Para garantizar la precisión del análisis de sentimiento y la extracción de temas, se utilizó una estrategia **Zero‑shot con control de formato** combinada con instrucciones explícitas de salida JSON. 

#### Técnicas aplicadas:

1. **Zero‑shot con restricción de formato**
   - El prompt instruye al modelo a responder *solo* con JSON válido, sin markdown ni texto adicional.
   - Se define explícitamente la estructura esperada (`sentimiento`, `tema`, `resumen`).
   - Esta aproximación reduce el post‑procesamiento y minimiza errores de parseo.

2. **Instrucción de rol**
   - Se le asigna el rol de “analista de sentimiento” para contextualizar la tarea.

3. **Control de vocabulario**
   - Los valores permitidos para `sentimiento` y `tema` se definen en el prompt (positivo/negativo/neutro, y las categorías de tema).
   - Esto fuerza al modelo a elegir dentro de un conjunto cerrado, mejorando la consistencia.

4. **Manejo de errores**
   - En caso de fallo en el parseo o respuesta inválida, se retorna un objeto por defecto (`neutro`, `Otro`, “Error al procesar”) para no interrumpir el flujo.

#### Ejemplo de prompt completo:

```text
Eres un analista de sentimiento. Responde únicamente en JSON válido.

IMPORTANTE:
- Responde SOLO JSON válido
- NO uses markdown
- NO uses ```json
- NO agregues texto adicional

Analiza el siguiente mensaje de un cliente de una cafetería.
Responde SOLO en JSON con esta estructura exacta:
{
  "sentimiento": "positivo | negativo | neutro",
  "tema": "Servicio al Cliente | Calidad del Producto | Precio | Limpieza | Otro",
  "resumen": "Resumen corto del mensaje"
}

Mensaje: "{texto}"
```

### Diagramas C4

#### C1 – Diagrama de Contexto

![C1](https://raw.githubusercontent.com/wil93h/whatsapp-dashboard-app/refs/heads/main/diagram/Diagram-C1%20-%20Context.drawio.png)

#### C2 – Diagrama de Contenedores

![C2](https://raw.githubusercontent.com/wil93h/whatsapp-dashboard-app/refs/heads/main/diagram/Diagram-C2%20-%20Container.drawio.png)

#### C3 – Diagrama de Componentes (Código)

![C3](https://raw.githubusercontent.com/wil93h/whatsapp-dashboard-app/refs/heads/main/diagram/Diagram-C3%20-%20Component.drawio.png)

#### C4 – Diagrama de Despliegue

![C3](https://raw.githubusercontent.com/wil93h/whatsapp-dashboard-app/refs/heads/main/diagram/Diagram-C3%20-%20Component.drawio.png)

### Customer Journey Map (AS IS / TO BE)

| Etapa | AS IS (proceso actual) | TO BE (con el sistema) |
|------|------------------------|------------------------|
| 1. Pre-visita | El cliente no tiene un canal claro para dejar feedback. | El cliente conoce el número de WhatsApp del café mediante afiches o redes sociales. |
| 2. Llegada y pedido | El cliente realiza el pedido; no se registra su experiencia. | Sin cambios en esta etapa. |
| 3. Consumo | La experiencia no se captura en tiempo real. | El cliente vive la experiencia (producto, servicio, limpieza). |
| 4. Post-consumo | Si quiere opinar, debe pedir un formulario en papel o hablar con un empleado. | El cliente escanea un código QR o escribe directamente al número de WhatsApp y envía su mensaje. |
| 5. Recepción del feedback | Los comentarios se acumulan en papeles o mensajes sueltos. | Twilio recibe el mensaje y lo envía al webhook del backend. |
| 6. Análisis | El gerente lee manualmente los comentarios, sin métricas consolidadas. | El backend guarda el mensaje, lo analiza con IA y actualiza la base de datos. |
| 7. Visualización | No hay un tablero centralizado; las decisiones se basan en percepciones subjetivas. | El dashboard muestra gráficos de sentimientos, temas y mensajes recientes en tiempo real. |
| 8. Toma de decisiones | El gerente actúa cuando una queja es recurrente, pero sin datos precisos. | El gerente identifica tendencias (ej. muchas quejas sobre limpieza) y toma acciones basadas en datos objetivos. |

---

### Matriz de Valor (Decisiones de Negocio)

| # | Decisión de negocio | Insight del dashboard | Acción propuesta | KPI de seguimiento |
|---|--------------------|----------------------|------------------|--------------------|
| 1 | Ajuste de precios | El tema “Precio” aparece con frecuencia y el sentimiento asociado es mayoritariamente negativo. | Realizar un estudio de mercado local y considerar promociones, combos o ajustes de precio para equilibrar percepción de valor. | Reducción del % de menciones negativas del tema “Precio” en 30 días. |
| 2 | Reforzar protocolos de limpieza | El tema “Limpieza” muestra un sentimiento negativo recurrente. | Incrementar la frecuencia de limpieza, implementar checklist visibles, capacitar al personal en higiene. | Disminución del 50% en menciones negativas del tema “Limpieza” en 60 días. |
| 3 | Capacitación en servicio al cliente | El tema “Servicio al Cliente” tiene sentimiento negativo o su volumen es bajo respecto a otros temas. | Lanzar un programa de capacitación en atención, medir satisfacción post-capacitación, reconocer a empleados destacados. | Aumento del porcentaje de mensajes positivos en “Servicio al Cliente” y reducción de quejas asociadas. |



## Contribuciones y mejoras futuras

- **Autenticación y seguridad**:
  - Verificar la firma de Twilio en el webhook para asegurar que las solicitudes provienen realmente de Twilio y no de un atacante.
  - Implementar autenticación (JWT, API keys) en los endpoints del backend para restringir el acceso al dashboard y a los datos.
- **Análisis de tendencias por período**: Agregar filtros por día, semana, mes para visualizar la evolución del sentimiento y los temas a lo largo del tiempo.
- **Respuestas automáticas a clientes**: Confirmar la recepción del mensaje y, si es necesario, derivar a un agente o proporcionar información útil (horarios, promociones).
- **Sistema de colas (Celery/Redis)**: Procesar los mensajes de forma asíncrona para manejar picos de volumen sin bloquear la respuesta del webhook.
- **Few‑shot**: Incorporar ejemplos de mensajes reales en el prompt para mejorar la precisión en casos ambiguos.
- **Chain‑of‑Thought**: Solicitar una breve justificación antes de devolver el JSON, ayudando en casos complejos y permitiendo depuración.
- **Evaluación continua**: Implementar un sistema de monitoreo para ajustar el prompt según la calidad de las respuestas reales.
- **Trazabilidad**: Enriquecer el modelo de datos con metadatos de auditoría: ID de ejecución del modelo, latencia de respuesta, versión del prompt utilizado, y usuario/entorno. Esto facilitará la trazabilidad, depuración y mejora continua del sistema.

----------

© 2025 – Café de El Salvador – Challenge 