from ask import alexa
from poolmon import poolmon
from credentials import APIKEY, APIURL, TEMPTYPE

poolmon.api_url = APIURL
poolmon.api_key = APIKEY
preferred_temp_type=TEMPTYPE

def lambda_handler(request_obj, context={}):
    return alexa.route_request(request_obj)

@alexa.default_handler()
def default_handler(request):
    return alexa.create_response(message="Default response", end_session=False)

@alexa.intent_handler('CurrentPoolTemp')
def current_pool_temp(request):
    response = poolmon.request('/temperature/pool')
    temp = int(round(response['measurements'][0]['temperature'][preferred_temp_type]))
    message = "The temperature in the pool is %s degrees" % temp
    
    return alexa.create_response(message=message, end_session=True)
