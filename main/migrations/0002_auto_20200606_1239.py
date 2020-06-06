# Generated by Django 3.0.6 on 2020-06-06 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categoty',
            new_name='Category',
        ),
        migrations.AlterField(
            model_name='institution',
            name='institution_type',
            field=models.SmallIntegerField(choices=[(0, 'Fundacja'), (1, 'Organizacja pozarządowa'), (2, 'Zbiórka lokalna')], default=0),
        ),
    ]
