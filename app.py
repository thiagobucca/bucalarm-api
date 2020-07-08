from cgi import parse_qs
from wsgiref.simple_server import make_server
import subprocess
import urlparse
import os
import json


def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)
    if environ['REQUEST_METHOD'] == 'POST':
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        action_json = json.loads(request_body)
        print(action_json["action"])
        if action_json["action"] == "on":
            print("sim")
            #os.system("aplay /storage/siren.wav")
        else:
            print("nao")
            #os.system("killall -9 aplay")
        d = parse_qs(request_body)  # turns the qs to a dict
        return 'Alarm ON'
    else:  # GET
        d = parse_qs(environ['QUERY_STRING'])  # turns the qs to a dict
        option = ''.join('%s: %s' % (alarm) for alarm in d.iteritems())
        if option == "alarm: ['yes']":
            option = "sim"
            print("sim")
            #os.system("aplay /storage/siren.wav")
            #subprocess.call(["aplay", "/storage/siren.wav"])
        else:
            option = 'nao'
            print("nao")
            #os.system("killall -9 aplay")
        return option

        # return 'From GET: %s' % ''.join('%s: %s' % (k, v) for k, v in d.iteritems())
httpd = make_server('', 1337, app)
print "Serving on port 1337..."
httpd.serve_forever()
