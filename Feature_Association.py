import cv2
import json
import numpy as np
import url_to_images



def Image_Crop_Association(images,crops,Output_File):
    '''

    :param images: Dictionary containing image name and numpy array as key-value pair
    :param crops:  Dictionary containing crop  name and numpy array as key-value pair
    :param Output_File: The path or name of the json file in which you want to store the output
    :return: None - This function generates a json file output
    '''
    MIN_MATCH_COUNT = 10

    output_file_path = Output_File
    final_output_dict = {}

    for base in images.keys():

        img2 = cv2.cvtColor(images[base], cv2.COLOR_BGR2GRAY)

        print("\nFor Image :- " + str(base) + "\tThe crops that match are \n")
        final_output_dict[base] = []

        for crop in crops.keys():
            img1 = cv2.cvtColor(crops[crop][0], cv2.COLOR_BGR2GRAY)



            # Initiate SIFT detector
            sift = cv2.xfeatures2d.SIFT_create()

            # find the keypoints and descriptors with SIFT
            kp1, des1 = sift.detectAndCompute(img1, None)
            kp2, des2 = sift.detectAndCompute(img2, None)

            FLANN_INDEX_KDTREE = 0
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)

            flann = cv2.FlannBasedMatcher(index_params, search_params)
            try:
                matches = flann.knnMatch(des1, des2, k=2)
            except:
                continue

            good = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good.append(m)

            if len(good) > MIN_MATCH_COUNT:
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                matchesMask = mask.ravel().tolist()

                h, w = img1.shape
                pts = np.array([[0, 0], [0, h], [w , h], [w , 0]],dtype=np.float32).reshape(-1, 1, 2)
                try:
                    dst = cv2.perspectiveTransform(pts, M)
                except:
                    continue

                crops[crop][1] = 1
                img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
                print("Crop Image Name: " + str(crop))
                crop_tuple = (crop,[str(int(round(dst[0][0][0]))),str(int(round(dst[0][0][1]))),str(int(round(dst[2][0][0]))),str(int(round(dst[2][0][1])))])
                final_output_dict[base].append(crop_tuple)
                print(crop_tuple)

            else:
                print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
                matchesMask = None

    NA_List = []

    for key in crops.keys():
        if crops[key][1] == 0:
            NA_List.append(str(key))

    final_output_dict["NA"] = NA_List

    json_file_object = open(output_file_path, 'w', encoding="utf-8")
    json.dump(final_output_dict,json_file_object,ensure_ascii=False)
    json_file_object.close()

    print("The output json file has been generated")


if __name__ == '__main__':
    image_folder = 'images_from_url'
    crop_folder  = 'crops_from_url'
    output_file = 'main_output.json'

    images, crops = url_to_images.Image_Data_Generator(image_folder, crop_folder)
    print("Total number of images "+ str(len(images)))
    print("Total number of crops " + str(len(crops)))
    Image_Crop_Association(images,crops,output_file)