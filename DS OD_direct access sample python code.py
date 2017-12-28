from datetime 
import datetime 
import json, ast 
import requests 
import base64 

consumerKey = "CONSUMER KEY" 
consumerSecret = "CONSUMER SECRET KEY" 

keySecret = (consumerKey + ":" + consumerSecret).encode('utf-8')
consumerKeySecretB64 = base64.b64encode(keySecret).decode('utf-8') 
tokenResponse = requests.post("https://apistore.datasparkanalytics.com/token",
 data = { 'grant_type': 'client_credentials' },
 headers = { 'Authorization': 'Basic ' + consumerKeySecretB64 }) 
token = tokenResponse.json()['access_token'] 

queryBody = {
	"date": "2017-12-24",
	"timeSeriesReference": "origin",
	"location": {
		"locationType": "locationHierarchyLevel",
		"levelType": "origin_subzone",
		"id": "CHSZ03"
	},
	"queryGranularity": {
		"type": "period",
		"period": "P1D"
	},
	"aggregations": [{
		"metric": "unique_agents",
		"type": "hyperUnique",
		"describedAs": "unique_people"
	}],
	"dimensionFacets": ["destination_subzone", "dominant_mode"]
}

# token variable is a valid access token (see Getting Started) 
queryResponse = requests.post("https://apistore.datasparkanalytics.com:8243/odmatrix/v3/query",
 data = json.dumps(queryBody),
 headers = {
   'Authorization': 'Bearer ' + token,
   'Content-Type': 'application/json'
 }
) 

ODesult = [ast.literal_eval(json.dumps(i)) for i in queryResponse.json()] 

print ODResult