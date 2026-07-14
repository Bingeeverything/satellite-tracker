from skyfield.api import EarthSatellite, load, wgs84, S, E
import json

#Time Setup
ts = load.timescale()
t = ts.now()
print("Current UTC:", t.utc_datetime())

#Location
melbourne = wgs84.latlon(37.8136 * S, 144.9631 * E, elevation_m=28)
print("Observer Location:", melbourne)

#Downloading the ISS Data
max_days = 7.0  
name = 'stations.json' 

base = 'https://celestrak.org/NORAD/elements/gp.php'
url = base + '?GROUP=stations&FORMAT=json'

if not load.exists(name) or load.days_old(name) >= max_days:
    load.download(url, filename=name)

#Parsing the Data
with load.open(name) as f:
    data = json.load(f)

#Create EarthSatellite objects
sats = [EarthSatellite.from_omm(ts, fields) for fields in data]
print('Loaded', len(sats), 'satellites')

#Filter by ISS (NORAD ID 25544)
by_number = {sat.model.satnum: sat for sat in sats}
iss = by_number[25544]

satellite = iss.at(t)
me = melbourne.at(t)

difference = iss - melbourne
topocentric = difference.at(t)
alt, az, distance = topocentric.altaz()

#print the results
print(f"Altitude: {alt.degrees:.2f}°")
print(f"Azimuth:  {az.degrees:.2f}°")
print(f"Distance: {distance.km:.1f} km")