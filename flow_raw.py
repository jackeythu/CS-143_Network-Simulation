import time
from main_loop import queue # import the main loop

PACKET_SIZE = 16
PACKET_TIMEOUT = 1000

class Flow():
    '''
    Flow is responsible for data transmission control
    :param ID: flow ID
    :param Host* source: specify the source (Host)
    :param Host* destination: specify the destination (Host)
    :param int data_size: the size of data to be transmitted
    :param int algorithm: specify which congestion control algorithm to be used
    '''
    def __init__(self, env, ID, source, destination, data_size, algorithm = 0, count = 0, expeckted):
        self.ID = ID
        self.source = source
        self.destination = destination
        self.data_size = data_size
        self.expected = data_size / PACKET_SIZE
        self.algorithm = algorithm
        self.count = count
    
    def make_packet(self):
        '''
        make packet according to data_size, return an Array of packets
        '''
        packet = Packet(flow_ID = self.ID,
                        source = self.source,
                        destination = self.destination,
                        timestamp = time.time,
                        type = 'Data')
        return packet
    
    def send_packet(self, packet, type):
        '''
        Add send event to mainLoop
        '''
        queue.add(command_send(packet, self.source, self.destination, type))
    
    def receive_packet(self, packet):
        '''
        forward data packet to its destination
        forward routing packet to the corresponding router
        '''
        if (packet.type == 'Data' or packet.type == 'Routing'):
            send_packet(packet, packet.type)
        elif (packet.type == 'ACK'):
            if (packet.destination = self.source):
                count = count + 1
            else:
               send_packet(packet, packet.type) 
    
    def timeout_retrans(self, packet):
        '''
        Handle the situation while time out
        '''
        if (time.time() - packet.timestamp > PACKET_TIMEOUT):
            send_packet(packet)