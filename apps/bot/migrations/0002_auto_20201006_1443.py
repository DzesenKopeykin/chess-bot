# Generated by Django 3.1 on 2020-10-06 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='board',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='color',
            field=models.CharField(choices=[('w', 'white'), ('b', 'black')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='in_game',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='opponent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.user'),
        ),
    ]
