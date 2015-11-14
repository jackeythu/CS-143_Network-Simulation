class Router(object):
	def __init__(self,env,name,address,link,period = ROUTER_PERIOD):
		#address is string
		self.env = env
		self.address = address
		self.rt = {}
		self.link = []
		self.default_hop = None
		self.period = period
	def __str__(self):
		return address
	def initial_rt(self,all_host_ip):
		self.default_hop = self.link[0].destination.address
		for host_ip in all_host:
			self.rt[host_ip] = (float("inf"),self.default_hop)
		for link in self.link:
			self.rt[link.destination.address] = (1,link.destination.address)
		self.Generate_Router_Packet()
	def generate_router_packet(self):
		rp = routerPacket(timestamp = self.env.now, router_table = self.rt,source = self, acknowledgement = False)
		for lk in self.link:
			if isinstance(link.destination,Router):
				self.send(link = lk,packet = rp)
	def generate_ack_router_packet(self,router_packet):
		source_packet = router_packet
		ack_router_packet = routerPacket(source_packet.timestamp,router_table = self.rt,source = self,acknowledgement = True)
		for lk in self.link:
			if lk.destination == source_packet.source:
				self.send(link = lk,packet = ack_router_packet)
				break
	def search_rt(self,packet):
		#called when receive a datapacket. Used to find the next hop and forward data
		des_add = packet.destination.address
		if des_add in self.rt:
			nexthop = self.rt.get(des.address)[1]
			for lk in self.link:
				if lk.destination.address == nexthop:
					self.send(link = lk,packet = packet)
					break
		else:
			self.send(link = self.link[0],packet = packet)

	def receive(self,packet):
		#??? should we change the input parameter packet to event?
		#then event.value = packet

		#handle pacekt reception. Check if it is a data packet or router packet
		if isinstance(packet,dataPacket):
			self.search_rt(packet = packet)
		if isinstance(packet,routerPacket):
			if packet.acknowledgement == False:
				self.ack_router_packet(router_packet = packet)
			else:
				self.update_rt(router_packet = packet)

	def send(self,link,packet):
		link.add(packet = packet)

	def period_update(self,event):
		self.generate_router_packet()
		#create a event here????why???
		PeriodUpdate(env = self.env, delay = self.period,router = self)
	def update_rt(self,router_packet):
	"""
		Implement Bellman-Ford algorithm here.
        
        Measurement is link delay (DYNAMIC_ROUTE_DISTANCE_METRIC = True).
    """
    	metric = self.env.now-router_packet.timestamp
    	for(dest,val) in router_packet.router_table:
    		if dest in self.rt:
    			if self.rt.get(dest)[1] = router_packet.source.address:
    			# to get to the dest, the packet have to go through the routerA 
    			# which send the rt to this router. Simply add matrix upon
    			# the cost of routerA
    				self.rt[dest] = metric+val[0],router_packet.source.address
    				# in Junlin's code it write like this:
    				#if self.table[destination][1] == router_packet.source.address:
                     #   update_val = val[0] + metric, router_packet.source.address
                      #  self.table[destination] = update_val
                 else:
                 	if self.rt.get(dest)[0]>matrix+val[0]:
                 		self.rt[dest] = val[0]+metrix,router_packet.source.address

            else:
            	#the dest is not exists in rt, create it
            	self.rt[dest] = metric+val[0],router_packet.source.address

