# Generated by Django 4.0 on 2022-02-26 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboards', '0003_alter_historicprice_close_alter_historicprice_high_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoricPrice',
        ),
    ]
