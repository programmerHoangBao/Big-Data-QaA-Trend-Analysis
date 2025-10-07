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
  ![alt text](image-2.png)
- The content of the .env file is as follows:
  ![alt text](image-9.png)
- **QUESTION_AND_ANSWER_PATH**: Path to the file setup/dataset/Question_Add_Answer.jsonl
- **CHATBOX_API**: API of 'Chatbox-Service'
#### 2.2.3. Add file Chatbox-Service/mysite/.env

- Add the .env file to './Chatbox-Service/mysite' with the following content:
  ![alt text](image-1.png)
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
    ![alt text](image-4.png)
- Install the libraries from the requirements.txt file.
  - Run the following command in the project terminal: 'pip install -r requirements.txt'
    ![alt text](image-5.png)

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
  ![alt text](image-6.png)

#### 2.2.7. "Check if the Chatbox-Service is working properly."

- In the project terminal, run the following command: <br>
  python Chatbox-Service/mysite/manage.py runserver <br>
- If you see the message "Starting development server at xxxxxxx", it means you have successfully started the Chatbox-Service.