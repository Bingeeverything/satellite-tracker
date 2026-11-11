# Satellite Tracker

Identifying satellites in long-exposure night-sky photos taken on a phone (Samsung Galaxy S24 Ultra).

The pipeline finds satellite streaks in a photo, works out where in the sky the camera was pointing, and predicts where every known satellite was at the moment of the shot. Matching the two puts a name on each streak.

> All code in this repo is written by hand, without AI-generated code. The commit history records the debugging along the way.

## Status

| Stage | What it does | Status |
|---|---|---|
| 1. Metadata | Reads the sub-second capture time and GPS from EXIF with exiftool; asks for coordinates if they're missing | ✅ Done |
| 2. Image prep | Loads the DNG with tifffile, converts it to greyscale and scales it to 8-bit with 99.9th-percentile clipping | ✅ Done |
| 3. Streak detection | Subtracts the sky background (151×151 Gaussian blur), thresholds, and finds streak endpoints with a probabilistic Hough transform | ✅ Done (tuned on one photo) |
| 4. Orbital data | Downloads historical element sets for the capture date ±1 day from Space-Track, removes duplicates and loads them into Skyfield | ✅ Done |
| 5. Plate solving | Detects stars with DAOStarFinder and sends the 100 brightest to Astrometry.net to work out where the camera was pointing | 🚧 Written, not yet tested end to end |
| 6. Correlation | Computes each satellite's position at capture time, projects it onto the image and matches it to a detected streak | ⏳ Next |

## What I learned along the way

- **A phone's RAW file isn't really raw.** The S24 Ultra saves DNGs that are already demosaiced, so rawpy can't read them. tifffile can, because a DNG is a TIFF underneath.
- **Old photos need old orbits.** Current orbital data from CelesTrak gave wrong results for older photos, so the pipeline pulls historical element sets from Space-Track for the capture date.
- **Historical queries return duplicates.** A ±1-day window returns several element sets per satellite. Keeping one per catalogue number cut the number of objects to check by about 70%.

## Results

[Add an image of detected streaks here, and later the labelled version.]

## Requirements

- Python 3.10+
- [exiftool](https://exiftool.org/) installed
- Free accounts on [Space-Track](https://www.space-track.org/) and [Astrometry.net](https://nova.astrometry.net/) (for an API key)

## Setup

```bash
git clone https://github.com/Bingeeverything/satellite-tracker.git
cd satellite-tracker
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
EXIFTOOL_PATH="C:/path/to/exiftool.exe"
SPACETRACK_EMAIL="you@example.com"
SPACETRACK_PASSWORD="your-password"
ASTRONOMY_NET_API="your-astrometry-api-key"
```

## Usage

1. Put a DNG in `images/` and set `dng_path` at the top of `main.py` (it's hard-coded for now).
2. Run `python main.py`.
3. Detected streaks are saved to `Result Image.jpg`.

**Note:** the script writes GPS tags into the DNG in place, so run it on a copy of your photo.

## Roadmap

- Match streaks to named satellites (stage 6)
- Make streak detection work across photos, not just the one it was tuned on
- Tell satellites apart from planes and meteors
- Estimate angular speed from streak length and exposure time
- Estimate how fast an object is tumbling from brightness changes along its streak

## Built with

tifffile · NumPy · OpenCV · PyExifTool · Skyfield · spacetrack · Astropy · astroquery · photutils
