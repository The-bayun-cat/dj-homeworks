from django.shortcuts import render, get_object_or_404, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'

    # Получаем параметр сортировки
    sort = request.GET.get('sort', '')

    # Получаем все телефоны
    phones = Phone.objects.all()

    # Применяем сортировку
    if sort == 'name':
        phones = phones.order_by('name')
    elif sort == 'min_price':
        phones = phones.order_by('price')
    elif sort == 'max_price':
        phones = phones.order_by('-price')

    context = {
        'phones': phones
    }

    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'

    # Находим телефон по slug
    phone = get_object_or_404(Phone, slug=slug)

    context = {
        'phone': phone
    }

    return render(request, template, context)