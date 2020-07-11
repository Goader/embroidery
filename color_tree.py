from sklearn.neighbors import BallTree, DistanceMetric
from math import sqrt
import json
import numpy as np


def RGB_to_HEX(rgb):
    return "%02x%02x%02x" % rgb


def dist(rgbx, rgby):
    dR = rgbx[0] - rgby[0]
    dG = rgbx[1] - rgby[1]
    dB = rgbx[2] - rgby[2]

    if dR < 128:
        # return sqrt( 2 * dR * dR + 4 * dG * dG + 3 * dB * dB )
        return 2 * dR * dR + 4 * dG * dG + 3 * dB * dB
    else:
        # return sqrt( 3 * dR * dR + 4 * dG * dG + 2 * dB * dB )
        return 3 * dR * dR + 4 * dG * dG + 2 * dB * dB


def get_dmcs():
    with open("dmc.json", "r") as to_read:
        dmcs = json.load(to_read)
        to_read.close()
        return dict(dmcs)


def get_dmc_tree():
    metric = DistanceMetric.get_metric("pyfunc", func=dist)
    #metric = DistanceMetric.get_metric('euclidean')

    dmcs = get_dmcs()
    idxs = [thread["rgb"] for key, thread in dmcs.items()]
    tree = BallTree(np.array(idxs), leaf_size=250, metric=metric)
    return tree, dmcs, idxs


def get_thread(rgb, tree):
    idx = tree.query(np.array([rgb]), return_distance=False)
    return idx[0][0]


def get_thread_info(idx, idxs, dmcs):
    rgb = idxs[idx]
    hex_color = RGB_to_HEX(tuple(rgb))
    return dmcs[hex_color]["number"], rgb
