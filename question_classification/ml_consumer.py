import pika, json, os
from joblib import load

# RabbitMQ config
RABBITMQ_HOST = "rabbitmq_bitdata"
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = "admin"
RABBITMQ_PASSWORD = "admin"
RABBITMQ_QUEUE = "question_queue"

# HDFS output directory
OUTPUT_DIR = "/question_classification"

# Load ML model & vectorizer
model = load('./model/small/log_reg_model.joblib')
vectorizer = load('./model/small/vectorizer.joblib')
mlb = load('./model/small/mlb.joblib')

def predict_tags(question, threshold=0.3):
    """Predict tags for a given question with probability > threshold"""
    if not question or not question.strip():
        return []
    try:
        X_input = vectorizer.transform([question])
        y_pred_proba = model.predict_proba(X_input)[0]
        
        labels_probs = list(zip(mlb.classes_, y_pred_proba))
        
        filtered_labels = [label for label, prob in labels_probs if prob > threshold]
        
        return filtered_labels
    except Exception as e:
        print(f"Prediction error: {e}")
        return []

def callback(ch, method, properties, body):
    try:
        try:
            data = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            print("Received invalid JSON message. Ignoring.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
          
        question = data.get("question", "").strip()
        question_id = data.get("question_id")
        print(f"question id: {question_id}")
        print(f"Data input: {question}")
        if not question or question_id is None:
            print("Missing required fields (question/question_id). Ignoring.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        tags = predict_tags(question)
        data["tags"] = tags
        print(f"tags = {tags}")
        if not data["tags"]:
            print(f"No tags predicted for question_id={question_id}.")
            # ch.basic_ack(delivery_tag=method.delivery_tag)
            # return
        
        filename = f"/tmp/question_{question_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        os.system(f"hdfs dfs -mkdir -p {OUTPUT_DIR}")
        os.system(f"hdfs dfs -put -f {filename} {OUTPUT_DIR}/")

        print(f"Processed & saved: {filename}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    ))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=5)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()
