from django.core.management.base import BaseCommand
from pyexcel_odsr import get_data

from apps.core.models import Color, Faction


class Command(BaseCommand):
    help = 'core.Factions, core.Colors'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        data = get_data("database.ods")

        # ЗАГРУЗКА core.Faction
        factions = data["Faction"]
        # print(factions)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем core.Faction'))
        for line in factions[1:]:
            if line:
                try:
                    Faction.objects.create(
                        name=line[1]
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------

        # Загрузка core.Color
        colors = data["Color"]
        # print(colors)

        success = 0
        failed = 0
        self.stdout.write(self.style.SUCCESS(f'Загружаем core.Color'))
        for line in colors[1:]:
            if line:
                try:
                    Color.objects.create(
                        name=line[1]
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно, {success}'))
        self.stdout.write(self.style.ERROR(f'Провалено, {failed}'))
        # -----------------------------------------------------------
