# Generated by Django 4.1 on 2025-03-26 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='end_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='plated_end_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
