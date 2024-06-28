# Generated by Django 5.0.6 on 2024-05-23 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_product_rating_product_reviews_alter_product_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='picture',
            field=models.ImageField(default=1, upload_to='static/store/images/category'),
            preserve_default=False,
        ),
    ]
