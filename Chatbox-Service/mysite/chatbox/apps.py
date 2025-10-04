from django.apps import AppConfig
import threading
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class ChatboxConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'chatbox'
    
  def ready(self):
    """Run Kafka consumer in background when Django starts"""
    from .kafka_hdfs_pipeline import KafkaToHDFSConsumer

    def run_consumer():
      try:
        consumer = KafkaToHDFSConsumer()
        consumer.start()
      except Exception as e:
        logging.error(f"Kafka Consumer failed: {e}")

    thread = threading.Thread(target=run_consumer, daemon=True)
    thread.start()
    logging.info("Kafka Consumer started in background.")
