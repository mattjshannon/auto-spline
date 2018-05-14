# auto-spline

The premise is to improve upon the method in which we draw spline continua in astronomical spectra. For instance, here is the infrared spectrum of an observation from near the Galactic Center:

![Example spline continuum](/docs/images/fig3.png)

The observed data are shown in sky blue, and the solid black line defines the "continuum" level, i.e. the line dividing individual features (above the continuum) and bulk emission that cannot generally be separated (a mixture of starlight, emission from dust grains, small molecules, etc). Sometimes a secondary spline is drawn beneath the primary spline to identify "plateaus" (shaded green regions), which are thought to originate from different species than the underlying continuum emission or the individual features above.

Note the continuum (solid black line) is a **spline**, i.e. a *piecewise polynomial function*. The spline is determined by its **anchor points** (blue circles in the above figure), which combined with a degree of curvature (typically *k=3*) produces the curve we see above, for instance.

# How splines are currently drawn

As written above, the spline is determined by its *anchor points*. Thus, in the current methodology, it is important to choose appropriate x-axis (or abscissa--here, wavelength) positions for the anchor points. The idea is that the anchor points should (generally) sit on either side of an emission feature, so that we have a reasonably smooth continuum in the region of the feature itself. So for instance, the main PAH bands are at...

6.2, 7.7, 8.6, 11.2, 12.7 μm.

Thus, you typically see anchor points near [5.9 μm, 6.6 μm] (to isolate the 6.2 μm feature), [7.2 μm, 8.2 μm] (to isolate the 7.7 μm feature), and so on.

The *problem* is that depending on the noise levels and how much the continuum shape varies (which can be significant when you look at different astronomical objects), you can't in general "set-and-forget" hard-coded continuum anchor point locations. Instead, you inevitably need to adjust/wiggle the anchor points slightly -- in some places, this ends up meaning you need to allow a window of movement for an anchor point, or in other regions you end up needing to smooth your data to get a "good looking" continuum.

## The purpose of the spline

Generally, the purpose of the spline (and continuum in general for that matter) is so that you can extract trends, correlations and statistics from your data. The continuum is drawn because we basically assume that the small emission features (the wiggly bits) are easy to isolate/measure, whereas it is very difficult to discern the components that may be contributing to the underlying continuum/broad emission (which can be numerous).

In terms of data treneds, the strengths of the emission features are known to vary as well as correlate; for instance, if you measure the flux of the 6.2, 7.7 and 11.2 bands (i.e., integrate the emission near those wavelengths that lies above the continuum), you can find that there is in general a *very* strong correlation between the 6.2/11.2 flux ratio and the 7.7/11.2 flux ratio (i.e., a plot of 6.2/11.2 vs 7.7/11.2).

## The problem with splines

The issue is that drawing a spline ends up being a manual task -- you can start with a set of "these usually work" anchor points, including special modifications like smoothing or allowing for movement, but you inevitably need to examine and readjust most of the continua you draw.

# The premise

The idea here is: can we improve upon the way splines are drawn? Or for that matter, are they even strictly necessary? Ideally we would like to tease out correlations and trends without manually examining/adjusting each spline continuum. This would allow us to examine larger data sets than is feasible at the moment.

## Data

### Cubes

These data originate from a "spectral cube", i.e. the spectra are from observations that are adjacent on the sky (e.g., from a 30-pixel by 20-pixel cube, each pixel of which has a spectrum as in the above figure). As such, there is some degree of similarity/dependence between the spectra in these cubes.

There are four cubes, one for each of the following objects:
NGC 7023, NGC 2023 South, NGC 2023 North, and M17

The cubes have been split into text files for simplicity, one for each position in the cube (e.g., NGC7023_fazio_x0_y0.txt, NGC7023_fazio_x0_y2.txt, NGC7023_fazio_x2_y0.txt). 

Within each text file, there are five columns:

``wave, flux, fluxerr, continuum, continuum plateau``

Ignoring the last column for now, these correspond to...

``x, y, y-error, and fitted spline continuum (in y units)``

### Galcen

These data are from four astronomical fields directed toward the center of our Galaxy. They are ``C32, C35, OGLE`` and ``NGC 6522``. Each one contains less than two dozen spectra, split into text files (one for each position inside the field).

These data have the following format, with six columns:

``wave, flux, fluxerr, csub, csuberr, spline_flux``

We only need ``wave``, ``flux``, ``fluxerr`` and ``spline_flux`` to draw the spectrum as shown in the first figure.

# Checking out the data

For the cubes, see ``spline/spline.py`` which currently loads in the variables (wave, flux, fluxerr, spline) as 1D numpy arrays.
