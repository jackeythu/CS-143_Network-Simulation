import collections
import events
class TcpFast():
    def __init__(self):
        self.alpha = 8
        self.gamma = 0.5
        self.windowSize = 4
        self.baseRTT = float('inf')
        self.onTheFly = collections.deque()
        self.lastACKID = -1
        self.validTimeOutEvent = None
        
    def setFlow(self, flow):
        self.flow = flow
        self.engine = self.flow.engine
        
    def setWindowSize(self, windowSize):
        self.windowSize = windowSize
        
    def sendNewPackets(self):
        while len(self.onTheFly) < self.windowSize:
            if len(self.onTheFly) == 0: 
                self.sendPacket(self.lastACKID+1)
                self.onTheFly.append(self.lastACKID+1)
            else:
                self.sendPacket(self.onTheFly[-1]+1)
                self.onTheFly.append(self.onTheFly[-1]+1)
            
    def sendPacket(self, pck_id):
        if pck_id < self.flow.amount:
            packet = self.flow.generatePacket(pck_id)
            self.flow.sourceSend(packet)
        
    def receiveACK(self, ackPacket):
        pck_id = ackPacket.pck_id
        self.lastACKID  = max(self.lastACKID, pck_id-1)
        while len(self.onTheFly) > 0 and self.onTheFly[0] <= self.lastACKID:
            self.onTheFly.popleft()
            
        
        
    def setTimeOutEvent(self, time):
        event = events.Event.CreateEventPacketTimeOut(time, self)
        self.validTimeOutEvent = event
        self.engine.push_event(event)
        
    def react_to_flow_start(self, event):
        self.sendPacket(0)
        
    def react_to_time_out(self, event):
        if event != self.validTimeOutEvent:
            return
        
        
        
    def react_to_ack(self, packet):
        self.receiveACK(packet)
        self.sendNewPackets()