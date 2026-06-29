import numpy as np
import pandas as pd
import exiftool
import tifffile
from dotenv import load_dotenv
import os
import cv2

#Load variables from the .env file
load_dotenv()

#created a env file to store my exiftool file location
exiftool_path = os.getenv("EXIFTOOL_PATH", "exiftool")
dng_path = "images/20251015_034507.dng"

with exiftool.ExifToolHelper(executable=exiftool_path) as et:
    for d in et.get_tags([dng_path], tags= ["SubSecDateTimeOriginal", "GPSAltitude", "GPSPosition"]): #using gps position because its a composite tag and works better in this case
        for k, v in d.items():
            print(f"Dict: {k} = {v}")

#using tifffile to read the image, and then we open the image and get the mean
image =  tifffile.imread(dng_path)

#doing an arithmetic mean of the np array, so its now a 2d greyscale array
greyscale_image =  np.mean(image, axis= (2))
print(greyscale_image)

"""
In the following code, i lablelled a threshold of 100, below it is the dark sky, and above it is the stars, the city light pollution and such
Then initialized a variable "compare" which i used comparison operation to compare to the threshold, which give me the ndarray of True and False
then i converted the true and false to the int value of it using astype
and to finally printing it, so now i have a array with just 0s and 1s representing the darkness in the sky.
"""
threshold = 65
comparing = (greyscale_image > threshold)
binary_image = (comparing * 255).astype('uint8')

# total_cols = binary_image.shape[1]
# start_index = total_cols//3
# cropped_image = binary_image[:, start_index:]

# Detect points that form a line
lines = cv2.HoughLinesP(binary_image, 1, np.pi/180, 200, minLineLength=255, maxLineGap=4)

# Draw lines on the image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(binary_image, (x1, y1), (x2, y2),255, 3)
# Show result
cv2.imwrite("ResultImage.jpg", binary_image)
cv2.waitKey(0)