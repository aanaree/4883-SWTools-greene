#!/usr/local/bin/python3
import google_images_download  # importing the library
import random
import glob
#from image_package.color_functions import color_distance
from PIL import Image
import os
import sys
import cv2
from sklearn.cluster import KMeans
import numpy as np
import requests
import pprint

sys.path.append('/Users/griffin/Dropbox/Scripts-random/image_projects/image_package')

os.chdir("/Users/griffin/Code/Courses/1-Current_Courses/5143-Operating-Systems/Assignments/A00-hold")

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

def brightness(r,g,b):
    """A function to return the calculated "brightness" of a color.
    http://www.nbdtech.com/Blog/archive/2008/04/27/Calculating-the-Perceived-Brightness-of-a-Color.aspx
    Arguments:
        r: [int]
        g: [int]
        b: [int]
    Returns:
        Values between 0-1 (percent of 0-255)
    Used By:
        get_dominant_colors
    """
    return round(sqrt(pow(r,2) * .241  + pow(g,2) * .691 + pow(b,2) * .068 ) / 255,3)

def find_histogram(clt):
    """ Create a histogram with k clusters
    Arguments:
        :param: clt
        :return:hist
    Used By:
        get_dominant_colors
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def get_dominant_colors(img,save_path=None,n=3):
    """Get the dominant colors of an image.

    Arguments:
        img         -- the image [string, numpy.ndarray]
        save_path   -- out path for saving [string] (default None)
        n           -- number of clusters [int] (default 3)
    Returns:
        dictionary of colors
        load_subimages_data
    Requres:
        extract_cluster_color_values
        query_color
        brightness
    """

    #bg,_ = determine_background(img_path)

    # if its string open it
    if isinstance(img,str):
        if os.path.isfile(img):
            img = cv2.imread(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            usage("Error: image path not valid")

    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number

    # do the clustering
    clt = KMeans(n_clusters=n) #cluster number
    clt.fit(img)

    # help me with getting color values I can process
    hist = find_histogram(clt)
    colors = extract_cluster_color_values(hist, clt.cluster_centers_)

    start_delta = 3

    # help me NAME the colors
    # loop through each cluster
    for i in range(len(colors)):
        c = []
        
        # while we haven't found a named color match (increment delta)
        r=colors[i]['rgb'][0]
        g=colors[i]['rgb'][1]
        b=colors[i]['rgb'][2]
           
        r = requests.get('http://cs.mwsu.edu/~griffin/color-api/?r={}&g={}&b={}'.format(r,g,b))
        j = r.json()
        colors[i]['named_data'] = j['result']
        #colors[i]['brightness'] = brightness(colors[i]['rgb'][0],colors[i]['rgb'][1],colors[i]['rgb'][2])


        # {'percent': 0.26, 'rgb': [247, 246, 242], 'named_data': [{'name': 'quarter_alabaster',
        # calculate brightness
        
    for dictionary in colors:
        print(dictionary['percent'])
        print("")
    sys.exit()

    return colors

def extract_cluster_color_values(hist, centroids,ignore_background=False):
    """Get the dominant colors of an image.

    Arguments:
        hist        -- [numpy.ndarray]
        centroids   -- [numpy.ndarray] 
    Returns:
        dictionary of color values
    Used By:
        get_dominant_colors
    """

    colors = []
    
    for (percent, color) in zip(hist, centroids):
        rgb = []
        total = 0
        for c in color:
            c = round(float(c))
            total += c
            rgb.append(c)
        if ignore_background:
            if total > 15 and total < 750:
                colors.append({'percent':round(float(percent),2),'rgb':rgb})
        else:
            colors.append({'percent':round(float(percent),2),'rgb':rgb})

    return colors

def GetpixelfromImage(path):

    colors = []
    img = Image.open(path, "r")

    w = img.width
    h = img.height


    #loops through 
    for x in range(0, w):
        for y in range(0, h):
            r,g,b = img.getpixel((x,y))
            colors.append(img.getpixel((x,y)))
            #print (x,y," ", r,g,b, "\n")


    return colors
            


if __name__ == '__main__':

    # Creates a dictionary for the arguments the users will enter from the command line
    # args = {}

    colors = GetpixelfromImage("./die.jpg")
    rcolors = get_dominant_colors("./die.jpg",3)

    pprint.pprint(rcolors)
