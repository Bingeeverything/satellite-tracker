import numpy as np
import pandas as pd
import exiftool
import tifffile
from dotenv import load_dotenv
import os
import cv2
from phases import satellite_locator, download_historical_data, get_camera_pointing, convert_dng_to_jpg
from datetime import datetime, timedelta

#Load variables from the .env file
load_dotenv()

#created a env file to store my exiftool file location
exiftool_path = os.getenv("EXIFTOOL_PATH", "exiftool")
dng_path = "images/20250420_223850.dng"

# Master dictionary to hold data for all files
all_image_data = {}
file_paths = [dng_path]

with exiftool.ExifToolHelper(executable=exiftool_path) as et:
    for d in et.get_metadata(dng_path):
        for k, v in d.items():
            print(f"Dict: {k} = {v}")

with exiftool.ExifToolHelper(executable=exiftool_path) as et:
    for d in et.get_tags(file_paths, tags=["SubSecDateTimeOriginal", "GPSAltitude", "GPSPosition", "PreviewImageStart", "PreviewImageLength"]):
        current_file = d.get("SourceFile")
        
        # Clean the prefixes for this specific file's tags
        clean_data = {k.split(":")[-1]: v for k, v in d.items() if k != "SourceFile"}
        all_image_data[current_file] = clean_data

###checking if the GPS Position exists in the data
image_data = all_image_data.get(dng_path, {})
has_gps = "GPSAltitude" in image_data and "GPSPosition" in image_data

#calculating the time frame for the image when it was clicked    
timerange = image_data.get("SubSecDateTimeOriginal")
timerange = timerange.split(" ")[0]
base_date = datetime.strptime(timerange, "%Y:%m:%d")
date_before = base_date - timedelta(days = 1)
date_before = date_before.strftime("%Y-%m-%d")
date_after = base_date + timedelta(days = 1)
date_after = date_after.strftime("%Y-%m-%d")
epoch_range = f"{date_before}--{date_after}"
print(epoch_range)
print(all_image_data)
print(image_data)

if __name__ == "__main__":

    if not os.path.exists('historical_active.json'):
        print("Historical data not found locally. Initiating download...")
        download_historical_data(epoch_range)
    else:
        print("Historical data found locally. Bypassing API download.")

    if has_gps:
        user_gps = image_data.get("GPSPosition")
        user_alt = image_data.get("GPSAltitude")
        print(f"GPS data found for {dng_path}")
    else:
        print(f"Missing GPS data for {dng_path}!")
        # Prompt user for manual input
        try:
            user_gps = input("Enter Latitude Longitude (e.g., -37.8488 43.6432): ")
            user_alt = input("Enter Altitude in metres (e.g., 50): ")
        except ValueError:
            print("Invalid numerical input. Aborting.")
            exit(1)

    # Write the new coordinates to the DNG file
    print(f"Writing GPS data to {dng_path}...")
    with exiftool.ExifToolHelper(executable=exiftool_path) as et:
        et.set_tags(
            [dng_path],
            tags={
                "GPSPosition": user_gps,
                "GPSAltitude": user_alt,
            },
            params=["-overwrite_original"]
        )

    all_image_data[dng_path]["GPSPosition"] = user_gps
    all_image_data[dng_path]["GPSAltitude"] = user_alt
    print(user_gps)
    print(user_alt)

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
    signal = cv2.subtract(scaled_image, blurred)

    _, thresh_img = cv2.threshold(signal, 6, 255, cv2.THRESH_BINARY)

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

    # Save result as a clean black-and-white binary image
    cv2.imwrite("Result Image.jpg", thresh_img)
    cv2.waitKey(0)

    # Save result as a clean black-and-white binary image
    cv2.imwrite("Result Image.jpg", thresh_img)
    cv2.waitKey(0)

    filename = os.path.basename(dng_path)
    file_base = os.path.splitext(filename)[0]
    output_jpg_path = os.path.join("images", f"{file_base}.jpg")
    start_offset = all_image_data[dng_path].get("PreviewImageStart")
    length_bytes = all_image_data[dng_path].get("PreviewImageLength")
    if start_offset and length_bytes:
        png_image = convert_dng_to_jpg(dng_path, output_jpg_path, start_offset, length_bytes)
    else:
        print(f"Error: Embedded preview data missing from Exif tags for {dng_path}")


    header = get_camera_pointing(png_image)

    # Check if the DNG data exists in your master dictionary
    if dng_path in all_image_data:
        # Safely pull the keys from your existing dictionary structure
        SubSecDateTimeOriginal = all_image_data[dng_path].get("SubSecDateTimeOriginal")
        GPSPosition = all_image_data[dng_path].get("GPSPosition")

        # Verify both values were successfully extracted before processing
        if GPSPosition and SubSecDateTimeOriginal:
            # ExifTool separates Composite:GPSPosition using a comma and space
            lat, lon = GPSPosition.split(" ")
            lat = float(lat)
            lon = float(lon)
            # Execute your satellite timing function
            satellite_locator(SubSecDateTimeOriginal, lat, lon)
        else:
            print("Error: Missing required GPSPosition or SubSecDateTimeOriginal tags.")
    else:
        print(f"Error: No metadata found for {dng_path}")