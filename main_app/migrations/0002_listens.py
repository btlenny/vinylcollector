# Generated by Django 4.2.6 on 2023-11-01 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('rating', models.CharField(choices=[('B', 'Bad'), ('N', 'Neutral'), ('G', 'Great')], default='B', max_length=1)),
                ('vinyl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.vinyl')),
            ],
        ),
    ]