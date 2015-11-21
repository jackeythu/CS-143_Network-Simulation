from cs143_v1.events import *

import collections

PACKET_SIZE = 1024 * 8
ACK_PACKET_SIZE = 512 #CHECK IT
class Element(object):
    def __init__(self, engine, name=None):
        self.engine = engine
        self.name = name

class Packet(object):
    def __init__(self, source, destination, flow, timestamp,packetsize):
        self.source = source
        self.destination = destination
        self.flow = flow
        self.timestamp = timestamp
        self.packetsize = packetsize
        
class DataPacket(Packet):
    def __init__(self, source, destination, flow, timestamp, packetsize, acknowledgement, pck_id):
        super(DataPacket, self).__init__(source = source, destination = destination, flow = flow,
                                         timestamp = timestamp,packetsize = packetsize)
        self.acknowledgement = acknowledgement 
        self.pck_id = pck_id
                
class RouterPacket(Packet):
    def __init__(self, source, flow, timestamp, packetsize, routerTable, acknowledgement):
        super(RouterPacket, self).__init__(source = source, destination = 0, flow = flow,
                                           timestamp = timestamp, packetsize = packetsize)
        self.routerTable = routerTable
        self.acknowledgement = acknowledgement    
    
class Host(Element):
    def __init__(self, engine, name):    
        super(Host,self).__init__(engine, name)
        self.link = None
        self.flows = []
        
    def addFlow(self, flow):
        self.flows.append(flow)
        
    def send(self, packet):
        self.link.send(packet,self)
        
    def receive(self, packet):
        if packet.flow in self.flows:
            for flow in self.flows:
                if self == flow.source:
                    flow.sourceReceive(packet)
                if self == flow.destination:
                    flow.destinationReceive(packet)
    
    def react_to_packet_receipt(self, event):
        print "{} receive packet {}, {}".format(self.name, event.packet.acknowledgement, event.packet.pck_id)
        self.receive(event.packet)
                    
class Link(Element):
    def __init__(self, engine, name, node1, node2, delay, rate, buffer_size):
        super(Link,self).__init__(engine, name)
        self.node1 = node1
        self.node2 = node2
        self.delay = delay
        self.rate = rate
        self.buffer1 = Buffer(buffer_size)
        self.buffer2 = Buffer(buffer_size)
        self.busy = False
        self.attachToNode(node1)
        self.attachToNode(node2)
        
    
    def attachToNode(self,node):
        if isinstance(node, Host):
            if node.link != None:
                print "ERROR: Host should not have link now"
                return            
            node.link = self

    def send(self, packet, sender):
        
        if sender == self.node1:
            self.buffer1.push(packet)
        if sender == self.node2:
            self.buffer2.push(packet)
           
        if not self.busy:
            self.decide()
            
    def decide(self):
        lg1 = self.buffer1.bytes; lg2 = self.buffer2.bytes
        if lg1 == 0 and lg2 == 0:
            return 
        
        popper = None
        receiver = None
        if lg1>lg2:
            popper = self.buffer1
            receiver = self.node2
        else:
            popper = self.buffer2
            receiver = self.node1
        
        packet = popper.pop()
        costTime = self.delay + packet.packetsize / self.rate
        event = Event.CreateEventPacketReceipt(self.engine.curTime+costTime, receiver, packet)
        self.engine.push_event(event)
        
        event1 = Event(self.engine.curTime+costTime, self, EVENT_LINK_AVAILABLE)
        self.engine.push_event(event1)
        
        self.busy = True
            
    def react_to_link_available(self, event):
        print "{} link available".format(self.name)
        self.busy = False
        self.decide()
        
class Buffer():
    def __init__(self, buffer_size):
        self.buffer = collections.deque()
        self.bytes = 0
        self.buffer_size = buffer_size
        
    
    def push(self, packet):
        
        if self.bytes+packet.packetsize <= self.buffer_size:
            self.buffer.append(packet)
            self.bytes += packet.packetsize
            
    def pop(self):
        if self.bytes == 0 :
            print "Buffer underflow"
        else:
            
            packet = self.buffer.popleft()
            self.bytes -= packet.packetsize
            return packet
            
            
    


class Flow(Element):
    def __init__(self, engine, name, source, destination, amount):
        super(Flow, self).__init__(engine, name)
        self.source = source
        self.destination = destination
        self.amount = amount
        self.packetCounter = 0
        
        source.addFlow(self)
        destination.addFlow(self)
    
    def generatePacket(self):
        if self.packetCounter >= self.amount:
            print "ERROR: Trying to send more packets than amount"
            
        packet = DataPacket(self.source,self.destination,self, self.engine.getCurrentTime(), PACKET_SIZE, 
                            False, self.packetCounter)
        self.packetCounter += 1
        return packet
        
    def generateAckPacket(self,packet):
        ack_packet = DataPacket(packet.destination, packet.source,self, self.engine.getCurrentTime(), ACK_PACKET_SIZE, 
                                True, packet.pck_id+1)
        return ack_packet
        
    def sourceSend(self,packet):
        self.source.send(packet)
        
    def destinationSend(self,packet):
        self.destination.send(packet)
    
    def sourceReceive(self,packet):
        pass
    
    def destinationReceive(self,packet):      
        ack_packet = self.generateAckPacket(packet)
        self.destinationSend(ack_packet)
            
    def react_to_time_out(self):
        pass
    
    def react_to_flow_start(self, event):
        packet = self.generatePacket()
        self.sourceSend(packet)
        

    
    