import requests
import json
import datetime

def getWeather():
    weather_api = 'ca21216fd309c93287df5ad643170ed1'
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Seattle&appid="+weather_api+"&units=imperial")
    # parse response
    response_str = ""
    for line in response:
        response_str += line.decode("utf-8") 
        # parse json
    response_json = json.loads(response_str)
    current_temp = response_json["main"]["temp"]
    min_temp = response_json["main"]["temp_min"]
    max_temp = response_json["main"]["temp_max"]
    return str(current_temp), str(min_temp), str(max_temp)

def getCurrentDateTime():
    current_time = datetime.datetime.now()
    return current_time.strftime('%m/%d/%y %I:%M %p')

current_temp, min_temp, max_temp = getWeather()

print("Current temp: "+current_temp + " Min temp: " +  min_temp +  " Max temp: "  + max_temp)
#current_time = datetime.datetime.now()
#current_time = current_time.strftime('%m/%d/%y %I:%M %p')
current_time = getCurrentDateTime()
print(current_time)
