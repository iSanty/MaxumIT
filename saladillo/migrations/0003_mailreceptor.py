# Generated by Django 4.1.7 on 2023-03-22 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saladillo', '0002_primerainstancia'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailReceptor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(max_length=128)),
            ],
        ),
    ]