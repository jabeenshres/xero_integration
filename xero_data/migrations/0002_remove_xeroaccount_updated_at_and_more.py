# Generated by Django 5.1.7 on 2025-03-27 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xero_data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xeroaccount',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='xeroaccount',
            name='add_to_watchlist',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='xeroaccount',
            name='bank_account_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='xeroaccount',
            name='class_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='xeroaccount',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='xeroaccount',
            name='enable_payments_to_account',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='xeroaccount',
            name='has_attachments',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='xeroaccount',
            name='reporting_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='xeroaccount',
            name='reporting_code_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='xeroaccount',
            name='show_in_expense_claims',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='xeroaccount',
            name='system_account',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='xeroaccount',
            name='updated_date_utc',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='xeroaccount',
            name='account_id',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='xeroaccount',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='xeroaccount',
            name='tax_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='xeroaccount',
            name='type',
            field=models.CharField(max_length=50),
        ),
    ]
