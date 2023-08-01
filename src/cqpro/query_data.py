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
import xarray as xr
import pandas as pd
import numpy as np

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

    def get_data(self, lats: np.ndarray, lons: np.ndarray, history_start: str = None, history_end: str = None, xarray=False) -> pd.DataFrame:
        """.

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

        Returns
        -------
        DataFrame
            .
        """
        if history_start is None:
            history_start = self.history_min
        else:
            history_start = pd.to_datetime(history_start)

        if history_end is None:
            history_end = self.history_max
        else:
            history_end = pd.to_datetime(history_end)
    
        if not self.check_in_box_l(lats, lons) :
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
        
        # # print(self.file.sel(latitude=45.5, longitude=0.3, method='nearest'))
        # # print(f"{self.file.info()}")
        # # print('-'*50)
        # # df = df.sel(time=slice(history_start, history_end))
        # # print(f"{df.info() =} ")

        # mapped_lat = df['latitude'].to_numpy()
        # mapped_long = df['longitude'].to_numpy()
        # coord = np.column_stack((mapped_lat, mapped_long))

        # unique_coord, unique_id, unique_inverse = np.unique(coord, return_index=True, return_counts=False,
        #                                                 return_inverse=True, axis=0)
        
        # # print(f"{unique_coord = }")
        # # print(f"{unique_id = }")

        # nb_coords = len(lats)
        # nb_timestamps = len(pd.date_range(history_start, history_end, freq='H'))
        # lat_id = np.repeat(unique_id, nb_timestamps)
        # long_id = lat_id.copy()
        # time_id = np.resize(np.arange(nb_timestamps), nb_timestamps * nb_coords)

        # # print(xr.DataArray(lat_id, dims=var_name).values)
        # # print(xr.DataArray(long_id, dims=var_name))
        # # print(xr.DataArray(time_id, dims=var_name))

        # lats_ = xr.DataArray([44.3, 45.2], dims=['location'])
        # lons_ = xr.DataArray([-1.01, 0.3], dims=['location'])
        # print(lats_)

        # df.sel(longitude=lons_, latitude=lats_, method='nearest')
        # print(df)
        # exit()



        # res = df.isel(latitude=xr.DataArray(lat_id, dims=var_name),
        #     longitude=xr.DataArray(long_id, dims=var_name),
        #     time=xr.DataArray(time_id, dims=var_name))
        df.sel_points
        
        # print(lat_id)
        # print(xr.DataArray(lat_id, dims=var_name, coords='latitude'))
        # exit()
        # res = df.isel(latitude=lat_id,
        #     longitude=long_id,
        #     time=time_id)
        
        # print(f"{res = }")
        # # print(res.values())
        # # print(res['t2m'].values)
        # print('-'*50)
        # print(res.to_dataframe())
        # # # print(f"{res.info = }")
        # # print('-'*50)
        # # print(res.to_dataframe())
        # # print('-'*50)
        # # print(res[var_name])

        # if xarray:
        #     return df

        # # df = df.to_dataframe().reset_index()
        # # df['latitude'] = df['latitude'].astype('float32').round(1)
        # # df['longitude'] = df['longitude'].astype('float32').round(1)
        # # print(df)
        # # df = df.set_index(['longitude', 'latitude'])
        # # # df = df.loc[[(round(e[0], 1), round(e[1], 1)) for e in zip(lons, lats)], :]

        # # print(df)
        # # df = df.pivot(columns=['time'])
        # return df
        
    
    def poit_wise_indexing(self, subset_data: xr.Dataset, start_time: str, end_time: str) -> np.ndarray:
        
        unique_id = list(zip(subset_data.longitude.values, subset_data.latitude.values))
        print(unique_id)

        var_name = self._get_var_name()
        # create index arrays
        nb_coords = len(unique_id)
        nb_timestamps = len(pd.date_range(start_time, end_time, freq='H'))
        lat_id = np.repeat(unique_id, nb_timestamps)
        long_id = lat_id.copy()
        print(long_id)
        time_id = np.resize(np.arange(nb_timestamps), nb_timestamps * nb_coords)
        print(time_id)
        # indexing in 3D
        res = subset_data.isel(latitude=xr.DataArray(lat_id, dims=var_name),
                            longitude=xr.DataArray(long_id, dims=var_name),
                            time=xr.DataArray(time_id, dims=var_name))

        # convert to np.array for later calculation
        res_numpy = res[var_name].to_numpy()

        return res_numpy