from django.db import models

from core.models import TimeStampedModel
from user.models import User


class Company(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='회사 생성한 사람', )

    class Meta:
        db_table = 'company'


class CompanyContents(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    summary = models.TextField(verbose_name='소개글', default='', null=False)

    class Meta:
        db_table = 'company_contents'


class CompanyName(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'company_name'


class CompanyNameLanguage(models.Model):
    company_name = models.ForeignKey(CompanyName, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, null=False, blank=False)

    class Meta:
        db_table = 'company_name_language'


class CompanyTag(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'company_tag'
        constraints = [
            models.UniqueConstraint(
                fields=('company', 'language', 'name'),
                name='unique tag',
            ),
        ]

