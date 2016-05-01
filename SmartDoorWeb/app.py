from flask import Flask, render_template, session, redirect, url_for, escape, request
from extensions import mysql
import apis
import controllers
import hashlib

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = '/static/images'

# Initialize MySQL database connector
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'local_db'
mysql.init_app(app)


# Register the controllers
app.register_blueprint(controllers.userapi)
app.register_blueprint(controllers.friendsapi)
app.register_blueprint(controllers.loginapi)
app.register_blueprint(controllers.logoutapi)
app.register_blueprint(controllers.picturesapi)



@app.route('/')
def index_route():
	return render_template('index.html')

#Set the secret key
app.secret_key = '&??Jpl??4??z????o???#?'

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='0.0.0.0', port=3000, debug=True)
