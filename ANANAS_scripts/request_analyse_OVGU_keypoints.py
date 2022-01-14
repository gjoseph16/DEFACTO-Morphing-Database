#!/usr/bin/python

import sys
import base64
import json
import requests

if ( len(sys.argv) != 2 ):
    print 'Usage: python request_analyse.py "image"'
    sys.exit(0)

img_base64 = base64.b64encode(open(sys.argv[1], "rb").read())	
	
url = "https://ananas.cs.uni-magdeburg.de/api/anomalydetector/keypoints/analyse"
data = {'clientQueryId': 'OvGU analyse query', 'imageData': {'documentImage': img_base64}}
headers = {'Content-type': 'application/json'}
r = requests.post(url, data=json.dumps(data), headers=headers)

print r, r.json() 
print 'score: ' + str(r.json()['resultData']['score']) + '; evaluation: ' + r.json()['resultData']['evaluation']