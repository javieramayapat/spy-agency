from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import Hitman, Manager, ManagerUser

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_seed_data()
        self.stdout.write(
            self.style.SUCCESS("Seed data created successfully.")
        )


def create_seed_data():
    # Crea el big boss
    big_boss = User.objects.create(
        email="bigboss@example.com",
        is_superuser=True,
        is_staff=True,
        name="Giuseppi",
    )
    big_boss.set_password("password")
    big_boss.is_manager = False
    big_boss.is_hitman = False
    big_boss.save()

    big_boss = User.objects.get(id=1)

    # Crea 9 hitmen
    for i in range(1, 10):
        hitman = Hitman.objects.create(
            name=f"Hitman {i}", email=f"hitman{i}@example.com"
        )
        hitman.set_password("password")
        hitman.is_hitman = True
        hitman.is_manager = False
        hitman.save()

        manager_user = ManagerUser.objects.create(
            user_id=hitman.id, manager_id=big_boss.id
        )
        manager_user.save()

    # Crea 3 managers
    for i in range(1, 4):
        manager = Manager.objects.create(
            name=f"Manager {i}",
            email=f"manager{i}@example.com",
        )
        manager.set_password("password")
        manager.is_manager = True
        manager.is_hitman = False
        manager.save()

        manager_user = ManagerUser.objects.create(
            user_id=manager.id, manager_id=big_boss.id
        )
        manager_user.save()
