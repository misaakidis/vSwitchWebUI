import subprocess
import sys

HOST="root@192.168.88.251"
# Ports are handled in ~/.ssh/config since we use OpenSSH
COMMAND="ovs-vsctl show"

ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
result = ssh.stdout.readlines()
if result == []:
    error = ssh.stderr.readlines()
    print >>sys.stderr, "ERROR: %s" % error
else:
    print result