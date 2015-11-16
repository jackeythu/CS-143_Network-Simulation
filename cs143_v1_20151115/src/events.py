import heapq
#from cs143_v1.actor import Router


EVENT_LINK_AVAILABLE = 'LinkAvailable'
EVENT_PACKET_RECEIPT = 'PacketReceipt'
EVENT_ROUTINGTABLE_OUTDATED = 'RoutingTableOutdated'
EVENT_PACKET_TIMEOUT = 'PacketTimeOut'
EVENT_FLOW_START = 'FlowStart'


class Event:

    def __init__(self, time, reactor, type):
        self.time = time
        self.reactor = reactor
        self.type = type

    def execute(self):
        print 'at time: [{}] '.format(self.time),
        if (self.type == EVENT_LINK_AVAILABLE):
            self.reactor.react_to_link_available(self)
        if (self.type == EVENT_PACKET_RECEIPT):
            self.reactor.react_to_packet_receipt(self)
        if (self.type == EVENT_ROUTINGTABLE_OUTDATED):
            self.reactor.react_to_routing_table_outdated(self)
        if (self.type == EVENT_PACKET_TIMEOUT):
            self.reactor.react_to_time_out(self)
        if (self.type == EVENT_FLOW_START):
            self.reactor.react_to_flow_start(self)

    @staticmethod
    def CreateEventPacketReceipt(time, reactor, packet):
        event = Event(time, reactor, EVENT_PACKET_RECEIPT)
        event.packet = packet
        return event 
        

class Reactor:
    def __init__(self, name):
        self.name = name

    def react_to_event_a(self):
        print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'event_a')

    def react_to_event_b(self):
        print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'event_b')

    def react_to_event_c(self):    
        print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'event_b')

class SimEngine:
    def __init__(self,maxtime):
        self.queue = []
        self.MAXTIME = maxtime
        self.curTime = 0
        
    def getCurrentTime(self):
        return self.curTime

    def push_event(self, event):
        # push (event.time, event), so that it will be ordered by event.time
        heapq.heappush(self.queue, (event.time, event))

    def pop_event(self):
        # pop the event
        return heapq.heappop(self.queue)[1]

    def execute_top(self):
        event = self.pop_event()
        self.curTime += event.time
        event.execute()

    def run(self):
        while len(self.queue) > 0 and self.curTime < self.MAXTIME:
            self.execute_top()
            
            
