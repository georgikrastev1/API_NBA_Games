# Generated by Django 3.2.6 on 2021-08-22 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_wins'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Scores',
            new_name='Player_Scores',
        ),
        migrations.AlterModelOptions(
            name='wins',
            options={'verbose_name_plural': 'Wins'},
        ),
    ]
