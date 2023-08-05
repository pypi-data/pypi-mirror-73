from obspy.geodetics import gps2dist_azimuth
from math import sin, cos, radians
from obspy import read
from pandas import read_csv
from glob import glob
import os
import numpy as np



from obspy.geodetics import gps2dist_azimuth
from math import sin, cos, radians
from obspy import read
from pandas import read_csv
import os
import numpy as np


# rotate then correlate
def rotation_matrix(baz):
    baz_rad = radians(baz)
    rot_er = -sin(baz_rad)
    rot_nr = -cos(baz_rad)
    rot_et = -cos(baz_rad)
    rot_nt = sin(baz_rad)

    #return(rot_nr, rot_nt, rot_er, rot_et)
    return(np.asarray([[1, 0, 0], [0, rot_nr, rot_nt], [0, rot_er, rot_et]]))


def add_metadata(tr, seedid1, seedid2, lat1, lat2, lon1, lon2):

    tr.stats.network = seedid1.split('.')[0]
    tr.stats.station = seedid1.split('.')[1]
    tr.stats.location = ''
    tr.stats.channel = seedid1.split('.')[3]
    tr.stats.sac.stlo = lon1
    tr.stats.sac.stla = lat1
    tr.stats.sac.evlo = lon2
    tr.stats.sac.evla = lat2
    tr.stats.sac.kuser0 = seedid2.split('.')[0]
    tr.stats.sac.kevnm = seedid2.split('.')[1]
    tr.stats.sac.kuser1 = ''
    tr.stats.sac.kuser2 = seedid2.split('.')[3]
    tr.stats.sac.user0 = 1
    geoinf = gps2dist_azimuth(lat1, lon1, lat2, lon2)
    tr.stats.sac.dist = geoinf[0]
    tr.stats.sac.az = geoinf[1]
    tr.stats.sac.baz = geoinf[2]


def apply_rotation(fls, stationlistfile, output_directory):
    # Apply rotation of the horizontal components for the cross-correlation output.
    # Note that the source input remains E, N, Z
    # i.e. instead of C_nn = sum(source_nn * crosscorr(G1_nn, G2_nn)) we will have
    # C_rr = sum(source_nn * crosscorr(G1_rn, G2_rn))
    c_test = read(fls[4])[0]
    len_tseries = c_test.stats.npts

    C = np.zeros((len_tseries, 3, 3))
    # load data
    c_ee = read(fls[0])[0]
    c_en = read(fls[1])[0]
    c_ez = read(fls[2])[0]
    c_ne = read(fls[3])[0]
    c_nn = read(fls[4])[0]
    c_nz = read(fls[5])[0]
    c_ze = read(fls[6])[0]
    c_zn = read(fls[7])[0]
    c_zz = read(fls[8])[0]

    C[:, 0, 0] = c_zz.data
    C[:, 0, 1] = c_zn.data
    C[:, 0, 2] = c_ze.data
    C[:, 1, 0] = c_nz.data
    C[:, 1, 1] = c_nn.data
    C[:, 1, 2] = c_ne.data
    C[:, 2, 0] = c_ez.data
    C[:, 2, 1] = c_en.data
    C[:, 2, 2] = c_ee.data
    # get locations
    meta = read_csv(stationlistfile)

    net1, sta1, loc1, cha1 = os.path.basename(fls[0]).split('.')[0: 4]
    try:
        net2, sta2, loc2, cha2 = os.path.basename(fls[0]).\
            split('--')[1].split('.')[0: 4]
    except IndexError:
        net2, sta2, loc2, cha2 = os.path.basename(fls[0]).split('.')[4: 8]

    channel_basename = cha1[0: 2]

    print(sta1, sta2)
    lat1 = float(meta[meta['sta'] == sta1].iloc[0]['lat'])
    lat2 = float(meta[meta['sta'] == sta2].iloc[0]['lat'])
    lon1 = float(meta[meta['sta'] == sta1].iloc[0]['lon'])
    lon2 = float(meta[meta['sta'] == sta2].iloc[0]['lon'])

    baz = gps2dist_azimuth(lat1, lon1, lat2, lon2)[2]

    # get rotation matrix
    G = rotation_matrix(baz)
    # recombine
    C_rot = np.matmul(np.matmul(G.T, C), G)

    tr_rr = c_nn.copy()
    tr_tt = c_ee.copy()
    tr_rt = c_ne.copy()
    tr_tr = c_en.copy()
    tr_zr = c_zn.copy()
    tr_zt = c_ze.copy()
    tr_rz = c_nz.copy()
    tr_tz = c_ez.copy()

    tr_rr.data = C_rot[:, 1, 1]  # c_rr_data
    tr_tt.data = C_rot[:, 2, 2]  # c_tt_data
    tr_rt.data = C_rot[:, 1, 2]  # c_rt_data
    tr_tr.data = C_rot[:, 2, 1]  # c_tr_data
    tr_zt.data = C_rot[:, 0, 2]  # c_zt_data
    tr_zr.data = C_rot[:, 0, 1]  # c_zr_data
    tr_tz.data = C_rot[:, 2, 0]  # c_tz_data
    tr_rz.data = C_rot[:, 1, 0]  # c_rz_data

    # copy / add metadata
    seedid1 = "{}.{}.{}.".format(net1, sta1, loc1)
    seedid2 = "{}.{}.{}.".format(net2, sta2, loc2)

    cha_r = channel_basename + "R"
    cha_t = channel_basename + "T"
    cha_z = channel_basename + "Z"
    add_metadata(tr_rr, seedid1 + cha_r, seedid2 + cha_r, lat1, lat2, lon1, lon2)
    add_metadata(tr_tt, seedid1 + cha_t, seedid2 + cha_t, lat1, lat2, lon1, lon2)
    add_metadata(tr_rt, seedid1 + cha_r, seedid2 + cha_t, lat1, lat2, lon1, lon2)
    add_metadata(tr_tr, seedid1 + cha_t, seedid2 + cha_r, lat1, lat2, lon1, lon2)
    add_metadata(tr_zr, seedid1 + cha_z, seedid2 + cha_r, lat1, lat2, lon1, lon2)
    add_metadata(tr_zt, seedid1 + cha_z, seedid2 + cha_t, lat1, lat2, lon1, lon2)
    add_metadata(tr_rz, seedid1 + cha_r, seedid2 + cha_z, lat1, lat2, lon1, lon2)
    add_metadata(tr_tz, seedid1 + cha_t, seedid2 + cha_z, lat1, lat2, lon1, lon2)
    

    
    # write
    filename_tr_rr = os.path.join(output_directory, seedid1 + cha_r + "--" + seedid2 + cha_r + ".sac")
    filename_tr_tt = os.path.join(output_directory, seedid1 + cha_t + "--" + seedid2 + cha_t + ".sac")
    filename_tr_rt = os.path.join(output_directory, seedid1 + cha_r + "--" + seedid2 + cha_t + ".sac")
    filename_tr_tr = os.path.join(output_directory, seedid1 + cha_t + "--" + seedid2 + cha_r + ".sac")
    filename_tr_rz = os.path.join(output_directory, seedid1 + cha_r + "--" + seedid2 + cha_z + ".sac")
    filename_tr_tz = os.path.join(output_directory, seedid1 + cha_t + "--" + seedid2 + cha_z + ".sac")
    filename_tr_zt = os.path.join(output_directory, seedid1 + cha_z + "--" + seedid2 + cha_t + ".sac")
    filename_tr_zr = os.path.join(output_directory, seedid1 + cha_z + "--" + seedid2 + cha_r + ".sac")
    
    
    
    
    tr_rr.write(filename_tr_rr, format="SAC")
    tr_tt.write(filename_tr_tt, format="SAC")
    tr_rt.write(filename_tr_rt, format="SAC")
    tr_tr.write(filename_tr_tr, format="SAC")
    tr_rz.write(filename_tr_rz, format="SAC")
    tr_tz.write(filename_tr_tz, format="SAC")
    tr_zt.write(filename_tr_zt, format="SAC")
    tr_zr.write(filename_tr_zr, format="SAC")
    
