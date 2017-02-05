import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '13cdd7a1665f4928bfccc726cd521700',
}

params = urllib.urlencode({
    # Request parameters
    'language': 'unk',
    'detectOrientation ': 'true',
})

data = open('happy-person.jpg', 'rb').read()
conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
conn.request("POST", "/emotion/v1.0/recognize?%s" % params, data, headers)
response = conn.getresponse()
data = response.read()
print(data)
conn.close()
