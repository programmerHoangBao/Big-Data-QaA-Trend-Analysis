from django.db import models

# Create your models here.
class Session(models.Model):
  id = models.BigAutoField(primary_key=True)
  create_at = models.DateTimeField(auto_now_add=True)
  modify_at = models.DateTimeField(auto_now=True)
  is_deleted = models.BooleanField(default=False)
  
  def __str__(self):
    return f"Session {self.id}"
  
class Question(models.Model):
  id = models.BigAutoField(primary_key=True)
  session_id = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="questions")
  text = models.TextField()
  create_at = models.DateTimeField(auto_now_add=True)
  modify_at = models.DateTimeField(auto_now=True)
  is_deleted = models.BooleanField(default=False)
  
  def __str__(self):
    return f"Question {self.id} - {self.text[:50]}"
  
class Answer(models.Model):
  id = models.BigAutoField(primary_key=True)
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
  text = models.TextField()
  create_at = models.DateTimeField(auto_now_add=True)
  modify_at = models.DateTimeField(auto_now=True)
  is_deleted = models.BooleanField(default=False)

  def __str__(self):
    return f"Answer to Q{self.question.id} - {self.text[:50]}"
