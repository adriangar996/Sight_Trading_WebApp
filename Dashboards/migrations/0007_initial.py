# Generated by Django 4.0 on 2022-03-08 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Dashboards', '0006_delete_predictions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Predictions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(default='', max_length=1)),
                ('day1', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('day5', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('day14', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('day30', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('day90', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
    ]
