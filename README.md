# Automated Satellite Pass Correlator

## Overview
This repository contains a Python-based computer vision and astrodynamics pipeline designed to automatically detect and identify active satellites in long-exposure astrophotography. By bridging uncompressed sensor data with SGP4 orbital propagation, the algorithm projects real-world topocentric ephemerides onto a 2D camera pixel space.

## System Architecture (Phase 1)
The pipeline is strictly divided into five distinct mathematical and data processing milestones:

### 1. Raw Metadata Parsing & Matrix Instantiation
- **Objective:** [Extracting the EXIF Metadata]
- **Implementation:** Utilizes `exiftool` to extract `SubSecDateTimeOriginal` and GPS coordinates, and `tifffile` to load the 16-bit uncompressed `.dng` sensor data into a continuous NumPy array.

### 2. Radiometric Scaling & High-Pass Filtering
- **Objective:** [A GreyScale Image]
- **Implementation:** Normalizes 16-bit sensor data to standard 8-bit matrices using 99.9th percentile clipping to prevent outlier corruption. Extracts the low-frequency background (Milky Way/skyglow) using a massive Gaussian kernel (151x151) and performs Saturation Subtraction to isolate the high-frequency satellite signals.

### 3. Geometric Feature Extraction (Hough Space)
- **Objective:** [Finding the Streaks of Satellites]
- **Implementation:** Passes the mathematically flattened background through a probabilistic Hough Transform to extract the terminal Cartesian vectors (Start X/Y, End X/Y) of continuous streaks while ignoring static stellar points. 

### 4. Ephemeris Generation & Orbital Mechanics
- **Objective:** Calculate the Topocentric Altitude and Azimuth of all active satellites relative to the observer at the exact moment of exposure.
- **Implementation:** Leverages the `Skyfield` library to download JSON OMM TLE data from CelesTrak. Utilizes the SGP4 physical model to calculate ECEF coordinates, subtracting the observer's physical WGS84 location to generate a local horizon mask (discarding satellites below 15 degrees).[To be Perfected]
### 5. Projective Geometric Correlator (WIP)
- **Objective:** Mathematically project the 3D sky onto a flat 2D sensor plane to cross-reference orbital models with physical pixel tracks.
- **Implementation:** [To be completed - Pinhole Camera Model and FOV Projection]

## Prerequisites & Installation
* Python 3.10+
* `exiftool` (Must be installed at the system level or path defined in `.env`)
* Required Python Libraries: In the requirements.txt file

```bash
# Clone the repository
git clone [...]

# Install dependencies
pip install -r requirements.txt

# Setup Environment Variables
# Create a .env file in the root directory and add:
EXIFTOOL_PATH="C:/path/to/your/exiftool.exe"
