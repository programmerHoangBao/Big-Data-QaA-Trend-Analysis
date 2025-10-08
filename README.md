# Big-Data-QaA-Trend-Analysis

## 1. Overview

## 2. Set up project

### 2.1. Prerequisite

- Set up hadoop 3.3.6 on docker ([Installation guide link](https://github.com/programmerHoangBao/Set-up-hadoop-3.3.6-on-docker.git)).
- Install Spark 3.5.7 ([Installation guide link](https://drive.google.com/file/d/1oLYXTA-X_rznSAoZUIn2dW6FbORIShMY/view?usp=drive_link)).
- Set up Kafka, PostgreSQL on docker ([Installation guide link](https://drive.google.com/file/d/13bWzsVKBacuOildf6SzavSIh1fo12wqB/view?usp=drive_link)).

### 2.2. Set up Chatbox-Service

#### 2.2.1. Install directory setup

- You install the setup folder from the provided link:
  - [Link-driver-directory-setup](https://drive.google.com/drive/folders/12Vg7QTOihddRnX76jhiJmjS97qsnoTo1?usp=drive_link)

#### 2.2.2. Add file .env

- Add file .env:
  <img width="1350" height="767" alt="image-2" src="https://github.com/user-attachments/assets/5fceb873-2639-4ef2-a630-ad14ace0569a" />

- The content of the .env file is as follows:
  <img width="1094" height="123" alt="image-9" src="https://github.com/user-attachments/assets/b80b2f18-079a-4661-a327-547afd7861cb" />

- **QUESTION_AND_ANSWER_PATH**: Path to the file setup/dataset/Question_Add_Answer.jsonl
- **CHATBOX_API**: API of 'Chatbox-Service'
#### 2.2.3. Add file Chatbox-Service/mysite/.env

- Add the .env file to './Chatbox-Service/mysite' with the following content:
  <img width="713" height="572" alt="image-1" src="https://github.com/user-attachments/assets/44bc7d41-f643-4326-a889-dab1541f6dda" />

- **Part 1: Database Configuration**
  - **DB_NAME**: The name of the database your application connects to. Example: mydb, salesdb, school_db.
  - **DB_USER**: The username used to access the database. Example: root, admin, postgres, app_user.
  - **DB_PASSWORD**: The password for the database user above.
  - **DB_HOST**: The host address of the database server (localhost, 127.0.0.1,.....).
  - **DB_PORT**: The port number the database is listening on (MySQL → 3306, PostgreSQL → 5432, SQL Server → 1433,...).
- **Part 2: Security**
  - **SECRET_KEY**: A secret string used to sign or encrypt sensitive data (sessions, tokens, CSRF, etc.). For frameworks like Django, Flask, or Node.js, this is critical for app security.
- **Part 3: AI / FAISS Configuration (for Q&A search systems)**
  - **QA_INDEX_PATH**: Path to the FAISS index file. This binary file stores vector embeddings for similarity search in Q&A/chat systems.
  - **QA_META_PATH**: Path to a metadata JSON file that contains extra information (original text, IDs, references) for the vectors stored in FAISS.
- **Part 4: Kafka Configuration (Data Streaming)**
  - **KAFKA_SERVER**: Address of the Kafka broker or cluster. Example: localhost:9092, kafka:9092, or multiple brokers like broker1:9092,broker2:9092.
  - **KAFKA_TOPIC**: The Kafka topic name your app will produce to or consume from. Example: chatbox_data, event_logs, qa_stream.
- **Part 5: HDFS (Hadoop Distributed File System) Configuration**
  - **HDFS_URL**: The URL of the HDFS NameNode. Typical formats:
    http://namenode:9870 or hdfs://namenode:9000.
  - **HDFS_USER**: The Hadoop user name used when interacting with HDFS. Example: hadoop, root, or a custom user.
  - **HDFS_PATH**: The path in HDFS where data is stored or read. Example: /user/root/data, /chatbox_data/logs/.

#### 2.2.4. Install libray

- For safety, you should create a virtual environment (venv) to install the libraries.
  - **Step 1**: Open the terminal in the project directory and run the command 'py -m venv .venv' or 'python -m venv .venv'.
  - **Step 2**: Run the command '.venv\Scripts\activate'
   <img width="816" height="205" alt="image-4" src="https://github.com/user-attachments/assets/14ce65e9-cafa-44c1-82b3-02125a9844b5" />

- Install the libraries from the requirements.txt file.
  - Run the following command in the project terminal: 'pip install -r requirements.txt'
   <img width="2560" height="1528" alt="image-5" src="https://github.com/user-attachments/assets/09307168-cb04-4f0f-876d-a15ce250369b" />


#### 2.2.5. Config hosts

- Open Notepad as Administrator, then open the file 'C:\Windows\System32\drivers\etc\hosts'.
- Add the following lines to the end of the file: <br>
  127.0.0.1 datanode1 <br>
  127.0.0.1 datanode2 <br>
  127.0.0.1 datanode3 <br>

#### 2.2.6. Django management commands

- In the project terminal, run the following two commands: <br>
  'python Chatbox-Service/mysite/manage.py makemigrations' <br>
  'python Chatbox-Service/mysite/manage.py migrate'
  <img width="2560" height="1528" alt="image-6" src="https://github.com/user-attachments/assets/22fe26f2-9d72-435f-b9b0-7fb26bf54ea7" />


#### 2.2.7. "Check if the Chatbox-Service is working properly."

- In the project terminal, run the following command: <br>
  python Chatbox-Service/mysite/manage.py runserver <br>
- If you see the message "Starting development server at xxxxxxx", it means you have successfully started the Chatbox-Service.
