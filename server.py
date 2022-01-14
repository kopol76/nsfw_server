#!/usr/bin/env python

#import urlparse
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from classify_nsfw import get_score_net, load_model
import requests

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        message = ""

        self._set_headers()
        url_img = self.path[1:]

        # load image
        try:
            img = None
            r = requests.get(url_img)
            if r.status_code == 200:
                img = r.content

            if img != None:
                message = get_score_net(image_data = img, caffe_net = nsfw_net, caffe_transformer = caffe_transformer)
            else:
                message = "exception: error load image "

        except Exception as e:
            logging.exception("exception: " + str(e))
            message = "exception: " + str(e)

        self.wfile.write(str(message).encode("utf-8"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("".encode("utf-8"))


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


nsfw_net, caffe_transformer = load_model()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        print(int(argv[1]))
        run(port=int(argv[1]))
    else:
        run()
