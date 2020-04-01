from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home(name=None):
    return render_template("home.html", name=name)

@app.route('/about/')
def about(name=None):
    return render_template("about.html", name=name)

if __name__ == "__main__":
    app.run(debug=True)
