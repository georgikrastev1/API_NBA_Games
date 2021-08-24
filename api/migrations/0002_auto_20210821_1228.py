# Generated by Django 3.2.6 on 2021-08-21 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brands',
            options={'verbose_name_plural': 'Brands'},
        ),
        migrations.AlterModelOptions(
            name='games',
            options={'verbose_name_plural': 'Games'},
        ),
        migrations.AlterModelOptions(
            name='players',
            options={'verbose_name_plural': 'Players'},
        ),
        migrations.AlterModelOptions(
            name='scores',
            options={'verbose_name_plural': 'Scores'},
        ),
        migrations.AlterModelOptions(
            name='teams',
            options={'verbose_name_plural': 'Teams'},
        ),
        migrations.AlterField(
            model_name='games',
            name='team_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_1', to='api.teams'),
        ),
        migrations.AlterField(
            model_name='games',
            name='team_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_2', to='api.teams'),
        ),
    ]
