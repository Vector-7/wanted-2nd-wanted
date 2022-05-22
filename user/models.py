from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core.models import TimeStampedModel


class ModelUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,
                    email: str,
                    nickname: str,
                    password: str,
                    level: str = 'client'):

        if not email:
            raise ValueError('Email empty')
        if not nickname:
            raise ValueError('Nickname empty')
        if not password:
            raise ValueError('Password empty')

        level_map = {
            'admin': 0,
            'company_client': 1,
            'client': 2,
        }

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            level=level_map[level],
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        user = self.create_user(
            email=email,
            password=password,
            nickname=nickname,
            level='admin',
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimeStampedModel, PermissionsMixin):
    objects = ModelUserManager()

    USER_LEVEL = [
        (2, 'client'),
        (1, 'company_client'),
        (0, 'admin'),
    ]

    USER_LEVEL_MAP = {
        'client': 2,
        'company_client': 1,
        'admin': 2,
    }

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

    @property
    def is_staff(self):
        return self.level == 0

    def has_module_perms(self, app_label):
        return self.level == 0

    @property
    def is_superuser(self):
        return self.level == 0
