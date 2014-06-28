from fabric.api import run, hide, settings

#env.user = 'root'
#env.hosts = 'root@192.168.88.251'

with hide('output'):
	with settings(host_string='192.168.88.251'):

		def host_type():
			return run('uname -a')

		def host_mem():
		    return run("free -t -m")
		    
		def host_arp():
		    return run("cat /proc/net/arp")

		def ovs_show_cfg():
			return run('ovs-vsctl show')	

		def ovs_add_bridge(name):
			return run("ovs-vsctl add-br %s" % name)

		def ovs_del_bridge(name):
		    return run("ovs-vsctl del-br %s" % name) 
