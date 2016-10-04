'''
Author: <Johnny Hsu, aka. Yu Wei, Hsu>
Date: <09/29/2016>
Version: 0.1
Description: Taxi, Weather, Event dataset aggregation and clean
'''
from os import listdir
import datetime
import csv
from geopy.distance import vincenty
import argparse
# command prompt
# > python data_preprocess.py <filename.csv>
parser = argparse.ArgumentParser(usage='data_preprocess.py fname ')
parser.add_argument("fname", type = str, help = "assign output filename")
args = parser.parse_args()


def merge_file(key_word, data):
	files = [file for file in listdir() if not file.find(key_word)]
	for file in files:
		read_file(file, data)


def read_file(fname, data): 
	with open(fname) as fp:
		file = csv.reader(fp)
		header = next(file, None)
		
		# The attribute of header is the key of dictionary
		if not data:
			for attribute in header:
				data[attribute] = []

		# read every line in the file, except the header, and store it as dictionary
		# format: {f1: [d11,d21, ...],f2: [d21,d22], } like json
		for line in file:
			i = 0
			for attribute in header:
				data[attribute].append(line[i])
				i+=1



def merge_data(taxi_data, weather_data, event_data):



	# The threshold of distance of event location and taxi drop off location
	min_distance = 0.5 # unit: mile

	# Create key refers to weather features and list to contain weather weather data
	for weather_feature in weather_data.keys():
		if weather_feature not in taxi_data:
			taxi_data[weather_feature] = []

	for event_feature in event_data.keys():
		if event_feature not in taxi_data:
			taxi_data[event_feature] = [[]]


	for taxi_index in range(len(taxi_data["tpep_pickup_datetime"])):
	
		# taxi_data["tpep_pickup_datetime"][i], format: "yyyy-mm-dd hh:mm", i = 0, 1, 2, ..., n
		# weather_data["DATE"][i], format: "yyyy-mm-dd hh:mm", i = 0, 1, 2, ..., n
		# event_data["start_time"][i], format: "yyyy-mm-dd hh:mm", i = 0, 1, 2, ..., n
		# date, format: [yyyy-mm-dd , hh:mm]
		# date[0].split("-") , format: [mm, dd, yyyy]
		# date[1].split(":") , format: [hh, mm]
		# taxi_data["dropoff_latitude"][i], format: 41.4343, i = 0, 1, 2, ..., n

		date = taxi_data["tpep_pickup_datetime"][taxi_index].split()
		time = date[0].split("-") +  date[1].split(":")
		time = [int(value) for value in time]

		taxi_time = datetime.datetime(time[0], time[1], time[2], time[3], time[4])
		taxi_location = (taxi_data["dropoff_latitude"][taxi_index],taxi_data["dropoff_longitude"][taxi_index])
		

		#  merge the weather dataset into Taxi dataset based on one condition
			# if taxi pick up time is between weather measure time 1 and weather measure time 2
			# ,then weather measure 1 belongs the this taix ride.

		for index in range(len(weather_data["DATE"])):

			date = weather_data["DATE"][index].split()
			time = date[0].split("-") +  date[1].split(":")
			time = [int(value) for value in time]
			weather_time_2 = datetime.datetime(time[0], time[1], time[2], time[3], time[4])

			if index == 0:
				weather_time_1 = datetime.datetime(time[0], time[1], time[2], 0 , 0)
		
			elif time[4] != 59: 
				if time[3] == 0:
					date = weather_data["DATE"][index - 2].split()
				else:
					date = weather_data["DATE"][index - 1].split()
							
				time = date[0].split("-") +  date[1].split(":")
				time = [int(value) for value in time]
				weather_time_1 = datetime.datetime(time[0], time[1], time[2], time[3], time[4])

			if taxi_time >= weather_time_1 and taxi_time < weather_time_2:
				for weather_feature in weather_data.keys():
		
					if weather_data[weather_feature][index] != "": 
						taxi_data[weather_feature].append(weather_data[weather_feature][index])
					else:
						taxi_data[weather_feature].append('None')


		# merge the event dataset into Taxi dataset based on two conditions
			# if dictance of event location and taxi drop off location are under threshold
			# if taxi pick up time is between event start time and end time
			# then, the event belongs to this taxi ride.

		for event_index in range(len(event_data["start_time"])):
		
			start_date = event_data["start_time"][event_index]
			end_date = event_data["stop_time"][event_index]

			if start_date != "None":
				start_date= start_date.split()
				start_time = start_date[0].split("-") +  start_date[1].split(":")
				start_time = [int(value) for value in start_time]
				event_time_1 = datetime.datetime(start_time[0], start_time[1], start_time[2], start_time[3], start_time[4])
			else:
				event_time_1 = datetime.datetime.now()

			if end_date != "None":	
				end_date = end_date.split()
				end_time = end_date[0].split("-") +  end_date[1].split(":")
				end_time = [int(value) for value in end_time]
				event_time_2 = datetime.datetime(end_time[0], end_time[1], end_time[2],end_time[3], end_time[4])
			else:
				event_time_2 = datetime.datetime.now()

			event_location = (event_data["latitude"][event_index], event_data["longitude"][event_index])
			distance = vincenty(taxi_location, event_location).miles

			if distance <= min_distance and taxi_time >= event_time_1 and taxi_time <= event_time_2:
				for event_feature in event_data.keys():
					taxi_data[event_feature][taxi_index].append(event_data[event_feature][event_index])
			
		for event_feature in event_data.keys():
			if len(taxi_data[event_feature][taxi_index])== 0:
				taxi_data[event_feature][taxi_index].append("None") 

		
		for event_feature in event_data.keys():
			taxi_data[event_feature].append([])				



def write_file(fname, data):

	with open(fname, "w") as fp:
		lst = []
		for feature in sorted(data.keys(), reverse = True):
			lst.append(feature)
		table_header = ",".join(lst) + "\n"
		fp.write(table_header)	

		for i in range(len(data["VendorID"])):
			lst = []
			for feature in sorted(data.keys(),reverse = True):
				value = data[feature][i]
				if type(value)==str:
					lst.append(value)
				elif type(value) == list:
					lst.append(" | ".join(value))
			fp.write(",".join(lst) + "\n")	



def main():

	event_key_word = "event"
	weather_key_word = "weather"
	taxi_key_word = "yellow_tripdata"
	fname = args.fname 
	event_data = {}
	weather_data = {}

	merge_file(event_key_word, event_data)
	merge_file(weather_key_word, weather_data)
	

	# The reason why not to merge all taxi data into one file is the number of taxi data point is huge
	# The number of all taxi data point exceeds the limitation of list's index

	taxi_files = [file for file in listdir() if not file.find(taxi_key_word)]
	taxi_data = [ {} for i in range(len(taxi_files)) ]
	
	# aggegtae each taxi data file with other data separately

	for i in range(len(taxi_files)):
		read_file(taxi_files[i], taxi_data[i])
		merge_data(taxi_data[i], weather_data, event_data)
	
	# combine each separate final datasets
	output_data = taxi_data[0] 
	for i in range(1,len(taxi_data)):
		for feature in output_data:
			output_data[feature].extend(taxi_data[i][feature])
	


	write_file(fname, output_data)




if __name__ == '__main__':
	main()