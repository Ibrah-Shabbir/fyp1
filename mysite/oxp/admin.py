
from django.contrib import admin

from .models import User
from .models import Product
from .models import Category
from .models import Service
from .models import Images
from .models import Comment
from .models import Post

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Images)
admin.site.register(Comment)
admin.site.register(Post)

