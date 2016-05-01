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

friendsapi = Blueprint('friendsapi', __name__, template_folder='views')

def execute(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    return cur.fetchall()

def update(query):
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()
    return cursor.lastrowid

@userapi.route('/friends', methods=['GET'])
def getAllFriendData():
	attributes = {}
	response_num = 200

	if not 'username' in session:
		response_num = 403
		attributes = {
			"error": "permission denied"
		}
	else: 
		friendData = query("SELECT * FROM Friends WHERE username = '"+session['username']+"'")
		attributes = {
			"friends" : friendData[0]; 
		}
	obj = jsonify(attributes)
	obj.status_code = response_num
	return obj

#send in the friend id to delete 
@userapi.route('/friends', methods=['DELETE'])
def deleteFriend():
	friendid = request.get_json()['friendid']
	attributes = {}
	response_num = 201
	#check to make sure current user has accesst to delete this 
	user_with_access = query("SELECT username FROM Friends WHERE friendid = '"+friendid+"'")

	if not 'username' in session:
		response_num = 404
		attributes = {
			"error": "no session exists"
		}
	#user has permission to delete the profile 
	if user_with_access[0][0] == session['username']:
		update("DELETE FROM Friends WHERE friendid = '"+friendid+"'")
		attributes = {
			"username": session['username'],
			"friendid" : friendid
		}

	else: 
		attributes = {
			"error" : "permission denied"
		}
		response_num = 403
	obj = jsonify(attributes)
	obj.status_code = response_num
	return obj


#creating a new profile (pass in name, picture url, access, possible time)
@userapi.route('/friends', methods=['POST'])
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
		if args['access'] == 'timed':
			update("INSERT INTO Friends(username, name, picture_url, access, time) VALUES('"+session['username']+"', '"+args['name']+"', '"+args['picture_url']+"', '"+args['access']+"', '"+args['time']+"')")
		else:
			update("INSERT INTO Friends(username, name, picture_url, access) VALUES('"+session['username']+"', '"+args['name']+"', '"+args['picture_url']+"', '"+args['access']+"')")
		friendid = query("SELECT MAX(friendid) FROM Friends")
		attributes = {
			"username": session['username'],
			"friendid": friendid
		}
	obj = jsonify(attributes)
	obj.status_code = response_num 
	return obj


@userapi.route('/friends', methods=['PUT'])
def editFriend():
	args = request.get_json()
	attributes = {}
	response_num = 201
	user_with_access = query("SELECT username FROM Friends WHERE friendid = '"+friendid+"'")
	if not 'username' in session:
		response_num = 404
		attributes = {
			"error": "no session exists"
		}
	else if user_with_access[0][0] == session['username']: #update on the fields we've inputted 
		attributes = {"username:" session['username']}
		for key in ['name', 'picture_url', 'access', 'time']:
			if key in args: 
				execute("UPDATE Friends SET '"+key+"' = '"+args[key]+"' WHERE friendid = '"+args['friendid']+"'")
				attributes[key] = args['key']
	else: 
		attributes = {
			"error" : "permission denied"
		}
		response_num = 403
	obj = jsonify(attributes)
	obj.status_code = response_num 
	return obj




