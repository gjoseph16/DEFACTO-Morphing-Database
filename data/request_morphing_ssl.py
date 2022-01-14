#!/usr/bin/python

import base64
import json
import requests
import os.path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--image1', required=True, action='store', dest='image1', help='source image')	
parser.add_argument('--image2', required=True, action='store', dest='image2', help='target image')	
parser.add_argument('--method', action='store', dest='method', help='combined(default) / splicing / complete')	
parser.add_argument('--alpha', action='store', dest='alpha', help='blending parameter, real value between 0.0 and 1.0')
parser.add_argument('--blendgeometry', action='store_true', dest='blendgeometry', help='apply alpha to geometry blending (default avg. geometry)')
parser.add_argument('--alignment', action='store_true', dest='alignment', help='pre-processing: zero-roll rotation + ICAO compliant cut')
parser.add_argument('--ICAO', action='store_true', dest='ICAO', help='post-processing: ICAO compliant cut')
parser.add_argument('--passportscale', action='store_true', dest='passportscale', help='post-processing: passport scaling (413x531 pixels)')
parser.add_argument('--landmarks1', action='store', dest='landmarks1', help='list of 68 facial landmarks for the source image')	
parser.add_argument('--landmarks2', action='store', dest='landmarks2', help='list of 68 facial landmarks for the target image')	
args = parser.parse_args()
	
img1_base64 = base64.b64encode(open(args.image1, "rb").read())
img2_base64 = base64.b64encode(open(args.image2, "rb").read())	

if args.method is not None:


    method = args.method
else:
    method = 'combined'
	       
if args.alpha is not None:
    alpha = args.alpha
else:	
    alpha = '0.5' 

data = {'image1': img1_base64, 'image2': img2_base64, 'method': method, 'alpha': alpha}	

if args.alignment is True:
    data['alignment'] = '1'
else:
    data['alignment'] = '0'
if args.ICAO is True:
    data['ICAO'] = '1'
else:
    data['ICAO'] = '0'	
if args.passportscale is True:
    data['passport'] = '1'
else:
    data['passport'] = '0'
if args.blendgeometry is True:
    data['avggeometry'] = '0'
else:
    data['avggeometry'] = '1'
if args.landmarks1 is not None:
    data['landmarks1'] = open(args.landmarks1, "rt").read()
if args.landmarks2 is not None:
    data['landmarks2'] = open(args.landmarks2, "rt").read()
	
url = "https://ananas.cs.uni-magdeburg.de/api/morphing"
headers = {'Content-type': 'application/json'}
r = requests.post(url, data=json.dumps(data), headers=headers)

print r, len(r.json())

if r.status_code == 200:
    name = list()
    name.append(os.path.basename(args.image1).split('.')[0])
    name.append(os.path.basename(args.image2).split('.')[0])
    ext = '_' + method + '_alpha' + alpha + '.png'

    for index in range(len(r.json())):
        morph = name[index] + '_' + name[1-index] + ext
        f = open(morph,"wb")
        f.write( base64.b64decode(r.json()['morph'+str(index+1)]) )
        f.close()
        print 'saved as: ' + morph
elif r.status_code == 400:
    print r.json()['Error']



