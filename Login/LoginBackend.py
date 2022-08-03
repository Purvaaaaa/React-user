from flask import Flask, send_from_directory, request
import json
import random
import io
import credentials
import time
import dbquery
from flask_cors import CORS, cross_origin
import re

def authentication():
    pass


userData = [{
    "FirstName": "Code",
    "Lastname": "Handbook"
}, {
    "FirstName": "Ravi",
    "Lastname": "Shanker"
}, {
    "FirstName": "Salman",
    "Lastname": "Khan"
}, {
    "FirstName": "Ali",
    "Lastname": "Zafar"
}, {
    "FirstName": "Test",
    "LastName": "Last Name test"
}
]

userprofileObject=[]
def addUserProfileData(data):
    userprofileObject.append(data)

def validateUserProfileData(userData):
    authentication=False
    for data in userprofileObject:
        print(data)
        print(userData)
        if userData['userid'] == data['userid'] and userData['userPassword'] == data['userPassword']:
            authentication = True
    return authentication

app = Flask(__name__, static_folder='build', static_url_path='/')
cors = CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/api/getter/', methods=['GET'])
def getter_api():
    return json.dumps({'backend': random.randint(0, 1000)})


@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, 'index.html')


auth = '1'
count = 0


# Get the creds from the post request from back end
@app.route('/api/creds/', methods=['POST'])
@cross_origin(origin='127.0.0.1',headers=['Content- Type','Authorization'])
def creds():  # Authenticate the request and send it to front end

    my_bytes_value = request.data
    fix_bytes_value = my_bytes_value.replace(b"'", b'"')
    my_json = json.load(io.BytesIO(fix_bytes_value))

    # This thing below created problem saying "credentials" has no attribute encryption hence just reading values from ui
    # ui_creds = credentials.encryption(my_json['email'], my_json['password'])
    ui_id = my_json['id']
    ui_password = my_json['password']
    # server_creds = dbquery.creds_db(ui_creds.uname_en)

    global auth
    try:
        # db_password = server_creds.findPass()

        dataToValidate = {"userid":ui_id,"userPassword":ui_password}
        if validateUserProfileData(dataToValidate) == True:
            auth = 'great success'
        else:
            auth = 'fail'
    except Exception as e:
        print(e)
        print('not working')
        auth = 'nouser'

    print(auth)
    return auth


@app.route('/api/auth/', methods=['GET'])
def authentication():
    return json.dumps({'authetication': auth})


def getLastName(firstName):
    for data in userData:
        if data['FirstName'] == firstName:
            return data['Lastname']
    else:
        return -1


@app.route('/api/getusersurname/<username>', methods=['GET'])
def getUserLastname(username):
    status = 2
    lastname = ""
    data = getLastName(username)
    if (data == -1):
        status = 1
    else:
        lastname = data
        status = 0
    return json.dumps({'status': status, 'lastname': lastname})

@app.route("/api/validate-signup/", methods=["POST"])
def response_validation():
    # get data from front end - json format
    request_data = request.json

    # signup response set at the beginning
    response = {"API-Signup-Response":''}
    # error codes

    error_code_2 = "Invalid username"
    error_code_3 = "Invalid password"

    # Username validation - only numbers and letters allowed
    # Get username value from json form
    username = request_data["username"]
    # test if username is alphanumeric
    """if not (username.isalnum()):
        print("username is not alphanumeric")
        response["API-Signup-Response"] = "Invalid username"
        return json.dumps(response)"""

    # Email validation - use regex to validate that:
    #
    #   email has an @ symbol
    #   before the @ symbol that letters are alphanumeric and/or contain .
    #   after the @ symbol that there is a (.)
    #   after the . symbol that that the domain is alpha
    # Get email value from json form
    email = request_data["username"]
    email_rules = "^[a-zA-Z0-9\.]+@[a-zA-Z0-9]+\.[a-z]$"
    """if not (re.match(email, email_rules)):
        print("email does not match email convetions")
        response["API-Signup-Response"] = "Invalid email"
        return json.dumps(response)"""

    # Password validation - use regex to validate that only numbers and letters allowed
    password = request_data["password"]
    email_rules = "^[a-zA-Z0-9\.]+@[a-zA-Z0-9]+\.[a-z]$"
    # TODO Technical Debt: passwords are only alphanumeric
    # TODO Technical Debt: passwords do not have a length, cap, num, spec chars requirements
    """if not (re.match(email, email_rules)):
        print("password is not alphanumeric")
        response["API-Signup-Response"] = "Invalid password"
        return json.dumps(response)"""

    # temporary code for database detection of email
    """if (dbquery.check_existing_email(email)):
        print("email already exists")
        response["API-Signup-Response"] = "Invalid email"
        return json.dumps(response)

    # temporary code for database detection of username
    if (dbquery.check_existing_user(username)):
        print("user already exists")
        response["API-Signup-Response"] = "Invalid username"
        return json.dumps(response)"""

    # valid input
    response["API-Signup-Response"] = "Valid input"
    # create user in the database with credentials
    #dbquery.create_user(username, email, password) # commented as db operation will be performed later
    userSighnUpData={'userid':username,'password':password}
    addUserProfileData(userSighnUpData)
    return response



if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
