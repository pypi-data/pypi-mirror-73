"""
Author: "Rafiga Masmaliyeva, Kaveh Babai, Garib N. Murshudov"

    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""

import fire


from tobvalid.mixture.gaussian_mixture import GaussianMixture
from tobvalid.mixture.invgamma_mixture import InverseGammaMixture
import tobvalid.stats.silverman as sv
import tobvalid.parsers.gparser as gp
import tobvalid.stats.pheight as ph
import tobvalid.local.analysis as lc
import tobvalid.stats.outliers as ot
import os
import shutil
import numpy as np



def tobvalid(i, o=None, m=1, t=1e-5, hr=150, a="all", it=100):

    mode = m
    try:
        file_name = process_input(i)
        out = proccess_output(i, o, file_name)
        process_analysis(a)
        process_mode(mode)
        process_tolerance(t)
        process_dpi(hr)

        if a in ['all', 'local']:
            lc.local_analysis(i, out)
        if a in ['all', 'global']:
            (s, data, data_with_keys) = gp.gemmy_parse(i)
            process_data(data)
    except ValueError as e:
        return e

    if a == 'local':
        return 

    if s == 0:
        return "Resolution is 0"

    ot.print_outliers(out + "/Interquartile outliers.txt", data, data_with_keys)

    data = ot.remove_outliers(data)


    if len(data) <= 100:
        return "There is not sufficient amount of data to analyse, the results may left questions. Do not hesitate to contact ToBvalid team"

    z = None


    p_data = ph.peak_height(data, s)
    gauss = GaussianMixture(mode, tol=t)
    gauss.fit(p_data)
    if gauss.n_modes > 1:
        z = gauss.Z[:, ::-1]
    gauss.savehtml(out, file_name, dpi=hr)
    mode = gauss.n_modes 

    inv = InverseGammaMixture(mode, tol=t, max_iter=it)
    inv.fit(data, z=z)       
    inv.savehtml(out, file_name, dpi=hr)


    if inv.n_modes == 1:
        if (max(inv.alpha) > 10 or max(np.sqrt(inv.betta) > 30)):
          print("High values of alpha and/or beta parameters. Please consider the structure for re-refinement with consideraton of blur or other options")




def process_data(data):
    if min(data) < 0:
        raise ValueError(
            "Zero or minus values for B factors are observed. Please consider the structure model for re-refinement or contact the authors")


def process_input(i):
    if not os.path.exists(i):
        raise ValueError("Input path {} doesn't exist".format(i))

    if not os.path.isfile(i):
        raise ValueError("{} is not file".format(i))

    return os.path.basename(os.path.splitext(i)[0])


def proccess_output(i, o, file_name):

    out = ""
    if o == None:
        out = os.getcwd()
    else:
        if not os.path.exists(o):
            raise ValueError("output path {} doesn't exist".format(o))

        if not os.path.isdir(o):
            raise ValueError("{} is not directory".format(o))
        out = o

    out = out + "/" + file_name

    try:
        if os.path.exists(out) and os.path.isdir(out):
            shutil.rmtree(out)
        os.mkdir(out)
    except OSError:
        raise ValueError("Creation of the directory %s failed" % out)

    return out


def process_analysis(a):
    if a in ['all', 'global', 'local']:
        return

    raise ValueError("-a has to be 'all', 'global' or 'local'")


def process_mode(mode):
    if mode == 'auto':
        return
    if not isinstance(mode, int):
        raise ValueError("-m has to be integer or 'auto'")

    if mode < 1:
        raise ValueError("-m has to be greater than zero or equal to 'auto'")


def process_tolerance(t):
    if not isinstance(t, float) and not isinstance(t, int):
        raise ValueError("-t has to be float")

    if t <= 0:
        raise ValueError("-t has to be greater than zero")


def process_dpi(d):
    if not isinstance(d, int):
        raise ValueError("-d has to be integer")

    if d < 72:
        raise ValueError("-d has to be greater or equal to 72 ")


def main_func():
    fire.Fire(tobvalid)

if __name__ == '__main__':
    fire.Fire(tobvalid)
