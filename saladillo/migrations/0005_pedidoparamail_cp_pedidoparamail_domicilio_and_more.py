# Generated by Django 4.1.7 on 2023-06-09 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saladillo', '0004_hojaruta'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidoparamail',
            name='cp',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedidoparamail',
            name='domicilio',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedidoparamail',
            name='estado_hr',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedidoparamail',
            name='localidad',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
    ]
