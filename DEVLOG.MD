- Thursday November 5
{Added a solve PNP from open cv to get the rotation vectors, for that i had to see the time i took the photo, went to stellarium to that exact time down to seconds, and i know this is very mechanical but i would change it later, but after this, i went to ms paint and got the X and y coords for 4 points, i also got the RA and declination from stellarium for those 4 stars
and then calculated them in degrees and     K = np.array([
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
    ], dtype=np.float32)
    calacuted values for this extrinsic matrix and plugged in the pnp function to get the vectors}


- Wednesday November 11
{Finally getting the output streak from projecting the x y z, i also cleared that for an import inside the package i need to do .(filename) also i added some more arguments that i had to pass to satellite locator for it do project the poiints}


- Thursday November 19
{Foxed the point to point line thing in main.py but still have the duplicate streaks to fix out, but finally got the list of streaks from 3000 sats}

-Monday November 22
{feat(correlator): add bounding-box filter for finite trajectory matching

- Constrain streak endpoint correlation to the satellite's finite segment bounds (+/- 10px margin)
- Prevent infinite-line false positives across unrelated regions of the frame
- Rank valid candidates by lowest mean perpendicular distance for 1-to-1 matching
- added back topocentric .altaz
- will try inccreasing my lowest error to check what goes on since rn i got 0 satellites, maybe because of my exposure time but ill try}

- Tuesday November 24
{not sure why the output is like this Streak Detected from Pixel L to A matches the trajectory of satellite ((np.int32(1091), np.int32(732)), (np.int32(1095), np.int32(463)))
where does the L and A come from
}