#!/usr/local/bin/python3
import google_images_download  # importing the library
import random
import glob
#from image_package.color_functions import color_distance
from PIL import Image
import os
import sys
sys.path.append(
    '/Users/griffin/Dropbox/Scripts-random/image_projects/image_package')


"""
"""


def paste2images():
    im = Image.new("RGB", (1024, 1024), "white")

    im1 = Image.open('./Resources/emojis_64x64/-1.png')
    im2 = Image.open('./Resources/emojis_64x64/+.png')

    bbx1 = im1.getbbox()
    bbx2 = im2.getbbox()

    print(bbx1)
    print(bbx2)

    im.paste(im1, (10, 10))
    im.paste(im2, (225, 0))

    im.show()


def pasteRandomLocations():
    files = glob.glob('./Resources/emojis_64x64/**/*.jpg', recursive=True)
    print(len(files))
    im = Image.new("RGBA", (1024, 1024), "white")

    for f in files:
        tmp = Image.open(f).convert("RGBA")
        im.paste(tmp, (random.randint(0, 1024-64),
                 random.randint(0, 1024-64)), tmp)
        tmp.close()
    im.show()


def pasteInOrder():
    # opens a directory and gets a list of files based on a wildcard
    files = glob.glob('./Resources/emojis_64x64/**/*.png', recursive=True)

    print(len(files))

    sorted(files)

    # create new 1924x1924 image with white background
    im = Image.new("RGBA", (1924, 1924), "white")

    # starting x and y
    x = 0
    y = 0

    # loops through the files
    for f in files:
        tmp = Image.open(f).convert("RGBA")
        im.paste(tmp, (x, y), tmp)
        tmp.close()
        x += 64
        if x > 1924:
            x = 0
            y += 64
    im.show()


def GetpixelfromImage():

    img = Image.open("GOT.png", "r")
    #img.GetpixelfromImage()
    #pix = img.load()
    #print(pix[0,0])
    w = img.width
    h = img.height

    # for x in range(width):
    # for y in range(height):

    #loops through 
    for x in range(0, w):
        for y in range(0, h):
            r,g,b = img.getpixel((x,y))
            print (x,y," ", r,g,b, "\n")

    r,g,b = img.getpixel((115,50))
    print (115,50," ", r,g,b, "\n")
    #r,g,b = img.getpixel((0,0))
    #print (r,g,b)
            


if __name__ == '__main__':

    # Creates a dictionary for the arguments the users will enter from the command line
    # args = {}

    GetpixelfromImage()
	# paste2images()
	# pasteRandomLocations()

	# talked about in office
	# pasteInOrder()

	# 1) Open an image and loop through it in a similar way getting pixel color 
	# tmp = Image.open("someimage.png").convert("RGBA")
	# x,y = tmp.size
	# loop using my x,y 
	# img.getpixel((x, y)) # x=1, y=1