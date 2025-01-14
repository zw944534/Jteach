# Generated by Django 3.2.7 on 2022-08-03 15:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_articletemplate_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='lastSubscribeDate',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='nowArticleProduce',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='nowArticleSearch',
            field=models.IntegerField(default=0),
        ),
    ]
