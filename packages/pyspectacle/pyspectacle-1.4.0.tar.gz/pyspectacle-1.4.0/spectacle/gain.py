"""
Code relating to gain calibration, such as loading gain maps.
"""

import numpy as np

def load_gain_map(root, return_filename=False):
    """
    Load the gain map located at `root`/calibration/gain.npy

    If `return_filename` is True, also return the exact filename used.
    """
    filename = root/"calibration/gain.npy"
    gain_map = np.load(filename)
    if return_filename:
        return gain_map, filename
    else:
        return gain_map


def convert_to_photoelectrons_from_map(gain_map, data):
    """
    Convert `data` from normalised ADU to photoelectrons using a map of gain
    in each pixel `gain_map`.
    """
    data_converted = data / gain_map

    return data_converted
