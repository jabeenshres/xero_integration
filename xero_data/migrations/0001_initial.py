# Generated by Django 5.1.7 on 2025-03-27 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='XeroAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('tax_type', models.CharField(blank=True, max_length=100, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
