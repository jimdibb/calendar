#!/usr/bin/env python

import requests
import json
import re
from datetime import datetime,time,date
from yattag import Doc
import sys
import time as timetime # this is funny so as not to conflict with datetime.time imported above

iconreg = re.compile('([\d]+)[nd]')

def adjustIcon(icon, dateT):
	
	b = iconreg.search(icon)
	basename= b.group(1)
	hour = dateT.hour
	if (debug):
		print(icon)
		print(basename)
		print(hour)
	if (hour < 7 or hour > 19):
		day_night='n'
	else:
		day_night='d'
	return (basename+day_night+'.png')

#return yyyy-mm-dd delta days in the future	
def days_future(today, day_delta):
	newdate = date.fromordinal(today.toordinal() + day_delta)
	day = newdate.strftime('%A')
	tdata = timetime.localtime()
	if (tdata.tm_isdst>0):
		noonhour = 11 # in dst this is the closest match to noon
	else:
		noonhour = 13 # in non-dst this is the closest match
	if (debug):
		print noonhour
	noontime = datetime.combine(newdate, time(noonhour))
	if (debug):
		print (newdate)
		print (noontime)
	return (newdate,day,noontime)
	
def process_high_low(wdata, today):
	highlow={}
	for i in wdata['list']: # i is each indivdual 3 hour weather report
		d = date.fromtimestamp(i['dt'])
		
		t=i['main']['temp'] # the temp at that time
		
		if (d in highlow.keys()): # if we've already seen this one, compare high and low
			if (t < highlow[d]['low']):
				highlow[d]['low']=t
			if (t > highlow[d]['high']):
				highlow[d]['high']=t
		else:
			highlow[d]={'low':t, 'high':t} # haven't seen this one, set high/low to whatever this is
	if (debug):
		print (highlow)
	return(highlow)
	
debug=0 #use the api to grab the data.  Use the practice data below if set to true.
			# the debug date matches the data

if (debug):
	#practice data
	resp={u'city': {u'country': u'US', u'id': 4937230, u'coord': {u'lat': 42.2793, u'lon': -71.4162}, u'name': u'Framingham'}, u'message': 0.007, u'list': [{u'clouds': {u'all': 92}, u'rain': {u'3h': 0.325}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-27 03:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490583600, u'main': {u'temp_kf': -0.14, u'temp': 34.47, u'grnd_level': 1034.55, u'temp_max': 34.71, u'sea_level': 1044.12, u'humidity': 85, u'pressure': 1034.55, u'temp_min': 34.47}, u'wind': {u'speed': 4.65, u'deg': 129.001}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.275}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-27 06:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490594400, u'main': {u'temp_kf': -0.1, u'temp': 33.73, u'grnd_level': 1031.95, u'temp_max': 33.92, u'sea_level': 1041.63, u'humidity': 97, u'pressure': 1031.95, u'temp_min': 33.73}, u'wind': {u'speed': 4.5, u'deg': 118.502}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.71}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-27 09:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490605200, u'main': {u'temp_kf': -0.07, u'temp': 35.24, u'grnd_level': 1029.13, u'temp_max': 35.36, u'sea_level': 1038.73, u'humidity': 100, u'pressure': 1029.13, u'temp_min': 35.24}, u'wind': {u'speed': 4.76, u'deg': 112.508}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.615}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-27 12:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1490616000, u'main': {u'temp_kf': -0.03, u'temp': 38.84, u'grnd_level': 1026.92, u'temp_max': 38.9, u'sea_level': 1036.34, u'humidity': 100, u'pressure': 1026.92, u'temp_min': 38.84}, u'wind': {u'speed': 5.19, u'deg': 127.502}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.53}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-27 15:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1490626800, u'main': {u'temp_kf': 0, u'temp': 46.08, u'grnd_level': 1024.68, u'temp_max': 46.08, u'sea_level': 1034.1, u'humidity': 97, u'pressure': 1024.68, u'temp_min': 46.08}, u'wind': {u'speed': 5.19, u'deg': 147.502}}, {u'clouds': {u'all': 100}, u'rain': {u'3h': 1.12}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-27 18:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1490637600, u'main': {u'temp_kf': 0, u'temp': 50.99, u'grnd_level': 1021.21, u'temp_max': 50.99, u'sea_level': 1030.48, u'humidity': 98, u'pressure': 1021.21, u'temp_min': 50.99}, u'wind': {u'speed': 4.05, u'deg': 154.005}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 3.87}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-27 21:00:00', u'weather': [{u'main': u'Rain', u'id': 501, u'icon': u'10d', u'description': u'moderate rain'}], u'dt': 1490648400, u'main': {u'temp_kf': 0, u'temp': 52.46, u'grnd_level': 1018.81, u'temp_max': 52.46, u'sea_level': 1028.18, u'humidity': 99, u'pressure': 1018.81, u'temp_min': 52.46}, u'wind': {u'speed': 4.43, u'deg': 187.005}}, {u'clouds': {u'all': 100}, u'rain': {u'3h': 1.43}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-28 00:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490659200, u'main': {u'temp_kf': 0, u'temp': 49.16, u'grnd_level': 1019.09, u'temp_max': 49.16, u'sea_level': 1028.45, u'humidity': 99, u'pressure': 1019.09, u'temp_min': 49.16}, u'wind': {u'speed': 1.74, u'deg': 309.501}}, {u'clouds': {u'all': 48}, u'rain': {u'3h': 0.29}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-28 03:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490670000, u'main': {u'temp_kf': 0, u'temp': 44.11, u'grnd_level': 1020.02, u'temp_max': 44.11, u'sea_level': 1029.34, u'humidity': 100, u'pressure': 1020.02, u'temp_min': 44.11}, u'wind': {u'speed': 3.85, u'deg': 10.5043}}, {u'clouds': {u'all': 64}, u'rain': {u'3h': 0.030000000000001}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-28 06:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490680800, u'main': {u'temp_kf': 0, u'temp': 40.53, u'grnd_level': 1020.43, u'temp_max': 40.53, u'sea_level': 1029.89, u'humidity': 100, u'pressure': 1020.43, u'temp_min': 40.53}, u'wind': {u'speed': 3.87, u'deg': 5.00006}}, {u'clouds': {u'all': 88}, u'rain': {u'3h': 0.029999999999999}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-28 09:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490691600, u'main': {u'temp_kf': 0, u'temp': 38.53, u'grnd_level': 1020.56, u'temp_max': 38.53, u'sea_level': 1029.99, u'humidity': 100, u'pressure': 1020.56, u'temp_min': 38.53}, u'wind': {u'speed': 2.95, u'deg': 19.5046}}, {u'clouds': {u'all': 88}, u'rain': {u'3h': 0.06}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-28 12:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1490702400, u'main': {u'temp_kf': 0, u'temp': 38.3, u'grnd_level': 1021.76, u'temp_max': 38.3, u'sea_level': 1031.1, u'humidity': 100, u'pressure': 1021.76, u'temp_min': 38.3}, u'wind': {u'speed': 3.38, u'deg': 33.002}}, {u'clouds': {u'all': 80}, u'rain': {u'3h': 0.039999999999999}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-28 15:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1490713200, u'main': {u'temp_kf': 0, u'temp': 43.69, u'grnd_level': 1022.09, u'temp_max': 43.69, u'sea_level': 1031.43, u'humidity': 89, u'pressure': 1022.09, u'temp_min': 43.69}, u'wind': {u'speed': 3.38, u'deg': 38.5005}}, {u'clouds': {u'all': 80}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-28 18:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04d', u'description': u'broken clouds'}], u'dt': 1490724000, u'main': {u'temp_kf': 0, u'temp': 50.38, u'grnd_level': 1021.18, u'temp_max': 50.38, u'sea_level': 1030.51, u'humidity': 81, u'pressure': 1021.18, u'temp_min': 50.38}, u'wind': {u'speed': 3.31, u'deg': 68.0001}}, {u'clouds': {u'all': 80}, u'rain': {u'3h': 0.0099999999999998}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-28 21:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1490734800, u'main': {u'temp_kf': 0, u'temp': 52.65, u'grnd_level': 1020.06, u'temp_max': 52.65, u'sea_level': 1029.44, u'humidity': 80, u'pressure': 1020.06, u'temp_min': 52.65}, u'wind': {u'speed': 3.15, u'deg': 104.504}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 0.19}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-29 00:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490745600, u'main': {u'temp_kf': 0, u'temp': 48.28, u'grnd_level': 1020.7, u'temp_max': 48.28, u'sea_level': 1030.07, u'humidity': 89, u'pressure': 1020.7, u'temp_min': 48.28}, u'wind': {u'speed': 3.29, u'deg': 99.5006}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 1.36}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-29 03:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490756400, u'main': {u'temp_kf': 0, u'temp': 43.45, u'grnd_level': 1021.17, u'temp_max': 43.45, u'sea_level': 1030.58, u'humidity': 97, u'pressure': 1021.17, u'temp_min': 43.45}, u'wind': {u'speed': 3.4, u'deg': 80.5021}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 1.23}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-29 06:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490767200, u'main': {u'temp_kf': 0, u'temp': 41.19, u'grnd_level': 1021.06, u'temp_max': 41.19, u'sea_level': 1030.47, u'humidity': 100, u'pressure': 1021.06, u'temp_min': 41.19}, u'wind': {u'speed': 3.11, u'deg': 56.0024}}, {u'clouds': {u'all': 100}, u'rain': {u'3h': 1.17}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-29 09:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490778000, u'main': {u'temp_kf': 0, u'temp': 40.31, u'grnd_level': 1020.24, u'temp_max': 40.31, u'sea_level': 1029.64, u'humidity': 100, u'pressure': 1020.24, u'temp_min': 40.31}, u'wind': {u'speed': 3.31, u'deg': 45.5}}, {u'clouds': {u'all': 92}, u'rain': {u'3h': 1.54}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-29 12:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1490788800, u'main': {u'temp_kf': 0, u'temp': 40.18, u'grnd_level': 1021.04, u'temp_max': 40.18, u'sea_level': 1030.5, u'humidity': 100, u'pressure': 1021.04, u'temp_min': 40.18}, u'wind': {u'speed': 4.36, u'deg': 31.0005}}, {u'clouds': {u'all': 88}, u'rain': {u'3h': 0.75}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-29 15:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1490799600, u'main': {u'temp_kf': 0, u'temp': 42.45, u'grnd_level': 1021.91, u'temp_max': 42.45, u'sea_level': 1031.3, u'humidity': 99, u'pressure': 1021.91, u'temp_min': 42.45}, u'wind': {u'speed': 4.72, u'deg': 35.0009}}, {u'clouds': {u'all': 80}, u'rain': {u'3h': 0.54}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-29 18:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1490810400, u'main': {u'temp_kf': 0, u'temp': 43.81, u'grnd_level': 1022.2, u'temp_max': 43.81, u'sea_level': 1031.59, u'humidity': 99, u'pressure': 1022.2, u'temp_min': 43.81}, u'wind': {u'speed': 5.39, u'deg': 29.5002}}, {u'clouds': {u'all': 80}, u'rain': {u'3h': 0.02}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-29 21:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1490821200, u'main': {u'temp_kf': 0, u'temp': 45.62, u'grnd_level': 1022.09, u'temp_max': 45.62, u'sea_level': 1031.45, u'humidity': 81, u'pressure': 1022.09, u'temp_min': 45.62}, u'wind': {u'speed': 4.29, u'deg': 29.5157}}, {u'clouds': {u'all': 0}, u'rain': {u'3h': 0.010000000000002}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-30 00:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490832000, u'main': {u'temp_kf': 0, u'temp': 40.67, u'grnd_level': 1022.9, u'temp_max': 40.67, u'sea_level': 1032.3, u'humidity': 91, u'pressure': 1022.9, u'temp_min': 40.67}, u'wind': {u'speed': 2.91, u'deg': 61.0009}}, {u'clouds': {u'all': 0}, u'rain': {u'3h': 0.039999999999999}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-30 03:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10n', u'description': u'light rain'}], u'dt': 1490842800, u'main': {u'temp_kf': 0, u'temp': 34.64, u'grnd_level': 1024.11, u'temp_max': 34.64, u'sea_level': 1033.69, u'humidity': 96, u'pressure': 1024.11, u'temp_min': 34.64}, u'wind': {u'speed': 2.28, u'deg': 23.0031}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-30 06:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01n', u'description': u'clear sky'}], u'dt': 1490853600, u'main': {u'temp_kf': 0, u'temp': 33.84, u'grnd_level': 1024.85, u'temp_max': 33.84, u'sea_level': 1034.31, u'humidity': 82, u'pressure': 1024.85, u'temp_min': 33.84}, u'wind': {u'speed': 6.76, u'deg': 337.502}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-30 09:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01n', u'description': u'clear sky'}], u'dt': 1490864400, u'main': {u'temp_kf': 0, u'temp': 33.5, u'grnd_level': 1025.75, u'temp_max': 33.5, u'sea_level': 1035.38, u'humidity': 86, u'pressure': 1025.75, u'temp_min': 33.5}, u'wind': {u'speed': 7.18, u'deg': 340.01}}, {u'clouds': {u'all': 0}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-30 12:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01d', u'description': u'clear sky'}], u'dt': 1490875200, u'main': {u'temp_kf': 0, u'temp': 34.39, u'grnd_level': 1028.12, u'temp_max': 34.39, u'sea_level': 1037.82, u'humidity': 76, u'pressure': 1028.12, u'temp_min': 34.39}, u'wind': {u'speed': 8.79, u'deg': 350.5}}, {u'clouds': {u'all': 76}, u'rain': {u'3h': 0.07}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-30 15:00:00', u'weather': [{u'main': u'Rain', u'id': 500, u'icon': u'10d', u'description': u'light rain'}], u'dt': 1490886000, u'main': {u'temp_kf': 0, u'temp': 40.16, u'grnd_level': 1030.41, u'temp_max': 40.16, u'sea_level': 1039.87, u'humidity': 74, u'pressure': 1030.41, u'temp_min': 40.16}, u'wind': {u'speed': 8.57, u'deg': 26.5028}}, {u'clouds': {u'all': 20}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-30 18:00:00', u'weather': [{u'main': u'Clouds', u'id': 801, u'icon': u'02d', u'description': u'few clouds'}], u'dt': 1490896800, u'main': {u'temp_kf': 0, u'temp': 45.57, u'grnd_level': 1030.75, u'temp_max': 45.57, u'sea_level': 1040.12, u'humidity': 60, u'pressure': 1030.75, u'temp_min': 45.57}, u'wind': {u'speed': 5.14, u'deg': 9.00189}}, {u'clouds': {u'all': 32}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-30 21:00:00', u'weather': [{u'main': u'Clouds', u'id': 802, u'icon': u'03d', u'description': u'scattered clouds'}], u'dt': 1490907600, u'main': {u'temp_kf': 0, u'temp': 47.4, u'grnd_level': 1030.43, u'temp_max': 47.4, u'sea_level': 1039.91, u'humidity': 50, u'pressure': 1030.43, u'temp_min': 47.4}, u'wind': {u'speed': 4.79, u'deg': 7.50528}}, {u'clouds': {u'all': 56}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-31 00:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04n', u'description': u'broken clouds'}], u'dt': 1490918400, u'main': {u'temp_kf': 0, u'temp': 41, u'grnd_level': 1032.38, u'temp_max': 41, u'sea_level': 1042.03, u'humidity': 57, u'pressure': 1032.38, u'temp_min': 41}, u'wind': {u'speed': 4.21, u'deg': 55.0042}}, {u'clouds': {u'all': 8}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-31 03:00:00', u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'02n', u'description': u'clear sky'}], u'dt': 1490929200, u'main': {u'temp_kf': 0, u'temp': 35.4, u'grnd_level': 1034.2, u'temp_max': 35.4, u'sea_level': 1043.82, u'humidity': 66, u'pressure': 1034.2, u'temp_min': 35.4}, u'wind': {u'speed': 4.25, u'deg': 91.0016}}, {u'clouds': {u'all': 12}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-31 06:00:00', u'weather': [{u'main': u'Clouds', u'id': 801, u'icon': u'02n', u'description': u'few clouds'}], u'dt': 1490940000, u'main': {u'temp_kf': 0, u'temp': 29.81, u'grnd_level': 1034.98, u'temp_max': 29.81, u'sea_level': 1044.72, u'humidity': 83, u'pressure': 1034.98, u'temp_min': 29.81}, u'wind': {u'speed': 3.33, u'deg': 57.0007}}, {u'clouds': {u'all': 56}, u'rain': {}, u'sys': {u'pod': u'n'}, u'dt_txt': u'2017-03-31 09:00:00', u'weather': [{u'main': u'Clouds', u'id': 803, u'icon': u'04n', u'description': u'broken clouds'}], u'dt': 1490950800, u'main': {u'temp_kf': 0, u'temp': 28.08, u'grnd_level': 1036.36, u'temp_max': 28.08, u'sea_level': 1046.16, u'humidity': 83, u'pressure': 1036.36, u'temp_min': 28.08}, u'wind': {u'speed': 2.37, u'deg': 10.5016}}, {u'clouds': {u'all': 88}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-31 12:00:00', u'weather': [{u'main': u'Clouds', u'id': 804, u'icon': u'04d', u'description': u'overcast clouds'}], u'dt': 1490961600, u'main': {u'temp_kf': 0, u'temp': 33.73, u'grnd_level': 1037.39, u'temp_max': 33.73, u'sea_level': 1047.1, u'humidity': 81, u'pressure': 1037.39, u'temp_min': 33.73}, u'wind': {u'speed': 3.62, u'deg': 27.5001}}, {u'clouds': {u'all': 48}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-31 15:00:00', u'weather': [{u'main': u'Clouds', u'id': 802, u'icon': u'03d', u'description': u'scattered clouds'}], u'dt': 1490972400, u'main': {u'temp_kf': 0, u'temp': 43.68, u'grnd_level': 1037.51, u'temp_max': 43.68, u'sea_level': 1047.07, u'humidity': 63, u'pressure': 1037.51, u'temp_min': 43.68}, u'wind': {u'speed': 3.4, u'deg': 79.0051}}, {u'clouds': {u'all': 48}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-31 18:00:00', u'weather': [{u'main': u'Clouds', u'id': 802, u'icon': u'03d', u'description': u'scattered clouds'}], u'dt': 1490983200, u'main': {u'temp_kf': 0, u'temp': 47.3, u'grnd_level': 1036.03, u'temp_max': 47.3, u'sea_level': 1045.71, u'humidity': 51, u'pressure': 1036.03, u'temp_min': 47.3}, u'wind': {u'speed': 3.36, u'deg': 106.5}}, {u'clouds': {u'all': 32}, u'rain': {}, u'sys': {u'pod': u'd'}, u'dt_txt': u'2017-03-31 21:00:00', u'weather': [{u'main': u'Clouds', u'id': 802, u'icon': u'03d', u'description': u'scattered clouds'}], u'dt': 1490994000, u'main': {u'temp_kf': 0, u'temp': 46.9, u'grnd_level': 1034.37, u'temp_max': 46.9, u'sea_level': 1044.02, u'humidity': 48, u'pressure': 1034.37, u'temp_min': 46.9}, u'wind': {u'speed': 4.72, u'deg': 145.002}}], u'cod': u'200', u'cnt': 39}
	today= date(2017,3,26)
	
	
else:
		
	# get the data
	params = {'id': 4937230 , 'APPID': '52f0dd946b72eb3df249d0c507fc24da', 'units':'imperial'}
	request = "http://api.openweathermap.org/data/2.5/forecast"
	data=requests.get(request, params = params)
	if (data.status_code != 200):
		data.raise_for_status()
	resp=data.json()
	today= date.today()
	
	with open("/home/pi/tmp/currentWeather.log", 'a') as logfile:
		print (datetime.now().isoformat(' '))
		logfile.write(datetime.now().isoformat(' ')+'\n')
		logfile.write(data.text+'\n')
	
if (debug):
	print("today is %s" % today)

highlow=process_high_low(resp, today) # create the table of highs and lows per day

doc, tag,text = Doc().tagtext()
doc.asis('<!DOCTYPE html>')
with tag('html'):
	with tag('head'):
		doc.asis('<link rel="stylesheet" href"mystyles.css"/>')
		doc.asis('<META HTTP-EQUIV="refresh" CONTENT="900">')
	with tag('body'):
		
		with tag('h3'):
			text('Local Weather')
			
	
		with tag('table'):
			with tag('tr'):
				i = resp['list'][0] # this gets the first report, which is closest to the weather 'now'
				dt= datetime.fromtimestamp(resp['list'][0]['dt'])
				with tag('td'):
					with tag('b'):
						text("Today %i F" % i['main']['temp'])
				
				with tag('td'):
					with tag('img', src="http://openweathermap.org/img/w/"+adjustIcon(i['weather'][0]['icon'],dt)):
						pass
				with tag('td'):
					
					text("%i / %i" % (highlow[today]['high'], highlow[today]['low']))
			
			
			for d in range(1,5):
				newdate , day, noontime = days_future(today,d)
				if (debug):
					print ("Noon =")
					print (noontime)
				for i in resp['list']:
					dt= datetime.fromtimestamp(i['dt'])
					if (debug):
						print (dt)
					if (noontime == dt):
						with tag('tr'):	
							with tag('td'):
								text(day)
							
							with tag('td'):
								with tag('img', src="http://openweathermap.org/img/w/"+adjustIcon(i['weather'][0]['icon'],dt)):
									pass
							with tag('td'):
								text("%i / %i" % (highlow[newdate]['high'], highlow[newdate]['low']))	
						break	
with open("/home/pi/tmp/currentWeather.html", 'w')	as target:
	target.write(doc.getvalue())
	
		
	
		
