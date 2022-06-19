from django import forms
from django.contrib.auth.hashers import make_password

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
        question.author_id = self._user.id
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
        answer.author_id = self._user.id
        answer.save()
        return answer


class UserCreation(forms.Form):
    username = forms.CharField(label='username')
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError('Не задано имя пользователя')
        try:
            models.User.objects.get(username=username)
            raise forms.ValidationError('Такой пользователь уже существует')
        except models.User.DoesNotExist:
            pass
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError('Не указан адрес электронной почты')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError('Не указан пароль')
        self.raw_password = password
        return make_password(password)

    def save(self):
        user = models.User(**self.cleaned_data)
        user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password')


    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError('Не задано имя пользователя')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError('Не указан пароль')
        return password
