
PACKET_SIZE = 1024 * 8

class packet():
    def __init__(self, source, destination, timestamp):
        self.source = source
        self.destination = destination
        self.timestamp = timestamp
        self.size = PACKET_SIZE
        
class dataPacket(packet):
    def __init__(self, source, destination, timestamp, acknowledgement, pck_id):
        super(dataPacket, self).__init__(source = source, destination = destination, timestamp = timestamp)
        self.acknowledgement = acknowledgement 
        self.pck_id = pck_id
                
class routerPacket(packet):
    def __init__(self, source, timestamp, routerTable, acknowledgement):
        super(routerPacket, self).__init__(source = source, destination = 0, timestamp = timestamp)
        self.routerTable = routerTable
        self.acknowledgement = acknowledgement
        