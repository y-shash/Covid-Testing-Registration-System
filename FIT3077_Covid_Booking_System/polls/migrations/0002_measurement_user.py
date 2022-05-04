# Generated by Django 4.0.4 on 2022-04-28 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=200)),
                ('distance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('givenName', models.CharField(max_length=200)),
                ('familyName', models.CharField(max_length=200)),
                ('userName', models.CharField(max_length=200)),
                ('phoneNumber', models.IntegerField(default=0)),
                ('isCustomer', models.BooleanField(default=False)),
                ('isReceptionist', models.BooleanField(default=False)),
                ('isHealthcareWorker', models.BooleanField(default=False)),
            ],
        ),
    ]
