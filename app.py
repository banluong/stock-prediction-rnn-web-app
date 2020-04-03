from flask import Flask
from flask import render_template
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home(name=None):
    return render_template("home.html", name=name)

@app.route('/about/')
def about(name=None):
    return render_template("about.html", name=name)

def full_plot(y_inv, ytest_inv, ypred_inv):
    plt.plot(np.arange(0, len(y_inv)), y_inv, 'g', label="history")
    plt.plot(np.arange(len(y_inv), len(y_inv) + len(ytest_inv)), ypred_inv, 'r', label="prediction")
    plt.ylabel('Value')
    plt.xlabel('Time Step')
    plt.legend()
    plt.show()

    return plt

if __name__ == "__main__":
    app.run(debug=True)
