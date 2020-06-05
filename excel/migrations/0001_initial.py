# Generated by Django 3.0.3 on 2020-06-04 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Excel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'excels',
            },
        ),
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, null=True)),
                ('Plate_No', models.IntegerField(null=True)),
                ('Replicate_No', models.IntegerField(null=True)),
                ('Well_No', models.CharField(max_length=250, null=True)),
                ('Index_No', models.IntegerField(default=0)),
                ('KaiChem_ID', models.CharField(max_length=250, null=True, verbose_name='카이참')),
                ('Conc_nM', models.IntegerField(default=0)),
                ('Cell', models.CharField(max_length=250, null=True, verbose_name='세포')),
                ('Time', models.IntegerField(default=0)),
                ('RNA_Ext_Date', models.IntegerField(default=0)),
                ('Lib_Prep_Date', models.IntegerField(default=0)),
                ('Seq_Req_Date', models.IntegerField(default=0)),
                ('NGS_Data_Date', models.IntegerField(default=0)),
                ('excel_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='excel.Excel')),
            ],
            options={
                'db_table': 'sheets',
            },
        ),
    ]
