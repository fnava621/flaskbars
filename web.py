import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flaskext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
#app.config['SQLALCHEMY_ECHO'] = !os.environ.get('PROD')
app.config['SQLALCHEMY_ECHO'] = True
#app.debug = !os.environ.get('PROD')
app.debug = True
db = SQLAlchemy(app)

class Bar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, name):
        self.name = name

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/addBar", methods=['POST'])
def addBar():
    bar = Bar(request.form['name'])
    db.session.add(bar)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/listBars")
def listBars():
    bars = Bar.query.all()
    return jsonify(bars)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)