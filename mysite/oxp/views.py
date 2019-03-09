import time

from django.http import HttpResponse
import json
from django.shortcuts import get_object_or_404
import datetime
#from django.utils import timezone
#from django.core.files.images import ImageFile
from Lib import os, base64
#from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
from .models import User, Category, Product, Images, Service
from .myUtils import *


#import cloudinary
#import cloudinary.uploader
#import cloudinary.api
#from rest_framework.decorators import api_view
#from .serializers import ProductSerializer
#from .serializers import UserSerializer
#import string
#from django.contrib.auth import login, authenticate
#from django.contrib.auth.forms import UserCreationForm

#from django.contrib.auth.hashers import make_password, check_password


def index(request):
    print(settings.MEDIA_ROOT)
    return HttpResponse("Hello, world. You're at the student index in FYPPPPPP111111111.")


def login(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        #email=request.POST.get('email')
        email = json_data['email']
        print(email)
        password=request.POST.get('password')
        password = json_data['password']
        print(password)
        list=[]
        if User.objects.filter(email__iexact=email).filter(password__exact=password).exists():
            user=User.objects.get(email=email)
            response_dict = dict()
            response_dict['f_name']=user.f_name
            response_dict['l_name']=user.l_name
            response_dict['id']=user.id
            response_dict['email']=user.email
            response_dict['contact_no']=user.phoneNo
            list.append(response_dict)
            response={
                "data":list,
                'status_code': "200"
                         }
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            response = {
                "data": "user does not exist",
                'status_code': "404"
            }
            return HttpResponse(json.dumps(response), content_type="application/json")

    return HttpResponse(json.dumps('LOGIN REQUEST METHOD UNIDENTIFIED!'), content_type="application/json")


def signup(request):
    if request.method == "POST":
        json_data = json.loads(request.body) #Fetching JSON data
        l_name = json_data['l_name']
        f_name = json_data['f_name']
        city = json_data['city']
        address = json_data['address']
        phone = json_data['phoneNo']
        email = json_data['email']
        # To encrypt the password. This creates a password hash with a random salt.
        password = json_data['password']
        #password_hash = make_password(json_data['password'])
        #password = password_hash
        if not (User.objects.filter(email__iexact=email).exists()):
            if User.objects.create(f_name=f_name, l_name=l_name, city=city, address=address,
                        phoneNo=phone, email=email, password=password):

                return HttpResponse('Data Has been added!', content_type="application/json")
            else:
                return HttpResponse('Signup! unable to add user', content_type="application/json")
        else:
            return HttpResponse('Signup! user with this email already exists', content_type="application/json")

    else:
        return HttpResponse("SIGNUP REQUEST METHOD UNIDENTIFIED", content_type="application/json")


def category(request):
    if request.method == 'GET':
        cat_id = int(request.GET.get('cat_id', 0))
        category_list = []
        if cat_id > 0:
            try:
                cat_obj = Category.objects.get(pk=cat_id)
                response_dict = dict()
                response_dict['id'] = cat_obj.id
                response_dict['name'] = cat_obj.name
                response_dict['description'] = cat_obj.description
                response_dict['image_url'] = cat_obj.get_image_url()
                category_list.append(response_dict)
                response = {
                    'data': category_list,
                    'status_code': "200"
                }
                return HttpResponse(json.dumps(response), content_type="application/json")

            except Category.DoesNotExist:
                response = {
                    'data': dict(),
                    'status_code': "200"
                }
                return HttpResponse(json.dumps(response), content_type="application/json")

        else:

         for cat_obj in Category.objects.filter(is_active=True):
            response_dict = dict()
                #response_dict['id'] = cat_obj.id
                #response_dict['name'] = cat_obj.name
            response_dict['description'] = cat_obj.description
#               #response_dict['image_url'] = cat_obj.get_image_url(cat_obj)
                #response_dict['image_url'] = cat_obj.get_image_url()
            category_list.append(response_dict)
            response = {
                'data': category_list,
                'status_code': "200"
             }
        return HttpResponse(json.dumps(response), content_type="application/json")


def product(request):
    if request.method=='GET':
        user_id = int(request.GET.get('user_id', 0))
        print('GETT')
        except_string="user does not exist"
        if user_id > 0:
            try:
                user = User.objects.get(pk=user_id)
                print (user.id)
                if Product.objects.filter(user_id__exact=user_id).exists():
                    print(user.id)
                    user_products=Product.objects.filter(user_id=user_id)
                    products_list=[]

                    for x in user_products:

                        response_dict = dict()
                        try:
                            product_image = Images.objects.get(product_id=x.id)
                            response_dict['image_url']=str(product_image.get_image_url())
                            print("TRYYYYYYYY")
                        except Images.DoesNotExist:
                            category_image=Category.objects.get(pk=x.category_id)
                            print("EXCEPTTTTTTTTTTTTTT DOES NOT EXIST")
                        response_dict['ID'] = x.id
                        response_dict['user'] = x.user.email
                        response_dict['name'] = x.name
                        response_dict['description'] = x.description
                        response_dict['price'] = x.price
                        response_dict['quantity'] = x.quantity
                        response_dict['category'] = x.category.description
                        products_list.append(response_dict)
                    response = {
                        'data': products_list,
                        'status_code': "200"
                    }
                    return HttpResponse(json.dumps(response), content_type="application/json")

                else:
                    response = {
                        'data': "there is no prduct against the user id",
                        'status_code': "404"
                    }
                    return HttpResponse(json.dumps(response), content_type="application/json")
            except User.DoesNotExist:
                response = {
                    'data': except_string,
                    'status_code': "404"
                }
                return HttpResponse(json.dumps(response), content_type="application/json")
            return HttpResponse("length is 1")

        else:
             products_list=[]
             active_products = Product.objects.filter(is_active=True)
             for x in active_products:
                    response_dict = dict()
                    try:
                         product_image = Images.objects.get(product_id=x.id)
                         response_dict['image_url'] = str(product_image.get_image_url())
                         print("TRYYYYYYYY")

                    except Images.DoesNotExist:
                         category_image = Category.objects.get(pk=x.category_id)
                         #response_dict['image_url'] = category_image.get_image_url()
                         print("EXCEPTTTTTTTTTTTTTT DOES NOT EXIST")
                    response_dict['ID'] = x.id
                    response_dict['user'] = x.user.email
                    response_dict['name'] = x.name
                    response_dict['description'] = x.description
                    response_dict['price'] = x.price
                    response_dict['quantity'] = x.quantity
                    response_dict['category'] = x.category.description
                    products_list.append(response_dict)
             response = {
                     'data': products_list,
                     'status_code': "200"
             }
             return HttpResponse(json.dumps(response), content_type="application/json")
        return HttpResponse("GETT")

    elif request.method == 'POST':
        print('POSTT')
        json_data = json.loads(request.body)
        email = json_data['email']
        name = json_data['name']
        category = json_data['category']
        description = json_data['description']
        price=int(json_data['price'])
        quantity = int(json_data['quantity'])
        image = json_data['image']

        if User.objects.filter(email__iexact=email).exists():
            if Category.objects.filter(description__iexact=category).exists():
                print(category)
                _user = User.objects.get(email=email)
                _category = Category.objects.get(description=category)

                created_user = Product.objects.create(user=_user, name=name, category=_category,
                                                      description=description, price=price, quantity=quantity,
                                                      created_date=datetime.date.today(),
                                                      updated_date=datetime.date.today())

                filename = FileName()
                if SaveImage(image,filename):
                    print("img true")
                    _created_image = Images.objects.create(product=created_user, name=filename)
                else:
                    print("img false")
                    _created_image = Images.objects.create(product=created_user, name=_category.name)
                response = {
                    "string_response": "created",
                    'status_code': "200",
                }
                return HttpResponse(json.dumps(response), content_type="application/json")

            else:
                response = {
                    "string_response":category+" category does not exist" ,
                    'status_code': "404",
                }
                return HttpResponse(json.dumps(response), content_type="application/json")

        else:
            response = {
                "string_response": "user having email '"+email+"' doesn't exist",
                'status_code': "404",
            }
            return HttpResponse(json.dumps(response), content_type="application/json")
        return HttpResponse("POSTT")


    elif request.method=='PUT':
        print('PUTT')
        if request.method == 'PUT':
            json_data = json.loads(request.body)
            id=json_data['id']
            user_id=json_data['user_id']
            image=json_data['image']
            if User.objects.filter(id=user_id).exists():
             if Product.objects.filter(id=id, user_id=user_id).exists():
                 filename=FileName()
                 if SaveImage(image,filename):

                    print("nooooooooooooooooooooo")
                    print(image)
                    if Images.objects.filter(product_id=id).exists():
                        print ("found in PUTT request "+id)
                        image_obj=Images.objects.get(product_id=id)
                        print(image_obj.name)
                        DeleteImage(image_obj.name)
                        count0 = Images.objects.filter(product_id=id).update(name=filename)

                        count=Product.objects.filter(id=id).update(name=json_data['name'], price=json_data['price'],description=json_data['description'], quantity=json_data['quantity'])
                        print("time is "+str(datetime.date.today()))
                        # products.update()
                        updated=Product.objects.filter(id=json_data['id'])  #error comes by using get for x in updated:

                        if count==1:
                            print("count is 1")
                            data = {}
                            for x in updated:

                                 data['id']=x.id
                                 data['name']=x.name
                                 data['description']=x.description
                                 data['quantity']=x.quantity
                                 data['email']=x.user.email
                        
                           
                            response = {"string_response":data ,
                                'status_code': "200",
                                }
                            return HttpResponse(json.dumps(response), content_type="application/json")
                        else:
                            string ="updated more than one products"
                            response = {"string_response": string,
                                'status_code': "404",
                            }

                        return HttpResponse(json.dumps(response), content_type="application/json")
                 else:
                     return HttpResponse("save image else", content_type="application/json")
                 return HttpResponse("helll", content_type="application/json")

             else:
                string = "product with ID " + id + " does not exist"
                print(string)
                response={"error_reason":string,
                     'status_code':"404",
                 }
                return HttpResponse(json.dumps(response), content_type="application/json")
            else:
                string = "user does not exist"
                print(string)
                response = {"error_reason": string,
                            'status_code': "404",
                            }
                return HttpResponse(json.dumps(response), content_type="application/json")
            response = {"string_response": "ERROR DETECTED WHILE PUT REQUEST",
                        'status_code': "404",
                        }
            return HttpResponse(json.dumps(response), content_type="application/json")


    elif request.method=='DELETE':
        print('DELETEE')
        id=request.GET.get('id')
        user_id=request.GET.get('user_id')
        print(id)
        if Product.objects.filter(id=id,user_id=user_id).exists():
            print(id)
            product = Product.objects.get(id=id)
            if Images.objects.filter(product_id=id).exists():
                print("in imageeee block")
                image=Images.objects.get(product_id=id)
                DeleteImage(image.name)
                product.delete()
                print(image.name)
                response = {
                    "string_response": "IMAGE + PRODUCT DELETED",
                    "status_code": "200"
                }
                return HttpResponse(json.dumps(response), content_type="application/json")
            else:
                product.delete()
                response = {
                    "string_response": "IMAGE NOT FOUND AGAINST THE PRODUCT",
                    "status_code": "200"
                }
                return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            string = "CANT'T DELETE PRODUCT BECAUSE USER DOES NOT HAVE THIS PRODUCT"
            response = {
                "string_response": string,
                "status_code": "404"
            }
            return HttpResponse(json.dumps(response), content_type="application/json")
        response = {
            "string_response": "DELETE REQUEST COULDN'T BE ACCOMPLISHED",
            "status_code": "200"
        }

        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponse("PRODUCT REQUEST METHOD UNIDENTIFIED IN PRODUCT")

def service(request):
        if request.method == 'GET':
            user_id = int(request.GET.get('user_id', 0))
            print('GETT')
            except_string = "user does not exist"
            if user_id > 0:
                try:
                    user = User.objects.get(pk=user_id)
                    print(user.id)
                    if Service.objects.filter(user_id__exact=user_id).exists():
                        print(user.id)
                        user_service = Service.objects.filter(user_id=user_id)
                        service_list = []
                        for x in user_service:
                            response_dict = dict()
                            response_dict['id'] = x.id
                            response_dict['user'] = x.user.email
                            response_dict['name'] = x.name
                            response_dict['description'] = x.description
                            response_dict['is_active'] = x.is_active
                            service_list.append(response_dict)
                        response = {
                            'data': service_list,
                            'status_code': "200"
                        }
                        return HttpResponse(json.dumps(response), content_type="application/json")

                    else:
                        response = {
                            'data': "there is no service against the user id",
                            'status_code': "404"
                        }
                        return HttpResponse(json.dumps(response), content_type="application/json")
                except User.DoesNotExist:
                    response = {
                        'data': except_string,
                        'status_code': "404"
                    }
                    return HttpResponse(json.dumps(response), content_type="application/json")
                return HttpResponse("length is 1")

            else:
                service_list = []
                active_service = Service.objects.filter(is_active=True)
                for x in active_service:
                    response_dict = dict()
                    response_dict['id'] = x.id
                    response_dict['user'] = x.user.email
                    response_dict['name'] = x.name
                    response_dict['description'] = x.description
                    response_dict['is_active'] = x.is_active
                    service_list.append(response_dict)
                response = {
                    'data': service_list,
                    'status_code': "200"
                }
                return HttpResponse(json.dumps(response), content_type="application/json")
            return HttpResponse("GETT")

        elif request.method == 'POST':
            print('POSTT')
            json_data = json.loads(request.body)
            email = json_data['email']
            name = json_data['name']
            description = json_data['description']
            is_active = bool(json_data['is_active'])
            print(is_active)
            if User.objects.filter(email__iexact=email).exists():
                    _user = User.objects.get(email=email)
                    created_service = Service.objects.create(user=_user, name=name, description=description,is_active=is_active)
                    response = {
                        "string_response": "SERVICE CREATED",
                        'status_code': "200",
                    }
                    return HttpResponse(json.dumps(response), content_type="application/json")
            else:
                response = {
                    "string_response": "user having email '" + email + "' doesn't exist",
                    'status_code': "404",
                }
                return HttpResponse(json.dumps(response), content_type="application/json")
            return HttpResponse("POSTT")


        elif request.method == 'PUT':
            print('PUTT')
            json_data = json.loads(request.body)
            user_id = json_data['user_id']
            try:
                    user = User.objects.get(pk=user_id)
                    print(user.id)
                    id = json_data['id']
                    if Service.objects.filter(id=id,user_id=user_id).exists():
                        name = json_data['name']
                        description = json_data['description']
                        is_active = bool(json_data['is_active'])
                        count = Service.objects.filter(id=json_data['id']).update(name=name, description=description,
                                                                                  is_active=is_active)
                        updated = Service.objects.filter(id=id)  # error comes by using get for x in updated:
                        if count == 1:
                            print("count is 1")
                            data = {}
                            for x in updated:
                                data['id'] = x.id
                                data['name'] = x.name
                                data['description'] = x.description
                                data['is_active'] = x.is_active
                                data['email'] = x.user.email

                                response = {"string_response": data,
                                            'status_code': "200",
                                            }
                                return HttpResponse(json.dumps(response), content_type="application/json")
                        else:
                            response = {"string_response": "updated more than one products",
                                        'status_code': "404",
                                        }
                            return HttpResponse(json.dumps(response), content_type="application/json")

                    else:
                        string = "CANT'T UPDATE SERVICE BECAUSE USER DOES NOT HAVE THIS SERVICE"
                        response = {"string_response": string,
                                    'status_code': "404",
                                    }
                        return HttpResponse(json.dumps(response), content_type="application/json")
            except User.DoesNotExist:
                response = {
                        'data': "USER DOES NOT EXIST",
                        'status_code': "404"}

                return HttpResponse(json.dumps(response), content_type="application/json")
            response = {"string_response": "ERROR DETECTED WHILE SERVICE PUT REQUEST",
                            'status_code': "404",
                            }
            return HttpResponse(json.dumps(response), content_type="application/json")


        elif request.method == 'DELETE':
            print('DELETEE')
            user_id = request.GET.get('user_id')
            id = request.GET.get('id')
            print(id)
            print(user_id)
            if Service.objects.filter(id=id, user_id=user_id).exists():
                print(id)
                service = Service.objects.get(id=id)
                service.delete()
                response = {
                    "string_response": "SERVICE DELETED",
                    "status_code": "200"
                }
                return HttpResponse(json.dumps(response), content_type="application/json")

            else:
                string = "CANT'T DELETE SERVICE BECAUSE USER DOES NOT HAVE THIS SERVICE"
                response = {
                    "string_response": string,
                    "status_code": "404"
                }
                return HttpResponse(json.dumps(response), content_type="application/json")
            response = {
                "string_response": "DELETE REQUEST COULDN'T BE ACCOMPLISHED",
                "status_code": "200"
            }

            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            return HttpResponse("PRODUCT REQUEST METHOD UNIDENTIFIED IN PRODUCT")


