import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import time


class UserManager(BaseUserManager):
    def create_user(self, username, email, firstName, lastName, password=None):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            firstName=firstName,
            lastName=lastName,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)

    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)

    # Unix timestamp fields
    createdAt = models.BigIntegerField(default=int(time.time() * 1000))
    updatedAt = models.BigIntegerField(default=int(time.time() * 1000))

    # User fields
    createdBy = models.CharField(
        null=True,
        blank=False,
    )
    updatedBy = models.CharField(
        null=True,
        blank=False,
    )
    isDeleted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "firstName", "lastName"]

    class Meta:
        db_table = "user"
