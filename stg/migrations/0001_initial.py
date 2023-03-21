# Generated by Django 4.1.7 on 2023-03-21 14:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='clientes_emails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField()),
                ('nombre', models.CharField(max_length=128)),
                ('email_1', models.EmailField(db_column='emal 1', max_length=254)),
                ('email_2', models.EmailField(db_column='emal 2', max_length=254)),
                ('email_3', models.EmailField(db_column='emal 3', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='pedidos',
            fields=[
                ('numero', models.IntegerField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(null=datetime.date(2023, 3, 21))),
                ('codigo_cliente', models.IntegerField()),
                ('codigo_articulo', models.CharField(max_length=128)),
                ('cantidad', models.IntegerField()),
                ('importe', models.IntegerField()),
                ('importe_total_comprobante', models.IntegerField()),
                ('fechavencimiento1', models.DateField(null=True)),
                ('ordendecompra', models.CharField(max_length=128)),
                ('fecha_entrega', models.DateField(null=True)),
            ],
        ),
    ]
