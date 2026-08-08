from skyfield.api import EarthSatellite, load, wgs84
import json
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta
from spacetrack import SpaceTrackClient
import os

def satellite_locator(SubSecDateTimeOriginal, lat, lon):
    #Time Setup
    ts = load.timescale()
    time_string = SubSecDateTimeOriginal
    iso_string = time_string.replace(":", "-", 2)
    dt = datetime.fromisoformat(iso_string)
    t = ts.from_datetime(dt)
    print("Current UTC:", t.utc_datetime())

    #Location
    melbourne = wgs84.latlon(lat, lon, elevation_m=28)
    tz = pytz.timezone('Australia/Melbourne')
    print("Observer Location:", melbourne)

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
    print('Loaded', len(sats), 'historical satellites')

    me = melbourne.at(t)
    return satellites_dict

 