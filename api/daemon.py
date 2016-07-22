from credentials import DBCONN, AMBIENTSENSOR, POOLSENSOR
from tzlocal import get_localzone
import sys, os, time, psycopg2, random, datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

def get_temp(sensor):
	ready = False
	while not ready:
		f = open(base_dir+sensor, 'r')
		lines = f.readlines()
		f.close()
		
		if lines[0].strip()[-3:] == 'YES':
			ready = True
	
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]

		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
        
		return temp_c, temp_f
	return None

def insert_measurement(cur, measurement_type, temp_c, temp_f):
	local_tz = get_localzone()
	
	data = {}
	data['type'] = measurement_type
	data['degrees_farenheit'] = temp_f
	data['degrees_celsius'] = temp_c
	data['measured_at'] = datetime.datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
	
	query = """
		INSERT INTO measurements (type, measured_at, degrees_celsius, degrees_farenheit) 
			VALUES ('{type}', '{measured_at}', {degrees_celsius}, {degrees_farenheit})""".format(**data)
	
	return cur.execute(query)

while True:
	try:
		with psycopg2.connect(DBCONN) as conn:
			with conn.cursor() as cur:
				insert_measurement(cur, 'ambient', *get_temp(AMBIENTSENSOR))
				insert_measurement(cur, 'pool', *get_temp(POOLSENSOR))
	except KeyboardInterrupt:
		sys.exit(0)
	except:
		print "Unexpected exception occurred"
	
	time.sleep(5*60)
