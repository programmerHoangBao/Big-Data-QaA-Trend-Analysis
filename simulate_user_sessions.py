from time import sleep
import requests
import json
import os
from dotenv import load_dotenv
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

API_BASE = os.getenv('CHATBOX_API')
SESSION_API = f"{API_BASE}/create-session/"
QUESTION_API = f"{API_BASE}/create-question/"
ANSWER_API = f"{API_BASE}/create-answer/?question_id="

DATA_FILE = os.getenv('QUESTION_AND_ANSWER_PATH')
MAX_THREADS = 10

def load_questions():
    """Read all question texts from merged_posts.jsonl"""
    questions = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line.strip())
            question = obj.get("Question", {})
            q_text = (question.get("BodyText", "") + "\n" + question.get("BodyCode", "")).strip()
            if q_text:
                questions.append(q_text)
    return questions


def create_session():
    resp = requests.post(SESSION_API)
    if resp.status_code == 201:
        data = resp.json()
        return data["session_id"]
    else:
        print(f"Failed to create session ({resp.status_code}):", resp.text)
        return None


def create_question(session_id, question_text):
    payload = {"session_id": session_id, "text": question_text}
    resp = requests.post(QUESTION_API, json=payload)
    if resp.status_code == 201:
        return resp.json()["data"]["question_id"]
    else:
        print(f"Failed to create question (session {session_id}, status {resp.status_code}):", resp.text)
        return None


def create_answer(question_id):
    resp = requests.post(f"{ANSWER_API}{question_id}")
    if resp.status_code == 201:
        return resp.json()["data"]["answer_text"]
    else:
        print(f"Failed to create answer (question_id={question_id}, status {resp.status_code}):", resp.text)
        return None


def run_session(session_index, questions):
    """A function that represents an independent session."""
    print(f"[Session {session_index}] 🌀 Creating session...")
    session_id = create_session()
    if not session_id:
        return

    # Randomize the number of questions in the session.
    k_question = random.randint(1, 5)
    print(f"[Session {session_index}] Created (id={session_id}), will create {k_question} questions...")

    # Randomly select k_question questions from the file.
    for _ in range(k_question):
        sleep(0.8)
        q_text = random.choice(questions)
        q_id = create_question(session_id, q_text)
        if q_id:
            print(f"[Session {session_index}] | Created Question {q_id}")
            answer = create_answer(q_id)
            if answer:
                print(f"[Session {session_index}] | Got answer for Question {q_id} ({len(answer)} chars)")
        else:
            print(f"[Session {session_index}] | Skipped a question due to error.")


def main():
    # Load question data.
    questions = load_questions()
    if not questions:
        print("No questions loaded from merged_posts.jsonl.")
        return

    # Randomize the number of sessions (1–5).
    count_session = random.randint(1, 3)
    print(f"Starting simulation with {count_session} sessions... ({datetime.now()})")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(run_session, i + 1, questions) for i in range(count_session)]
        for f in as_completed(futures):
            f.result()

    print(f"Simulation finished at {datetime.now()}")


if __name__ == "__main__":
    index = 0
    while (True):
      print(f"Running: {index}")
      main()
      index += 1
      sleep(1)
