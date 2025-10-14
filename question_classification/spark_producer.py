from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
from pyspark.sql.functions import col
import pika, json

# RabbitMQ config
RABBITMQ_HOST = "rabbitmq_bitdata"
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = "admin"
RABBITMQ_PASSWORD = "admin"
RABBITMQ_QUEUE = "question_queue"

# HDFS paths
input_path = "hdfs://namenode:9000/chatbox_data"

# Define schema
schema = StructType([
    StructField("session_id", IntegerType(), True),
    StructField("question_id", IntegerType(), True),
    StructField("question", StringType(), True),
    StructField("answer", StringType(), True),
    StructField("timestamp", TimestampType(), True)
])

def create_spark_session(app_name="SparkProducer"):
    return (
        SparkSession.builder
        .appName(app_name)
        .getOrCreate()
    )

def send_to_rabbitmq(batch_df, batch_id):
    """Send each row of the batch to RabbitMQ as JSON"""
    if batch_df.isEmpty():
        return

    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    ))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    rows = batch_df.toJSON().collect()
    for row in rows:
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=row,
            properties=pika.BasicProperties(delivery_mode=2)  # persistent
        )
    connection.close()
    batch_df.show(truncate=False)
    print(f"[Batch {batch_id}] Sent {len(rows)} messages to RabbitMQ")

if __name__ == "__main__":
    spark = create_spark_session()
    df = (
        spark.readStream
        .schema(schema)
        .option("multiLine", True)
        .option("maxFilesPerTrigger", 1)
        .json(input_path)
    )

    query = (
        df.writeStream
        .foreachBatch(send_to_rabbitmq)
        .outputMode("append")
        .start()
    )

    query.awaitTermination()
