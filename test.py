import flask
import requests
import json
import os
import googlemaps
#from geolocation.main import GoogleMaps
#from geolocation.distance_matrix.client import DistanceMatrixApiClient
#from googlemaps import exceptions

app = flask.Flask(__name__)

url = 'https://developers.zomato.com/api/v2.1/'
apikey='&apikey=c5062d18e16b9bb9d857391bb32bb52f'

@app.route('/webhook', methods=['POST'])
def webhook():
    req = flask.request.get_json()
    res = processRequest(req)
    print("response :")
    res=json.dumps(res, indent=4)
    r = flask.make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print("result r")
    print(r)
    return r
def processRequest(req):
    result = req.get("result")
    parameters = result.get("parameters")
    u_loc = str(parameters.get("landmark"))
    u_type = str(parameters.get("type"))
    u_cuisine = str(parameters.get("cuisines"))
    u_Collections = str(parameters.get("Collections"))
    #url to fetch the details of the client location
    location_url=url+'locations?query='+u_loc+apikey
    json_data = requests.get(location_url).json()
    
    entity_id=json_data.get('location_suggestions')[0].get('entity_id')
    entity_type=json_data.get('location_suggestions')[0].get('entity_type')
    city_id=json_data.get('location_suggestions')[0].get('city_id')
    lat=json_data.get('location_suggestions')[0].get('latitude')
    longi=json_data.get('location_suggestions')[0].get('longitude')
    search_url=url+'search?radius=3000&sort=cost&count=10&entity_id='+str(entity_id)+'&entity_type='+str(entity_type)+'&lat='+str(lat)+'&lon='+str(longi)+'&cuisines=7'+apikey
    json_data=requests.get(search_url).json()
    print(search_url)
    #print(json.dumps(json_data, indent = 4))
    #print(json.dumps(json_data,indent=4))
    '''namedict=[]
    urldict=[]
    for x in range(len(json_data.get('restaurants'))):
        namedict.append(json_data.get('restaurants')[x].get('restaurant').get('name'))
        urldict.append(json_data.get('restaurants')[x].get('restaurant').get('order_url'))'''
    
    #speech=str(namedict)+str(urldict)
    speech=str(json_data.get('restaurants')[0].get('restaurant').get('name'))+str(json_data.get('restaurants')[0].get('restaurant').get('order_url'))
    print(speech)
    print(type(speech))

    return {
        "speech": speech,
        "displayText": speech,
        "source":"Zomato top restaurants"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT',5000))
    print("Starting app %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
