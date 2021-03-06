
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from . import models
from . import forms


def test(request, *args, **kwargs):
    return HttpResponse('OK')

def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page, paginator

def main(request):
    question = models.Question.objects.new()
    page, paginator = paginate(request, question)
    paginator.baseurl = '/?page='
    return render(request, 'index.html', {
        'name': 'New',
        'questions': page.object_list,
        'paginator': paginator, 'page': page,
    })

def popular(request):
    questions = models.Question.objects.popular()
    page, paginator = paginate(request, questions)
    paginator.baseurl = '/popular/?page='
    return render(request, 'index.html', {
        'name': 'Popular',
        'questions': page.object_list,
        'paginator': paginator, 'page': page,
    })

def question(request, id):
    try:
        q = models.Question.objects.get(id=id)
    except models.Question.DoesNotExist:
        raise Http404
    if request.method == "POST":
        form = forms.AnswerForm(request.POST)
        form._user = request.user
        if form.is_valid():
            _ = form.save()
            url = q.get_url()
            return HttpResponseRedirect(url)
        else:
            question = get_object_or_404(models.Question, pk=id)
            answer = models.Answer.objects
            answer = answer.filter(question=question.pk)
            form = forms.AnswerForm()
            return render(request, 'question.html', {
                'question': question,
                'answers': answer,
                'form': form
            })
    else:
        question = get_object_or_404(models.Question, pk=id)
        answer = models.Answer.objects
        answer = answer.filter(question=question.pk)
        form = forms.AnswerForm()
        return render(request, 'question.html', {
            'question': question,
            'answers': answer,
            'form': form
        })

def question_add(request):
    if request.method == "POST":
        form = forms.AskForm(request.POST)
        form._user = request.user
        if form.is_valid():
            post = form.save()
            url = post.get_url()
            return HttpResponseRedirect(url)
        else:
            return render(request, 'ask.html', {
                'form': form
            })
    else:
        form = forms.AskForm()
    return render(request, 'ask.html', {
            'form': form
    })

def signup(request):
    if request.method == 'POST':
        form = forms.UserCreation(request.POST)
        if form.is_valid():
            post = form.save()
            return log_in(request)
        else:
            return render(request, 'signup.html', {
                    'form': form
            })
    else:
        form = forms.UserCreation()
    return render(request, 'signup.html', {
        'form': form
    })


def log_in(request):
    error = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                error = u'???????????????? ?????????? / ???????????? (is None){}'.format(user)
                return render(request, 'login.html', {'form': form,
                                                  'error': error})
        else:
            error = u'???????????????? ?????????? / ???????????? (is not valid)'
            return render(request, 'login.html', {'form': form,
                                                          'error': error})
    else:
        form = forms.LoginForm()
        return render(request, 'login.html', {'form': form,
                                              'error': error})

