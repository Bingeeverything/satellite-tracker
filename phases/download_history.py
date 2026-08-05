import os
import json
from dotenv import load_dotenv
from spacetrack import SpaceTrackClient

load_dotenv()
email = os.getenv("SPACETRACK_EMAIL")
password = os.getenv("SPACETRACK_PASSWORD")

if not email or not password:
    raise ValueError("Missing Space Track Credentials in .env file")

print("Authenticating with SpaceTrack")

st = SpaceTrackClient(identity= email, password=password)

data = st.gp_history(
    epoch='2025-04-19--2025-04-21',
    decay_date='null-val', 
    format='json'
)

filename = 'historical_active.json'
with open(filename, 'w') as f:
    # If spacetrack handed us a raw string, just write it directly to the file
    if isinstance(data, str):
        f.write(data)
    # If it handed us a parsed dictionary/list, then safely dump it
    else:
        json.dump(data, f, indent=4)

print("historial_active.json is ready")