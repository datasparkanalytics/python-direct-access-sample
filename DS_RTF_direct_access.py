from datetime import datetime 
import json, ast 
import requests 
import base64 

consumerKey = "CONSUMER KEY" 
consumerSecret = "SECRET KEY" 

keySecret = (consumerKey + ":" + consumerSecret).encode('utf-8')
consumerKeySecretB64 = base64.b64encode(keySecret).decode('utf-8') 
tokenResponse = requests.post("https://apistore.datasparkanalytics.com/token",
 data = { 'grant_type': 'client_credentials' },
 headers = { 'Authorization': 'Basic ' + consumerKeySecretB64 }) 
token = tokenResponse.json()['access_token'] 

queryBody = {
	"date": "2017-12-24",
	"location": {
		"locationType": "locationHierarchyLevel",
		"levelType": "staypoint_subzone",
		"id": "SRSZ03"
	},
	"queryGranularity": {
		"type": "period",
		"period": "P1D"
	},
	"aggregations": [{
		"metric": "total_stays",
		"type": "longSum",
		"describedAs": "total_stay"
	}, {
		"metric": "sum_stay_duration",
		"type": "longSum",
		"describedAs": "total_stay_duration"
	}],
	"filter": {
		"type": "selector",
		"dimension": "agent_gender",
		"value": "M"
	},
	"dimensionFacets": ["agent_home_planningregion"]
}

# token variable is a valid access token (see Getting Started) 
queryResponse = requests.post("https://apistore.datasparkanalytics.com:8243/staypoint/v2/query",
 data = json.dumps(queryBody),
 headers = {
   'Authorization': 'Bearer ' + token,
   'Content-Type': 'application/json'
 }
) 

StaypointResult = [ast.literal_eval(json.dumps(i)) for i in queryResponse.json()] 

print StaypointResult