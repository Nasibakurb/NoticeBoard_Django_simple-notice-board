from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from ClothShop.forms import ProductForm, CommentForm
from .models import Product, Comment


@login_required
def edit_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm(instance=product)
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    return render(request, 'edit_product.html', {'form': form, 'product': product, 'username': username})


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm()
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    return render(request, 'create_product.html', {'form': form, 'username': username})


def index(request):
    username = None
    products = Product.objects.all()

    products_per_page = 4
    paginator = Paginator(products, products_per_page)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        username = request.user.username

    return render(request, 'index.html', {'username': username, 'products': products})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_view')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comments = Comment.objects.filter(product=product)
    comments_per_page = 2

    paginator = Paginator(comments, comments_per_page)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    return render(request, 'product_detail.html', {'product': product,
        'comments': comments, 'username': username})


def add_comment(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = CommentForm()

    comments = Comment.objects.filter(product=product)

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    return render(request, 'product_detail.html', {'product': product, 'form': form, 'comments': comments, 'username': username})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('product_detail', product_id=comment.product.id)

    return redirect('product_detail', product_id=comment.product.id)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()

    return redirect('index')
