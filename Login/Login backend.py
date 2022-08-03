from flask import Flask, send_from_directory, request
import json
import random
import io
import credentials
import time
import dbquery


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
}

]

app = Flask(__name__, static_folder='build', static_url_path='/')


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
def creds():  # Authenticate the request and send it to front end

    my_bytes_value = request.data
    fix_bytes_value = my_bytes_value.replace(b"'", b'"')
    my_json = json.load(io.BytesIO(fix_bytes_value))
    ui_creds = credentials.encryption(my_json['email'], my_json['password'])
    server_creds = dbquery.creds_db(ui_creds.uname_en)

    global auth
    try:
        db_password = server_creds.findPass()
        print(db_password)
        if db_password == ui_creds.password_en:
            auth = 'great success'
        else:
            auth = 'fail'
    except:
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


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
