from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = 'https://test-api-615.herokuapp.com/api/feedback/test'
res = requests.get(API_URL)
Headers = {'Content-Type': 'application/json'}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        userID = request.form['userid']
        # need to store slider value
        sliderVal = str(request.form['myRange'])
        if userID == '':
            return render_template('index.html',
                                   message='Please enter User ID')
        dataToPOST = {
            "userID": userID,
            "sliderVal": sliderVal
        }
        # Return err message if userID already exists
        dataGOT = requests.get(API_URL).json()
        IDs = []
        for i in dataGOT:
            IDs.append(i["userID"])
        if userID in IDs:
            return render_template('index.html',
                                   message='UserID already exists')
        response = requests.post(API_URL, json=dataToPOST, headers=Headers)
        return render_template('thankyou.html',
                               message='Submission details: {}'.
                               format(str(response.json())))
        # return render_template('index.html',
        #                        message='You have already submitted')

@app.route("/researcher")
def researcher():
    return render_template('researcher.html')

@app.route("/researcher/submit", methods=['POST'])
def researcher_submit():
    if request.method == 'POST':
        col_name = request.form['col_name']
        return render_template('test.html', message='{}'.format(col_name))


if __name__ == '__main__':
    app.run()
