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
from src.cqpro.download_data import Downloader
from src.cqpro.query_data import retriever
import os

def test_download():

    DATASET='reanalysis-era5-single-levels'
    VARS = ['2m_temperature']
    YEARS = [2020]
    HOURS = ['23:00'] # ['%02d:00' % (e,) for e in range(24)] # All hours
    DAYS = ['01', '02'] # ['%02d' % (e,) for e in range(1, 32)] # All days
    MONTHS = ['09'] # ['%02d' % (e,) for e in range(1, 13)] # All months
    RESOL = 0.1
    OUTPUT_PATH = '../data/' # choose an existing path 

    d = Downloader(variables=VARS, years=YEARS, months=MONTHS, days=DAYS, hours=HOURS, output_path=OUTPUT_PATH,
                    dataset=DATASET, resolution=RESOL, country='France')
    # Simple thread
    d.download()
    # Multi thread here 2 threads
    # d.download(num_proc = 2)
    assert '2m_temperature_2020_09_to_2020_09.nc' in os.listdir(OUTPUT_PATH)


def test_query():
    PATH = '../data/'
    file_name = "2m_temperature_2020_09_to_2020_09.nc"

    r = retriever(path=PATH, file_name=file_name)
    df = r.get_data([48.641, 48.642, 46.24, 44.25645], [-2, -2.03, -1, 0.2135],  
                    '2020-09-01 23:00:00', '2020-09-02 23:00:00')
    
    assert df.shape != (0, 0)