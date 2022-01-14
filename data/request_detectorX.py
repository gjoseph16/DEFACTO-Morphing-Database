#!/usr/bin/python

import sys
import base64
import json
import requests

if ( len(sys.argv) < 3 ):
    print "Usage: python request_detectorX.py <1|2|3|4|5|6|7|8|9> <DocumentImage> [LiveImage]"
    print "    1 - Keypoints, OVGU"
    print "    2 - GoogLeNet-based, HHI"
    print "    3 - FaceNet-based, IPK"
    print "    4 - Benford, OVGU"
    print "    5 - De-morphing, OVGU"
    print "    6 - Degradation, OVGU"
    print "    7 - VGG19-based (naive), HHI"
    print "    8 - VGG19-based (multi-class), HHI"
    print "    9 - High-Dim LBP, IPK"
    print "    10 - VGG19-based (high-freq), HHI"
    print "    11 - Keypoints v2, OVGU"	
    print "    12 - De-morphing v2, OVGU"	
    print "    13 - Degradation v2, OVGU"	
    sys.exit(0)

docImg_base64 = base64.b64encode(open(sys.argv[2], "rb").read())	

url = "http://141.44.30.147:5001/api/anomalydetector" + sys.argv[1] + "/analyse"	
headers = {'Content-type': 'application/json'}
data = {'clientQueryId': 'OvGU test request', 'imageData': {'documentImage': docImg_base64}}
if ( sys.argv[1] == '3' ):
    data['imageData']['additionalParameter'] = 'jpg'
if ( sys.argv[1] == '5' ):
    liveImg_base64 = base64.b64encode(open(sys.argv[3], "rb").read())
    data['imageData']['liveImage'] = liveImg_base64

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
	




