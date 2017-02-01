import requests, json, simplejson, urllib

data = {
  'ticketerservice': '441',
  'service': '441',
  'operatorRef': 'ABSU',
  'direction': 'inbound',
  'timestamp': 'Tue Jan 31 2017 14:25:26 GMT+0000 (GMT Standard Time)'
}

data = requests.post('http://absu.coachparks.com/widget/GetLiveBuses', data=data)

jdata = json.loads(data.content)
for bus in jdata['Buses']:

    orig_lat =  51.426634
    orig_lng =  -0.572648
    dest_lat = float(bus['Latitude'])
    dest_lng = float(bus['Longitude'])

    orig_coord = orig_lat, orig_lng
    dest_coord = dest_lat, dest_lng
    print orig_coord
    print dest_coord
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
    result= simplejson.load(urllib.urlopen(url))
    print result
    driving_time = result['rows'][0]['elements'][0]['duration']['value']
