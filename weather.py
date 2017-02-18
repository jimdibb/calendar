import requests
import re
import datetime
from yattag import Doc


#convert kelvin to farenheit
def k_to_f (temp):
	return temp * 9/5 - 459.67

#return yyyy-mm-dd delta days in the future	
def days_future(today, day_delta):
	newdate = datetime.date.fromordinal(today.toordinal() + day_delta)
	isodate = newdate.isoformat()
	day = newdate.strftime('%A')
	return (isodate,day) 
	
	
#dayname = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')

# get the data
#params = {'id': 4937230 , 'APPID': '52f0dd946b72eb3df249d0c507fc24da', 'units':'imperial'}
#request = "http://api.openweathermap.org/data/2.5/forecast"
#resp=requests.get(request, params = params)

#practice data
resp={"cod":"200","message":0.0063,"cnt":38,"list":[{"dt":1487397600,"main":{"temp":23.56,"temp_min":23.55,"temp_max":23.56,"pressure":1015.22,"sea_level":1024.94,"grnd_level":1015.22,"humidity":79,"temp_kf":0},"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03n"}],"clouds":{"all":32},"wind":{"speed":4.99,"deg":264.001},"sys":{"pod":"n"},"dt_txt":"2017-02-18 06:00:00"},{"dt":1487408400,"main":{"temp":21.36,"temp_min":21.36,"temp_max":21.36,"pressure":1014.63,"sea_level":1024.39,"grnd_level":1014.63,"humidity":83,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":2.55,"deg":233.006},"sys":{"pod":"n"},"dt_txt":"2017-02-18 09:00:00"},{"dt":1487419200,"main":{"temp":24.19,"temp_min":24.19,"temp_max":24.19,"pressure":1014.59,"sea_level":1024.19,"grnd_level":1014.59,"humidity":81,"temp_kf":0},"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}],"clouds":{"all":32},"wind":{"speed":5.32,"deg":215.5},"sys":{"pod":"d"},"dt_txt":"2017-02-18 12:00:00"},{"dt":1487430000,"main":{"temp":37.83,"temp_min":37.83,"temp_max":37.83,"pressure":1012.98,"sea_level":1022.35,"grnd_level":1012.98,"humidity":67,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":5.97,"deg":218.501},"sys":{"pod":"d"},"dt_txt":"2017-02-18 15:00:00"},{"dt":1487440800,"main":{"temp":46.61,"temp_min":46.61,"temp_max":46.61,"pressure":1009.84,"sea_level":1019.19,"grnd_level":1009.84,"humidity":64,"temp_kf":0},"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],"clouds":{"all":12},"wind":{"speed":9.19,"deg":224.5},"sys":{"pod":"d"},"dt_txt":"2017-02-18 18:00:00"},{"dt":1487451600,"main":{"temp":48.63,"temp_min":48.63,"temp_max":48.63,"pressure":1007.51,"sea_level":1016.8,"grnd_level":1007.51,"humidity":69,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"02d"}],"clouds":{"all":8},"wind":{"speed":7.96,"deg":227.505},"sys":{"pod":"d"},"dt_txt":"2017-02-18 21:00:00"},{"dt":1487462400,"main":{"temp":44.45,"temp_min":44.45,"temp_max":44.45,"pressure":1007.13,"sea_level":1016.4,"grnd_level":1007.13,"humidity":79,"temp_kf":0},"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02n"}],"clouds":{"all":12},"wind":{"speed":8.97,"deg":239.501},"sys":{"pod":"n"},"dt_txt":"2017-02-19 00:00:00"},{"dt":1487473200,"main":{"temp":45.06,"temp_min":45.06,"temp_max":45.06,"pressure":1006.97,"sea_level":1016.26,"grnd_level":1006.97,"humidity":80,"temp_kf":0},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}],"clouds":{"all":88},"wind":{"speed":8.86,"deg":247.502},"sys":{"pod":"n"},"dt_txt":"2017-02-19 03:00:00"},{"dt":1487484000,"main":{"temp":45.81,"temp_min":45.81,"temp_max":45.81,"pressure":1006.98,"sea_level":1016.28,"grnd_level":1006.98,"humidity":78,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],"clouds":{"all":80},"wind":{"speed":7.63,"deg":264},"sys":{"pod":"n"},"dt_txt":"2017-02-19 06:00:00"},{"dt":1487494800,"main":{"temp":44.38,"temp_min":44.38,"temp_max":44.38,"pressure":1008.4,"sea_level":1017.7,"grnd_level":1008.4,"humidity":83,"temp_kf":0},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}],"clouds":{"all":88},"wind":{"speed":7.25,"deg":279.003},"sys":{"pod":"n"},"dt_txt":"2017-02-19 09:00:00"},{"dt":1487505600,"main":{"temp":42.21,"temp_min":42.21,"temp_max":42.21,"pressure":1011.14,"sea_level":1020.46,"grnd_level":1011.14,"humidity":86,"temp_kf":0},"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],"clouds":{"all":24},"wind":{"speed":6.76,"deg":280.501},"sys":{"pod":"d"},"dt_txt":"2017-02-19 12:00:00"},{"dt":1487516400,"main":{"temp":49.02,"temp_min":49.02,"temp_max":49.02,"pressure":1012.53,"sea_level":1021.68,"grnd_level":1012.53,"humidity":74,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":6.31,"deg":281.002},"sys":{"pod":"d"},"dt_txt":"2017-02-19 15:00:00"},{"dt":1487527200,"main":{"temp":52.85,"temp_min":52.85,"temp_max":52.85,"pressure":1012.08,"sea_level":1021.24,"grnd_level":1012.08,"humidity":64,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":6.85,"deg":275.507},"sys":{"pod":"d"},"dt_txt":"2017-02-19 18:00:00"},{"dt":1487538000,"main":{"temp":51.05,"temp_min":51.05,"temp_max":51.05,"pressure":1013.18,"sea_level":1022.48,"grnd_level":1013.18,"humidity":63,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":7.34,"deg":288.501},"sys":{"pod":"d"},"dt_txt":"2017-02-19 21:00:00"},{"dt":1487548800,"main":{"temp":42.14,"temp_min":42.14,"temp_max":42.14,"pressure":1016.57,"sea_level":1025.96,"grnd_level":1016.57,"humidity":75,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":6.96,"deg":297.503},"sys":{"pod":"n"},"dt_txt":"2017-02-20 00:00:00"},{"dt":1487559600,"main":{"temp":37.74,"temp_min":37.74,"temp_max":37.74,"pressure":1018.88,"sea_level":1028.31,"grnd_level":1018.88,"humidity":83,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":6.62,"deg":304.511},"sys":{"pod":"n"},"dt_txt":"2017-02-20 03:00:00"},{"dt":1487570400,"main":{"temp":34.36,"temp_min":34.36,"temp_max":34.36,"pressure":1019.87,"sea_level":1029.38,"grnd_level":1019.87,"humidity":90,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":6.08,"deg":304.5},"sys":{"pod":"n"},"dt_txt":"2017-02-20 06:00:00"},{"dt":1487581200,"main":{"temp":33.02,"temp_min":33.02,"temp_max":33.02,"pressure":1020.54,"sea_level":1030.19,"grnd_level":1020.54,"humidity":90,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":6.17,"deg":301},"sys":{"pod":"n"},"dt_txt":"2017-02-20 09:00:00"},{"dt":1487592000,"main":{"temp":32.73,"temp_min":32.73,"temp_max":32.73,"pressure":1022.52,"sea_level":1032.1,"grnd_level":1022.52,"humidity":91,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":6.08,"deg":304.5},"sys":{"pod":"d"},"dt_txt":"2017-02-20 12:00:00"},{"dt":1487602800,"main":{"temp":42.71,"temp_min":42.71,"temp_max":42.71,"pressure":1024.08,"sea_level":1033.49,"grnd_level":1024.08,"humidity":75,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":6.22,"deg":317.004},"sys":{"pod":"d"},"dt_txt":"2017-02-20 15:00:00"},{"dt":1487613600,"main":{"temp":44.02,"temp_min":44.02,"temp_max":44.02,"pressure":1023.77,"sea_level":1033.28,"grnd_level":1023.77,"humidity":62,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":8.19,"deg":330.504},"sys":{"pod":"d"},"dt_txt":"2017-02-20 18:00:00"},{"dt":1487624400,"main":{"temp":40.5,"temp_min":40.5,"temp_max":40.5,"pressure":1025.73,"sea_level":1035.16,"grnd_level":1025.73,"humidity":59,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":9.19,"deg":342.002},"sys":{"pod":"d"},"dt_txt":"2017-02-20 21:00:00"},{"dt":1487635200,"main":{"temp":33.59,"temp_min":33.59,"temp_max":33.59,"pressure":1029.82,"sea_level":1039.47,"grnd_level":1029.82,"humidity":68,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":8.63,"deg":357.003},"sys":{"pod":"n"},"dt_txt":"2017-02-21 00:00:00"},{"dt":1487646000,"main":{"temp":30.48,"temp_min":30.48,"temp_max":30.48,"pressure":1032.2,"sea_level":1041.95,"grnd_level":1032.2,"humidity":75,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":7.4,"deg":359.001},"sys":{"pod":"n"},"dt_txt":"2017-02-21 03:00:00"},{"dt":1487656800,"main":{"temp":28.64,"temp_min":28.64,"temp_max":28.64,"pressure":1033.25,"sea_level":1042.97,"grnd_level":1033.25,"humidity":75,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":6.17,"deg":357.501},"sys":{"pod":"n"},"dt_txt":"2017-02-21 06:00:00"},{"dt":1487667600,"main":{"temp":26.29,"temp_min":26.29,"temp_max":26.29,"pressure":1033.2,"sea_level":1042.92,"grnd_level":1033.2,"humidity":85,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":5.41,"deg":355.502},"sys":{"pod":"n"},"dt_txt":"2017-02-21 09:00:00"},{"dt":1487678400,"main":{"temp":24.53,"temp_min":24.53,"temp_max":24.53,"pressure":1034.71,"sea_level":1044.53,"grnd_level":1034.71,"humidity":85,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":5.17,"deg":351.001},"sys":{"pod":"d"},"dt_txt":"2017-02-21 12:00:00"},{"dt":1487689200,"main":{"temp":35.72,"temp_min":35.72,"temp_max":35.72,"pressure":1035.32,"sea_level":1044.88,"grnd_level":1035.32,"humidity":68,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":4.5,"deg":14},"sys":{"pod":"d"},"dt_txt":"2017-02-21 15:00:00"},{"dt":1487700000,"main":{"temp":39.79,"temp_min":39.79,"temp_max":39.79,"pressure":1033.44,"sea_level":1043.01,"grnd_level":1033.44,"humidity":62,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"02d"}],"clouds":{"all":8},"wind":{"speed":4.27,"deg":31.5039},"sys":{"pod":"d"},"dt_txt":"2017-02-21 18:00:00"},{"dt":1487710800,"main":{"temp":38.54,"temp_min":38.54,"temp_max":38.54,"pressure":1031.78,"sea_level":1041.38,"grnd_level":1031.78,"humidity":58,"temp_kf":0},"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}],"clouds":{"all":36},"wind":{"speed":3.18,"deg":63.5},"sys":{"pod":"d"},"dt_txt":"2017-02-21 21:00:00"},{"dt":1487721600,"main":{"temp":29.45,"temp_min":29.45,"temp_max":29.45,"pressure":1031.08,"sea_level":1040.75,"grnd_level":1031.08,"humidity":75,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],"clouds":{"all":68},"wind":{"speed":2.93,"deg":89.5002},"sys":{"pod":"n"},"dt_txt":"2017-02-22 00:00:00"},{"dt":1487732400,"main":{"temp":27.6,"temp_min":27.6,"temp_max":27.6,"pressure":1029.61,"sea_level":1039.43,"grnd_level":1029.61,"humidity":77,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],"clouds":{"all":76},"wind":{"speed":2.39,"deg":159.503},"sys":{"pod":"n"},"dt_txt":"2017-02-22 03:00:00"},{"dt":1487743200,"main":{"temp":28.22,"temp_min":28.22,"temp_max":28.22,"pressure":1027.49,"sea_level":1037.1,"grnd_level":1027.49,"humidity":82,"temp_kf":0},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}],"clouds":{"all":88},"wind":{"speed":3.4,"deg":184.501},"sys":{"pod":"n"},"dt_txt":"2017-02-22 06:00:00"},{"dt":1487754000,"main":{"temp":30.58,"temp_min":30.58,"temp_max":30.58,"pressure":1025.15,"sea_level":1034.73,"grnd_level":1025.15,"humidity":85,"temp_kf":0},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}],"clouds":{"all":100},"wind":{"speed":4.05,"deg":208.501},"sys":{"pod":"n"},"dt_txt":"2017-02-22 09:00:00"},{"dt":1487764800,"main":{"temp":31,"temp_min":31,"temp_max":31,"pressure":1023.33,"sea_level":1033.02,"grnd_level":1023.33,"humidity":89,"temp_kf":0},"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}],"clouds":{"all":48},"wind":{"speed":4.61,"deg":221.002},"sys":{"pod":"d"},"dt_txt":"2017-02-22 12:00:00"},{"dt":1487775600,"main":{"temp":38.32,"temp_min":38.32,"temp_max":38.32,"pressure":1020.85,"sea_level":1030.39,"grnd_level":1020.85,"humidity":77,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"clouds":{"all":64},"wind":{"speed":5.41,"deg":221.508},"sys":{"pod":"d"},"dt_txt":"2017-02-22 15:00:00"},{"dt":1487786400,"main":{"temp":44.07,"temp_min":44.07,"temp_max":44.07,"pressure":1017.81,"sea_level":1027.22,"grnd_level":1017.81,"humidity":73,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"clouds":{"all":64},"wind":{"speed":4.85,"deg":239.501},"sys":{"pod":"d"},"dt_txt":"2017-02-22 18:00:00"},{"dt":1487797200,"main":{"temp":42.28,"temp_min":42.28,"temp_max":42.28,"pressure":1016.24,"sea_level":1025.64,"grnd_level":1016.24,"humidity":90,"temp_kf":0},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":{"all":76},"wind":{"speed":3.2,"deg":264.503},"rain":{"3h":0.1625},"sys":{"pod":"d"},"dt_txt":"2017-02-22 21:00:00"}],"city":{"id":4937230,"name":"Framingham","coord":{"lat":42.2793,"lon":-71.4162},"country":"US"}}

today= datetime.date(2017, 2, 17)
#today= datetime.date.today()

doc, tag,text = Doc().tagtext()
doc.asis('<!DOCTYPE html>')
with tag('html'):
	with tag('body'):
		
		with tag('h1'):
			text('Framingham Weather')
	
		with tag('table'):
			with tag('tr'):
				i = resp['list'][0] # this gets the first report, which is closest to the weather 'now'
					
				with tag('td'):
					text("Now")
				with tag('td'):
					text(today.isoformat())
				with tag('td'):
					text(i['weather'][0]['main'])
				with tag('td'):
					text(i['main']['temp'])	
				
			#print ("Now: %s : %s    Temp = %d" % (today, i['weather'][0]['main'], i['main']['temp']))

			d=1
			isodate , day = days_future(today,d)
			newdate = re.compile(isodate +' 18:00:00') #UTC is about 4-5 hours ahead, get the report from 6 pm, which is early afternoon
			for i in resp['list']:
				with tag('tr'):	
					
					if newdate.search(i['dt_txt']):
						with tag('td'):
							text(day)
						with tag('td'):
							text(isodate)
						with tag('td'):
							text(i['weather'][0]['main'])
						with tag('td'):
							text(i['main']['temp'])	
						#print ("%s : %s : %s    Temp = %d" % (day, isodate, i['weather'][0]['main'], i['main']['temp']))
						d+=1
						isodate , day = days_future(today,d)
						newdate = re.compile(isodate +' 18:00:00')

target = open("currentWeather.html", 'w')	
target.write(doc.getvalue())
target.close()
		
	
		
