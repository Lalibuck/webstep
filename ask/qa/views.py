from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from models import Question


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
    question = Question.objects.new()
    page, paginator = paginate(request, question)
    paginator.baseurl = '/?page='
    page = paginator.page(page)
    return render(request, 'index.html', {
        'questions': page.object_list,
        'paginator': paginator, 'page': page,
    })

def popular(request):
    question = Question.objects.popular()
    page, paginator = paginate(request, question)
    paginator.baseurl = '/popular/?page='
    page = paginator.page(page)
    return render(request, 'index.html', {
        'questions': page.object_list,
        'paginator': paginator, 'page': page,
    })

def question(request, id):
    question = get_object_or_404(Question, slug=id)
    return render(request, 'blog/post_details.html', {
        'question': question,
    })