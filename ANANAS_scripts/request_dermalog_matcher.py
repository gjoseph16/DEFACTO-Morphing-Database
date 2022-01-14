# Dermalog Facerecognition Webservice:
# https://40035-face.dc.dermalog.com/api/dermalog/facerecognition
#
# Der Service wird ueber HTTP POST mit JSON Requests (Content-Type: application/json) angesprochen.
# Request Format:
# {
# "image1": "$Base64EncodedImage....",
# "image2": "$Base64EncodedImage....",
# "minFaceSize": $INTEGER
# }
# Response Format (Status 200):
# {
# "image1Quality": $INTEGER [0-99],
# "image2Quality": $INTEGER [0-99],
# "matchingScore": $FLOAT [0-99]
# }
# Response Format (Status 400, 500):
# {
# "ErrorMessage": "$Message"
# }
#
# Die Base64 kodierten Bilder koennen im JPG oder PNG Format vorliegen. 
#
# Der "minFaceSize" Parameter bestimmt die Groesse in Pixeln des kleinsten zu findenden 
# Gesichtes und beeinflusst massgeblich die Verarbeitungszeit. 
# Je kleiner der Parameter, desto laenger die Verarbeitungszeit der Anfrage. 
# Bei zu grossen Werten werden entsprechend keine Gesichter mehr gefunden zum matchen. 
# "minFaceSize" kann nicht kleiner sein als 0.15*[groesste Dimension der Eingabebilder].
#
import sys
import base64
import json
import requests


if ( len(sys.argv) != 3 ):
    print 'Usage: python request_dermalog_matcher.py "image1" "image2"'
    sys.exit(0)

img1_base64 = base64.b64encode(open(sys.argv[1], "rb").read())	
img2_base64 = base64.b64encode(open(sys.argv[2], "rb").read())
minFaceSize = 200
	
url = "https://40035-face.dc.dermalog.com/api/dermalog/facerecognition"
data = {'image1': img1_base64, 'image2': img2_base64, 'minFaceSize': minFaceSize}
headers = {'Content-type': 'application/json'}
r = requests.post(url, data=json.dumps(data), headers=headers)

print r.json()
print 'score: ' + str(r.json()['matchingScore'])



