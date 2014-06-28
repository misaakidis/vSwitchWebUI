import subprocess
import sys

HOST="root@192.168.88.251"

def uname():
	# Ports are handled in ~/.ssh/config since we use OpenSSH
	COMMAND="uname -a"

	ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
	                       shell=False,
	                       stdout=subprocess.PIPE,
	                       stderr=subprocess.PIPE)
	result = ssh.stdout.readlines()
	if result == []:
	    error = ssh.stderr.readlines()
	    return "ERROR: %s" % error
	else:
	    return result