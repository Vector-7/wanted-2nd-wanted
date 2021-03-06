# Generated by Django 4.0.4 on 2022-05-26 00:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='회사 생성한 사람'),
        ),
        migrations.AddConstraint(
            model_name='companytagitem',
            constraint=models.UniqueConstraint(fields=('tag', 'language', 'name'), name='company_tag_unique'),
        ),
        migrations.AddConstraint(
            model_name='companyname',
            constraint=models.UniqueConstraint(fields=('language', 'name'), name='company_language_unique'),
        ),
    ]
