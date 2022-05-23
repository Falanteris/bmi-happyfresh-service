import os,json
from dotenv import load_dotenv
from gevent.pywsgi import WSGIServer
from endpoints.calculator import app as calculator_endpoint
from flask import Flask

load_dotenv()

app = Flask(__name__)

app.register_blueprint(calculator_endpoint)


HOST = os.getenv("SERVICE_HOST")
PORT = int(os.getenv("SERVICE_PORT"))

if __name__ == "__main__":
    http_server = WSGIServer((HOST,PORT), app)
    print("[+] Running server on {}:{}".format(HOST,PORT))
    http_server.serve_forever()
