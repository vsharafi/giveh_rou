# Generated by Django 5.0.6 on 2024-06-01 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0036_remove_color_farsi_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='farsi_name',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]