# Generated by Django 4.0.5 on 2022-06-07 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_uuidtaggeditem_alter_post_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(),
        ),
    ]
