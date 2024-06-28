# Generated by Django 5.0.1 on 2024-05-14 07:25

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_color_remove_product_color_product_available_colors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='slug',
            new_name='the_slug',
        ),
        migrations.AlterField(
            model_name='color',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=None),
        ),
    ]
