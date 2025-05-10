from kafka import KafkaConsumer
import json
import asyncio
from pathlib import Path
import sys
from base64 import b64decode

ROOT_DIR = Path(__file__).resolve().parents[1]  # ajuste conforme estrutura real
sys.path.append(str(ROOT_DIR))

from image_message import ImageMessage

message_queue = asyncio.Queue()

# Garante que a pasta 'photos' exista
PHOTOS_DIR = Path(__file__).parent / "photos"
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

async def start_kafka_consumer():
    loop = asyncio.get_event_loop()

    def consume():
        consumer = KafkaConsumer(
            'topic.frame.processado',
            bootstrap_servers='kafka:29092',
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id='websocket-group',
            value_deserializer=lambda m: m.decode('utf-8')
        )

        for msg in consumer:
            try:
                data = json.loads(msg.value)
                frame_msg = ImageMessage(**data)

                # Salva a imagem
                filename = PHOTOS_DIR / f"frame_{msg.offset}.jpg"
                with open(filename, "wb") as f:
                    f.write(b64decode(frame_msg.frame))

                # Adiciona metadados
                frame_msg.metadata["status"] = "salvo_em_disco"
                frame_msg.metadata["saved_to"] = str(filename)
                frame_msg.metadata["offset"] = msg.offset

                asyncio.run_coroutine_threadsafe(message_queue.put(frame_msg), loop)
                consumer.commit()
            except Exception as e:
                print(f"Erro ao consumir mensagem: {e}")

    loop.run_in_executor(None, consume)
