from datetime import datetime 
import json, ast 
import requests 
import base64 

consumerKey = "CONSUMER KEY" 
consumerSecret = "CONSUMER SECRET" 

keySecret = (consumerKey + ":" + consumerSecret).encode('utf-8')
consumerKeySecretB64 = base64.b64encode(keySecret).decode('utf-8') 
tokenResponse = requests.post("https://apistore.datasparkanalytics.com/token",
 data = { 'grant_type': 'client_credentials' },
 headers = { 'Authorization': 'Basic ' + consumerKeySecretB64 }) 
token = tokenResponse.json()['access_token'] 

queryBody = {
 "date": "2017-11-02",
 "location": {
   "locationType": "locationHierarchyLevel",
   "levelType": "discrete_visit_subzone",
   "id": "RCSZ05"
 },
 "queryGranularity": {
   "type": "period",
   "period": "PT1H"
 },
 "aggregations": [
   {
     "metric": "unique_agents",
     "type": "hyperUnique",
     "describedAs": "footfall"
   }
 ],
 	"filter": {
		"type": "bound",
		"dimension": "agent_year_of_birth",
		"lower": "1992",
		"upper": "1998",
		"ordering": "numeric"
	},
	"dimensionFacets": ["agent_gender"]
} 

# token variable is a valid access token (see Getting Started) 
queryResponse = requests.post("https://apistore.datasparkanalytics.com:8243/discretevisit/v2/query",
 data = json.dumps(queryBody),
 headers = {
   'Authorization': 'Bearer ' + token,
   'Content-Type': 'application/json'
 }
) 

footfallResult = [ast.literal_eval(json.dumps(i)) for i in queryResponse.json()] 

print footfallResult