from rest_framework import serializers
from .models import Session, Question, Answer

class SessionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Session
    fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Question
    fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Answer
    fields = '__all__'

class QuestionCreateSerializer(serializers.ModelSerializer):
  session_id = serializers.IntegerField(required=True)

  class Meta:
    model = Question
    fields = ['session_id', 'text']

  def validate_session_id(self, value):
    if not Session.objects.filter(id=value).exists():
      raise serializers.ValidationError("Session does not exist.")
    return value

  def create(self, validated_data):
    session = Session.objects.get(id=validated_data['session_id'])
    return Question.objects.create(
        session_id=session,
        text=validated_data['text']
    )

