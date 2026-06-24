import numpy as np
import pandas as pd
import exiftool
import tifffile
from dotenv import load_dotenv
import os

#Load variables from the .env file
load_dotenv()

#created a env file to store my exiftool file location
exiftool_path = os.getenv("EXIFTOOL_PATH", "exiftool")
dng_path = "images/20250611_173841.dng"

with exiftool.ExifToolHelper(executable=exiftool_path) as et:
    for d in et.get_tags([dng_path], tags= ["SubSecDateTimeOriginal", "GPSAltitude", "GPSPosition"]): #using gps position because its a composite tag and works better in this case
        for k, v in d.items():
            print(f"Dict: {k} = {v}")

#using tifffile to read the image, and then we open the image and get the mean
image =  tifffile.imread(dng_path)

#doing an arithmetic mean of the np array, so its now a 2d greyscale array
greyscale_image =  np.mean(image, axis= (2))
print(greyscale_image)