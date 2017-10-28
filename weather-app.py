from flask import Flask, request, render_template
import requests


LOCATION_SERVICE_URL = 'https://location-ms.herokuapp.com/weather/api/1.0/addresses/convert'
WEATHER_SERVICE_URL = 'https://weather-ms.herokuapp.com/weather/api/1.0/reports/history'


app = Flask(__name__)


@app.route('/')
def show_form():
    return render_template('report_form.html')


@app.route('/form_data', methods=['POST'])
def get_report():
    address = request.form['address']
    date = request.form['date']
    weeks = request.form['weeks']

    rsp = requests.get(LOCATION_SERVICE_URL, params={'address': address})
    coord = rsp.json()

    params = {
        'address': ",".join([str(x) for x in coord['location'].values()]),
        'date': date,
        'w': weeks
    }
    rsp = requests.get(WEATHER_SERVICE_URL, params=params)
    return render_template('report_result.html', data=rsp.json()['data'])


if __name__ == '__main__':
    app.run()
