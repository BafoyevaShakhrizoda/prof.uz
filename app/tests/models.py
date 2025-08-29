from django.db import models
from app.users.models import BaseModel

class Test(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    total_questions = models.IntegerField()
    duration = models.IntegerField(help_text='Duration in minutes')
    
    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Testlar'
    
    def __str__(self):
        return self.title


class Question(BaseModel):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    
    def __str__(self):
        return self.text[:50]


class Answer(BaseModel):
    questions = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text
    
    
