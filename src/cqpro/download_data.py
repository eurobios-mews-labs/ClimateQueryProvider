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
import os
import sys
import cdsapi
import multiprocessing.dummy as mp

sys.path.append(os.path.dirname(__file__))

from utils import get_bbox

class Downloader:
    """ Main class to download meteo data via the cds api
    """

    def __init__(self, variables, years, months, days, hours, output_path,
                 LAT_MIN=None, LAT_MAX=None, LON_MIN=None, LON_MAX=None, country='France',
                 dataset='reanalysis-era5-single-levels', resolution=0.1, **kwargs):

        if country is None:
            if LAT_MIN is None or LAT_MAX is None or LON_MIN is None or LON_MAX is None:
                raise Exception("Please provide a box or a country")
            self.LAT_MAX = LAT_MAX
            self.LAT_MIN = LAT_MIN
            self.LON_MAX = LON_MAX
            self.LON_MIN = LON_MIN
        else:
            print(country)
            bbox = get_bbox()
            self.LAT_MAX, self.LAT_MIN, self.LON_MIN, self.LON_MAX = \
                bbox[bbox['country_name'] == country] \
                [['LAT_MAX', 'LAT_MIN', 'LON_MIN', 'LON_MAX']].values[0]

        self.c = cdsapi.Client()
        self.dataset = dataset
        self.variables = variables
        self.years = years
        self.months = months
        self.days = days
        self.time = hours
        self.grid = [resolution, resolution]
        self.output_path = output_path
        self.kwargs = kwargs

    def download_var(self, var: str) -> None:
        """Main function to download 1 variable
        
        Parameters
        ----------
        var : str
            Name of variable : list of available variables here : 
            https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation

        Returns
        -------
        None
        """

        print('downloading historic for ' + var)

        name = f"{var}_{self.years[0]}_{self.months[0]}_to_{self.years[-1]}_{self.months[-1]}"
        if var == 'wind':
            var = ['10m_u_component_of_wind', '10m_v_component_of_wind']

        dico_args = {'product_type': 'reanalysis',
                        'format': 'netcdf',
                        'variable': var,
                        'year': self.years,
                        'month': self.months,
                        'day': self.days,
                        'grid': self.grid,
                        'area': [self.LAT_MAX, self.LON_MIN, self.LAT_MIN, self.LON_MAX],
                        'time': self.time}
        dico_args.update(self.kwargs)

        self.c.retrieve(self.dataset, dico_args, self.output_path + name + '.nc')
    
    def download(self, num_proc: int = 1):
        """Main function to download all variables in parallel

        Although the server does not process queries in parallel, a query can be run while others are downloading
        
        Parameters
        ----------
        num_proc : int
            Number of proc to be used

        Returns
        -------
        None
        """

        if num_proc < 2:
            for var in self.variables:
                self.download_var(var)
        else:
            pool = mp.Pool(processes=num_proc)
            pool.map(self.download_var, self.variables)
            pool.close()
            pool.join()
