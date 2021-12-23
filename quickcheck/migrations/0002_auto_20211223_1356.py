# Generated by Django 3.2.9 on 2021-12-23 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickcheck', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': '城市', 'verbose_name_plural': '城市'},
        ),
        migrations.AddField(
            model_name='city',
            name='summary',
            field=models.TextField(default=1, max_length=100, verbose_name='概览'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='city',
            name='policy',
            field=models.TextField(max_length=10000, verbose_name='详细政策'),
        ),
    ]