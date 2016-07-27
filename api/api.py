from flask import Flask, request, jsonify
from credentials import DBCONN, APIKEY
from psycopg2.extras import RealDictCursor
from tzlocal import get_localzone
import psycopg2, datetime, pytz

app = Flask(__name__)

allowed_types = ['single', 'all', 'min', 'max', 'avg']

@app.route("/temperature/pool")
def pool():
    return __do_request('pool')

@app.route("/temperature/ambient")
def ambient():
    return __do_request('ambient')

def __do_request(measurement_type):
    api_key = request.headers.get('x-api-key')
    if api_key != APIKEY:
        return jsonify(error=403, message='forbidden'), 403
    
    min_date = request.args.get('min_date')
    max_date = request.args.get('max_date')
    aggregate = request.args.get('type')
    
    if min_date:
        try:
            min_date = datetime.datetime.strptime(min_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify(error=400, message='unrecoginized min_date format', expected_format='YYYY-MM-DD HH:MM:SS'), 400
        
    if max_date:
        try:
            max_date = datetime.datetime.strptime(max_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify(error=400, message='unrecognized max_date format', expected_format='YYYY-MM-DD HH:MM:SS'), 400
        
    if not aggregate and not min_date and not max_date:
        aggregate = 'single'
    elif not aggregate:
        aggregate = 'all'
    elif aggregate not in allowed_types:
        return jsonify(error=400, message='unrecognized type', allowed_types=['single', 'all', 'min', 'max', 'avg']), 400
    
    return jsonify(measurements=__do_temperature_query(measurement_type, min_date=min_date, max_date=max_date, aggregate_type=aggregate))

def __do_temperature_query(measurement_type, min_date=None, max_date=None, aggregate_type="all"):
    if aggregate_type == 'avg':
        query = "SELECT '"+measurement_type+"' as type, AVG(degrees_celsius) as degrees_celsius, AVG(degrees_farenheit) as degrees_farenheit, MIN(measured_at) as measured_at"
    else:
        query = "SELECT * "
    
    where = []
    where.append("type='%s'" % measurement_type)
    
    if min_date:
        where.append("measured_at > '%s'" % min_date)
    if max_date:
        where.append("measured_at <= '%s'" % max_date)
    
    query = query + ' FROM measurements WHERE ' + ' and '.join(where)
    
    if aggregate_type == 'min':
        query += ' ORDER BY degrees_farenheit LIMIT 1'
    elif  aggregate_type == 'max':
        query += ' ORDER BY degrees_farenheit DESC LIMIT 1'
    elif aggregate_type == 'single':
        query += ' ORDER BY measured_at DESC LIMIT 1'
    
    with psycopg2.connect(DBCONN) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            
            rows = []
            for row in cur.fetchall():
                formatted = format_row(row, aggregate_type)
                if formatted:
                    rows.append(formatted)
            
            return rows

def format_row(row, aggregate_type='all'):
    if 'measured_at' not in row or row['measured_at'] == None:
        return None
    
    if aggregate_type == 'all':
        aggregate_type = 'single'
    
    local_tz = get_localzone()
    
    ret = {}
    ret['aggregate_type'] = aggregate_type
    ret['timestamp'] = local_tz.localize(row['measured_at']).isoformat('T')
    ret['measurement_type'] = row['type']
    ret['temperature'] = {}
    ret['temperature']['degrees_farenheit'] = round(row['degrees_farenheit'], 3)
    ret['temperature']['degrees_celsius'] = round(row['degrees_celsius'], 3)
    return ret

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18015)
