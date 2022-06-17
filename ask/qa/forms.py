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

    def clean(self):
        title = self.cleaned_data['title']
        if not is_valid(title):
            raise forms.ValidationError(
                u'Некорректные данные'
            )
        return title

    def save(self):
        ask = models.Question()
        ask.save()
        return ask

class AnswerForm(forms.Form):
    text = forms.CharField()
    question = forms.IntegerField(label='question')

    def clean(self):
        question = self.cleaned_data['question']
        if not is_digit(question):
            raise forms.ValidationError(
                u'Некорректные данные'
            )
        return question

    def save(self):
        ask = models.Answer()
        ask.save()
        return ask