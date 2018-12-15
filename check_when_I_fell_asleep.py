import subprocess, shlex
from datetime import timezone
from time import strftime
import datetime
import signal

###### Needs adjusting ######
MIN_HOURS_OF_SLEEP = 4
ONE_HOUR_IN_TD_UNITS = 3600

# Clean exit with interrupt
def exit_function(signal, frame):
	print()
	exit()

def input_hour(dt):
	input_hour = None
	options = list(map(str, list(range(0,24))))
	while input_hour != "" and input_hour not in options:
		input_hour = input(f"\nEnter hour(0-23) you woke up. Ex: now(\'{dt}\')\nIf left blank, it will assume now is your wake time: ")
	if input_hour != "":
		return int(input_hour)
	else:
		return None

def check_logfile_bash():
	command = "pmset -g log"
	args = shlex.split(command)
	data = subprocess.check_output(args).decode()
	data = data.split(sep='\n')
	dates = [d for d in data if "TurnedOff" in d]
	return dates

if __name__ == '__main__':
	signal.signal(signal.SIGINT, exit_function)
	# Get date and time now
	dt = datetime.datetime.now()
	change_hour = input_hour(dt)
	if (change_hour):
		dt = dt.replace(hour = change_hour)
	awakeTimestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())

	dates = check_logfile_bash()
	for d in dates[::-1]:
		ndt = datetime.datetime.strptime(d[0:19],"%Y-%m-%d %H:%M:%S")
		timestamp = int(ndt.replace(tzinfo=timezone.utc).timestamp())
		if awakeTimestamp - timestamp > MIN_HOURS_OF_SLEEP * ONE_HOUR_IN_TD_UNITS:
			print(awakeTimestamp - timestamp)
			if input(f"Time and date you most likely went to bed:\n\n{ndt}\n\nIf not enter '0': ") != '0':
				break

#######################################################
## Another approach to getting log data (unfinished) ##
#######################################################
def check_system_logfile():
	with open("/private/var/log/system.log") as f:
		data = f.read()
		data = data.split(sep='\n')

		print(data[-4])
		print(data[-4][7:9])
		print(int(data[-4][7:9]))

		print(data[-4][7:9])
		print(int(data[-4][7:9]))

		# for i in range(len(data)-2,-1,-1):
		# 	print(data[i])
		# 	if int(data[i+1][7:9]) - int(data[i][7:9]) > 1:
		# 		print(data[i+1], data[i])
		# print(data[0:3])

