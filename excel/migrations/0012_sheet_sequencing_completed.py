# Generated by Django 3.0.3 on 2021-01-11 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0011_auto_20201211_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheet',
            name='Sequencing_Completed',
            field=models.CharField(max_length=250, null=True),
        ),
    ]