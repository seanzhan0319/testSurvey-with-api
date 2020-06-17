from flask import Flask, render_template, request
import requests

app = Flask(__name__)

MONGODB_URL = 'https://test-api-615.herokuapp.com/api/feedback'
res = requests.get(MONGODB_URL)
Headers = {'Content-Type':'application/json'}

# {'userID': 'test04', 'sliderVal': 'put-04', 'q1': 'anssss1', 'q2': 'anssss2', 'q3': 'anssss3'}

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()