"""
Buffer is used to store data when link is busy sensing data.

:param int capacity: maximum number of bits that a buffer can store
:param link: it is the class Link. Each link contains a Buffer

:ivar int size: maximum number of bits that a buffer can store
:ivar link: it is the class Link. Each link contains a Buffer
:ivar list container: used to contain packets in the buffer now
:ivar int current_occupancy: number of bits in the buffer now

:function add(self, packet): Add the packet to the Buffer when Link is busy sending data.
          Add packet to the buffer when it is not full(i.e. haven't reach the buffer capacity),
          otherwise, drop the packet.
          Use Queue here because of its FIFO characteristic
          
          :param packet: packet coming from flow will be added to the buffer when link is busy
:function get(): As soon as the Link is not busy sending data, it will get the packet stored in the 
          buffer
"""
import Queue
import Link

class Buffer():

    def _init_(self, env, size, link):
        super(Buffer, self)._init_(env = env)
        self.link = Link
        self.container = Queue()
        self.size = size
        self.curent_occupancy = 0
        
    def add(self, packet):
        if self.current_occupancy + packet.size <= self.size:
            self.container.put(packet)
            self.current_occupancy = self.current_occupancy + packet.size
            self.env.log.BufferState(link = self.link, occupancy = self.current_occupancy)
           # return True
        
        else:
            self.env.log.PacketDrop(link = self.lin)
            self.env.log.BufferState(link = self.link, occupancy = self.current_level)
            #return False
    
    def get(self):
            packet = self.container.get()
            #timeout param?
            self.current_occupancy = self.occupancy - packet.size
            self.env.log.BufferState(link = self.link, occupancy = self.current_occupancy)
            return packet
        