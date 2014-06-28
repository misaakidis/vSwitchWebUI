from flask import Flask, jsonify
from flask.ext.httpauth import HTTPDigestAuth
from test import uname

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bad key'
auth = HTTPDigestAuth()

if not app.debug:
    import logging
    file_handler = logging.FileHandler('./vSwitch.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

users = {
    "admin": "admin",
}

@auth.error_handler
def auth_error():
    return "Authentication Required"

#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

@app.route('/logout/')
@auth.login_required
def logout():
    return "Hello, %s!" % auth.username()

@app.route('/api/v1.0/')
@auth.login_required
def getApiRoot():
	return "API root, access granted to %s" % auth.username()

@app.route('/api/v1.0/uname/', methods=['GET'])
@auth.login_required
def getUname():
	return jsonify(uname=uname())


if __name__ == '__main__':
    app.run()