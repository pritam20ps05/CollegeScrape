from flask import Flask, render_template, Response
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

with app.app_context():
    from api.api_routes import api
    app.register_blueprint(api)

# Page routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/counsellingsearch/')
def counselSearch():
    return render_template('counsellingsearch.html')

@app.route('/collegesearch/')
def collegeSearch():
    return render_template('underconstruction.html')

@app.errorhandler(404)
def not_found(e):
    return  Response(render_template('404.html'), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)