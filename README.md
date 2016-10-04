# Dataset-aggregation
This code is to use Python 3.5 to merge three datasets into one dataset 
based on the temporal stamp and spatial stamp<br>
<br>


The three dataset are the following.<br>
1.Yellow Taxi Record Dataset:<br> 
source: http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml <br>
template: yellow_tripdata_template1.csv <br>
template: yellow_tripdata_template2.csv<br>
<br>
2.Weather Hourly Dataset:
source: https://www.ncdc.noaa.gov/cdo-web/datasets <br>
template: weather_template.csv <br>
<br>
3.Event Dataset
source: eventful API http://api.eventful.com/ <br>
template: event_template.csv <br>
I also make a python file to download events from event api, output is csv file.<br>

Tempral stamp: Taxi pick up time, weather measurement time, and event time<br>
Spatial stamp: Taxi drop off location and event location <br>
basically, the weather location is only only location in one city.<br>

Before run the data_preprocess.py, please save all datasets under the same directory, including the p
data_preprocess.py<br>
In command prompt, run the following command propmt<br>
$ python data_preprocess.py  filename <br>

filename: this is the filename you'd like to name the output file, e.g. data_template.csv <br>

You can check the output format in the data_template.csv

