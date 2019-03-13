from django.db import models
from datetime import datetime
from django.utils.timezone import datetime
from django.conf import settings



class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phoneNo = models.CharField(max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=50, default="xyz")
   # image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=100, default="kkkiiko")
    is_active = models.BooleanField(default=True)  # This field is used to active to deactive category

    def get_image_url(self):
     return settings.URLL+self.name
     pass


class Product(models.Model):
    #id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=50)
    # created_date = models.DateTimeField(auto_now_add=True, null=True)
    #updated_date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateField(default=datetime.now)
    updated_date = models.DateField(default=datetime.now)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)  # This field is used to active to deactive Products
   # image = models.ImageField(upload_to='dbimages/',null=True)
    """def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        else:
            return None"""
    '''def __str__(self):
        return self.id, self.name, self.user, self.category, self.price, self.description, self.created_date,\
               self.updated_date, self.quantity'''

class Service(models.Model):
    #id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Images(models.Model):
    # image_id = models.AutoField(primary_key=True, unique=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=50)

    def get_image_url(self):
        if not self.name=='':
         return settings.URLL+self.name
        else:
         pass


class Post(models.Model):
    #id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    likes = models.CharField(max_length=50)

class Comment(models.Model):
    #id = models.AutoField(primary_key=True, unique=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


