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

picturesapi = Blueprint('picturesapi', __name__, template_folder='views')

def execute(query):
	cur = mysql.connection.cursor()
	cur.execute(query)
	return cur.fetchall()

def update(query):
	cursor = mysql.connection.cursor()
	cursor.execute(query)
	mysql.connection.commit()
	return cursor.lastrowid

@userapi.route('/pictures', methods=['GET'])
def getAllPictureData():
	attributes = {}
	response_num = 200

	if not 'username' in session:
		response_num = 403
		attributes = {
			"error": "permission denied"
		}
	else: 
		currentPic = query("SELECT current_picture FROM Picture WHERE username = '"+session['username']+"'")[0][0]
		attributes = {
			"pictures" : currentPic; 
		}
	obj = jsonify(attributes)
	obj.status_code = response_num
	return obj

@userapi.route('/pictures', methods=['POST'])
def addFriend():
	args = request.get_json()
	attributes = {}
	response_num = 201
	if not 'username' in session:
		response_num = 404
		attributes = {
			"error": "no session exists"
		}
	else: 
		#check whether or not this username exists already. 
		#if exists, then replace picture
		#else, just add the picture
		update("INSERT INTO Picture(username, current_picture) VALUES('"+session['username']+"', '"+args['current_picture']+" ')")
		attributes = {
			"username": session['username'],
			"current_picture": current_picture
		}
	obj = jsonify(attributes)
	obj.status_code = response_num 
	return obj
