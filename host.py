from packet import dataPacket

class Host():
    def __init__(self, IP_address, link, flow):
        self.IP_address = IP_address
        self.link = link
        self.flow = flow
        
    def __str__(self):
        return "Host IP address:" + self.IP_address
    def send(self, packet):
        self.link.add(packet)
      
    def receive(self, packet):
        #event.value???
        if packet.destination == self.destination:
            if isinstance(packet, dataPacket):
                #if received packet is acknowledgement
                if packet.acknowledgement:
                    if packet.source == self.flow.destination and packet.destination == self.flow.source:
                        self.flow.ack_received(packet)
                #if host receives a dataPacket
                else:
                    if packet.source == self.flow.source and packet.destination == self.flow.destinaton:
                        self.flow.packet_received(packet)
            