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

logoutapi = Blueprint('logoutapi', __name__, template_folder='views')

@logoutapi.route('/logout', methods=['DELETE'])
#send username and password for request 
def logout(): 
	obj = {"username" : session['username']}
	session.delete()
	obj.status_code = 200 
	return obj 
