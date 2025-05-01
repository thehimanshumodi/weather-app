from django.shortcuts import render,  HttpResponse
import json
import requests

def weather(request):
    error_message = None
    data = {}
    if request.method == "POST":
        city = request.POST.get("city")
        source = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=f103c33ea8b5af1832a9d7bb6afc3821"
        try:
            list_of_data = requests.get(source.format(city)).json()
            if list_of_data.get("cod") != 200:
                error_message = list_of_data.get("message", "Error retrieving weather data.")
            else:
                data = {
                    "country_code": str(list_of_data["sys"]["country"]),
                    "coordinate": str(list_of_data["coord"]["lon"]) + " " + str(list_of_data["coord"]["lat"]),
                    "temp": round((list_of_data["main"]["temp"]-32) * 5/9.0, 2), 
                    "humidity": str(list_of_data["main"]["humidity"]),
                }
        except Exception as e:
            error_message = "Failed to retrieve weather data."
    data["error_message"] = error_message
    return render(request, "weather.html", data)
