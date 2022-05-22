# Generated by Django 4.0.4 on 2022-05-22 15:12

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='고유 이메일 주소')),
                ('nickname', models.CharField(max_length=32, unique=True, verbose_name='사용자 이름')),
                ('level', models.IntegerField(choices=[('client', 2), ('company_client', 1), ('admin', 0)], default=2, verbose_name='사용자 레벨(client=2,company=1,admin=0)')),
            ],
            options={
                'db_table': 'user',
            },
            managers=[
                ('objects', user.models.ModelUserManager()),
            ],
        ),
    ]
