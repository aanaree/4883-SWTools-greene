"""
Course: CMPS 4883
Assignemt: A07
Date: March 15 2019
Github username: aanaree
Repo url: https://github.com/aanaree/4883-SWTools-greene/tree/master/Assignments/A07
Name: Ackeem Greene
Description: 
    Compares an image  in a folder and finds the closest image to it in the folder.
"""
# import the necessary packages
import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt


def mse(image1, image2):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
	err /= float(image1.shape[0] * image1.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err
 
def compare_images(image1, image2, title):
	# compute the mean squared error and structural similarity
	m = mse(image1, image2)
	
    # create figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f" % (m))
 
	# dislays original image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(image1, cmap = plt.cm.gray)
	plt.axis("off")
 
	# displays the closest image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(image2, cmap = plt.cm.gray)
	plt.axis("off")
 
	# show the images
	plt.show()

def resize(img,width,height):
    """
    This resizes the image while maintining aspect ratio. 
    """
    
    wpercent = float(width / float(img.shape[0]))
    hsize = int((float(img.shape[1])*float(wpercent)))
    img = cv2.resize(img, (width ,height))

    return img

if __name__ == '__main__':
    
    #Creates a dictionary for the arguments the users will enter from the command line
    args = {}

    # Creates a list to store all the Image's path
    aImages = []

    #Checks to see if the user enters arguments besides the file name
    if (len(sys.argv)>1):
        #Loops through the list of arguments entered after the file name
        for arg in sys.argv[1:]:
            #Splits the arguments on the = into a key value pair
            k,v = arg.split('=')
            args[k] = v
        #Searches the dictionary to see if a folder was entered
    if 'folder' in args:
        #If the key exists then the folder is set to what the user entered
        folder = args["folder"]
    else: 
        #Sets default folder
        folder = "emoticons"
    
    #Searches the dictionary for the image name
    if 'image' in args:
        image = args["image"]
    else:
        #Sets default image
        image = "boom.png"
      
    #Creates the original photo path
    orgimg = folder + '/' + image
    if (os.path.isfile(orgimg)):
        
        #Reads the image and converts it to greyscale
        original = cv2.imread(orgimg)
        original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        w,h = original.shape
       
        #Loops through the files in the give folder
        for filename in os.listdir(folder):
            #Checks to see if it is a picture format of (.jpg,.png,jpeg)
            if filename.endswith(".jpg") or filename.endswith(".jpeg")  or filename.endswith(".png"): 
                #Checks that the original image in not added to the list
                if (os.path.join(folder, filename) != folder + '\\'+ image):
                    
                    #Replaces all \ with / so that the path can be found
                    aImages.append(os.path.join(folder, filename).replace('\\','/'))
                
        if (len(aImages)>1):#opens the first image and converts it to greyscale
            im =cv2.imread(aImages[0])
            im =cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        
            #Calculates the mean squared value from the original to the first image
            closest = mse(original,im)
            
            #Loops through the dictionary of image paths
            for images in aImages:
                #opens the image and converts it to greyscale
                im =cv2.imread(images)
                im =cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                #Resize the images to the size of the original
                im=resize(im,w,h)
                
                #Calculates mean squared distance of the image to the original image
                meansqval = mse(original,im)
                
                #Checks to see if the mean squared value is more than 0
                if (meansqval >0):
                    #Checks if the mse is less than the one currently closest
                    if (meansqval < closest):
                        closest = meansqval
                        
            # Loops throguh all the images again
            for images in aImages:
                #Read and convert images to greyscale again
                im =cv2.imread(images)
                im =cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                im=resize(im,w,h)
                #If this is the closest image to the original both are printed
                if ( mse(original,im) == closest):
                    compare_images(original, im, "Original --- Closest Image")
        else:
            #Tells the user the folder has no other images but the original
            print("The Folder Is Empty!!")
        
    else:
        #lets the user know they have entered an invalid path
        print("This Photo OR Photo Path Does Not Exist!")