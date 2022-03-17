'''
Created on 2022年2月13日

@author: chu
'''
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid



# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=100, default='1')
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    
    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
            
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this table')
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    user = models.ForeignKey(Profile,  on_delete=models.CASCADE, related_name='product')
    category = models.CharField(max_length=100,default='1')
    
    def _str_(self):
        return self.name
    
class Article(models.Model):
    id = models.UUIDField(primary_key=True,default = uuid.uuid4, help_text='unique Id for this table')
    src = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    pic = models.ImageField(default='default.jpg', upload_to='article_images')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='article')
    
    def _str_(self):
        return self.product.name
