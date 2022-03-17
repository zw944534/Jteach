'''
Created on 2022年2月14日

@author: chu
'''
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
