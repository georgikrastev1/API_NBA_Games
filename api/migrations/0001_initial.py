# Generated by Django 3.2.6 on 2021-08-21 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_date', models.DateField()),
                ('team_1', models.CharField(max_length=100)),
                ('team_2', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Signed_contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date_contract', models.DateField()),
                ('end_date_contract', models.DateField()),
                ('brand_signed_with', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.brands')),
                ('player_signed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.players')),
            ],
        ),
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scored_points', models.IntegerField()),
                ('game_scored', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.games')),
                ('player_scored', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.players')),
            ],
        ),
        migrations.AddField(
            model_name='players',
            name='player_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.teams'),
        ),
    ]