GloBiMaps - A Probabilistic Data Structure for In-Memory Processing of Global Raster Datasets
========

We are happy to announce that our latest research on a randomized data structure GloBiMap for high-resolution, low-cardinality global raster information (e.g., which place on Earth contains a building) has been selected for full-paper presentation at ACM SIGSPATIAL GIS. This repository contains some source code, which has been simplified to be independent from our Big Geospatial Data infrastructure.


Brought to you by

Martin Werner \
Technical Unviersity of Munich \
TUM Faculty of Aerospace and Geodesy \
Professorship for Big Geospatial Data Management


# API Overview

## Functions exported in the Python module

All functions you should use are exported in the class globimap, which you can instantiate more than once
in your code.

The functions are:

- rasterize (x,y, s0, s1): rasterize region from x,y with width s0 and height s1 and get a 2D numpy matrix back
- correct (x,y,s0,s1): apply correction (on local data cache, use rasterize before! There is no check you did it!)
- put (x,y): set a pixel at x,y
- get (x,y): get a pixel (as a bool)
- configure (k,m): set k hash functions and m bit (does allocate!)
- clear (): clear and delete everything
- summary(): give a summary of the data structure as a string (use for debugging from python, takes some time to generate)
- map(mat,o0,o1): basically "places" the matrix mat at o0, o1 setting values, which must be binary.
- enforce(mat, o0,o1): basically adds error correction information for the region map with these parameters would affect.

Some patterns / remarks:

- you should !not! call correct without rasterize. Rasterize uses the probabilistic layer and correct applies error correction to this very same storage.
- If you don't call put (or map) after using enforce, you are guaranteed to have no errors. If you add something, new errors can appear.


# A nice example application: Sierpinski's Triangle
In [test.py](#files) or in the file [sample.py](https://github.com/mwernerds/globimap/blob/master/src/sample.py) in the git repository you find a complete walk-through of how globimaps can be applied. To keep this git small, we generate
a sparse dataset algorithmically, in fact, we generate a point cloud that is dense in Sierpinski's triangle, that is, for
n to infinity, this becomes the Sierpinski triangle. In this way, our dataset is generated in 12 LOCs instead of downloading
a few megabytes.

I tuned parameters to show some things: First of all, the size is 4096x4096 pixels and we insert 500,000 points following
the so-called Chaos game: Having chosen some random location (usually inside the triangle, though this does not matter in the long run), randomly select one of the corners and update the current location to the middle of the straight line connecting the current location with the corner. Doing so infinitely creates a dense set of points in the Sierpinski fractal. Good for our purpose, as we need a sparse binary dataset.

With these parameters, two obvious ways of representing this are available:

- As a numpy array (as it is) with 32 bit per entry, that is exactly 64 MB.
- As a bit array (with one bit per pixel), that is 2 MB
- As a set of coordinates (with two bytes per coordinate, that is 4 byte per set pixel) ~1,4 MB (depends randomly on the start point)

Hence, let us look for a good size for a GloBiMap that helps us with this dataset. What about 1MB?

Okay, 1 MB is 2^23 bits, therefore, you see logm=23 in the source code.

With this, we can afford 15 hashes and get great results. Running sample.py results in

```
Memory: 1024.000000 KB
Hashes: 15 
(4096, 4096)
100%|██████████| 500000/500000 [00:04<00:00, 101727.62it/s]
Ones: 349162
Coordinate Memory (4 bytes): 1396648
Raster Memory (1 bit per pixel): 2048 KB
logm:23mask=83886070x7fffff
filter.size=8388608
Step 1: Probabilistic Encoding
Step 2: Error Correction Information
{
"storage:": 1,
"ones:": 3895346,
"foz:": 0.535639,
"eci": 163
}

Step 3: Rasterize
Have 0 errors for a BER of 0.000000
```

That is, first of all, the capacity is used well (about 0.53 FOZ), the ECI is 163 pixels (that is another 650 bytes for error correction information). And finally, it is error-free (after applying error correction algorithm).

If you now go a bit more agressive, you can chose half a megabyte for starge.As a consequence,
the number of hash functions should (roughly) be half. The following image has been generated with
0.5 MB of storage and 8 hash functions. Now, you see uniform noise in the random layer. But still, the number
of errors is only 50,633, that is 200k of error correction information (2x 2 byte per pixel). Hence, an error-free
data structure consumes only about 700k, much less than the one megabyte we chose for the almost error-free version.

# Resources

This package is meant to model sparse, global datasets in spatial computing. As these are typically large and copyrighted,
they did not make it to Github, but you will find information on those on my web page (sooner or later) as
well as in the paper.

- https://martinwerner.de/blog/2019/10/06/globimaps-sigspatial.html
- Werner, M. (2019). GloBiMaps - A Probabilistic Data Structure for In-Memory Processing of Global Raster Datasets. In 27th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (SIGSPATIAL ’19).


The paper is directly available from here: https://martinwerner.de/pdf/2019globimap.pdf