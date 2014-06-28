from fabric.api import run

def host_type():
	run('uname -a')

def host_mem():
    run("free -t -m")
    
def host_arp():
    run("cat /proc/net/arp")

def ovs_show_cfg():
	run('ovs-vsctl show')	

def ovs_add_bridge(br_name):
	run("ovs-vsctl add-br %s" % br_name)

def ovs_add_port(br_name, p_name):
    run("ovs-vsctl add-port %s %s" % (br_name, p_name)) 

def ovs_add_port_vlan(br_name, p_name, vlan):
    run("ovs-vsctl add-port %s %s tag= %s " % (br_name, p_name, vlan)) 

def ovs_del_bridge(br_name):
    run("ovs-vsctl add-port %s" % br_name) 

def ovs_list_ports(br_name):
    run("ovs-vsctl list-ports %s" % br_name)
    
    
