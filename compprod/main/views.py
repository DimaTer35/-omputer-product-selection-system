from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q

from django.shortcuts import render
from .models import Product, ProductAttributeValue, Favorites, Category, AnswerOption, Question


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    attributes = ProductAttributeValue.objects.filter(product=product)
    return render(request, 'product_detail.html', {'product': product, 'attributes': attributes})


def product_list(request):
    category_id = request.GET.get('category')
    sort = request.GET.get('sort')
    search_query = request.GET.get('search')
    cpu_freq = request.GET.getlist('cpu_freq')
    ram_size = request.GET.getlist('ram_size')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()
    categories = Category.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(manufacturer__name__icontains=search_query)
        )

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if '2.5' in cpu_freq:
        products = products.filter(id=26)
    elif '3.4' in cpu_freq:
        products = products.filter(id=27)

    if '32' in ram_size:
        products = products.filter(id=26)
    elif '16' in ram_size:
        products = products.filter(id=27)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    context = {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'sort': sort,
        'search_query': search_query,
        'cpu_freq': cpu_freq,
        'ram_size': ram_size,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'product_list.html', context)


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        user = request.user
        user.username = username
        user.email = email
        user.save()

        return redirect('profile')

    return render(request, 'profile.html')


@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorites.objects.get_or_create(user=request.user, product=product)
    if created:
        return render(request, 'favorite_added.html', {'product': product})
    else:
        return render(request, 'favorite_exists.html', {'product': product})

@login_required
def favorite_list(request):
    favorites = Favorites.objects.filter(user=request.user).select_related('product')
    return render(request, 'favorite_list.html', {'favorites': favorites})

@login_required
def remove_favorite(request, favorite_id):
    favorite = get_object_or_404(Favorites, id=favorite_id, user=request.user)
    if request.method == 'POST':
        favorite.delete()
    return redirect('favorite_list')


def expert_system(request):
    questions = Question.objects.all()
    if request.method == 'POST':
        answers = {}
        for question in questions:
            answer = request.POST.get(f'question_{question.id}')
            answers[question.id] = answer

        recommended_products = Product.objects.all()

        for question_id, answer_text in answers.items():
            if question_id == 1:
                category = Category.objects.filter(name__iexact=answer_text).first()
                if category:
                    recommended_products = recommended_products.filter(category=category)
            elif question_id == 2:
                try:
                    budget = float(answer_text)
                    recommended_products = recommended_products.filter(price__lte=budget)
                except ValueError:
                    pass
            elif question_id == 3:  # Цель использования
                if answer_text == "Офисная работа и интернет серфинг":
                    recommended_products = recommended_products.filter(id__in=[12, 13, 16, 17])
                elif answer_text == "Игры":
                    recommended_products = recommended_products.filter(id__in=[8, 9, 10, 14])
                elif answer_text == "Графический дизайн и видеомонтаж":
                    recommended_products = recommended_products.filter(id__in=[8, 9, 10, 11, 14, 15])
                elif answer_text == "Программирование и разработки":
                    recommended_products = recommended_products.filter(sid__in=[10, 11, 12, 13, 15])
            elif question_id == 4:  # Бренд
                if answer_text == "Да, хочу выбирать из известных брендов.":
                    recommended_products = recommended_products.filter(id__in=[8, 10, 12, 15, 16])
                elif answer_text == "Нет, бренд не имеет значения.":
                    recommended_products = recommended_products.filter(id__in=[9, 11, 13, 14, 17])
            elif question_id == 5:  # Внешний вид
                if answer_text == "Да, хочу стильные и красивые компоненты":
                    recommended_products = recommended_products.filter(id__in=[10, 8, 14, 15])
                elif answer_text == "Нет, внешний вид не имеет значения":
                    recommended_products = recommended_products.filter(id__in=[8, 9, 10, 11, 12, 13, 14, 15, 16, 17])

        if recommended_products.count() > 1:
            recommended_products = recommended_products.order_by('-price')[:1]

        return render(request, 'expert_system_result.html', {'products': recommended_products})

    return render(request, 'expert_system.html', {'questions': questions})






