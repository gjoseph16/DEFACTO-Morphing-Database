#!/usr/bin/python

import sys
import base64
import json
import requests

if ( len(sys.argv) != 2 ):
    print('Usage: python request_analyse.py "documentImage" ')
    sys.exit(0)
  
img_base64 = base64.b64encode(open(sys.argv[1], "rb").read())

url = 'https://ananas.ipk.fraunhofer.de:5050/component_ipk/frvt'

data = {'clientQueryId': 'OvGU anfrage', 'imageData': { 'documentImage': img_base64, 'additionalParameter': 'jpg' } }
headers = {'Content-type': 'application/json'}
r = requests.post(url, data=json.dumps(data), headers=headers, verify='ananas.ipk.fraunhofer.de.crt')

print r, r.json() 
print 'score: ' + str(r.json()['resultData']['score']) + '; evaluation: ' + r.json()['resultData']['evaluation']