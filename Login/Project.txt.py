from flask import Flask,send_from_directory,request,jsonify
import json
import random
import io
import credentials
import time
import dbquery
import Projects
import re

def authentication():
    pass

app=Flask(__name__,static_folder='build',static_url_path='/')


@app.route("/api/create_project/", methods = ['POST'])
def createProject():
    # receive post data as a json
    project = request.json
    projectID = project['ProjectID']
    projectName = project['ProjectName']
    projectOwner = project['Owner']
    projectDescription = project['Description']
    projectHWSets = project['HWSets']

    NO_ERROR = "No Error"
    ERROR_CODE_1 = "ProjectID is a not an integer"
    ERROR_CODE_2 = "ProjectID Already Exists"

    # Validate using regex that proejct id is only numbers 
    if not re.match("^[0-9*]+$", projectID):
        return jsonify ({"Create-Project-Response": "Success", "Error": ERROR_CODE_1})

    # check if the project has a unique project id
    if (Projects.isProjectIDUnique(projectID)):
        # create the project in the database
        Projects.createProject(projectID, projectName, projectOwner, projectDescription, projectHWSets)
        # return a success
        return jsonify ({"Create-Project-Response": "Success", "Error": NO_ERROR})

    else:
        # return a fail
        return jsonify ({"Create-Project-Response": "Fail", "Error": ERROR_CODE_2})



@app.route('/api/getter/',methods=['GET'])
def getter_api():
    return json.dumps({'backend': random.randint(0, 1000)})

@app.route('/',methods=['GET'])
def index():
    return send_from_directory(app.static_folder,'index.html')

auth='1'
count=0
@app.route('/api/creds/',methods=['POST'])    ###Get the creds from the post request from back end
def creds():        ###Authenticate the request and send it to front end
    
    my_bytes_value = request.data
    fix_bytes_value = my_bytes_value.replace(b"'", b'"')
    my_json = json.load(io.BytesIO(fix_bytes_value))  
    ui_creds=credentials.encryption(my_json['email'],my_json['password'])
    server_creds=dbquery.creds_db(ui_creds.uname_en)
        
    global auth
    try:
        db_password=server_creds.findPass()
        print(db_password)
        if db_password==ui_creds.password_en:
            auth='great success'
        else:
            auth='fail'
    except:
        print('not working')
        auth='nouser'
    
    print(auth)
    return auth


@app.route('/api/auth/',methods=['GET'])
def authentication():
    return json.dumps({'authetication':auth})