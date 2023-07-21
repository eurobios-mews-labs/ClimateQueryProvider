# Copyright 2023 Eurobios
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import numpy as np
import pandas as pd
import os

def get_bbox():
    bbox = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/bbox_countries.csv')
    return bbox

def deg_to_rad(alpha):
    """

    :param alpha: angle in degrees
    :return: angle in rad
    """
    return alpha * np.pi / 180

def compute_wind_speed(u_ms, v_ms):
    return np.sqrt(u_ms ** 2 + v_ms ** 2)

def compute_wind_dir(u_ms, v_ms):
    """

    :param u_ms: east west wind speed
    :param v_ms: south north wind wpeed
    :return: wind direction
    """
    return np.mod(180 + np.arctan2(v_ms, u_ms) * 180 / np.pi, 360)

def compute_normal_wind(ws, wd, azimuth):
    """

    :param ws: wind speed
    :param wd: wind direction in rad
    :param azimuth: azimuth of the line
    :return:
    """
    wd = np.mod(wd, 180)
    wd = deg_to_rad(wd)
    azimuth = deg_to_rad(azimuth)
    return np.abs(ws * np.sin(wd - azimuth))

def compute_normal_wind(ws, wd, azimuth):
    """

    :param ws: wind speed
    :param wd: wind direction
    :param azimuth: azimuth of the line
    :return:
    """
    wd = np.mod(wd, 180)
    wd = deg_to_rad(wd)
    azimuth = deg_to_rad(azimuth)
    return np.abs(ws*np.sin(wd-azimuth))

# def get_neighbors_coords(self, lat, lon):
#     """
#     Function to get nearest grid coordinates
#     :param lat: latitude
#     :param lon: longitude
#     :return: l
#     """

#     lat_inf = pr.LATS[pr.LATS <= lat][-1]
#     lat_sup = pr.LATS[pr.LATS > lat][0]
#     lon_inf = pr.LONS[pr.LONS <= lon][-1]
#     lon_sup = pr.LONS[pr.LONS > lon][0]

#     return {'lat_inf': lat_inf, 'lat_sup': lat_sup, 'lon_inf': lon_inf, 'lon_sup': lon_sup,
#             'coords': [(lat_inf, lon_inf), (lat_inf, lon_sup), (lat_sup, lon_inf), (lat_sup, lon_sup)]}

# # bilinear interpolation

# def get_meteo_data_interpolate(self, lat, lon, l_vars, l_y=range(2000, 2010)):
#     """
#     Function to interpolate data for a given latitude and longitude
#     :param lat: latitude
#     :param lon: longitude
#     :param l_vars: liste of variables
#     :param l_y: list of years
#     :return:
#     """
#     neighbors = self.get_neighbors_coords(lat, lon)
#     lat_inf, lat_sup, lon_inf, lon_sup = neighbors['lat_inf'], \
#                                          neighbors['lat_sup'], \
#                                          neighbors['lon_inf'], \
#                                          neighbors['lon_sup']

#     print('Interpolation from 4 nearest gps points')

#     f11 = self.get_meteo_data(lat_inf, lon_inf, l_vars=l_vars, l_y=l_y)
#     f12 = self.get_meteo_data(lat_inf, lon_sup, l_vars=l_vars, l_y=l_y)
#     f21 = self.get_meteo_data(lat_sup, lon_inf, l_vars=l_vars, l_y=l_y)
#     f22 = self.get_meteo_data(lat_sup, lon_sup, l_vars=l_vars, l_y=l_y)

#     dfx = f21 - f11
#     dfy = f12 - f11
#     dfxy = f11 + f22 - f21 - f12

#     dx = lat - lat_inf
#     dy = lon - lon_inf
#     Dx = lat_sup - lat_inf
#     Dy = lon_sup - lon_inf

#     f_ret = f11 + (dfx*dx)/Dx + (dfy*dy)/Dy + (dfxy*dx*dy)/(Dx*Dy)

#     return f_ret