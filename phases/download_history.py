import os
import json
from dotenv import load_dotenv
from spacetrack import SpaceTrackClient

def download_historical_data(epoch_range):
    load_dotenv()
    email = os.getenv("SPACETRACK_EMAIL")
    password = os.getenv("SPACETRACK_PASSWORD")
    
    if not email or not password:
        raise ValueError("Missing Space Track Credentials in .env file")
    
    print("Authenticating with SpaceTrack...")
    st = SpaceTrackClient(identity=email, password=password)
    
    print(f"Querying Space-Track for Epoch: {epoch_range}")
    data = st.gp_history(
        epoch=epoch_range,
        decay_date='null-val',
        format='json'
    )
    
    filename = 'historical_active.json'
    with open(filename, 'w') as f:
        if isinstance(data, str): 
            f.write(data)
        else:
            json.dump(data, f, indent=4)
    print("historical_active.json is ready!")