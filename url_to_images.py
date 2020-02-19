import cv2
import os
import re
import urllib.request
import numpy as np
from PIL import Image



def Image_Data_Generator(Image_folder, Crop_folder):
  '''

  :param Image_folder: Path to the folder containing the base images
  :param Crop_folder:  Path to the folder containing the crop images
  :return: Two dictionaries - crops and images - which contatin the name and
                              numpy array representation of images
  '''

  image_folder_filepath = Image_folder
  crop_folder_filepath = Crop_folder

  crop_association_flag = 0
  crops = {}
  for filename in os.listdir(crop_folder_filepath):
    img = cv2.imread(os.path.join(crop_folder_filepath, filename))
    if img is not None:
      crops[str(filename)] = [img, crop_association_flag]

  images = {}
  for filename in os.listdir(image_folder_filepath):
    img = cv2.imread(os.path.join(image_folder_filepath, filename))

    if img is not None:
      images[str(filename)] = img
  return images, crops


def url_to_cvImage(crop_url,base_url):
  '''

  :param crop_url: The url of the crops.txt
  :param base_url: The url of the images.txt
  :return: None - It creates two folders and populates them with the images from the url
  '''

  print("Getting Images directly from the URLs provided\nPlease wait :)")

  crop_image_url_list = []
  base_image_url_list = []

  crop_data = urllib.request.urlopen(crop_url)
  base_data = urllib.request.urlopen(base_url)


  for line_crop in crop_data:
    crop_image_url_list.append(line_crop[:-1].decode('ASCII'))

  for line_base in base_data:
    base_image_url_list.append(line_base[:-1].decode('ASCII'))

  crops  = {}
  images = {}
  crop_association_flag = 0


  os.mkdir('images_from_url/')
  os.mkdir('crops_from_url/')


  for base in base_image_url_list:
    base_image = Image.open(urllib.request.urlopen(base))
    opencv_base_image = np.array(base_image)
    opencv_base_image = cv2.cvtColor(opencv_base_image, cv2.COLOR_RGB2BGR)
    base_name = re.split('/', base)
    if opencv_base_image is not None:
      # images[str(base_name[-1])] = opencv_base_image
      cv2.imwrite('images_from_url/' + base_name[-1], opencv_base_image)

  print("Finished processing the images_url")

  for crop in crop_image_url_list:
    crop_image = Image.open(urllib.request.urlopen(crop))
    opencv_crop_image = np.array(crop_image)
    opencv_crop_image = cv2.cvtColor(opencv_crop_image, cv2.COLOR_RGB2BGR)
    crop_name = re.split('/',crop)
    if opencv_crop_image is not None:
      # crops[str(crop_name[-1])] = [opencv_crop_image, crop_association_flag]
      cv2.imwrite('crops_from_url/' + crop_name[-1], opencv_crop_image)

  print("Finished processing the crops_url")

  print("Total number of images " + str(len(base_image_url_list)))
  print("Total number of crops " + str(len(crop_image_url_list)))

if __name__ == '__main__':

  crop_url = 'https://s3.amazonaws.com/msd-cvteam/interview_tasks/crops_images_association_2/crops.txt'
  base_url = 'https://s3.amazonaws.com/msd-cvteam/interview_tasks/crops_images_association_2/images.txt'


  url_to_cvImage(crop_url, base_url)

  print("Pre-processing Complete !")