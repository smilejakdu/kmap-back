# Generated by Django 3.1.2 on 2020-11-05 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0009_auto_20201104_1557'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sheet',
            old_name='Library_Prep_Date',
            new_name='Library_Prep_date',
        ),
        migrations.AlterField(
            model_name='sheet',
            name='Compound_treatment_time',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='Replicate',
            field=models.CharField(max_length=100, null=True),
        ),
    ]