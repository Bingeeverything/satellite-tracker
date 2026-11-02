from skyfield.api import EarthSatellite, load, wgs84
import json
import pytz
from datetime import datetime

def satellite_locator(SubSecDateTimeOriginal, lat, lon):
    #Time Setup
    ts = load.timescale()
    bluffton = wgs84.latlon(lat, lon)
    time_string = SubSecDateTimeOriginal
    iso_string = time_string.replace(":", "-", 2)
    dt = datetime.fromisoformat(iso_string)
    t = ts.from_datetime(dt)
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

    for sat in sats[:]:
        difference = sat - bluffton
        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()
        
        if alt.degrees < 0:
            sats.remove(sat)

    print('Loaded', len(sats), 'historical satellites')

    return satellites_dict

 