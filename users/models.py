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
#    1->normal 2->subscribe 3->advSubcriber 4->vipSubcrisber  admin->admin
    permission = models.CharField(max_length=100, default='1')
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    lastSubscribeDate = models.DateField(null=True,blank=True)
    nowArticleSearch = models.IntegerField(default=0)
    nowArticleProduce = models.IntegerField(default=0)
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
    wordcloud = models.CharField(max_length=500)
    category = models.CharField(max_length=100,default='1')
    
    def _str_(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save()

    
class Article(models.Model):
    id = models.UUIDField(primary_key=True,default = uuid.uuid4, help_text='unique Id for this table')
    src = models.CharField(max_length=200)
    time = models.CharField(max_length=200,default='0')
    likes = models.CharField(max_length=200,default='0')
    commentCount = models.CharField(max_length=200,default='0')
    content = models.TextField(blank=True)
    pic = models.ImageField(default='default.jpg', upload_to='article_images')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='article')
    
    def _str_(self):
        return self.product.name

class ArticleTemplate(models.Model):
    id = models.UUIDField(primary_key=True,default = uuid.uuid4, help_text='unique Id for this table')
    creator = models.CharField(max_length=150);
    templatedType = models.CharField(max_length=150,blank=True);
    product_category = models.CharField(max_length=100,blank=True);
    catch = models.CharField(max_length=350,blank=True);
    preCatch =  models.CharField(max_length=350,blank=True);
    subCatch =  models.CharField(max_length=350,blank=True);
    headLine = models.CharField(max_length=350,blank=True);
    mainBody = models.TextField(blank=True);
    bodyText = models.TextField(blank=True);
    pattern = models.TextField(blank=True);
    description = models.CharField(max_length=350,blank=True);
    advantage_1 = models.TextField(blank=True);
    advantage_2 = models.TextField(blank=True);
    advantage_3 = models.TextField(blank=True);
    reason_1 = models.TextField(blank=True);
    reason_2 = models.TextField(blank=True);
    reason_3 = models.TextField(blank=True);
    slogan = models.TextField(blank=True);
    bodyPoint = models.CharField(max_length=350,blank=True);
    bodyCopy = models.TextField(blank=True);
