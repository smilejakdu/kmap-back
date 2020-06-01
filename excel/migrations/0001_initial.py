# Generated by Django 3.0.3 on 2020-06-01 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Plate_No', models.IntegerField(null=True)),
                ('Replicate_No', models.IntegerField(null=True)),
                ('Well_No', models.IntegerField(null=True)),
                ('Index_No', models.IntegerField(default=0)),
                ('KaiChem_ID', models.CharField(max_length=250, null=True, verbose_name='카이참')),
                ('Conc_nM', models.IntegerField(default=0)),
                ('Cell', models.CharField(max_length=250, null=True, verbose_name='세포')),
                ('Time', models.IntegerField(default=0)),
                ('RNA_Ext_Date', models.IntegerField(default=0)),
                ('Lib_Prep_Date', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'gene_datas',
            },
        ),
    ]
