from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy

from app.forms import LoginForm, RegisterForm
from app.models import Question, Answer


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


@login_required(login_url=reverse_lazy('login'))
def index(request):
    questions = Question.objects.all()
    page = paginate(request, questions)

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
    one_question = Question.objects.get(id=question_id)
    answers = Answer.objects.filter(question=one_question)
    page = paginate(request, answers)

    return render(request, 'question.html', context={
        'question': one_question,
        'answers': page.object_list,
        'page_obj': page,   
    })

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

