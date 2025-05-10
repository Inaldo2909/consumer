import base64
import json
from kafka import KafkaProducer
from datetime import datetime

# Configuração do produtor Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # ou 'kafka:29092' se estiver rodando DENTRO do container
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Carrega uma imagem e converte para base64
with open("frame_exemplo.jpg", "rb") as img_file:
    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

# Dados do frame
message = {
    "frame": img_base64,
    "metadata": {
        "source": "test-script",
        "timestamp": datetime.now().isoformat()
    }
}

# Envia para o tópico
producer.send("topic.frame.processado", value=message)
producer.flush()

print("Mensagem enviada com sucesso!")
