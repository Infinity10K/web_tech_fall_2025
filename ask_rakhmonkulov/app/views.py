from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST

from app.forms import LoginForm, RegisterForm
from app.models import Question, Answer, Profile, QuestionLike

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
    questions = Question.objects.annotate(likes_count=Count('question_like')).all()
    page = paginate(request, questions)

    return render(request, 'index.html', context={
        'questions': page.object_list,
        'page_obj': page,
    })

def hot(request):
    questions = Question.objects.annotate(likes_count=Count('question_like')).all()[::-1]
    page = paginate(request, questions)

    print(page)

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
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def users(request):
    profiles = Profile.objects.all()

    return render(request, 'users.html', context={
        'profiles': profiles,
    })

@require_POST
@login_required
def like_question(request, question_id):
    profile = Profile.objects.get(id=request.user.id)
    question = Question.objects.annotate(likes_count=Count('question_like')).get(id=question_id)
    question_like, is_created = QuestionLike.objects.get_or_create(question=question, profile=profile)

    if not is_created:
        question_like.delete()

    return JsonResponse({'likeCount': question.likes_count})
