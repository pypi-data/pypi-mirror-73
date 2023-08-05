# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wetterdienst',
 'wetterdienst.additionals',
 'wetterdienst.constants',
 'wetterdienst.data_models',
 'wetterdienst.download',
 'wetterdienst.enumerations',
 'wetterdienst.exceptions',
 'wetterdienst.file_path_handling',
 'wetterdienst.indexing',
 'wetterdienst.parsing_data']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.4.0,<0.5.0',
 'beautifulsoup4>=4.9.1,<5.0.0',
 'cachetools>=3.1.1,<4.0.0',
 'dateparser>=0.7.4,<0.8.0',
 'docopt>=0.6.2,<0.7.0',
 'fire>=0.3.1,<0.4.0',
 'h5py==2.10.0',
 'munch>=2.5.0,<3.0.0',
 'numpy==1.18.3',
 'pandas==1.0.4',
 'python-dateutil>=2.8.0,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'scipy==1.4.1',
 'tables==3.6.1']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata==1.6.1'],
 'ipython': ['ipython>=7.10.1,<8.0.0',
             'ipython-genutils>=0.2.0,<0.3.0',
             'matplotlib>=3.0.3,<4.0.0']}

entry_points = \
{'console_scripts': ['wetterdienst = wetterdienst.cli:run']}

setup_kwargs = {
    'name': 'wetterdienst',
    'version': '0.1.0',
    'description': 'Python library to ease access to open weather data',
    'long_description': '# Wetterdienst - a Python library to ease access to open weather data\n\n[![Tests](https://github.com/earthobservations/wetterdienst/workflows/Tests/badge.svg)](https://github.com/earthobservations/wetterdienst/actions?workflow=Tests)\n![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)\n![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)\n![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)\n[![codecov](https://codecov.io/gh/earthobservations/wetterdienst/branch/master/graph/badge.svg)](https://codecov.io/gh/earthobservations/wetterdienst)\n[![PyPI](https://img.shields.io/pypi/v/wetterdienst.svg)](https://pypi.org/project/wetterdienst/)\n[![License](https://img.shields.io/github/license/earthobservations/wetterdienst)](https://github.com/earthobservations/wetterdienst/blob/master/LICENSE.md)\n\n## 1. Introduction\n\nThe library **Wetterdienst** was created as an alternative to [rdwd](https://github.com/brry/rdwd),\nan R package that I had used for downloading station data from the German Weather Service \n([Deutscher Wetterdienst](https://www.dwd.de/EN)). Though in the beginning it was a self chosen project to get into \nPython, over time and by the help of others the project evolved step by step to a solid project.\n\nSpeaking about the available data, discussion over the last years regarding the data policy of data collected by country\nofficials have led to a series of open-data initiatives and releases in Europe and Germany as part of it. The German \nWeather Service has in the followup deployed their data via a file server. However this file server is neither handy to\nuse (not even being compared with an API) nor has it a real structure but rather some really big bugs - or better be\ncalled "anomalies". The library streamlines those anomalies to simplify the data gathering process.\n\n**CAUTION**\nAlthough the data is specified as being open, the DWD asks you to reference them as Copyright owner. To check out \nfurther, follow [this](https://www.dwd.de/EN/ourservices/opendata/opendata.html) and \n[this](https://www.dwd.de/EN/service/copyright/copyright_artikel.html?nn=495490&lsbId=627548)\n\n## 2. Types of data\n\nThe library is based upon data available \n[here](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/). The approximate structure is \ncovered in DWD_FILE_SERVER_STRUCTURE.md\n\nThe available parameters are sorted in different time scales:\n\n- per minute / **1_minute**\n- per 10 minutes / **10_minutes**\n- per hour / **hourly**\n- 3 times a day / **subdaily**\n- per day / **daily**\n- per month / **monthly**\n- per year / **annual**\n\nThe available parameters are also sorted in different periods:\n\n- historical values covering all the measured data / **historical**\n- recent values covering data from latest plus a certain range of historical data / **recent**\n- current values covering only latest data / **now**\n\nIt is also possible to use enumeration keywords. This table lists the available enumeration keyword mappings on the CDC server.\n\n|Paramater/Granularity                       |1_minute                             |   10_minutes                    |hourly | subdaily | daily     |monthly | annual| \n|----------------|-------------------------------|-----------------------------|-----------------------------|----------------|-------------|-----------------------------|-----------------------------|\n| `TEMPERATURE_SOIL = "soil_temperature"`  | :x: | :x: | :heavy_check_mark:| :x: | :heavy_check_mark: |:x: | :x:|\n| `TEMPERATURE_AIR = "air_temperature"` |:x: | :heavy_check_mark:| :heavy_check_mark:| :heavy_check_mark:| :x:|:x: |:x: |\n| `PRECIPITATION = "precipitation"`    | :heavy_check_mark: | :heavy_check_mark: |:x: |:x: | :x:| :x:|:x: |\n| `TEMPERATURE_EXTREME = "extreme_temperature"` | :x:|:heavy_check_mark: | :x:|:x: | :x:|:x: |:x: |\n| `WIND_EXTREME = "extreme_wind"  `  |:x: | :heavy_check_mark: | :x:| :x:|:x: |:x: |:x: |\n| `SOLAR = "solar"`  | :x: | :heavy_check_mark: | :heavy_check_mark:|:x: | :heavy_check_mark:| :x:|:x: |\n| `WIND = "wind"  ` |:x: |:heavy_check_mark: | :heavy_check_mark:|:heavy_check_mark:|:x: |:x: |:x: |\n| `CLOUD_TYPE = "cloud_type"`  |:x: | :x: | :heavy_check_mark:|:x: |:x: |:x: |:x: |\n| `CLOUDINESS = "cloudiness"  `    | :x: | :x: |:heavy_check_mark: |:heavy_check_mark: | :x:| :x:| :x:|\n| `SUNSHINE_DURATION = "sun"` |:x: |:x: | :heavy_check_mark:| :x:|:x:|:x:|:x: |\n| `VISBILITY = "visibility"`  | :x:|  :x:|:heavy_check_mark: |:heavy_check_mark: |:x: | :x:| :x:|\n| `WATER_EQUIVALENT = "water_equiv"`  | :x:| :x: |:x: |:x: |:heavy_check_mark: |:x: | :x:|\n| `PRECIPITATION_MORE = "more_precip"  `    | :x: | :x: |:x: |:x: | :heavy_check_mark:|:heavy_check_mark: | :heavy_check_mark:|\n| `PRESSURE = "pressure"` | :x:|:x: | :heavy_check_mark:|:heavy_check_mark:|:x: |:x:|:x: |\n| `CLIMATE_SUMMARY = "kl"`  |:x: | :x: |:x: | :heavy_check_mark:|:heavy_check_mark: |:heavy_check_mark: |:x: |\n| `MOISTURE = "moisture"` |:x: | :x: |:x: | :heavy_check_mark:|:x: |:x: |:x: |\n| `WIND_SYNOP = "wind_synop"` |:x: | :x: | :heavy_check_mark:|:x: |:x: |:x: |:x: |\n| `DEW_POINT = "dew_point"` |:x: | :x: | :heavy_check_mark:|:x: |:x: |:x: |:x: |\n| `WEATHER_PHENOMENA = "weather_phenomena"` |:x: | :x: |:x: |:x: | :heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|\n\n## 3. Functionality of the toolset\n\nThe toolset provides different functions/classes which are:\n\n- metadata_for_dwd_data\n    - discover what data for a set of parameters (parameter, time_resolution, period_type) is available, \n    especially which stations can be found. \n    - with **create_new_file_index**, the function can be forced to retrieve a new list of files from the server, \n    which is usually avoided as it rarely changes.\n- create_file_list_for_dwd_server:\n    - is used with the help of the metadata to retrieve file paths to files for a set of parameters + station id\n    - here also **create_new_file_index** can be used\n- download_dwd_data:\n    - is used with the created file paths to **download and store** the data (second os optionally, in a hdf)\n- parse_dwd_data:\n    - is used to get the data into the Python environment in shape of a pandas DataFrame. \n    - the data will be ready to be analyzed by you!\n- get_nearest_station:\n    - calculates the nearest weather station based on the coordinates for the requested data\n    - it returns a list of station ids that can be used to download the data\n- collect_dwd_data:\n    - combines create_file_list_for_dwd_server, download_dwd_data and parse_dwd_data for multiple stations\n- DWDStationRequest:\n    - a class that can combine multiple periods/date ranges for any number of stations for you\n    \nAdditionally the following functions allow you to reset the cache:\n\n- reset_file_index_cache:\n    - reset the cached file index to get latest list of files (only required for constantly running system)\n- reset_meta_index_cache:\n    - reset the cached meta index to get latest list of files (only required for constantly running system)\n \n### Basic usage:\n\nTo retrieve meta data and get a first insight:\n```\nimport wetterdienst\nfrom wetterdienst.enumerations.period_type_enumeration import PeriodType\nfrom wetterdienst.enumerations.time_resolution_enumeration import TimeResolution\nfrom wetterdienst.enumerations.parameter_enumeration import Parameter\n\nmetadata = wetterdienst.metadata_for_dwd_data(\n    parameter=Parameter.PRECIPITATION_MORE,\n    time_resolution=TimeResolution.DAILY,\n    period_type=PeriodType.HISTORICAL\n)\n```\n\nThe column **HAS_FILE** indicates if the station has a file with data on the server.\n\nTo retrieve observation data:\n``` \nimport wetterdienst\nfrom wetterdienst.enumerations.period_type_enumeration import PeriodType\nfrom wetterdienst.enumerations.time_resolution_enumeration import TimeResolution\nfrom wetterdienst.enumerations.parameter_enumeration import Parameter\n\nstation_data = wetterdienst.collect_dwd_data(\n    station_ids=[1048], \n    parameter=Parameter.CLIMATE_SUMMARY, \n    time_resolution=TimeResolution.DAILY, \n    period_type=PeriodType.HISTORICAL\n)\n```\n\nAlso one may try out DWDStationRequest, a class to define the whole request, which also covers the definition of a \nrequested time range, which may combine different periods of one data for you.\n\nAlso check out the more advanced examples in the **example** folder.\n\n## 4. About the metadata\n\nThe metadata is usually parsed from a txt file. That is not the case for 1-minute historical precipitation, where the\nmetadata is separately stored for each station. To get a comparable metadata sheet, the files for each station have to\nbe parsed and combined. This step takes a bit of time to fulfill, so don\'t expect an instantaneous return here.\n\n## 5. Anomalies\n\nAs already said in the introduction, the file server has lots of special cases. We want to point out here hourly solar\ndata, which has no obvious given period type. Still one can find the thought of period in the file description, which\nis **recent** and was defined as such in the library.\n\n## 7. Conclusion\n\nFeel free to use the library if you want to automate the data access and analyze the german climate. Be aware that this \nlibrary is developed voluntarily and we rely on your feedback regarding bugs, features, etc...\n\n## 8. Getting started\n```\npip install wetterdienst\nwetterdienst --help\n```\n\n## 9. Development\nFor hacking on the library, you might want to follow these steps:\n```\n# Acquire sources\ngit clone https://github.com/earthobservations/wetterdienst\ncd wetterdienst\n\n# Install dependencies\npoetry install\n\n# Run tests\npoetry run pytest\n\n# Invoke comand line tool\npoetry shell\nwetterdienst --help\n```\n\n____\n\n## Docker support\n\nTo use Wetterdienst in a Docker container, you just have to build the image from this project\n```\ndocker build -t "wetterdienst" .\n```\n\nTo run the tests in the given environment, just call \n```\ndocker run -ti -v $(pwd):/app wetterdienst:latest poetry run pytest tests\n```\nfrom the main directory. To work in an iPython shell you just have to change the command `pytest tests/` to `ipython`.\n\n#### Command line script  \nYou can download data as csv files after building docker container.\nCurrently, only the `collect_dwd_data` is supported by this service.\n\n```\ndocker run \\\n    -ti -v $(pwd):/app wetterdienst:latest poetry run python wetterdienst/run.py \\\n    collect_dwd_data "[1048]" "kl" "daily" "historical" /app/dwd_data/ False False True False True True\n```\n\nThe `wetterdienst` command is also available through Docker:\n```\ndocker run -ti -v $(pwd):/app wetterdienst:latest poetry run wetterdienst\n```\n',
    'author': 'Benjamin Gutzmann',
    'author_email': 'gutzemann@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://earthobservations.github.io/wetterdienst/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
