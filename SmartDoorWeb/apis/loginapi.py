from datetime import datetime
from collections import namedtuple
from flask import *
from extensions import mysql
from werkzeug import secure_filename
import json
import os
import hashlib
import re 
import uuid

loginapi = Blueprint('loginapi', __name__, template_folder='views')

def format_pw(password, input_pw): 
	algorithm='sha512' #nameofthealgorithmtouseforencryption 
	dbPassword = input_pw.split('$')
	algorithm = dbPassword[0]
	salt = dbPassword[1].encode('utf-8')	
	m = hashlib.new(algorithm) 
	m.update(salt + password) 
	password_hash = m.hexdigest()
	return "$".join([algorithm,salt,password_hash])

@loginapi.route('/login', methods=['POST'])
#send username and password for request 
def login(): 
	login_args = request.get_json()
	username = login_args['username']
	raw_password = login_args['password']
	password = format_pw(raw_password)
	user_info = execute("SELECT password, firstname, lastname, email FROM User WHERE username = '" + username + "'")

	return_num = 200 

	if (password == user_info[0][0]):
		session['username'] = username
		session['firstname'] = user_info[0][1]
		session['lastname'] = user_info[0][2]
		session['email'] = user_info[0][3]

		data = {
			'username': username
		}
	else: 
		return_num = 404 
		errors = {
			'error': "process failed"
		}

	obj = jsonify(data)
	obj.status_code = return_num
	return obj






