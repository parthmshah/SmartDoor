# from api import *

from datetime import datetime
from collections import namedtuple
from flask import *
from extensions import mysql
from werkzeug import secure_filename
import json
import hashlib
import os
import re
import uuid
from extensions import mysql

userapi = Blueprint('userapi', __name__, template_folder='views')

def execute(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    return cur.fetchall()

def update(query):
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()
    return cursor.lastrowid

def format_pw(password): 
	algorithm='sha512' #nameofthealgorithmtouseforencryption 
	salt=uuid.uuid4().hex #saltasahexstringforstorageindb
	m = hashlib.new(algorithm) 
	m.update(salt + password) 
	password_hash = m.hexdigest()
	return "$".join([algorithm,salt,password_hash])

@userapi.route('/user', methods=['GET'])
def check_if_session():
	response_num = 201
	attributes = {} 
	if not 'username' in session:
		response_num = 403
		attributes = {
			"error": "permission denied"
		}
	else: 
		attributes = {
			"username" : session['username'],
			"firstname" : session['firstname'],
			"lastname" : session['lastname'],
			"email" : session['email']
		}
	obj = jsonify(attributes)
	obj.status_code = response_num
	return obj


#creating a user input username, firstname, lastname, email, password
@userapi.route('/user', methods=['POST'])
def edit_user():
	args = request.get_json()
	attributes = {}
	response_num = 201

	args = request.get_json();
	userdata_query = execute("SELECT * FROM User WHERE username = '"+args[username]+"' OR email = '"+args[email]+"'")
	if not userdata_query: 
		formatted_pw = format_pw(args['password'])
		update("INSERT INTO User VALUES ('"+args['username']+"', '"+args[firstname]+"', '"+args[lastname]+"', '"+format_pw+"', '"+args[email])+"')")
		attributes = {
			"success": "user profile created" 
		}

	else: 
		response_num = 404	
		attributes = {
			"failure": "username or email already exists" 
		}
	obj = jsonify(attributes)
	obj.status_code = response_num 
	return obj









