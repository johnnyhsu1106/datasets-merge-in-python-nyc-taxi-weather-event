# Dataset-Merge
This code is to use Python 3.5 to merge three datasets into one dataset 
based on the temporal stamp and spatial stamp<br>
<br>
I use the dataset collected in New York as example.<br>
Basically, you can choose any location you'd like to analyze.<br>

The three dataset are the following.<br>
1.Yellow Taxi Record Dataset:<br> 
&nbsp; source: http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml <br>
&nbsp; template: yellow_tripdata_template1.csv <br>
&nbsp; template: yellow_tripdata_template2.csv<br>
<br>
2.Weather Hourly Dataset:
&nbsp; source: https://www.ncdc.noaa.gov/cdo-web/datasets <br>
&nbsp; template: weather_template.csv <br>
<br>
3.Event Dataset
&nbsp; source: eventful API http://api.eventful.com/ <br>
&nbsp; template: event_template.csv <br>
&nbsp; I also make a python file to download events from event api, output is csv file.<br>

Tempral stamp: Taxi pick up time, weather measurement time, and event time<br>
Spatial stamp: Taxi drop off location and event location <br>
basically, the weather location is only only location.<br>
However, it could be multi-locations but the source code will need to be modified.<br>
In the source code, the variable determining the which event belongs to which taxi ride is called " min_distance".<br>
The default value is 0.5 miles. You can adjust it based on your criteria.<br>

Before run the data_preprocess.py, please save all datasets under the same directory, including the data_preprocess.py<br>

In command prompt, run the following command propmt in MacOS<br>
&nbsp; $ python data_preprocess.py filename <br>
or in Windows<br>
&nbsp; &gt; python data_preprocess.py filename <br>

filename: this is the filename you'd like to name the output file, e.g. data_template.csv <br>
You can check the output format in the data_template.csv

