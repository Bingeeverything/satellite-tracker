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