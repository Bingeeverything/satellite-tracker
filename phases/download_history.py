import os
import json
from dotenv import load_dotenv
from spacetrack import SpaceTrackClient
from main import epoch_range


#to run this file, have to run python -m phases.download_history so python thinks of this as the parent directory
#since otherwise it wont run because we are importing a variable from main.py which is outside the folder pf phases



load_dotenv()
email = os.getenv("SPACETRACK_EMAIL")
password = os.getenv("SPACETRACK_PASSWORD")

if not email or not password:
    raise ValueError("Missing Space Track Credentials in .env file")

print("Authenticating with SpaceTrack")

st = SpaceTrackClient(identity= email, password=password)
epoch_range = epoch_range

data = st.gp_history(
    epoch = epoch_range,
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