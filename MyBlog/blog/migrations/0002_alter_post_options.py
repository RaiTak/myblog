# Generated by Django 5.0.3 on 2024-03-20 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Статью', 'verbose_name_plural': 'Статьи'},
        ),
    ]