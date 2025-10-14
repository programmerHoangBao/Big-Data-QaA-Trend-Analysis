import os
import json
import uuid
import logging
import pika
from hdfs import InsecureClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_POPT", 5672))
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")

HDFS_URL = os.getenv("HDFS_URL")
HDFS_USER = os.getenv("HDFS_USER")
HDFS_PATH = os.getenv("HDFS_PATH")


class RabbitMQToHDFSConsumer:
    def __init__(self):
        self.hdfs_client = InsecureClient(HDFS_URL, user=HDFS_USER)
        if not self.hdfs_client.status(HDFS_PATH, strict=False):
            self.hdfs_client.makedirs(HDFS_PATH)

        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        self.channel.basic_qos(prefetch_count=1)

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{HDFS_PATH}/chatbox_{timestamp}_{uuid.uuid4().hex}.json"

        with self.hdfs_client.write(file_name, encoding="utf-8", overwrite=True) as writer:
            json.dump(data, writer, ensure_ascii=False, indent=2)

        logging.info(f"Wrote message to HDFS: {file_name}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        logging.info("Started RabbitMQ→HDFS Consumer")
        self.channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=self.callback)
        self.channel.start_consuming()
