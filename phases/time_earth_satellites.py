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
    visible_satellites = {}

    for sat in sats[:]:
        difference = sat - bluffton
        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()
            
        if alt.degrees >= 0:
            #Create the data payload
            tracking_data = {
                "satellite_object": sat,
                "alt": alt,
                "az": az,
                "distance": distance
            }
            
            #Assign it to BOTH keys independently
            visible_satellites[sat.name] = tracking_data          #Key 1: The Name string
            visible_satellites[sat.model.satnum] = tracking_data  #Key 2: the model

    # To use it later:
    #for sat, coords in visible_satellites.items():
    #   print(f"{sat.name}: Alt={coords['alt'].degrees}, Az={coords['az'].degrees}")

    sats = list(visible_satellites.values())
    print('Loaded', len(sats), 'historical satellites')
    return visible_satellites

    