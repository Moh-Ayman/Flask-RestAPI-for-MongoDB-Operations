from flask import Flask, jsonify, request, make_response, render_template, session, flash
from pymongo import MongoClient
from bson.json_util import dumps
import jwt
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash 
import json
import os

app = Flask(__name__)

def INIT():
    try:
        applog(" - INIT() -- Started","n")
        applog(" - INIT() -- Declaring Global Variables","n")
        global bin_dir
        global project_dir
        global var_dir
        global lib_dir
        global conf_dir
        global log_dir
        global app_log_file
        global config_file
        global CONFIGS
        global mongoClient
        applog(" - INIT() -- Global Variables Declared","n")
        
        applog(" - INIT() -- Getting Script Current Abs Path","n")        
        current_path = os.path.dirname(os.path.realpath(__file__))
        bin_dir = current_path
        applog(" - INIT() -- Defining Project Abs Paths","n")        
        project_dir = os.path.abspath(os.path.join(current_path, os.pardir))
        var_dir = os.path.join(project_dir,"var")
        lib_dir = os.path.join(project_dir,"lib")
        log_dir = os.path.join(project_dir,"log")
        app_log_file = os.path.join(log_dir,"app.log")
        conf_dir = os.path.join(project_dir,"conf")
        config_file = os.path.join(conf_dir,"flask_app.conf")
        applog(" - INIT() -- Starting READ_CONF()","n")        
        CONFIGS=READ_CONF(config_file)
        applog(" - INIT() -- READ_CONF() Ended","n")  
        applog(" - INIT() -- Configurations: \n" + str(CONFIGS),"d")
        applog(" - INIT() -- Starting MongoConnect()","n")        
        mongoClient = MongoConnect()
        applog(" - INIT() -- MongoConnect() Ended","n")
    except(ValueError,IOError) as err:
        applog(" - INIT() -- "+str(err),"e")      

def READ_CONF(Conf_File_Path):
    try:
        applog(" - READ_CONF() -- Started","n")
        applog(" - READ_CONF() -- Configuration File:" + str(Conf_File_Path),"d")
        applog(" - READ_CONF() -- Open Configuration File","n")
        CONF_FILE_OPENED = open(Conf_File_Path) 
        applog(" - READ_CONF() -- Read JSON Data","n")
        DATA = json.load(CONF_FILE_OPENED)
        applog(" - READ_CONF() -- Close File Connection","n")
        CONF_FILE_OPENED.close()
        applog(" - READ_CONF() -- Returning CONFIGS","n")
        return DATA
    except(ValueError,IOError) as err:
        applog(" - READ_CONF() -- "+str(err),"e")

def format_time():
    try:
        t = datetime.datetime.now()
        s = t.strftime('%m-%d-%Y %H:%M:%S.%f')
        return s[:-3]
    except (ValueError,IOError) as err:
        log(" - Main() -- Error Occured \n"+str(err),"e")

def applog(message,status):
    try:
        if status=="e":
                f.write(format_time() + " -0000 ERROR " + str(message)+"\n")
        elif status=="s":
                f.write(format_time() + " -0000 SUCCESS " + str(message)+"\n")
        elif status=="n":
                f.write(format_time() + " -0000 INFO " + str(message)+"\n")
        elif status=="w":
                f.write(format_time() + " -0000 WARNING " + str(message)+"\n")
        elif status=="d":
                f.write(format_time() + " -0000 Data " + str(message)+"\n")
    except (ValueError,IOError) as err:
        applog(" - Main() -- Error Occured \n"+str(err),"e")

def MongoConnect():
    try:
        applog(" - MongoConnect() -- Started","n")
        applog(" - MongoConnect() -- Setting Connection String","n")
        myclient = MongoClient(
            host=CONFIGS["MongoDB"]["DB_IP"], 
            port=CONFIGS["MongoDB"]["DB_PORT"], 
            username=CONFIGS["MongoDB"]["DB_Username"],
            password=CONFIGS["MongoDB"]["DB_Password"],
            authSource=CONFIGS["MongoDB"]["authSource"]
            )
        #myclient = MongoClient('mongodb://admin:admin@192.168.182.140:27017/?authSource=test')
        applog(" - MongoConnect() -- Returning Connection Client","n")
        return myclient
    except (ValueError,IOError) as err:
        applog(" - MongoConnect() -- "+str(err),"e")    

app.config['SECRET_KEY'] = 'thisisthesecretkey'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can view this!'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'This is only available for people with valid tokens.'})

@app.route('/api/hello/1/hi')
def hello():
    return "Hello"

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'secret':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

def mongo_add(db,col,payload):
    try:
        mydb = mongoClient[db]
        mycol = mydb[col]
        if isinstance(payload, dict):
            mycol.insert(payload)
            return str(payload)
        elif isinstance(payload, list):
            mycol.insert_many(payload)
            return str(payload)
        else:
            return server_error("Payload Data not either List or Dict")
    except Exception as e:
        return server_error(e)

def mongo_fetch_all(db,col):
    try:
        mydb = mongoClient[db]
        mycol = mydb[col]
        mydoc = mycol.find({},{ "_id": 0})
        mydoc_json = list(mydoc)
        return mydoc_json
    except Exception as e:
        return server_error(e) 

def mongo_filter(db,col,query,lim):
    try:
        mydb = mongoClient[db]
        mycol = mydb[col]
        mydoc = mycol.find(query,{ "_id": 0}).limit(lim)
        mydoc_json = list(mydoc)
        return mydoc_json
    except Exception as e:
        return server_error(e)
    
@app.route("/mk/api/v1/add/<db>/<col>", methods=['POST'])
def add_doc(db,col):
    try:
        if not request.method=='POST':
            return method_not_allowed(request.method)
        payload=request.json
        if payload and request.method=='POST':
            payload = mongo_add(db,col,payload)
            response = jsonify("Item Added Successfully")
            response.status_code = 200
            return response
        else:
            return not_found("No Payload Found")
    except Exception as e:
        return server_error(e)

@app.route("/mk/api/v1/fetch/<db>/<col>/all", methods=['GET'])
def fetch_all_doc(db,col):
    try:
        if not request.method=='GET':
            return method_not_allowed(request.method)
        data = mongo_fetch_all(db,col)
        response = jsonify("Item Added Successfully")
        response.status_code = 200
        return jsonify(data)
    except Exception as e:
        return server_error(e)
     
@app.route("/mk/api/v1/filter/<db>/<col>/<lim>", methods=['GET'])
def filter_doc(db,col,lim):
    try:
        if not request.method=='GET':
            return method_not_allowed(request.method)
        if lim.isdigit():
            pass
        else:
            return not_found("Invalid Limit")
        args = request.args
        args = args.to_dict()
        data = mongo_filter(db,col,args,int(lim))
        response = jsonify("Item Added Successfully")
        response.status_code = 200
        return jsonify(data)
    except Exception as e:
        return server_error(e)    
     
@app.errorhandler(404)
def not_found(error):
    message ={'Status': 404, 'Message':'Not Found '+str(request.url)+'\n Error:\n'+str(error)}
    response=jsonify(message)
    response.status_code = 404
    return response

@app.errorhandler(500)
def server_error(error):
    message ={'Status': 500, 'Message':'Internal Server Error '+str(request.url)+'\n Error:\n'+str(error)}
    response=jsonify(message)
    response.status_code = 500
    return response

@app.errorhandler(405)
def method_not_allowed(error):
    message ={'Status': 405, 'Message':'Method Not Allowed '+str(request.url)+'\n Method:\n'+str(error)}
    response=jsonify(message)
    response.status_code = 405
    return response


if __name__ == '__main__':
    try:
        applog(" - Main() -- Started","n")
        applog(" - Main() -- Starting INIT()","n")
        INIT()
        applog(" - Main() -- INIT() Ended","n")
        with open(app_log_file,'a+') as f:
            app.run(CONFIGS["Flask_App"]["API_IP"],CONFIGS["Flask_App"]["API_PORT"],debug = CONFIGS["Flask_App"]["DEBUG_MODE"])
        f.close()
    except (ValueError,IOError) as err:
        applog(" - Main() -- Error Occured \n"+str(err),"e")