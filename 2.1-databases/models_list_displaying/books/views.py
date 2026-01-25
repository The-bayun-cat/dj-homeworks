# books/views.py
from django.shortcuts import render, get_object_or_404
from .models import Book
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, date


def books_view(request):
    template = 'books/books_list.html'

    # Получаем все книги, отсортированные по дате
    books = Book.objects.all().order_by('pub_date')

    context = {'books': books}
    return render(request, template, context)


def books_by_date_view(request, pub_date):
    template = 'books/books_list.html'

    # Преобразуем строку даты в объект date
    try:
        target_date = datetime.strptime(pub_date, '%Y-%m-%d').date()
    except ValueError:
        # Если дата некорректная, показываем все книги
        books = Book.objects.all().order_by('pub_date')
        context = {'books': books}
        return render(request, template, context)

    # Получаем книги для указанной даты
    books = Book.objects.filter(pub_date=target_date).order_by('pub_date')

    # Получаем предыдущую и следующую даты с книгами
    prev_date = Book.objects.filter(pub_date__lt=target_date).order_by('-pub_date').first()

    next_date = Book.objects.filter(pub_date__gt=target_date).order_by('pub_date').first()

    context = {
        'books': books,
        'pub_date': target_date,
        'prev_date': prev_date.pub_date if prev_date else None,
        'next_date': next_date.pub_date if next_date else None,
    }
    return render(request, template, context)


