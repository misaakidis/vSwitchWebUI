from fabric.api import run

def host_type():
	run('uname -a')

def host_mem():
    run("free -t -m")
    
def host_arp():
    run("cat /proc/net/arp")

def ovs_show_cfg():
	run('ovs-vsctl show')	

def ovs_add_bridge(name):
	run("ovs-vsctl add-br %s" % name)

def ovs_del_bridge(name):
    run("ovs-vsctl del-br %s" % name) 
