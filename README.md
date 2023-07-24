# Climate query provider

_**ClimateQueryProvider**_ is a python package proposed to download ECMWF data and to query downloaded data into dataframes

## Initial configuration :

1. Create an account on https://cds.climate.copernicus.eu
2. Go to https://cds.climate.copernicus.eu/api-how-to copy the url and key as given in the file $HOME/.cdsapirc  

## Package installation notice

To install the package using pip, execute the following command :

``` shell script
python -m pip install git+https://github.com/eurobios-scb/ClimateQueryProvider.git
```

Or by downloading the package and executing in the repo :

```shell script
python -m pip install .
```


## Basic usage

There are 2 main steps to get started with the package :

1. Download any meteo data available in ECMWF as hdf5 files https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview

2. Query downloaded data

## 1 - To download meteo data from ECMWF

Download of files should is done 1 variable at a time (1 file per variables)
exception for wind : key word wind is associated to 2 variables u10 and v10 which are eastward and northward component of the 10m wind

You can find the list of available variables here : https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation

Example of script to download wind and temperature data for year 2020 in France:

``` python
from cqpro.download_data import downloader

DATASET='reanalysis-era5-single-levels'
VARS = ['2m_temperature']
YEARS = [2020]
HOURS = ['%02d:00' % (e,) for e in range(24)] # All hours
DAYS = ['%02d' % (e,) for e in range(1, 32)] # All days
MONTHS = ['%02d' % (e,) for e in range(1, 13)] # All months
RESOL = 0.1
OUTPUT_PATH = 'data/' # choose an existing path 

d = downloader(variables=VARS, years=YEARS, months=MONTHS, days=DAYS, hours=HOURS, output_path=OUTPUT_PATH,
                dataset=DATASET, resolution=RESOL, country='France')
d.download()
```

Bounding boxes of countries are available in the package :
``` python
from cqpro.utils import get_bbox

bounding_boxes = get_bbox()
print(bounding_boxes)
``` 


## 2- To query downloaded data

``` python
from cqpro.query_data import retriever

path = '/' # Path for downloaded data
file_name = "2m_temperature.nc" # file name

r = retriever(path=path, file_name=file_name)

# history_start should always be before history_end and both fo them should be in the range of the file history

df = r.get_data(lat=45, lon=-3, history_start='2020-03-02', history_end='2020-03-03 03:03:00')

print(r._get_history_range())
print(r._get_grid_range())
print(r._get_var_name())

print(df)
```
