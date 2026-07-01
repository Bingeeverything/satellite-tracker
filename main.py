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

#dividing every pixel from the 99.9th place, so its kind of a median and not an outlier
max_pixel = np.percentile(greyscale_image, 99.9)

#making every pixel bigger than 255 to be m,ax 255
clipping = np.clip(greyscale_image, None, max_pixel)
scaled_image = ((clipping / max_pixel) * 255).astype('uint8')
print(scaled_image)

#blurring the image, and then subtracting the blur from the original image to leave just the trails
blurred = cv2.GaussianBlur(scaled_image, (151,151), 0)
signal_float = cv2.subtract(scaled_image, blurred)

_, thresh_img = cv2.threshold(signal_float, 6, 255, cv2.THRESH_BINARY)

# total_cols = binary_image.shape[1]
# start_index = total_cols//3
# cropped_image = binary_image[:, start_index:]

# Detect points that form a line
lines = cv2.HoughLinesP(thresh_img, 1, np.pi/180, 150, minLineLength=200, maxLineGap=10)

#coordinates
coordinates = []

# Draw lines on the image
if lines is not None:
    print(f"Success! Found {len(lines)} streaks.")
    for line in lines:
        x1, y1, x2, y2 = line.ravel()
        coordinates.append(((x1, y1), (x2, y2)))
        # Draw a bold white line (255) on the black background
        cv2.line(thresh_img, (x1, y1), (x2, y2), 255, 3)
else:
    print("Warning: No lines met the length requirement. The sky mask remains clear.")

print(coordinates)
# Save result as a clean black-and-white binary image
cv2.imwrite("Result Image.jpg", thresh_img)
cv2.waitKey(0)