import json
from sys import stderr
from flask import Flask, jsonify, abort, make_response, render_template, send_from_directory, url_for
from flask.ext.httpauth import HTTPDigestAuth
from fabfile import FabricSupport

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bad key'
auth = HTTPDigestAuth()
hosts = ['root@192.168.88.251']
fab = FabricSupport()


# Logging to file vSwitch.log
if not app.debug:
    import logging
    file_handler = logging.FileHandler('./vSwitch.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    # Uncomment next line to enable debugging output
    #logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


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

app.jinja_env.globals.update(getUsername=auth.username)

def getBridgesList():
    return fab.execute("ovs_list_bridges", hosts).values()[0].split("\r\n")


# Adding routes for the Web UI
@app.route('/')
@auth.login_required
def root():
    return render_template('index.html', error=None)

@app.route('/index.html')
@auth.login_required
def index():
    return render_template('index.html', error=None)

@app.route('/editmachine.html')
@auth.login_required
def editMachine():
    list = getBridgesList()[0].split("\r\n")
    return render_template('editmachine.html', bridges=getBridgesList())

@app.route('/machines.html')
@auth.login_required
def machines():
    return render_template('machines.html', error=None)

@app.route('/bridges.html')
@auth.login_required
def bridges():
    return render_template('bridges.html', bridges=getBridgesList().items())

@app.route('/logout/')
@auth.login_required
def logout():
    resp = make_response(render_template('logout.html'))
    resp.set_cookie('session', expires=0)
    return resp


# Adding routes for the API calls
@app.route('/api/v1.0/', methods=['GET'])
@auth.login_required
def getApiRoot():
	return "API root, access granted to %s" % auth.username()

@app.route('/api/v1.0/uname/', methods=['GET'])
@auth.login_required
def getUname():
	return jsonify(uname=fab.execute("host_type", hosts))

@app.route('/api/v1.0/bridge/', methods=['GET'])
@auth.login_required
def getBridges():
    return json.dumps(getBridgesList())

@app.route('/api/v1.0/bridge/<bridgeName>/ports', methods=['GET'])
@auth.login_required
def getBridgePorts(bridgeName):
    ovs_conf = fab.execute("ovs_show_cfg", hosts).values()
    bridge_list = ovs_conf[0].replace("\r\n","").split("Bridge");
    if any(bridgeName in bridge for bridge in bridge_list):
        bridge_conf = bridge
    return json.dumps(bridge_list)


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