'''
Created on 2022年2月14日

@author: chu
'''
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default.jpg', upload_to='profile_images'),
        ),
    ]