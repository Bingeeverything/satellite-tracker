import numpy as np
import pandas as pd
import exiftool
import rawpy
from dotenv import load_dotenv
import os

#Load variables from the .env file
load_dotenv()

#created a env file to store my exiftool file location
exiftool_path = os.getenv("EXIFTOOL_PATH", "exiftool")
dng_path = "images/20260309_064353.dng"

with exiftool.ExifToolHelper(executable=exiftool_path) as et:
    for d in et.get_metadata(dng_path):
        for k, v in d.items():
            print(f"Dict: {k} = {v}")