from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных

def recipes_view(request, dish):
    """Отображает рецепт для указанного блюда"""

    # Получаем количество порций из GET-параметра
    servings = request.GET.get('servings', 1)

    try:
        servings = int(servings)
    except ValueError:
        servings = 1

    # Проверяем, есть ли такое блюдо в базе данных
    if dish not in DATA:
        return HttpResponse(f'Рецепт для блюда "{dish}" не найден', status=404)

    # Получаем оригинальный рецепт
    recipe = DATA[dish]

    # Масштабируем ингредиенты в зависимости от количества порций
    scaled_recipe = {}
    for ingredient, amount in recipe.items():
        scaled_recipe[ingredient] = amount * servings

    # Подготавливаем контекст для шаблона
    context = {
        'recipe_name': dish,
        'recipe': scaled_recipe,
        'servings': servings,
    }

    return render(request, 'calculator/index.html', context)


def home_view(request):
    """Главная страница со списком доступных рецептов"""
    context = {
        'recipes': list(DATA.keys())
    }
    return render(request, 'calculator/home.html', context)

# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
