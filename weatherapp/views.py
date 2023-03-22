from django.shortcuts import render
import requests
from django.contrib import messages
from geopy.geocoders import Nominatim

# API key to get data
api_key = "784d30ac56f4e345881dd1d3fcf5dd6f"

# Create your views here.
def celcius(request):
    
    if request.method == 'POST':
        
        # Recieving the name of the city from post data in form
        city = request.POST['city'].lower()
        
        # OpenWeatherMap API to get data
        # Here, i have used the 5 Day/3 Hour Forecast API to get data
        # By using metric as unit, it gives the data in celcius
        weather_endpoint = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
        # Converting json response to python dictionary to use as context
        weather_response = requests.get(weather_endpoint).json()
        
        # To get the latitude and longitude for air quality api
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(city)
        
        # api to get air quality data
        aqi_endpoint = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={location.latitude}&lon={location.longitude}&appid={api_key}"
        
        # Converting json response to python dictionary to use as context
        aqi_response = requests.get(aqi_endpoint).json()
        aqi = aqi_response['list'][0]
        
        # to use the air quality index which is provided as an integer in the api response, as a quality name  
        aqindex = {
            # 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor.
            1:"Good",
            2:"Fair",
            3:"Moderate",
            4:"Poor",
            5:"Very Poor",
        }
        # Error handling in case user puts a wrong name
        try:
            
            # List comprehension to find the max temperature and min temperature values for every 3 hour
            tempmaxarr = [weather_response['list'][i]['main']['temp_max'] for i in range(40)]  
            tempminarr = [weather_response['list'][i]['main']['temp_min'] for i in range(40)]  
            
            # List comprehension to find the maximum value of max temperature for a day
            temp_max = [max(tempmaxarr[i:i+8]) for i in range(0,40,8)]
            
            # List comprehension to find the minimum value of max temperature for a day
            temp_min = [min(tempminarr[i:i+8]) for i in range(0,40,8)]
            
            # To get all the related dates and icons for the weather
            dt_txt = [weather_response["list"][i]["dt_txt"].split()[0] for i in range(0,40,8)]
            icons = [weather_response["list"][i]["weather"][0]["icon"] for i in range(0,40,8)]
            
            
            context = {
                
            'aqi' : aqi,
            # data for current weather
            "city" : weather_response["city"]["name"] ,
            "country" : weather_response["city"]["country"],
            "temperature" : round(weather_response["list"][0]["main"]["temp"]),
            "humidity" : weather_response["list"][0]["main"]["humidity"],
            "windspeed" : weather_response["list"][0]["wind"]["speed"],
            "description" : weather_response["list"][0]["weather"][0]["description"],
            
            # data for weather forecast
            "date1" : dt_txt[0],
            "temp_min1" : round(temp_min[0]),
            "temp_max1" : round(temp_max[0]),
            "icon1" : icons[0],
            
            "date2" : dt_txt[1],
            "temp_min2" : round(temp_min[1]),
            "temp_max2" : round(temp_max[1]),
            "icon2" : icons[1],
            
            "date3" : dt_txt[2],
            "temp_min3" : round(temp_min[2]),
            "temp_max3" : round(temp_max[2]),
            "icon3" : icons[2],
            
            "date4" : dt_txt[3],
            "temp_min4" : round(temp_min[3]),
            "temp_max4" : round(temp_max[3]),
            "icon4" : icons[3],
            
            "date5" : dt_txt[4],
            "temp_min5" : round(temp_min[4]),
            "temp_max5" : round(temp_max[4]),
            "icon5" : icons[4],

            "quality" : aqindex[aqi["main"]["aqi"]],
            "co":aqi["components"]["co"],
            "no":aqi["components"]["no"],
            "no2":aqi["components"]["no2"],
            "o3":aqi["components"]["o3"],
            "so2":aqi["components"]["so2"],
            "pm2":aqi["components"]["pm2_5"],
            "pm10":aqi["components"]["pm10"],
            "nh3":aqi["components"]["nh3"],
        }
        except:
            # error message in case user inputs a wrong name
            messages.error(request, "Invalid City Name")
            context = {'error':'city not found'}
        
        return render(request,'weatherapp/celcius.html',context)
        
    context = {}
    return render(request,'weatherapp/celcius.html',context)


def fahrenheit(request):
    
    if request.method == 'POST':
        
        # Recieving the name of the city from post data in form
        city = request.POST['city'].lower()
        
        # OpenWeatherMap API to get data
        # Here, I have used the 5 Day/3 Hour Forecast API to get data
        # By using metric as unit, it gives the data in fahrenheit
        endpoint = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=imperial&appid={api_key}"
       
        # Converting json response to python dictionary to use as context
        response = requests.get(endpoint).json()
        
        # To get the latitude and longitude for air quality api
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(city)
        
        # api to get air quality data
        aqi_endpoint = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={location.latitude}&lon={location.longitude}&appid={api_key}"
        
        # Converting json response to python dictionary to use as context
        aqi_response = requests.get(aqi_endpoint).json()
        aqi = aqi_response['list'][0]
        
        # to use the air quality index which is provided as an integer in the api response, as a quality name  
        aqindex = {
            # 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor.
            1:"Good",
            2:"Fair",
            3:"Moderate",
            4:"Poor",
            5:"Very Poor",
        }
        
        # Error handling in case user puts a wrong name
        try:
            
            # List comprehension to find the max temperature and min temperature values for every 3 hour
            tempmaxarr = [response['list'][i]['main']['temp_max'] for i in range(40)]  
            tempminarr = [response['list'][i]['main']['temp_min'] for i in range(40)]  
            
            # List comprehension to find the maximum value of max temperature for a day
            temp_max = [max(tempmaxarr[i:i+8]) for i in range(0,40,8)]
            
            # List comprehension to find the minimum value of max temperature for a day
            temp_min = [min(tempminarr[i:i+8]) for i in range(0,40,8)]
            
            # To get all the related dates and icons for the weather
            dt_txt = [response["list"][i]["dt_txt"].split()[0] for i in range(0,40,8)]
            icons = [response["list"][i]["weather"][0]["icon"] for i in range(0,40,8)]
            
            
            context = {
            # data for current weather
            "city" : response["city"]["name"] ,
            "country" : response["city"]["country"],
            "temperature" : round(response["list"][0]["main"]["temp"]),
            "humidity" : response["list"][0]["main"]["humidity"],
            "windspeed" : response["list"][0]["wind"]["speed"],
            "description" : response["list"][0]["weather"][0]["description"],
            
            # data for weather forecast
            "date1" : dt_txt[0],
            "temp_min1" : round(temp_min[0]),
            "temp_max1" : round(temp_max[0]),
            "icon1" : icons[0],
            
            "date2" : dt_txt[1],
            "temp_min2" : round(temp_min[1]),
            "temp_max2" : round(temp_max[1]),
            "icon2" : icons[1],
            
            "date3" : dt_txt[2],
            "temp_min3" : round(temp_min[2]),
            "temp_max3" : round(temp_max[2]),
            "icon3" : icons[2],
            
            "date4" : dt_txt[3],
            "temp_min4" : round(temp_min[3]),
            "temp_max4" : round(temp_max[3]),
            "icon4" : icons[3],
            
            "date5" : dt_txt[4],
            "temp_min5" : round(temp_min[4]),
            "temp_max5" : round(temp_max[4]),
            "icon5" : icons[4],

            "quality" : aqindex[aqi["main"]["aqi"]],
            "co":aqi["components"]["co"],
            "no":aqi["components"]["no"],
            "no2":aqi["components"]["no2"],
            "o3":aqi["components"]["o3"],
            "so2":aqi["components"]["so2"],
            "pm2":aqi["components"]["pm2_5"],
            "pm10":aqi["components"]["pm10"],
            "nh3":aqi["components"]["nh3"],
        }
        except:
            # error message in case user inputs a wrong name
            messages.error(request, "Invalid City Name")
            context = {'error':'city not found'}
        
        return render(request,'weatherapp/fahrenheit.html',context)
        
    context = {}
    return render(request,'weatherapp/fahrenheit.html',context)