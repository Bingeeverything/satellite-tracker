from skyfield.api import EarthSatellite, load, wgs84
import json
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta
from spacetrack import SpaceTrackClient
from dotenv import load_dotenv
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

    max_days = 7.0  
    name = 'stations.json' 

    name = 'historical_active.json' 

    # Bypass the URL download entirely and open the local historical file
    with open(name, 'r') as f:
        data = json.load(f)

    # Create EarthSatellite objects
    sats = [EarthSatellite.from_omm(ts, fields) for fields in data]
    print('Loaded', len(sats), 'historical satellites')

    # load_dotenv()
    # password = os.getenv("PASSWORD", "password")

    # st = SpaceTrackClient(identity='_______@gmail.com', password= password)

    # target_date = dt.strftime('%Y-%m-%d')
    # date_range = f"{target_date}-->{target_date} 23:59:59"
    # print(f"Querying Space-Track for historical TLEs on: {target_date}")

    # 4. Fetch the data
    # This queries the 'tle' class which provides historical data
    # raw_tle_data = st.gp_history(epoch=date_range, format='tle', limit=500)
    # lines = data.strip().split('\n')
   
    me = melbourne.at(t)

    visible_satellites = []
    return visible_satellites

 