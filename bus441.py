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

    orig_coord = str(orig_lat) + "," +str(orig_lng)
    dest_coord = str(dest_lat)+"," +str(dest_lng)
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+str(orig_coord)+"&destinations="+str(dest_coord)+"&mode=driving&key=AIzaSyBJz8a7fpvQ0-DPQa7aQvamU4wOlC6EKn0"
    result= simplejson.load(urllib.urlopen(url))
    print result
    driving_time = result['rows'][0]['elements'][0]['duration']['value']
    print driving_time
