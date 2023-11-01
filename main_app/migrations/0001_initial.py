from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vinyl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('album', models.CharField(max_length=100)),
                ('tracks', models.IntegerField()),
                ('year', models.IntegerField()),
            ],
        ),
    ]
