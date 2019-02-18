from flask import Flask

import urllib.request, urllib.parse, urllib.error

import twurl

import json

import ssl

import folium


# https://apps.twitter.com/

# Create App and get the four strings, put them in hidden.py



TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'



# Ignore SSL certificate errors

ctx = ssl.create_default_context()

ctx.check_hostname = False

ctx.verify_mode = ssl.CERT_NONE


from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='MovieMapApp', timeout = None)

from geopy.extra.rate_limiter import RateLimiter

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

map = folium.Map(location=[48.314775, 25.082925],
zoom_start=5)
fg_tf = folium.FeatureGroup(name="Twitter_friends_Layer")



while True:

    print('')

    acct = input('Enter Twitter Account:')

    if (len(acct) < 1): break

    url = twurl.augment(TWITTER_URL,

                        {'screen_name': acct, 'count': '5'})

    # print('Retrieving', url)

    connection = urllib.request.urlopen(url, context=ctx)

    data = connection.read().decode()



    js = json.loads(data)

    # print(json.dumps(js, indent=2))



    headers = dict(connection.getheaders())

    # print('Remaining', headers['x-rate-limit-remaining'])



    for u in js['users']:

        nick = u['screen_name']

        if "location" not in u:

            print('   * No location found')

            continue
        try:
            point = u["location"][:50]
            location = geolocator.geocode(point)
            fg_tf.add_child(folium.Marker(location=[location.latitude, location.longitude],
                                          popup= nick,
                                          icon=folium.Icon()))

        except:

            print('   * No location found')
        map.add_child(fg_tf)
        map.save('Twitter_Map.html')
        app = Flask(__name__)
        from flask import request
        @app.route('/addRegion', methods=['POST'])
        def addRegion():
            return request.form['Task2\Twitter_Map.html']
        app.run(debug = True)