#from network_sim.actor import Router

EVENT_LINK_AVAILABLE = 'LinkAvailable'
EVENT_PACKET_RECEIPT = 'PacketReceipt'
EVENT_ROUTINGTABLE_OUTDATED = 'RoutingTableOutdated'
EVENT_PACKET_TIMEOUT = 'PacketTimeOut'
EVENT_FLOW_START = 'FlowStart'
EVENT_ROUTINGTABLE_UPDATE = 'RoutingTableUpdate'

class Event:

    def __init__(self, time, reactor, type):
        self.time = time
        self.reactor = reactor
        self.type = type

    def execute(self):
        print ""
        print 'Time: [{}],'.format(self.time),
        print 'Event type: [{}],'.format(self.type),
        print 'Reactor: [{}] '.format(self.reactor.name)

        if (self.type == EVENT_LINK_AVAILABLE):
            self.reactor.react_to_link_available(self)
        if (self.type == EVENT_PACKET_RECEIPT):
            self.reactor.react_to_packet_receipt(self)
        if (self.type == EVENT_ROUTINGTABLE_OUTDATED):
            self.reactor.react_to_routing_table_outdated(self)
        if (self.type == EVENT_ROUTINGTABLE_UPDATE):
            self.reactor.react_to_routing_table_update(self)
        if (self.type == EVENT_PACKET_TIMEOUT):
            self.reactor.react_to_time_out(self)
        if (self.type == EVENT_FLOW_START):
            self.reactor.react_to_flow_start(self)

    @staticmethod
    def CreateEventPacketReceipt(time, reactor, packet):
        event = Event(time, reactor, EVENT_PACKET_RECEIPT)
        '''
            [Zilong]
            Why does the event has a variable packet here?
        '''
#         print 'CreateEventPacketReceipt, [{}] received at: [{}] '.format(reactor.name, time)
        event.packet = packet
        return event 
    @staticmethod
    def CreateEventPacketTimeOut(time, reactor):
        event = Event(time, reactor, EVENT_PACKET_TIMEOUT)
        return event
        
'''
    [Zilong]
    Why we need a separate class Reactor.
    All the event actions should be handled in each Class?
'''
# class Reactor:
#     def __init__(self, name):
#         self.name = name
# 
#     def react_to_event_a(self):
#         print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'event_a')
# 
#     def react_to_event_b(self):
#         print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'event_b')
# 
#     def react_to_event_c(self):    
#         print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'event_b')