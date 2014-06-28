from flask import Flask
from flask.ext.httpauth import HTTPDigestAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bad key'
auth = HTTPDigestAuth()

users = {
    "admin": "admin",
}

@auth.error_handler
def auth_error():
    return "Access Denied"

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

if __name__ == '__main__':
    app.run()