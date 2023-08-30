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

PATH_ERA5 = 'data/test/'
LON_MIN = -5
LON_MAX = 9
LAT_MIN = 42
LAT_MAX = 51.5
HOURS = ['%02d:00' % (e,) for e in range(24)]
DAYS = ['%02d' % (e,) for e in range(1, 32)]
MONTHS = ['%02d' % (e,) for e in range(1, 13)]
YEARS = range(1979, 2019)
RESOLUTION = 0.1
NB_LATS = 96
NB_LONS = 141

LATS = np.array([round(e, 1) for e in np.linspace(LAT_MIN, LAT_MAX, NB_LATS)])
LONS = np.array([round(e, 1) for e in np.linspace(LON_MIN, LON_MAX, NB_LONS)])
