from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI()
clients = []

# Permitir chamadas do frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Diretório onde está seu index.html
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Servir arquivos estáticos
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

LOG_PATH = "logs/websocket.log"

@app.websocket("/ws/frames")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Ignora mensagens do cliente
    except Exception:
        clients.remove(websocket)

async def broadcast(message: str):
    for client in clients:
        try:
            await client.send_text(message)
        except Exception:
            clients.remove(client)

if __name__ == "__main__":
    uvicorn.run("websocket_server:app", host="0.0.0.0", port=8000)
