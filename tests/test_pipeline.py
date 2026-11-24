import cv2
import numpy as np
from skyfield.api import EarthSatellite, load


def test_hough_detects_synthetic_streak():
    # Create a black 500x500 frame with a bright diagonal line (simulating a satellite streak)
    img = np.zeros((500, 500), dtype=np.uint8)
    cv2.line(img, (50, 50), (350, 350), 255, thickness=2)

    # Run probabilistic Hough transform (matching Stage 3)
    lines = cv2.HoughLinesP(
        img, rho=1, theta=np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10
    )

    assert lines is not None, "Expected to detect the synthetic satellite streak"
    assert len(lines) >= 1


def test_sgp4_propagation_produces_valid_position():
    # Sample ISS TLE data to verify Skyfield + SGP4 math works offline
    line1 = "1 25544U 98067A   24001.50000000  .00016717  00000-0  10270-3 0  9005"
    line2 = "2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.49815350424739"

    ts = load.timescale()
    sat = EarthSatellite(line1, line2, "ISS (ZARYA)", ts)
    t = ts.utc(2024, 1, 1, 12, 0, 0)

    geocentric = sat.at(t)
    position_km = geocentric.position.km

    # Ensure coordinates are finite numbers and at a realistic LEO distance (~6,700 km from Earth's center)
    assert not np.isnan(position_km).any()
    distance_from_earth_center = np.linalg.norm(position_km)
    assert 6500 < distance_from_earth_center < 7200
