from constants import *

class Event:

    def __init__(self, time, reactor, type):
        self.time = time
        self.reactor = reactor
        self.type = type

    def execute(self):
#         print ""
#         print 'Time: [{}],'.format(self.time),
#         print 'Event type: [{}],'.format(self.type),
#         print 'Reactor: [{}] '.format(self.reactor.name)

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
        event.packet = packet
        return event 
    
    @staticmethod
    def CreateEventPacketTimeOut(time, reactor, pck_id=None):
        event = Event(time, reactor, EVENT_PACKET_TIMEOUT)
        event.pck_id = pck_id
        return event




