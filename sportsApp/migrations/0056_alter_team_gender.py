# Generated by Django 4.2.7 on 2024-09-02 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsApp', '0055_alter_transaction_transaction_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='gender',
            field=models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHERS', 'Others')], max_length=25, null=True),
        ),
    ]