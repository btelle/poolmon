from ask import alexa
from poolmon import poolmon
from credentials import APIKEY, APIURL, TEMPTYPE
from responses import *

poolmon.api_url = APIURL
poolmon.api_key = APIKEY
preferred_temp_type=TEMPTYPE

def lambda_handler(request_obj, context={}):
    return alexa.route_request(request_obj)

@alexa.default_handler()
def default_handler(request):
    return alexa.create_response(message=DEFAULT_RESPONSE, end_session=False)

@alexa.intent_handler('AMAZON.HelpIntent')
def help_handler(request):
    return alexa.create_response(message=HELP_RESPONSE, end_session=False)

@alexa.intent_handler('AMAZON.CancelIntent')
def cancel_handler(request):
    return alexa.create_response(message=STOP_RESPONSE, end_session=True)

@alexa.intent_handler('AMAZON.StopIntent')
def stop_handler(request):
    return alexa.create_response(message=STOP_RESPONSE, end_session=True)

@alexa.intent_handler('CurrentPoolTemp')
def current_pool_temp(request):
    return get_temp_response('pool', CURRENT_POOL_TEMP_SUCCESS, CURRENT_POOL_TEMP_FAIL)

@alexa.intent_handler('CurrentAmbientTemp')
def current_ambient_temp(request):
    return get_temp_response('ambient', CURRENT_AMBIENT_TEMP_SUCCESS, CURRENT_AMBIENT_TEMP_FAIL)

@alexa.intent_handler('PastPoolTemp')
def past_pool_temp(request):
    min_date, max_date, date_type = poolmon.parse_date(request.slots['Date'])
    if date_type == 'day':
        aggregate_type = 'max'
    elif date_type == 'week' or date_type == 'year':
        aggregate_type = 'avg'
    else:
        return alexa.create_response(message=DATE_PARSE_FAIL, end_session=False)
    
    return get_temp_response('pool', PAST_POOL_TEMP_SUCCESS, PAST_POOL_TEMP_FAIL, min_date=min_date, max_date=max_date, aggregate_type=aggregate_type)

@alexa.intent_handler('PastAmbientTemp')
def past_ambient_temp(request):
    min_date, max_date, date_type = poolmon.parse_date(request.slots['Date'])
    if date_type == 'day':
        aggregate_type = 'max'
    elif date_type == 'week' or date_type == 'year':
        aggregate_type = 'avg'
    else:
        return alexa.create_response(message=DATE_PARSE_FAIL, end_session=False)
    
    return get_temp_response('ambient', PAST_AMBIENT_TEMP_SUCCESS, PAST_AMBIENT_TEMP_FAIL, min_date=min_date, max_date=max_date, aggregate_type=aggregate_type)

def get_temp_response(temperature_type, success_response, fail_response, min_date=None, max_date=None, aggregate_type=None):
    params={}
    if min_date:
        params['min_date'] = min_date
    if max_date:
        params['max_date'] = max_date
    if aggregate_type:
        params['aggregate_type'] = aggregate_type
    
    try:
        endpoint = '/temperature/%s' % temperature_type
        response = poolmon.request(endpoint, params=params)
        temp = int(round(response['measurements'][0]['temperature'][preferred_temp_type]))
        message = success_response % {'temp': temp}
        
        return alexa.create_response(message=message, end_session=True)
    except IndexError:
        return alexa.create_response(message=fail_response, end_session=True)
