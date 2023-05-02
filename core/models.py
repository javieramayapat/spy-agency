from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")

        user = Hitman(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_hitman = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.name


class Manager(User):
    user = models.ManyToManyField(User, related_name="managers", blank=True)


class Hitman(User):
    pass


class ManagerUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="manager_user"
    )


class Hit(models.Model):
    STATUS_CHOICES = (
        ("failed", "Failed"),
        ("completed", "Completed"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    target_name = models.CharField(max_length=255)
    brief_description = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_hits"
    )
    assigned = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_hits",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.target_name}"
