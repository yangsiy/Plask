#!flask/bin/python

from app import app

server_port = 5000
server_ip = '0.0.0.0'

app.run(host = server_ip, port = server_port, debug = True)