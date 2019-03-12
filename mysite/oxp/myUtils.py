from PIL import Image
from Lib import os, base64
import time

def DeleteImage(filename):

    if "some_image" in filename:
        if os.path.exists('static/images'):
            print("path exists")
            print(filename)
            #if os.path.isfile(filename):
            try:
                Image.open(os.path.join('static', 'images', filename))
                #im = Image.open(filename)
                print("is file")
                os.remove(os.path.join('static', 'images', filename))
            except IOError:
                print("file not found")


def SaveImage(image,filename):
    image_flag = False
    if ( image == '' or  image == "0"):
        print("image is empty")
        return image_flag
    else:
        data = base64.b64decode(image)
        with open(os.path.join('static', 'images', filename), 'wb') as f:
            print("image field is not empty")
            f.write(data)
            image_flag = True
            return image_flag


def FileName():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = 'some_image' + timestr + '.jpg'
    return filename
