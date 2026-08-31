from astroquery.astrometry_net import AstrometryNet
from astroquery.exceptions import TimeoutError as AstroTimeoutError
from dotenv import load_dotenv
from astropy.io import fits
import numpy as np
from astropy.stats import sigma_clipped_stats
from astroquery.astrometry_net import AstrometryNet
from photutils.detection import DAOStarFinder
import os
import tifffile
from PIL import ImageChops
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

        fits_file = image
        with fits.open(fits_file) as hdul:
            data = hdul[0].data
            header = hdul[0].header
            print(data.shape)
            data = np.mean(data, axis = 0)
            height, width = data.shape


        #get the stars
        mean, median, std = sigma_clipped_stats(data, sigma = 3.6)
        daofind = DAOStarFinder(fwhm=3.0, threshold= 5.0 * std)
        sources = daofind( data - median)

        #format and sort the stars
        sources.sort("flux", reverse=True)
        top_sources = sources[:100]
        x_positions = top_sources["x_centroid"]
        y_positions = top_sources["y_centroid"]
        x = list(x_positions)
        y = list(y_positions)

        submission_id = None
        max_network_retries = 3
        retry_delay = 10

        for attempt in range(max_network_retries):
            try:
                print(f"Uploading image to Astrometry.net (Attempt {attempt + 1})...")
                wcs_header = ast.solve_from_source_list(
                x=x,
                y=y,
                image_width=width,
                image_height=height,
                solve_timeout=5,
                scale_units = 'degwidth',
                scale_type = 'ev',
                scale_est = 76.1,
                scale_err = 20
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
            monitor_retries = 30
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