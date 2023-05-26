from flask import Flask
from login import login_azul
app = Flask(__name__)


@app.route('/')
def root():
    return "Get vai tomar no cu"

@app.route('/loginazul', methods=['POST'])
def login():
    login_azul()


if __name__ == '__main__':
    app.run()