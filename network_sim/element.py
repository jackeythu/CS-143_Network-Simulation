from events import *
from constants import *

import collections
import copy
import heapq

BIT_TO_PKT_SCALOR = 10 * 1024 * 1024 / PACKET_SIZE

# BIT_TO_PKT_SCALOR = 10e6 / 64e3

'''
    Definition for Packet
        1. DataPacket
        2. RouterPacket
'''
class Packet(object):
    def __init__(self, source, destination, timestamp,packetsize):
        self.source = source
        self.destination = destination
        #self.flow = flow
        self.timestamp = timestamp
        self.packetsize = packetsize
        
class DataPacket(Packet):
    def __init__(self, source, destination, flow, timestamp, packetsize, acknowledgement, pck_id):
        super(DataPacket, self).__init__(source = source, destination = destination,
                                         timestamp = timestamp,packetsize = packetsize)
        self.acknowledgement = acknowledgement 
        self.flow = flow
        self.pck_id = pck_id
    def setOriginalPacketTimestamp(self, timestamp):
        self.originalPacketTimestamp = timestamp
                
class RouterPacket(Packet):#???routerpacket does not contain flow info.generate in Router and use link to transmit
    def __init__(self, source, timestamp, packetsize, routerTable, acknowledgement):
        super(RouterPacket, self).__init__(source = source, destination = 0,
                                           timestamp = timestamp, packetsize = packetsize)
        '''
            [Zilong]
            There isn't a Flow associated with RouterPacket
        '''
        self.routerTable = routerTable
        self.acknowledgement = acknowledgement


class Element(object):
    def __init__(self, engine, name=None):
        self.engine = engine
        self.name = name

class Host(Element):
    def __init__(self, engine, name, address):    
        super(Host,self).__init__(engine, name)
        self.link = None
        self.flows = []
        self.address = address
        
    def addFlow(self, flow):
        self.flows.append(flow)
        
    def send(self, packet):
        print "[{}] {} start to send packet".format(self.engine.curTime, self.name)
        self.link.send(packet,self)
        
    def receive(self, packet):
        if isinstance(packet, DataPacket):
            if packet.flow in self.flows:
                for flow in self.flows:
                    if self == flow.source:
                        flow.sourceReceive(packet)
                    if self == flow.destination:
                        flow.destinationReceive(packet)
        if isinstance(packet, RouterPacket):
            rt = {}
            rt[self.address] = (0, self.address) 
            ackRouterPacket = RouterPacket(self, packet.timestamp, PACKET_SIZE, rt, True)
            self.send(ackRouterPacket)
    
    def react_to_packet_receipt(self, event):
        if isinstance(event.packet, RouterPacket):
            '''
                [Zilong]
                Slight change here.
                Original: print "{} receive packet {}".format(self.name, event.packet.acknowledgement)
            '''
            print "[{}] receive RouterPacket [{}]".format(self.name, event.packet.acknowledgement)

        if isinstance(event.packet, DataPacket):
            '''
                [Zilong]
                Slight change here.
                Original: print "{} receive packet {}, {}".format(self.name, event.packet.acknowledgement, event.packet.pck_id)
            '''
            if event.packet.acknowledgement == False:
                print "[{}] receive DataPacket [{}]".format(self.name, event.packet.pck_id)
            else:
                print "[{}] receive AckPacket [{}] (for DataPack [{}])".format(self.name, event.packet.pck_id, 
                                                                               event.packet.pck_id - 1)
                
        self.receive(event.packet)
                    
class Link(Element):
    def __init__(self, engine, name, node1, node2, delay, rate, buffer_size):
        super(Link,self).__init__(engine, name)
        self.node1 = node1
        self.node2 = node2
        self.delay = delay
        self.rate = rate
        '''
            [Zilong]
            Use two buffers to enable double-directional transmission
        '''
        self.buffer1 = Buffer(self.engine, buffer_size, self)
        self.buffer2 = Buffer(self.engine, buffer_size, self)
        self.busy = False
        #self.engine.recorder.record_link_rate(self, engine.getCurrentTime(), 0)
        self.attachToNode(node1)
        self.attachToNode(node2)
        
    
    def attachToNode(self,node):
        if isinstance(node, Host):
            '''
                [Zilong]
                Host can only corresponding to one Link at the same time
            '''
            if node.link != None:
                print "ERROR: Host should not have link now"
                return            
            node.link = self
        if isinstance(node, Router):
            if node == self.node1:
                node.links.append((self, 1))
            if node == self.node2:
                node.links.append((self, 2))

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
        
        self.busy = True
        #self.engine.recorder.record_link_rate(self, self.engine.getCurrentTime(), self.rate)
        self.engine.recorder.record_link_rate(self, self.engine.getCurrentTime(), self.rate)
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
        event1 = Event.CreateEventPacketReceipt(self.engine.curTime+costTime, receiver, packet)
        self.engine.push_event(event1)
        
        '''
            [Zilong]
            Just to update the link status after one packet is sent
            Set busy to False after it
        '''
        event2 = Event(self.engine.curTime+costTime, self, EVENT_LINK_AVAILABLE)
        self.engine.push_event(event2)
        
        
            
    def react_to_link_available(self, event):
#         print "{} link available".format(self.name)
        self.busy = False
        self.engine.recorder.record_link_rate(self, self.engine.getCurrentTime(), 0)
        self.decide()
        
class Buffer(Element):
    def __init__(self, engine, buffer_size, link):
        super(Buffer,self).__init__(engine)
        self.buffer = collections.deque()
        self.bytes = 0
        self.buffer_size = buffer_size
        self.link = link
        self.loss = 0
        
    
    def push(self, packet):
        
        if self.bytes + packet.packetsize <= self.buffer_size:
            print "use buffer"
            self.buffer.append(packet)
            self.bytes += packet.packetsize
            self.loss = 0
            self.engine.recorder.record_packet_loss(self.link, self.engine.getCurrentTime(), self.loss)
            self.engine.recorder.record_buffer_occupancy(self.link, self.engine.getCurrentTime(), self.bytes)
        else:
            '''
                [Zilong]
                Handle packet lost here
            '''
            self.loss += 1
           
            self.engine.recorder.record_packet_loss(self.link, self.engine.getCurrentTime(), self.loss)
            self.engine.recorder.record_buffer_occupancy(self.link, self.engine.getCurrentTime(), self.bytes)
            print 'Packet Lost: [{}],'.format(packet.pck_id)
         
    def pop(self):
        if self.bytes == 0 :
            print "Buffer underflow"
        else:
            
            packet = self.buffer.popleft()
            self.bytes -= packet.packetsize
            return packet
            
            
    
class Router(Element):
    def __init__(self, engine, name, address, updateTime=ROUTER_PACKET_GENERATION_INTERVAL):
        super(Router,self).__init__(engine, name)
        self.address = address
        self.updateTime = updateTime
        self.links = []
        self.defaultLink = None
        self.rt = {}#key: host ip addre, value:1:cost 2:next hop
        self.rt[address] = (0, address)
    
    def initialRT(self, all_node_addr):#should be called when creating network 
        self.defaultLink = self.links[0]
        for addr in all_node_addr:
            self.rt[addr] = (float('inf'), self.defaultLink)
            
        for link in self.links:#update those host that connect to router through one link
            if link[1] == 1:
                if isinstance(link[0].node2, Host):
                    self.rt[link[0].node2.address] = (1, link[0])
                
            if link[1] == 2:
                if isinstance(link[0].node1, Host):
                    self.rt[link[0].node1.address] = (1, link[0])
                
        self.broadcastRouterPacket()
                
    def broadcastRouterPacket(self):
        
        routerPacket =  RouterPacket(self, self.engine.getCurrentTime(), PACKET_SIZE, copy.copy(self.rt), True)
        for link in self.links:
            if link[1] == 1:
                #if isinstance(link[0].node2, Router):
                link[0].send(routerPacket, self)
            if link[1] == 2:
                #if isinstance(link[0].node1, Router):
                link[0].send(routerPacket, self)
                
    def broadcastRequestPacket(self):
        
        routerPacket =  RouterPacket(self, self.engine.getCurrentTime(), PACKET_SIZE, None, False)
        for link in self.links:
            if link[1] == 1:
                #if isinstance(link[0].node2, Router):
                link[0].send(routerPacket, self)
            if link[1] == 2:
                #if isinstance(link[0].node1, Router):
                link[0].send(routerPacket, self)
                    
    def generateACKRouterPacket(self, packet):
        neigh = packet.source.address  #ackrp use received packet's timestamp? or current Time??
        
        ackRouterPacket = RouterPacket(self, packet.timestamp, PACKET_SIZE, copy.copy(self.rt), True)
        self.send(neigh, ackRouterPacket)
    
    def send(self, destAddr, packet):      
        for link in self.links:
            if link[1] == 1:
                if link[0].node2.address == destAddr:
                    link[0].send(packet, self)
                    break
            if link[1] == 2:
                if link[0].node1.address == destAddr:
                    link[0].send(packet, self)
                    break 
                  
    def react_to_packet_receipt(self, event):
        
        packet = event.packet
        if isinstance(packet, DataPacket):
            print "{} receive data_packet {}, {}".format(self.name, event.packet.acknowledgement, event.packet.pck_id)
            self.rtRefer(packet)
            
        if isinstance(packet, RouterPacket):
            print "{} receive router_packet {}".format(self.name, event.packet.acknowledgement)
            if packet.acknowledgement == False:
                self.generateACKRouterPacket(packet)
            if packet.acknowledgement == True:
                self.updateRT(packet)
                
    def updateRT(self, neiPacket):#dynamic route distance metric
        neiRT = neiPacket.routerTable
        neiCost = self.engine.getCurrentTime() - neiPacket.timestamp #RTT
        flag = False
        for (destAddr, neiVal) in neiRT.items():
            if destAddr in self.rt:
                if self.rt[destAddr][1] == neiPacket.source.address:#if nexthop is neighRT, must update
                    updateVal = (neiVal[0]+neiCost, neiPacket.source.address)
                    
                    if self.rt[destAddr] != updateVal:
                        self.rt[destAddr] = updateVal 
                else:
                    if neiVal[0] + neiCost < self.rt[destAddr][0]:
                        flag = True
                        updateVal = (neiVal[0]+neiCost, neiPacket.source.address)
                        self.rt[destAddr] = updateVal
                        
            else:
                flag = True
                updateVal = (neiVal[0]+neiCost, neiPacket.source.address)
                self.rt[destAddr] = updateVal
        if flag:
            self.broadcastRouterPacket()
        print"{}".format(self.name)
        print self.rt
                    
        
                
    def rtRefer(self, packet):
        if packet.destination.address in self.rt:
            nextHop = self.rt[packet.destination.address][1]   
            print "{} is forwarding packet to {}".format(self.name, nextHop)
            self.send(nextHop, packet)
        else:
            self.send(self.links[0], packet)
        
    
        
    def react_to_routing_table_update(self, event):
        print "{} start to update rt at [{}]".format(self.name, self.engine.getCurrentTime())
        self.broadcastRequestPacket() 
        event = Event(self.engine.getCurrentTime() + self.updateTime, self, EVENT_ROUTINGTABLE_UPDATE)
        self.engine.push_event(event)      
  
            
    
        

class Flow(Element):
    def __init__(self, engine, name, source, destination, amount, tcp):
        super(Flow, self).__init__(engine, name)
        '''
            [Zilong]
            It seems that Flow can only be one-directional here.
            So, for each packet transmitted from Host A to Host B,
            there would be two flows?
            But actually, we only use one.
        '''
        self.source = source
        self.destination = destination
        self.amount = amount
        self.tcp = tcp
        self.tcp.setFlow(self)
        '''
            [Zilong]
            Change packetCounter to be domain variable
            Original:
                self.packetCounter = 0
        '''
        self.received_packets = list()
        self.packet_to_receive = 0
        
        '''
            [Mengchen] add self.outOfOrderPackets and self.lastOrderedPacketID
        '''
        self.outOfOrderPackets = []
        self.lastOrderedPacketID = 0
        
        source.addFlow(self)
        destination.addFlow(self)
        
    '''
        [Zilong]
        A slight change to make packetCounter a domain variable
        Original:
            def generatePacket(self):
                if self.packetCounter >= self.amount:
                    print "ERROR: Trying to send more packets than amount"
                    
                packet = DataPacket(self.source,self.destination,self, self.engine.getCurrentTime(), PACKET_SIZE, 
                                    False, self.packetCounter)
                self.packetCounter += 1
                return packet
    '''
    def generatePacket(self, pck_id):
#         if packetCounter >= self.amount:
#             print "ERROR: Trying to send more packets than amount"
            
        packet = DataPacket(self.source, self.destination, self, self.engine.getCurrentTime(), PACKET_SIZE, 
                            False, pck_id)
#         print 'packetCounter: {},'.format(packetCounter)
        
        return packet

        
    def generateAckPacket(self, packet):
        '''
            [Zilong]
            Add received_packet here, which should be in TCP.
            Just for test now
        
        cur_id = packet.pck_id
        
        if cur_id == self.packet_to_receive:
            self.packet_to_receive += 1
            for id in self.received_packets:
                if id == self.packet_to_receive:
                    self.packet_to_receive += 1
#                     self.received_packets.remove(id)
        elif cur_id > self.packet_to_receive:
            self.received_packets.append(cur_id)
        else:
            pass
        '''
        
        '''
            [Mengchen] modify the code to ensure the pck_id  is the pck that the receiver expected for the next pck
        '''
        if packet.pck_id <= self.lastOrderedPacketID:
            pass
        else:
            if packet.pck_id == self.lastOrderedPacketID+1:
                # this is the pck we expected
                self.lastOrderedPacketID += 1
                
                while self.outOfOrderPackets and self.outOfOrderPackets[0] == self.lastOrderedPacketID+1:
                    heapq.heappop(self.outOfOrderPackets)
                    self.lastOrderedPacketID +=1
                    
            else:
                #this pck is after the expected pck
                heapq.heappush(self.outOfOrderPackets, packet.pck_id)
                    
                
  
        
        ack_packet = DataPacket(packet.destination, packet.source, self, self.engine.getCurrentTime(), ACK_PACKET_SIZE, 
                                True, self.lastOrderedPacketID + 1)
        ack_packet.setOriginalPacketTimestamp(packet.timestamp)
        '''
            [Zilong]
            So, for each packet with pck_id
            The ACK packet of it will have pck_id = packet.pck_id + 1?
        '''
        return ack_packet
        
    def sourceSend(self,packet):
        self.source.send(packet)
        
    def destinationSend(self,packet):
        self.destination.send(packet)
    
    def sourceReceive(self,packet):
        if packet.acknowledgement == True:
            self.tcp.react_to_ack(packet)
        '''
            [Zilong]
            Because Flow is one-directional, so we need to handle ACK here
        '''
    
    def destinationReceive(self,packet):      
        ack_packet = self.generateAckPacket(packet)
        self.destinationSend(ack_packet)
        self.engine.recorder.record_flow_rate(self, self.engine.getCurrentTime(), PACKET_SIZE * BIT_TO_PKT_SCALOR)
        packet_delay = self.engine.getCurrentTime() - packet.timestamp
        print '------------'
        print packet_delay
       
        self.engine.recorder.record_packet_delay(self, self.engine.getCurrentTime(), packet_delay)
            
    def react_to_time_out(self, event):
        self.tcp.react_to_time_out(event)
    
    def react_to_flow_start(self, event):

        #print "--[{}]--".format(self.engine.curTime)
        self.tcp.react_to_flow_start(event)

