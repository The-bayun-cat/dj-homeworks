import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    help = 'Импорт телефонов из CSV файла'

    def handle(self, *args, **options):
        # Очищаем существующие данные (опционально)
        Phone.objects.all().delete()

        with open('phones.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                try:
                    phone = Phone(
                        id=int(row['id']),
                        name=row['name'],
                        price=float(row['price']),
                        image=row['image'],
                        release_date=datetime.strptime(row['release_date'], '%Y-%m-%d').date(),
                        lte_exists=row['lte_exists'].lower() == 'true',
                        slug=''  # slug будет сгенерирован автоматически при save()
                    )
                    phone.save()
                    self.stdout.write(self.style.SUCCESS(f'Успешно импортирован: {phone.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Ошибка при импорте {row["name"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Импорт завершен!'))