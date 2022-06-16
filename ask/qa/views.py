from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from . import models


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
    question = get_object_or_404(models.Question, pk=id)
    answer = models.Answer.objects
    answer = answer.filter(question=question.pk)
    return render(request, 'question.html', {
        'question': question,
        'answers': answer,
    })