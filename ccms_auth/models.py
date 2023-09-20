from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    is_locked = models.BooleanField(default=False)
    login_failures = models.PositiveIntegerField(default=0)
    last_login_attempt = models.DateTimeField(null=True, blank=True)

    @classmethod
    def create_user(cls, username, password=None, **extra_fields):
        """
        사용자 생성을 처리하는 사용자 정의 메서드
        """
        if not username:
            raise ValueError('The Username field must be set')
        now = timezone.now()
        user = cls(username=username, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=cls._db)
        return user
