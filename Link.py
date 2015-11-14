"""
Link is used to connect two ends (hosts or routers), it represent the physical layer of the network
where packets will be transmitted on it bit by bit.

:param source: it is a Host class or a Router class
:param destination: it is Host class or a Router class
:param float delay: amount of time required for a packet propagate on the link
:param float rate: speed of removing data from source
:param capacity: maximum propagating rate on the link

:ivar source: it is a Host class or a Router class
:ivar destination: it is Host class or a Router class
:ivar float delay: amount of time required for a packet propagate on the link
:ivar float rate: speed of removing data from source
:ivar list transmitting: packets (class) being transmitted on the link
:ivar capacity: maximum propagating rate on the link
:ivar bool occupy: whether currently sending data
:ivar float utilization: utilization of link, i.e. propagating rate/capacity
"""

import Buffer

class Link():
    def _init_(self, env, name, source, destination, delay, rate, buffer_size):
        super(Link, self)._init_(env = env, name = name)
        self.source = source
        self.destination = destination
        self.delay = delay
        self.rate = rate
        self.buffer = Buffer(env = env, size = buffer_size, link = self)
        self.occupy = False
        self.utilization = 0
        
    def _str_(self):
        return ('Link form ' + self.source.address + ' to ' + self.destination.address)
    
    def add(self,packet):
        if self.occupy:
            self.buffer.add(packet)
        else:
            self.send(packet)
            
    def react_to_link_available(self, event):
        self.occupy = False
        if not self.buffer.container.empty():
            self.send(self.buffer.get())
    
    def send(self, packet):
        self.occupy = True
        trx_time = packet.size / self.rate
        #need to chech with Jiawei 
        PacketReceipt(env=self.env, delay = self.delay + trx_time, receiver = self.destination, packet = packet)
        LinkAvailable(env = self.env, delay = trx_time, link = self)
        self.env.log.LinkState(link=self, packet_size = packet.size)       
        