from skyfield.api import EarthSatellite, load, wgs84
import json
import pytz
from datetime import datetime, timedelta
from .radian_convert import celestial_to_cartesian
import numpy as np
import cv2

def satellite_locator(SubSecDateTimeOriginal, lat, lon, rotation_vector, translation_vector, K, dist_coeffs, exposure_minutes = 12):
    #Time Setup
    ts = load.timescale()
    bluffton = wgs84.latlon(lat, lon)
    time_string = SubSecDateTimeOriginal
    iso_string = time_string.replace(":", "-", 2)
    dt = datetime.fromisoformat(iso_string)
    dt_end = dt + timedelta(minutes=exposure_minutes)
    t = ts.from_datetime(dt)
    t_end = ts.from_datetime(dt_end)

    print("Current UTC:", t.utc_datetime())

    name = 'historical_active.json' 

    # Bypass the URL download entirely and open the local historical file
    with open(name, 'r') as f:
        data = json.load(f)

    # Create EarthSatellite objects
    sats = [EarthSatellite.from_omm(ts, fields) for fields in data]
    satellites_dict = {}
    for sat in sats:
        satellites_dict[sat.model.satnum] = sat
    sats = list(satellites_dict.values())
    visible_satellites = {}

    for sat in sats[:]:
        difference = sat - bluffton
        topocentric = difference.at(t)
        topocentric_end = difference.at(t_end)
        ra, dec, distance = topocentric.radec()
        ra_end, dec_end, distance = topocentric.radec()
        ra_deg, ra_deg_end = ra.hours * 15, ra_end.hours * 15
        dec_deg, dec_deg_end = dec.degrees, dec_end.degrees

        X_start, Y_start, Z_start = celestial_to_cartesian(ra_deg, dec_deg)
        X_end, Y_end, Z_end = celestial_to_cartesian(ra_deg_end, dec_deg_end)

        packaged = np.array([
        [[X_start, Y_start, Z_start]],  # Row 0: The t (Start) coordinates
        [[X_end, Y_end, Z_end]]         # Row 1: The t_end (End) coordinates
    ], dtype=np.float32)

        projected, _ = cv2.projectPoints(packaged, rotation_vector, translation_vector, K, dist_coeffs)
        X, Y = projected[0, 0]

            
        if 0 <= X <= 4000 and 0 <= Y <= 3000:
            visible_satellites[sat.name] = (X, Y)

    # To use it later:
    #for sat, coords in visible_satellites.items():
    #   print(f"{sat.name}: Alt={coords['alt'].degrees}, Az={coords['az'].degrees}")

    sats = list(visible_satellites.values())
    print('Loaded', len(sats), 'historical satellites')
    return visible_satellites

    