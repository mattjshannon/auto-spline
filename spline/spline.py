#!/usr/bin/env python
"""
spline.py

Looking for trends and correlations in our data, with or without a spline fit?
"""


import glob
import numpy as np

from ipdb import set_trace as st


def read_spectrum(file_in, head_type='cube'):
    """Read in a spectrum from a text file, from a cube.

    Args:
        head_type (str): Either 'cube' or 'galcen', different data headers.

    Returns:
        wave (ndarray): Wavelength array.
        flux (ndarray): Flux array.
        fluxerr (ndarray): Flux error array.
        spline (ndarray): Spline continuum array.
    """

    # Read in spectrum file.
    # Loaded as 'str' initially due to a byte conversion issue.
    try:
        data_in = np.loadtxt(file_in, delimiter=',', dtype='str')
    except Exception as e:
        print(e)

    # Cut off the extraneous final column
    data_in = data_in[:, :-1].astype(float).T

    # Assign variables.
    if head_type == 'cube':
        wave, flux, fluxerr, spline, _ = data_in
    elif head_type == 'galcen':
        print("code this here.")
        st()

    return wave, flux, fluxerr, spline


def read_cube(obj_name):
    """Read in a spectrum from a data cube.

    Args:
        obj_name (str): One of ['NGC7023, 'NGC2023S, 'NGC2023N, 'M17']
        x (int): x position in map.
        y (int): y position in map.

    Returns:
        undecided
    """

    # Location of spectra files.
    data_dir = '../data/cubes/' + obj_name + '/spectra/'

    # For now, just a 1D list of files.
    spectra_files = np.sort(glob.glob(data_dir + '*.txt'))

    # Some holding variables. Can be 2D later, probably 1D is fine?
    all_wave = []
    all_flux = []
    all_fluxerr = []
    all_spline = []

    # Iterate over the list and return spectra
    for index, file_name in enumerate(spectra_files):

        # Read the spectra in. Maybe yield later on?
        tmp = read_spectrum(file_name)
        all_wave.append(tmp[0])
        all_flux.append(tmp[1])
        all_fluxerr.append(tmp[2])
        all_spline.append(tmp[3])

    # Convert to numpy arrays.
    all_wave = np.array(all_wave)
    all_flux = np.array(all_flux)
    all_fluxerr = np.array(all_fluxerr)
    all_spline = np.array(all_spline)

    return all_wave, all_flux, all_fluxerr, all_spline


# List of data cubes.
obj_list = ['NGC7023', 'NGC2023S', 'NGC2023N', 'M17']
obj = obj_list[0]

# Numpy arrays for wave, flux, fluxerr, spline.
# each element == data for one spectrum.
# i.e. should be 195 elements (spectra) for NGC 7023.
w, f, e, s = read_cube(obj)

print("Cube read OK!")



