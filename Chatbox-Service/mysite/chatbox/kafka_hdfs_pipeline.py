import os
import json
import logging
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from hdfs import InsecureClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
HDFS_URL = os.getenv("HDFS_URL")
HDFS_USER = os.getenv("HDFS_USER")
HDFS_PATH = os.getenv("HDFS_PATH")

def ensure_kafka_topic_exists(kafka_server, topic_name):
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=[kafka_server])
        existing_topics = admin_client.list_topics()
        if topic_name not in existing_topics:
            topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
            admin_client.create_topics(new_topics=[topic], validate_only=False)
            logging.info(f"Created Kafka topic: {topic_name}")
        else:
            logging.info(f"Kafka topic '{topic_name}' already exists.")
        admin_client.close()
    except Exception as e:
        logging.error(f"Failed to ensure Kafka topic: {e}")

class KafkaToHDFSProducer:
  def __init__(self, kafka_host=KAFKA_SERVER, topic=KAFKA_TOPIC):
    self.topic = topic
    self.producer = KafkaProducer(
      bootstrap_servers=[kafka_host],
      value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

  def send_message(self, data: dict):
    """Send data (question, answer, session_id, timestamp, ...) to Kafka."""
    self.producer.send(self.topic, value=data)
    self.producer.flush()
    logging.info(f"Sent message to Kafka topic={self.topic}: {data}")
    
class KafkaToHDFSConsumer:
  def __init__(
    self,
    kafka_host = KAFKA_SERVER,
    topic = KAFKA_TOPIC,
    hdfs_host = HDFS_URL,
    hdfs_user = HDFS_USER,
    hdfs_path = HDFS_PATH
  ):
    self.topic = topic
    self.consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[kafka_host],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="chatbox-hdfs-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
      )
    ensure_kafka_topic_exists(kafka_host, topic)
    self.hdfs_client = InsecureClient(hdfs_host, user=hdfs_user)
    self.hdfs_path = hdfs_path
    # Create the directory on HDFS if it does not exist.
    if not self.hdfs_client.status(self.hdfs_path, strict=False):
      self.hdfs_client.makedirs(self.hdfs_path)

  def start(self):
    """Listen to Kafka and write data to HDFS in real time."""
    logging.info(f"Starting Kafka→HDFS Consumer (topic={self.topic})")
    for message in self.consumer:
      data = message.value
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      file_name = f"{self.hdfs_path}/chatbox_{timestamp}.json"

      # Write data to a JSON file on HDFS.
      with self.hdfs_client.write(file_name, encoding="utf-8") as writer:
          json.dump(data, writer, ensure_ascii=False, indent=2)
      logging.info(f"Wrote message to HDFS: {file_name}")