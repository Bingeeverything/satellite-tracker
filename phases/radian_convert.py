import numpy as np

def celestial_to_cartesian(ra_deg, dec_deg):
    """
    Im taking the r to the stars as infinity so 1, since they are very far away and my sensor just knows thatt they are far far away, and my camera is a pinhole camera  so im just getting the coords and nothing else
    """

    ra_rad = np.radians(ra_deg)
    dec_rad = np.radians(dec_deg)

    X = np.cos(dec_rad) * np.cos(ra_rad)
    Y = np.cos(dec_rad) * np.sin(ra_rad)
    Z = np.sin(dec_rad)

    return (X, Y, Z)