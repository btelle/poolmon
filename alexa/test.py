from __future__ import print_function
from lambda_function import lambda_handler
import json

sample_json = """
{
    "session": {
    "sessionId": "SessionId.d461672c-2997-4d9d-9a8c-a67834acb9aa",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.a306b3a3-3331-43c1-87bd-87d29d16fac8"
    },
    "user": {
      "userId": "amzn1.account.AGBATYSC32Y2QVDQKOWJUUJNEYFA"
    },
    "new": true
    },
    "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.b22db637-b8f9-43c0-ae0c-1a9b35a02610",
    "timestamp": 1447911387582,
    "intent": {
      "name": "PastPoolTemp",
      "slots": {
        "Date":
          {
            "name": "Date", 
            "value": "2016-07-21"
          }
      }
    }
  }
}
"""

request_obj = json.loads(sample_json)
response = lambda_handler(request_obj)
print(json.dumps(response, indent=2))
