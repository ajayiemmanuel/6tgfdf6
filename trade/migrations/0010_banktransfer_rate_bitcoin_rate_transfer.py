# Generated by Django 5.0.7 on 2024-07-13 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0009_banktransfer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransfer',
            name='rate',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='bitcoin',
            name='rate',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('wallet', models.CharField(max_length=200, null=True)),
                ('bank', models.CharField(max_length=200, null=True)),
                ('accountnumber', models.CharField(max_length=200, null=True)),
                ('swift', models.CharField(max_length=200, null=True)),
                ('amount', models.CharField(max_length=200, null=True)),
                ('purpose', models.TextField(max_length=200, null=True)),
                ('time', models.DateField(auto_now=True)),
                ('transactionid', models.CharField(default='FDG637GDJYU**', max_length=200, null=True)),
                ('status', models.CharField(choices=[('Pending...', 'Pending...'), ('Approved', 'Approved'), ('Declined', 'Declined')], default='Pending...', max_length=200)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
