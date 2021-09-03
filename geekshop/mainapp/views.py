from django.shortcuts import render
from mainapp.models import Product


def main(request):
    title = 'Главная'
    products = Product.objects.all()[:4]
    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)


def products(request):
    title = 'Каталог'
    products = Product.objects.all()
    content = {'title': title, 'products': products}
    return render(request, 'mainapp/products.html', content)


def contact(request):
    title = 'Контакты'
    content = {'title': title}
    return render(request, 'mainapp/contact.html', content)

