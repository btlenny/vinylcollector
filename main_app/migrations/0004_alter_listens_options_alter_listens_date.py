# Generated by Django 4.2.6 on 2023-11-01 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_listens_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listens',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='listens',
            name='date',
            field=models.DateField(verbose_name='Feeding date'),
        ),
    ]