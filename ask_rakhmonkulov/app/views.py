from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [{
    'id': i,
    'title': f'Title #{i}',
    'text': 'Text',
} for i in range(30)]

ANSWERS = [{
    'id': i,
    'username': f'User #{i}',
    'text': 'Answer Text',
} for i in range(30)]


def paginate(request, objects, per_page=5):
    page_num = int(request.GET.get('page', 1))

    paginator = Paginator(objects, per_page)

    page = paginator.page(page_num)

    return page


def index(request):
    page = paginate(request, QUESTIONS)

    return render(request, 'index.html', context={
        'questions': page.object_list,
        'page_obj': page,
    })

def hot(request):
    page = paginate(request, QUESTIONS[::-1])

    return render(request, 'hot.html', context={
        'questions': page.object_list,
        'page_obj': page,
    })

def question(request, question_id):
    one_question = QUESTIONS[question_id]

    page = paginate(request, ANSWERS)

    return render(request, 'question.html', context={
        'question': one_question,
        'answers': page.object_list,
        'page_obj': page,   
    })