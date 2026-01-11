import csv
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    current_page = request.GET.get('page', 1)

    # Читаем данные из CSV файла
    stations_list = []
    try:
        # Открываем CSV файл с указанной кодировкой
        with open(settings.BUS_STATION_CSV, 'r', encoding='utf-8') as csvfile:
            # Используем DictReader для удобного доступа к данным по именам колонок
            reader = csv.DictReader(csvfile)

            # Проходим по всем строкам в файле
            for row in reader:
                # Формируем словарь с данными об остановке
                station = {
                    'Name': row.get('Name', '').strip(),
                    'Street': row.get('Street', '').strip(),
                    'District': row.get('District', '').strip(),
                }
                stations_list.append(station)

    except FileNotFoundError:
        # Если файл не найден, используем пустой список
        stations_list = []
    except Exception as e:
        # Для отладки можно вывести ошибку
        # print(f"Ошибка при чтении файла: {e}")
        stations_list = []

    # Создаем пагинатор - 10 элементов на страницу
    paginator = Paginator(stations_list, 10)

    # Получаем объект текущей страницы
    page_obj = paginator.get_page(current_page)

    # также передайте в контекст список станций на странице
    context = {
        'bus_stations': page_obj.object_list,  # Список станций на текущей странице
        'page': page_obj,  # Объект текущей страницы с информацией о пагинации
    }
    return render(request, 'stations/index.html', context)