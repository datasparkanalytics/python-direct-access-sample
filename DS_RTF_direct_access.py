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
  "location": {
    "locationType": "locationHierarchyLevel",
    "levelType": "subzone",
    "id": "OTSZ02"  },
  "aggregations": [
    {
      "metric": "unique_agents",
      "type": "hyperUnique"
    }  
  ]
}

# token variable is a valid access token (see Getting Started) 
queryResponse = requests.post("https://apistore.datasparkanalytics.com:8243/realtimefootfall/v2/query",
 data = json.dumps(queryBody),
 headers = {
   'Authorization': 'Bearer ' + token,
   'Content-Type': 'application/json'
 }
) 

FootfallResult = [ast.literal_eval(json.dumps(i)) for i in queryResponse.json()] 

print FootfallResult