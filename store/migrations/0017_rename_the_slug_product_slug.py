# Generated by Django 5.0.1 on 2024-05-14 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_rename_slug_product_the_slug_alter_color_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='the_slug',
            new_name='slug',
        ),
    ]
