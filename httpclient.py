#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

from queue import Empty
import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
from urllib.parse import urlparse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        # Parse url
        parsed_url = urlparse(url)
        # Get port and host
        port = parsed_url.port
        host = parsed_url.hostname
        # Get path and check whether path exists
        my_path = parsed_url.path
        if my_path:
            my_path = parsed_url.path
        else:
            my_path = '/'
        # Check if port exists, if not, set port to 80
        if port == None:
            port = 80
        self.connect(host, port)

        # The GET request
        get_request = "GET "+my_path+" HTTP/1.1\r\nHost: "+host+"\r\nUser-Agent:Linux\r\nConnection: close\r\n\r\n"

        # Send the request
        self.sendall(get_request)
        # Get data from the request that was sent
        data_received = self.recvall(self.socket)
        # Parse through data and get code
        headers = data_received.split('\r\n')
        code_header = headers[0]
        code = int(code_header.split()[1])
        # Parse through data and get body
        body = data_received.split('\r\n\r\n')[1]

        # Close connection
        self.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        # Parse url
        parsed_url = urlparse(url)
        # Get port and host
        port = parsed_url.port
        host = parsed_url.hostname
        # Get path and check whether path exists
        my_path = parsed_url.path
        if my_path:
            my_path = parsed_url.path
        else:
            my_path = '/'
        # Check if port exists, if not, set port to 80
        if port == None:
            port = 80
        self.connect(host, port)

        # Check if there were any arguments, if not, POST without arguments
        if args == None:
            post_request = "POST "+my_path+" HTTP/1.1\r\nHost: "+host+"Content-Type: application/x-www-form-urlencoded\r\nUser-Agent:Linux\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
        # If yes, get arguments and argument length and do POST
        else:
            args = urllib.parse.urlencode(args)
            length_of_args = str(len(args))
            post_request = "POST "+my_path+" HTTP/1.1\r\nHost: "+host+"Content-Type: application/x-www-form-urlencoded\r\nUser-Agent:Linux\r\nContent-Length: "+length_of_args+"\r\nConnection: close\r\n\r\n"+args+"\r\n\r\n"

        # Send the request
        self.sendall(post_request)
        # Get data from the request that was sent
        data_received = self.recvall(self.socket)
        # Parse through data and get code
        headers = data_received.split('\r\n')
        code_header = headers[0]
        code = int(code_header.split()[1])
        # Parse through data and get body
        body = data_received.split('\r\n\r\n')[1]

        # Close connection
        self.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
