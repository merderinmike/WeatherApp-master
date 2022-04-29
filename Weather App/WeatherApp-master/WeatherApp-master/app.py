from flask import Flask, render_template, request
import sqlite3
import json
import requests

app = Flask(__name__)

api = '2ff0835878e6453a7de1dc834f6d9999'
x = 0
@app.route('/', methods=['POST', 'GET'])
def home():
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
    weather = ""
    if request.method == "POST":
        if "search" in request.form:
            home.city = request.form.get("city")
            r = requests.get(url.format(home.city, api)).json()
            weather = {
                'city': home.city,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'humidity': r['main']['humidity'],
                'wind': r['wind']['speed'],
                'icon': r['weather'][0]['icon'],
                'temp_max': r['main']['temp_max'],
                'temp_min': r['main']['temp_min']
            }
    return render_template("index.html", weather=weather)


@app.route('/hourly', methods=['POST', 'GET'])
def hourly():
    hourly = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=imperial&appid={}'
    data = dict()
    if request.method == "POST":
        if "hourly" in request.form:
            city = home.city
            h = requests.get(hourly.format(city, api)).json()
            x = 0
            for i in h['list']:
                humidity = i['main']['humidity']
                description = i['weather'][0]['description']
                temp = i['main']['temp']
                date = i['dt_txt']
                icon = i['weather'][0]['icon']
                wind = i['wind']['speed']
                tempMax = i['main']['temp_max']
                tempMin = i['main']['temp_min']
                data[x] = [icon, date, description, temp, humidity, wind, tempMax, tempMin]
                x = x + 1
            print(data[3])
        return render_template("hourly.html", data=data, city=city)


if __name__ == '__main__':
    app.run(debug=True)
