# project/management/commands/user_groups_db.py:1
from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Chek and Add additional users groups of database."

    def handle(self, *args, **options):
        from persons import CATEGORY_STATUS

        try:
            Group.objects.all()
            self.stdout.write(self.style.SUCCESS("Database exists - all Successfully!"))
            [
                Group.objects.create(name=view[1])
                for view in CATEGORY_STATUS
                if Group.objects.filter(name=view[1]).count() == 0
            ]
            self.stdout.write(
                self.style.SUCCESS("Data was successfully added to database.")
            )
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(
                    "Database not found. Pleas create database and try again."
                )
            )
