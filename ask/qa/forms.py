from django import forms
from . import models

def is_valid(form):
    return True

def is_digit(form):
    if str(form).isdigit():
        return True
    else:
        return False

class AskForm(forms.Form):
    title = forms.CharField(label='title', max_length=100)
    text = forms.CharField(label='text', widget=forms.Textarea)

    def clean_ask(self):
        title = self.cleaned_data['title']
        if not is_valid(title):
            raise forms.ValidationError(
                u'Некорректные данные'
            )
        return title

    def save(self):
        question = models.Question(**self.cleaned_data)
        question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.CharField(label='text', widget=forms.Textarea)
    question = forms.IntegerField(label='question')

    def clean_question(self):
        question_id = self.cleaned_data['question']
        try:
            question = models.Question.objects.get(id=question_id)
        except models.Question.DoesNotExist:
            question = None
        return question

    def save(self):
        answer = models.Answer(**self.cleaned_data)
        answer.save()
        return answer