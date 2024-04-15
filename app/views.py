from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pycountry

# get china city info
cities = pycountry.subdivisions.get(country_code='CN')
city_list = []
for city in cities:
    # del unneeded fields
    if "Sheng" in city.name or "Shi" in city.name:
        city_name = city.name.split(" ")[0]
        city_list.append(city_name)

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'please use weather check!'


# return all city
@app.route("/city", methods=['GET'])
def get_cities():
    return jsonify({"code": 200, "data": city_list})


# city weather_info api
@app.route("/weather", methods=['GET'])
def get_city_2_weather():
    city_name = request.args.get('city')
    # city name error
    if city_name not in city_list:
        return jsonify({"code": 500001, "msg": f"{city_name} is error,please reselect!!", "data": []})
    res = requests.get(url=f"https://goweather.herokuapp.com/weather/{city_name}")

    # remote weather api error
    if res.status_code != 200:
        return jsonify({"code": 500002, "msg": f"request is network error， please reselect！！！", "data": []})

    # today city weather
    weather_dict = {
        "temperature": res["temperature"],
        "wind": res["wind"],
        "description": res["description"]
    }
    return jsonify({"code": 200, "data": weather_dict})