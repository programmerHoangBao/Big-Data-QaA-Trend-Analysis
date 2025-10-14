from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Session, Question, Answer
from .serializers import QuestionCreateSerializer
from chatbox import retriveval_based
from chatbox.kafka_hdfs_pipeline import KafkaToHDFSProducer
from chatbox.rabbitMQ_producer import RabbitMQProducer

# Create your views here.
@api_view(['POST'])
def create_session(request):
  session = Session.objects.create()
  return Response(
    {
      "message": "Session created successfully",
      "session_id": session.id,
      "created_at": session.create_at
    },
    status=status.HTTP_201_CREATED
  )
  
@api_view(['POST'])
def create_question(request):
  serializer = QuestionCreateSerializer(data=request.data)
  if serializer.is_valid():
    question = serializer.save()
    return Response({
            "message": "Question created successfully.",
            "data": {
                "question_id": question.id,
                "session_id": question.session_id.id,
                "text": question.text,
                "created_at": question.create_at
            }
        }, status=status.HTTP_201_CREATED)
  else:
    return Response({
            "message": "Invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['POST'])
def create_answer(request):
  question_id = request.query_params.get("question_id")
    
  if not question_id:
    return Response(
            {"message": "Missing 'question_id' parameter."},
            status=status.HTTP_400_BAD_REQUEST
          )
    
  try:
    question = Question.objects.get(id=question_id)
  except Question.DoesNotExist:
    return Response(
          {"message": f"Question with id {question_id} not found."},
          status=status.HTTP_404_NOT_FOUND
        )

  result = retriveval_based.search(question.text)
  
  if result and "message" not in result[0]:
    answer_text = result[0]['answer']
  else:
    answer_text = "Your question is beyond the system's understanding!"

  answer = Answer.objects.create(
      question=question,
      text=answer_text
  )
  
  # Send data to Kafka (automatically pushed to Hadoop via consumer).
  # producer = KafkaToHDFSProducer()
  # producer.send_message({
  #     "session_id": question.session_id.id,
  #     "question_id": question.id,
  #     "question": question.text,
  #     "answer": answer.text,
  #     "timestamp": str(answer.create_at)
  # })
  
  producer = RabbitMQProducer()
  producer.send_message({
    "session_id": question.session_id.id,
    "question_id": question.id,
    "question": question.text,
    "answer": answer.text,
    "timestamp": str(answer.create_at)
  })

  return Response({
        "message": "Answer created successfully.",
        "data": {
            "answer_id": answer.id,
            "question_id": question.id,
            "question_text": question.text,
            "answer_text": answer.text,
            "created_at": answer.create_at
        }
    }, status=status.HTTP_201_CREATED)

  
  
