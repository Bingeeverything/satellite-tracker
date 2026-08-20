from astroquery.astrometry_net import AstrometryNet
from astroquery.exceptions import TimeoutError as AstroTimeoutError
from dotenv import load_dotenv
from astropy.io import fits
import numpy as np
import os
import tifffile
from PIL import Image
import io
import requests
import time

def convert_dng_to_fits(dng_path, output_fits_path):
    image_data = tifffile.imread(dng_path)
    if len(image_data.shape) == 3 and image_data.shape[2] == 3:
        image_data = np.transpose(image_data, (2,0,1))

    hdu = fits.PrimaryHDU(image_data)
    hdu.writeto(output_fits_path, overwrite=True)
        
    return output_fits_path

def get_camera_pointing(image):
        ast = AstrometryNet()
        load_dotenv()
        ast.api_key = os.getenv("ASTRONOMY_NET_API")    

        submission_id = None
        max_network_retries = 3
        retry_delay = 5

        for attempt in range(max_network_retries):
            try:
                print(f"Uploading image to Astrometry.net (Attempt {attempt + 1})...")
                wcs_header = ast.solve_from_image(
                    image,
                    solve_timeout = 5
                )
                return wcs_header

            except AstroTimeoutError as e:
                print("Plate solving timed out, but upload succeeded. Switching to monitoring mode...")
                submission_id = e.args[1]
                break

            except requests.exceptions.RequestException as ce: 
                # Catch network connection drops, API server downtime, or SSL drops
                print(f"Network error encountered: {ce}")
                if attempt < max_network_retries - 1:
                    print(f"Retrying upload in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Critical network failure: All connection attempts exhausted.")
                    return None
                
        if submission_id:
            monitor_retries = 5
            print(f"Monitoring submission ID: {submission_id}")
            
            for m_attempt in range(monitor_retries):
                try:
                    wcs_header = ast.monitor_submission(submission_id, solve_timeout=120)
                    if wcs_header:
                        print("Successfully recovered WCS solution from submission monitoring!")
                        return wcs_header
                except AstroTimeoutError as e:
                    print(f"Job still processing on server (Monitoring attempt {m_attempt + 1}/{monitor_retries}). Waiting...")
                    time.sleep(30)
                except (requests.exceptions.RequestException, ConnectionError) as ce:
                    print(f"Network glitch while monitoring: {ce}. Retrying poll shortly...")
                    time.sleep(retry_delay)
                    
        print("Failed to retrieve camera pointing data.")
        return None