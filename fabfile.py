from fabric.api import run

def host_type():
	run('uname -a')

def ovs_show_cfg():
	run('ovs-vsctl show')	
