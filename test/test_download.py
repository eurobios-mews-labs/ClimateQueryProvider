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
from cqpro.download_data import downloader

DATASET='reanalysis-era5-single-levels'
VARS = ['2m_temperature']
YEARS = [2020]
HOURS = ['23:00'] # ['%02d:00' % (e,) for e in range(24)] # All hours
DAYS = ['01', '02'] # ['%02d' % (e,) for e in range(1, 32)] # All days
MONTHS = ['09'] # ['%02d' % (e,) for e in range(1, 13)] # All months
RESOL = 0.1
OUTPUT_PATH = 'data/' # choose an existing path 

d = downloader(variables=VARS, years=YEARS, months=MONTHS, days=DAYS, hours=HOURS, output_path=OUTPUT_PATH,
                dataset=DATASET, resolution=RESOL, country='France')
d.download()