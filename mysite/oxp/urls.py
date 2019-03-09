from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('simple/', csrf_exempt(views.create_product), name='create_product'),
    #path('get/', views.get_products, name='get_products'),
    #path('del/', views.delete_product, name='delete_product'),
    #path('update/', csrf_exempt(views.update_product), name='update_product'),
    path('login/', csrf_exempt(views.login), name="Login"),
    path('signup/', csrf_exempt(views.signup), name="Signup"),
    #path('get_specific_products/',csrf_exempt(views.get_specific_products),name='get_specific_products'),
    path('product/',csrf_exempt(views.product),name='product'),
    path('service/',csrf_exempt(views.service),name='service'),
    #path('raw/',views.raw,name='raw'),
    path('category/',csrf_exempt(views.category),name='category'),
]
