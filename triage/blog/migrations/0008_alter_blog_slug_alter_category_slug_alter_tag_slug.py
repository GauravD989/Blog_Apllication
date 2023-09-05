# Generated by Django 4.2.4 on 2023-09-05 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_blog_slug_category_slug_tag_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='', unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='', unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='', unique=True),
        ),
    ]
