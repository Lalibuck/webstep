from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class QuestionManager(models.Manager):

    def new(self):
        return self.order_by('-pk')

    def popular(self):
        return self.order_by('-rating')

class Question(models.Model):

    objects = QuestionManager()
    title = models.CharField(null=True, max_length=255)
    text = models.TextField(null=True)
    added_at = models.DateTimeField(null=True, auto_now_add=True)
    rating = models.IntegerField(null=True, default=0)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, null=True, related_name='liking_question_user')

    def get_url(self):
        return reverse('question', kwargs={'id': self.pk})

    def __str__(self):
        return self.title


class Answer(models.Model):

    text = models.TextField(null=True)
    added_at = models.DateTimeField(null=True, auto_now_add=True)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

