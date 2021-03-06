# Generated by Django 3.1 on 2020-10-06 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20201006_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='board',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='color',
            field=models.CharField(blank=True, choices=[('w', 'white'), ('b', 'black')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='opponent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.user'),
        ),
    ]
