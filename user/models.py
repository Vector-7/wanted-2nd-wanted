from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from core.models import TimeStampedModel


class ModelUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email: str, nickname: str,  password: str, level: str = 'client'):

        if not email:
            raise ValueError('Email empty')
        if not nickname:
            raise ValueError('Nickname empty')
        if not password:
            raise ValueError('Password empty')

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            level=level
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, last_name, first_name, password):
        user = self.create_user(
            email=email,
            password=password,
            nickname=nickname,
            level='admin',
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimeStampedModel):

    objects = ModelUserManager()

    USER_LEVEL = [
        ('client', 2),
        ('company_client', 1),
        ('admin', 0),
    ]

    email = models.EmailField(
        verbose_name='고유 이메일 주소',
        unique=True,
        max_length=255,
        null=False,
        blank=False,
    )
    nickname = models.CharField(
        verbose_name='사용자 이름',
        unique=True,
        max_length=32,
        null=False,
        blank=False,
    )
    level = models.IntegerField(
        verbose_name='사용자 레벨(client=2,company=1,admin=0)',
        default=2,
        null=False,
        choices=USER_LEVEL,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        db_table = 'user'
