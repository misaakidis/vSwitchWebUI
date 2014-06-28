from flask import Flask, jsonify, abort, render_template, send_from_directory
from flask.ext.httpauth import HTTPDigestAuth
from test import uname

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bad key'
auth = HTTPDigestAuth()


# Logging to file vSwitch.log
if not app.debug:
    import logging
    file_handler = logging.FileHandler('./vSwitch.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


# Custom flask handlers
@auth.error_handler
def auth_error():
    return "Authentication Required"

#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404



# Custom authentication
users = {
    "admin": "admin",
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


# Adding routes for the Web UI
@app.route('/')
@auth.login_required
def root():
    return render_template('index.html', error=None)

@app.route('/index.html')
@auth.login_required
def index():
    return render_template('index.html', error=None)

@app.route('/machines.html')
@auth.login_required
def machines():
    return render_template('machines.html', error=None)

@app.route('/logout')
@auth.login_required
def logout():
    abort(401)

# Adding routes for the API calls
@app.route('/api/v1.0/', methods=['GET'])
@auth.login_required
def getApiRoot():
	return "API root, access granted to %s" % auth.username()

@app.route('/api/v1.0/uname/', methods=['GET'])
@auth.login_required
def getUname():
	return jsonify(uname=uname())


# Rules for static files serving
@app.route('/js/<path:filename>')
def send_js(filename):
    return send_from_directory('static/js/', filename)

@app.route('/css/<path:filename>')
def send_css(filename):
    return send_from_directory('static/css/', filename)

@app.route('/img/<path:filename>')
def send_img(filename):
    return send_from_directory('static/img/', filename)

@app.route('/font/<path:filename>')
def send_font(filename):
    return send_from_directory('static/font/', filename)


# Do run the flask app
if __name__ == '__main__':
    app.run()