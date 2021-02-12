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

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse,urlencode


def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port_path(self,url):
        host = urlparse(url).hostname
        port = urlparse(url).port
        path = urlparse(url).path
        if port == None:
            port = 80
            return host,port,path
            
        elif path == None or '':
            path = '/'
            return host,port,path
        elif host == None:
            host = '127.0.0.1'
            return host,port,path

        else:
            return host,port,path


        
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        try:
            get_data = data.split(' ')
            code = int(get_data[1])
            return code
        except:
            raise Exception('no data found')
        

            
            
            

        


    def get_headers(self,data):
        #seperate data in to lines:
        header_data = data.split('\r\n')
        header_info = []
        start = 1
        while not header_data[start] == '' and start <= (len(header_data)+1):
            header_info.append(header_data[start])
            start += 1

        return header_info

    def get_body(self, data):
        if data:
            try:
                body_data = data.split('\r\n\r\n')[1]

            
            except:
                raise Exception('No content found')
        return body_data
    
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


        #https://github.com/Kay7777/CMPUT404-assignment-web-client/blob/master/httpclient.py
        #from kaysong:qsong
        

    

    def GET(self, url, args=None):
        
        host,port,path = self.get_host_port_path(url)
        self.connect(host,port)
        self.sendall("GET /" + path + " HTTP/1.1\r\n")
        self.sendall("Host: "+ host + "\r\n")
        self.sendall("User-Agent: Python-urllib\r\n")
        self.sendall("Accept: */*\r\n")
        self.sendall("Connection: close\r\n\r\n")
        response = self.recvall(self.socket)
        self.socket.close()
        code = self.get_code(response)
        print(code)
        body = self.get_body(response)

        return HTTPResponse(code,body)


        

        

        



    def POST(self, url, args=None):
        code = 500
        body = ""
        host,port,path = self.get_host_port_path(url)
        if args:
            it = urlencode(args)
            self.connect(host,port)
            self.sendall("POST /{} HTTP/1.1\r\n".format(path)+"Host: {}\r\n".format(host)+"User-Agent: Python-urllib\r\n"+"Accept: */*\r\n"+"Content-Type: application/x-www-form-urlencoded\r\n"+"Content-Length: {}\r\n".format(len(it))+"Connection: close\r\n\r\n{}".format(it))
            response = self.recvall(self.socket)
            self.socket.close()

        else:
            self.connect(host,port)
            self.sendall("POST /{} HTTP/1.1\r\n".format(path)+"Host: {}\r\n".format(host)+"User-Agent: Python-urllib\r\n"+"Accept: */*\r\n"+"Content-Type: application/x-www-form-urlencoded\r\n"+"Content-Length: 0\r\n"+"Connection: close\r\n\r\n")
            response = self.recvall(self.socket)
            self.socket.close()
        
        code = self.get_code(response)
        body = self.get_body(response)

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
