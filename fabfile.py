from fabric.api import env, execute, run, hide
import json

class FabricSupport:
	def __init__(self):
		pass

	with hide('output'):

		def host_type(self):
			return run('uname -a')

		def host_mem(self):
		    return run("free -t -m")
		    
		def host_arp(self):
		    return run("cat /proc/net/arp")

		def ovs_show_cfg(self):
			return run("ovs-vsctl show")	

		def ovs_list_bridges(self):
			return run("ovs-vsctl show | grep 'Bridge' | sed -e 's/^[ tab]\+Bridge //g'")
		
		def ovs_add_bridge(self, name):
			return run("ovs-vsctl add-br %s" % name)

		def ovs_del_bridge(self, name):
		    return run("ovs-vsctl del-br %s" % name)

		def ovs_add_port(self, br_name, p_name):
			return run("ovs-vsctl add-port %s %s" % (br_name, p_name)) 

		def ovs_add_port_vlan(self, br_name, p_name, vlan):
			return run("ovs-vsctl add-port %s %s tag= %s " % (br_name, p_name, vlan)) 

		def ovs_list_ports(self, br_name):
			return run("ovs-vsctl list-ports %s" % br_name)

		def ovs_ingress_policing_rate(self, br_name, rate_limit):
			return run("ovs-vsctl set Interface %s ingress_policing_rate=%s " % (br_name, rate_limit))

		def execute(self, task, hosts):
			get_task = "task = self.%s" % task
			exec get_task
			return execute(task, hosts=hosts)