# Generated by Django 4.1.7 on 2023-07-10 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saladillo', '0002_maestrocliente_num_celular'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articulo', models.CharField(max_length=128)),
                ('descripcion', models.CharField(max_length=256)),
            ],
        ),
    ]