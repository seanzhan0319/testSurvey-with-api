from flask import Flask, render_template, request, redirect, url_for
import requests
import pymongo

app = Flask(__name__)

Feedback_URL = 'https://test-api-615.herokuapp.com/api/feedback'
API_URL = Feedback_URL + '/test'
res = requests.get(API_URL)
Headers = {'Content-Type': 'application/json'}

### assume the flask expt app below is made from a template ### 

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


# admin_mongodburi = "mongodb+srv://admin:p123456@democluster-ee3kz"\
#     ".mongodb.net/demoDatabase?retryWrites=true&w=majority"
# admin_client = pymongo.MongoClient(admin_mongodburi)
# admin_db = admin_client.demoDatabase
admin_mongodburi = "mongodb://user:p123456@ds263248.mlab.com:63248/heroku_5qkz777p"
admin_client = pymongo.MongoClient(admin_mongodburi)
admin_db = admin_client["heroku_5qkz777p"]

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/signup/success", methods=["POST"])
def signup_success():
    if request.method == 'POST':
        username = request.form['usr_name']
        password = request.form['pwd']
        # need to safeguard username repetition
        # admin_db.add_user(username, password, roles=[{'role':'restricted', 'db':'restricted'}])
        admin_db.command("createUser", username, 
            pwd=password, roles=["restricted"])
        dataToPOST = {
            "username": username,
            "password": password
        }
        Dest_URL = Feedback_URL + '/credentials'
        sent = requests.post(Dest_URL, json=dataToPOST, headers=Headers)
        return render_template('signup.html',
            message='User ({}) created.'.format(username),
            should_login=True)

@app.route("/signup/success/redirect", methods=["POST"])
def signup_redirect():
    if request.method == 'POST':
        return redirect(url_for('login'))


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/researcher", methods=['POST'])
def researcher():
    if request.method == 'POST':
        username = request.form['usr_name']
        password = request.form['pwd']
        # # using mongoclient doens't give you the password
        # # NEED TO LOOK AT IF THE HASH OF PASSWORD MATCHES WITH THE CREDENTIALS
        # # for now, we will use a collection on mongodb to store credentials
        # users = admin_db.command('usersInfo', showCredentials=True)
        Dest_URL = Feedback_URL + '/credentials'
        dataGOT = requests.get(Dest_URL).json()
        for item in dataGOT:
            if item['username'] == username:
                if item['password'] == password:
                    return render_template('researcher.html', usr=username)
                else:
                    return render_template('login.html', 
                        message='Incorrect Password. Please try again.')
        return render_template('login.html', message='User does not exist')

@app.route("/researcher/submit", methods=['POST'])
def researcher_submit():
    if request.method == 'POST':
        col_name = request.form['col_name']
        username = request.form['usr']
        # need to safeguard collection already exists error
        admin_db.create_collection(col_name)
        role_name = "use-" + col_name
        admin_db.command("createRole", role_name, 
            privileges=[{
                'resource': { 'db': 'heroku_5qkz777p', 'collection': col_name },
                'actions': ['find', 'insert', 'remove', 'update' ]}],
            roles=[])
        # admin_db.command("updateUser", username, roles=[role_name])
        # print(admin_db.command("usersInfo", showPrivileges=True))
        admin_db.command("grantRolesToUser", username, roles=[{'role': role_name, 'db': 'heroku_5qkz777p'}])
        return render_template('researcher.html',
            message='Collection ({}) created.'.format(col_name))


if __name__ == '__main__':
    app.run()
