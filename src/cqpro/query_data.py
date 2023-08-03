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
import sys, os
sys.path.append(os.path.dirname(__file__))

import xarray as xr
import pandas as pd
import numpy as np
from utils import memo_chrono

class retriever:

    def __init__(self, path: str, file_name: str) -> None:

        self.file = xr.open_dataset(path + file_name)
        
        d_grid_range = self._get_grid_range()
        d_history_range = self._get_history_range()

        self.lat_min, self.lat_max, self.lon_min, self.lon_max = d_grid_range['lat_min'], d_grid_range['lat_max'], d_grid_range['lon_min'], d_grid_range['lon_max']
        self.history_min, self.history_max = d_history_range['min'], d_history_range['max']

        self.var_name = self._get_var_name()
        
    def _get_var_name(self) -> list:
        """Retrieve available variables in file.

        Parameters
        ----------
        None

        Returns
        -------
        list
            List of available variables.
        """

        if self.file is not None:
            return list(self.file.keys())[0]
        
    def _get_grid_range(self) -> dict:
        """Retrieve grid range in file.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            Minimal and maximal latitude and longitude.
        """
        
        lat_min, lat_max = self.file.latitude.min().item(), self.file.latitude.max().item()
        lon_min, lon_max = self.file.longitude.min().item(), self.file.longitude.max().item()

        return {'lat_min': lat_min, 'lat_max': lat_max, 'lon_min': lon_min, 'lon_max': lon_max}
    
    def _get_history_range(self) -> dict:
        """Retrieve history range in file.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            Minimal and maximal dates.
        """

        history_min, history_max = pd.to_datetime(self.file.time.min().item()), pd.to_datetime(self.file.time.max().item()) 

        return {'min': history_min, 'max': history_max}
    
    def check_in_box_l(self, lats, lons):
        """Check if list of gps points are in the grid range

        Parameters
        ----------
        lats : np.ndarray
            List of latitudes 
        lons : np.ndarray
            List of longitudes

        Returns
        -------
        bool
            True if all gps points are in the grid range of the file, False instead.
        """

        for lat, lon in zip(lats, lons):
            if self.check_in_box(lat, lon):
                continue
            else:
                return False
        return True
    
    def check_in_box(self, lat: float, lon: float) -> bool:
        """Check if gps point is in grid range.

        Parameters
        ----------
        lat : float
            Latitude.
        lon : float
            Longitude.

        Returns
        -------
        bool
            True if gps point in the grid range of the file, False instead.
        """
        if lat >= self.lat_min and lat <= self.lat_max and lon >= self.lon_min and lon <= self.lon_max:
            return True
        print('GPS point ({0}, {1}) not in the range'.format(lat, lon))
        return False
    
    def check_in_history(self, history_start: pd.Timestamp, history_end: pd.Timestamp) -> bool:
        """Check if start and end date are in history range.

        Parameters
        ----------
        history_start : Timestamp
            Beggining timestamp.
        history_end : Timestamp
            End timestamp.

        Returns
        -------
        bool
            True if the history queried is within history range, False instead.
        """
        if history_start > history_end:
            raise Exception('History start should be before History end')

        else :
            if history_start >= self.history_min and history_end <= self.history_max: 
                return True
            return False

    @memo_chrono
    def get_data(self, lats: np.ndarray, lons: np.ndarray, history_start: str = None, history_end: str = None,
                xarray: bool = False, check_in_box_bool: bool = False) -> pd.DataFrame:
        """Main function to retrieve meteo data

        Parameters
        ----------
        lats : np.ndarray
            List of latitudes.
        lons : np.ndarray
            List of longitudes
        history_start : Timestamp
            Beggining timestamp.
        history_end : Timestamp
            End timestamp.
        xarray : boolean
            True to retrieve data as a xarray.Dataset
        check_in_box_bool : boolean
            True to raise error if gps point not in the box / False to continue without checking

        Returns
        -------
        DataFrame
            .
        """
        if len(lats) != len(lons): raise Exception('longitudes and latitudes do not match length')

        if history_start is None:
            history_start = self.history_min
        else:
            history_start = pd.to_datetime(history_start)

        if history_end is None:
            history_end = self.history_max
        else:
            history_end = pd.to_datetime(history_end)
    
        if not self.check_in_box_l(lats, lons) and check_in_box_bool:
            raise Exception('lat and lon not in the box : lat range [{}, {}], lon range [{}, {}]'.format(self.lat_min, self.lat_max, self.lon_min, self.lon_max))
        
        if not self.check_in_history(history_start, history_end):
            raise Exception('History start and end not in the range of history [{}, {}]'.format(self.history_min, self.history_max))
        
        res = self.file.sel(time=slice(history_start, history_end))
        res = res.sel(latitude=xr.DataArray(lats, dims="z"), 
                            longitude=xr.DataArray(lons, dims="z"),
                            method='nearest')

        if xarray:
            return res

        df_res = res.to_dataframe().reset_index()
        df_res['true_longitude'] = df_res['z'].apply(lambda x: lons[x])
        df_res['true_latitude'] = df_res['z'].apply(lambda x: lats[x])
        df_res.rename(columns={'longitude': 'approx_longitude', 'latitude': 'approx_latitude',
                               'true_longitude': 'longitude', 'true_latitude': 'latitude'}, inplace=True)

        df_res = df_res[['time', 'longitude', 'approx_longitude', 'latitude', 'approx_latitude', self.var_name]]

        return df_res