from flask import Flask
from login import robot
app = Flask(__name__)

robot = robot()

@app.route('/')
def root():
    return "Teste"

@app.route('/loginazul', methods=['POST'])
def login():
    robot.abrir_navegador()


if __name__ == '__main__':
    app.run()