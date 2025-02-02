import json
import os
from dotenv import load_dotenv
from aiokafka import AIOKafkaProducer


load_dotenv()


KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")


class KafkaProducer:
    def __init__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    async def start(self):
        await self.producer.start()

    async def send(self, topic: str, message: dict):
        await self.producer.send_and_wait(topic, value=message)

    async def stop(self):
        await self.producer.stop()


kafka_producer = KafkaProducer()


async def send_logs_kafka(topic: str, action: str, status_code: int, details):
    details_serializable = json.loads(json.dumps(details, default=str))

    message = {"action": action, "status_code": status_code, "details": details_serializable}
    await kafka_producer.send(topic, message)
