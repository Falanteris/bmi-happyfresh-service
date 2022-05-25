import os,json
from dotenv import load_dotenv
from gevent.pywsgi import WSGIServer
from endpoints.calculator import app as calculator_endpoint
from flask import Flask
from prometheus_client import start_http_server

load_dotenv()

app = Flask(__name__)

app.register_blueprint(calculator_endpoint)


HOST = os.getenv("SERVICE_HOST")
PORT = int(os.getenv("SERVICE_PORT"))
MEMCACHE_HOST = os.getenv("MEMCACHE_HOST")
MEMCACHE_PORT = int(os.getenv("MEMCACHE_PORT"))

if __name__ == "__main__":
    http_server = WSGIServer((HOST,PORT), app)
    print("[+] Running server on {}:{}".format(HOST,PORT))
    start_http_server(8070)
    http_server.serve_forever()
