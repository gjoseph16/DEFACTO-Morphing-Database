#!/usr/bin/python

import sys
import base64
import json
import requests

if ( len(sys.argv) != 4 ):
    print "Usage: python request_matcherX.py <1|2|3|4> <FaceImage1> <FaceImage2>"
    print "    1 - Luxand FaceSDK"
    print "    2 - Fraunhofer IPK, Face Matcher based on DCNN, probably OpenFace"
    print "    3 - Dermalog Face Recognition"
    print "    4 - Face Matching based on dlib's face recognition tool"
    sys.exit(0)

img1_base64 = base64.b64encode(open(sys.argv[2], "rb").read())
img2_base64 = base64.b64encode(open(sys.argv[3], "rb").read())	

url = "http://141.44.30.147:5001/api/matcher" + sys.argv[1]	
headers = {'Content-type': 'application/json'}
data = {'clientQueryId': 'Test request', 
        'imageData': {'documentImage': img1_base64, 'liveImage': img2_base64}}
if ( sys.argv[1] == '2' ):
    data['imageData']['additionalParameter'] = 'jpg'
if ( sys.argv[1] == '3' ):
    data['imageData']['minFaceSize'] = 200

try:
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print r
except requests.exceptions.RequestException as e:
    print e

if r.status_code == 200:
    print r.json()
    print 'score:', r.json()['resultData']['score'], '; evaluation:', r.json()['resultData']['evaluation']
elif r.status_code == 400:
    print 'Error:', r.json()['message']
	





