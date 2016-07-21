from credentials import DBCONN, AMBIENTSENSOR, POOLSENSOR
import sys, os, time

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

def insert_measurement(type, temp_c, temp_f):
	pass

while True:
	try:
		insert_measurement('ambient', *get_temp(AMBIENTSENSOR))
		insert_measurement('pool', *get_temp(POOLSENSOR))
	except KeyboardInterrupt:
		sys.exit(0)
	except:
		print "Unexpected exception occurred"
	
	time.sleep(5*60)
    
    