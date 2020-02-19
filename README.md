# Image_Crop_Matching
A program to match crops with the image in which they are present. At the same time, the co-ordinates of the bounding box of the crop on the image is noted.


This is my first computer vision project. It was done as part of an interview process for an internship role that I applied for. It was quite interesting to work on this problem statement and hence I am presenting my code to you guys who might find it useful for working on their project or extending this one to do more creative stuff. 

Cheers! 


The images for this program were taken from urls of the image directly. You can easily modify it to access your stored images in your folders.

The core concept used here is the Scale Invariant Feature Transform (SIFT). This provides us immunity against the rotated and different sized images. Please google and try to understand the concept of the same. It'll really be pretty useful :p


The two main python files are :- 

**1)url_to_images.py**
- This is used to get the images and crop folder path as inputs and return as output the dictionaries with image name and numpy array as key-value pair.
- It also houses another function which gets the link for the txt file and then stores the images in folders in the system locally.

**2) Feature_Association.py**
- This contains the function that actually implements the sift algorithm.
- This generates the final json output.


