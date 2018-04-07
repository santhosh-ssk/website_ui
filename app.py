from flask import Flask,render_template,request,jsonify
import requests
import json
maps_api_key="AIzaSyDLd9n_vxzY4vt-wDC17Sx1TlVpANYCsY4"
app=Flask(__name__)

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/first_map")
def map():
	return render_template('first_map.html')

@app.route('/api/vi/list_shops/<lat>/<log>',methods=['POST'])
def list_shops(lat,log):
	print(lat,log,request.json)
	resp=requests.request("GET","https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+lat+","+log+"&radius=1000&type=restaurant&key="+maps_api_key)
	locations=json.loads((resp.content).decode())['results']
	respons=list()
	
	for location in locations:
		result={
			'lat':location['geometry']['location']['lat'],
			'lng':location['geometry']['location']['lng'],
			'name':location['name'],	
			'place_id':location['place_id'],
			'address':location['vicinity'],
			}
		if 'photos' in location.keys():
			result['photos']=[x['photo_reference'] for x in location['photos']]
		else:
			result['photos']=[]
		if 'rating' in location.keys():
			result['rating']=location['rating']
		else:
			result['rating']='Not Available'
		respons.append(result)
	return jsonify(respons)	
	
if __name__=="__main__":
	app.run(debug=True)