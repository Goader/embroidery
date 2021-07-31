from sklearn.neighbors import BallTree, DistanceMetric
import json
import os
import numpy as np


def RGB_to_HEX(rgb):
    return '%02x%02x%02x' % rgb


# Special metric based on human's sensitivity to red, green and blue
def dist(rgbx, rgby):
    dR = rgbx[0] - rgby[0]
    dG = rgbx[1] - rgby[1]
    dB = rgbx[2] - rgby[2]

    if dR < 128:
        return 2 * dR * dR + 4 * dG * dG + 3 * dB * dB
    else:
        return 3 * dR * dR + 4 * dG * dG + 2 * dB * dB


# Extracts all the threads stored in dmc.json as the dictionary
def get_dmcs():
    src_path = os.path.dirname(__file__)
    with open(os.path.join(src_path, 'dmc.json'), 'r') as to_read:
        dmcs = json.load(to_read)
        to_read.close()
        return dict(dmcs)


# Creates the Ball Tree with already inserted threads
def get_dmc_tree():
    metric = DistanceMetric.get_metric('pyfunc', func=dist)

    dmcs = get_dmcs()
    idxs = [thread['rgb'] for key, thread in dmcs.items()]
    tree = BallTree(np.array(idxs), leaf_size=5, metric=metric)
    return tree, dmcs, idxs


# Returns the most appropriate thread using the Ball Tree created above
def get_thread(rgb, tree, idxs, dmcs):
    idx = tree.query(np.array([rgb]), return_distance=False)
    rgb = idxs[idx[0][0]]
    hex_color = RGB_to_HEX(tuple(rgb))
    return dmcs[hex_color], rgb
