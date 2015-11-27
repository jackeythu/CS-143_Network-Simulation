import collections
import events

class TcpFast():
    def __init__(self):
        self.alpha = 8
        self.gamma = 0.125
        self.windowSize = 4
        self.baseRTT = float('inf')
        self.avgRTT = 0
        self.onTheFly = collections.deque()
        self.acknowledgedPacketID = -1
        self.validTimeOutEvent = None
        self.threshold = 128
        self.stateMachine = StateMachine(self)
        
    def setFlow(self, flow):
        self.flow = flow
        self.engine = self.flow.engine
        
    def setWindowSize(self, windowSize):
        self.windowSize = windowSize
        self.engine.recorder.record_window_size(self.flow, self.engine.getCurrentTime(), 
                                                self.windowSize)
        
    def sendNewPackets(self):
        while len(self.onTheFly) < self.windowSize:
            if len(self.onTheFly) == 0: 
                self.sendPacket(self.acknowledgedPacketID+1)
                self.onTheFly.append(self.acknowledgedPacketID+1)
            else:
                self.sendPacket(self.onTheFly[-1]+1)
                self.onTheFly.append(self.onTheFly[-1]+1)
            
    def sendPacket(self, pck_id):
        print "~~~~~~~~~~~~x",self.flow.amount
        if pck_id < self.flow.amount:
            print "send packet", pck_id
            packet = self.flow.generatePacket(pck_id)
            self.flow.sourceSend(packet)
            self.setTimeOutEvent(max(1, self.avgRTT))
        
    def receiveACK(self, ackPacket):
        pck_id = ackPacket.pck_id
        self.acknowledgedPacketID  = max(self.acknowledgedPacketID, pck_id-1)
        while len(self.onTheFly) > 0 and self.onTheFly[0] <= self.acknowledgedPacketID:
            self.onTheFly.popleft()
            
    def setTimeOutEvent(self, delay):
        event = events.Event.CreateEventPacketTimeOut(self.engine.getCurrentTime()+ delay, self.flow)
        self.validTimeOutEvent = event
        self.engine.push_event(event)
        
    def react_to_flow_start(self, event):
        self.sendPacket(0)
        
    def react_to_time_out(self, event):
        if event != self.validTimeOutEvent:
            return
        self.stateMachine.timeout()
            

    def react_to_ack(self, packet):
        RTT = self.engine.getCurrentTime() - packet.originalPacketTimestamp
        self.baseRTT = min(self.baseRTT,RTT)
        self.avgRTT = (1-self.gamma) * self.avgRTT + self.gamma * RTT
        print "!!!!!!!!!!!",self.baseRTT, RTT
#         windowSize = min(2*self.windowSize, (1-self.gamma)*self.windowSize + 
#                               self.gamma*(self.baseRTT/RTT*self.windowSize + self.alpha))
#         self.setWindowSize(windowSize)
        self.receiveACK(packet)
        self.stateMachine.ACK(packet, RTT)
        self.sendNewPackets()

class StateMachine(object):
    SLOW_START = 'slow_start'
    CONGESTION_CONTROL = 'congestion_control'
    FAST_RETRANSMIT = 'fast_retransmit'
    DONE = 'done'
    def __init__(self, algorithm):
        self.state = StateMachine.SLOW_START
        self.algorithm = algorithm
        self.lastAckID = -1
        self.dupTime = 0
        

        
    def ACK(self, ackPacket, RTT):
        print "ACK!!!!!!!!", ackPacket.pck_id
        if self.lastAckID == ackPacket.pck_id:
            self.dupTime += 1
        else:
            self.dupTime = 0
            self.lastAckID = ackPacket.pck_id
            
        if ackPacket == self.algorithm.flow.amount:
            self.state = StateMachine.DONE
            self.algorithm.setWindowSize(0)
            
        if self.state == StateMachine.DONE:
            return
        
    
        if self.state == StateMachine.SLOW_START:
            if self.dupTime <3:
                if self.algorithm.windowSize < self.algorithm.threshold:
                    self.algorithm.setWindowSize(self.algorithm.windowSize+1)
                else:
                    self.algorithm.setWindowSize(self.algorithm.windowSize+1.0/self.algorithm.windowSize)
                    self.state = StateMachine.CONGESTION_CONTROL
                return
            
            if self.dupTime >= 3:
                self.state = StateMachine.FAST_RETRANSMIT
                self.algorithm.threshold = self.algorithm.windowSize/2.0
                self.algorithm.setWindowSize(self.algorithm.windowSize/2.0+3)                
                self.algorithm.sendPacket(ackPacket.pck_id)                
                return
                
        if self.state == StateMachine.CONGESTION_CONTROL:
            if self.dupTime <3:
#                 self.algorithm.setWindowSize(self.algorithm.windowSize+1.0/self.algorithm.windowSize)
                windowSize = self.algorithm.windowSize
                windowSize = min(2*windowSize, (1-self.algorithm.gamma)*windowSize + 
                            self.algorithm.gamma*(self.algorithm.baseRTT/RTT*windowSize + self.algorithm.alpha))
                self.algorithm.setWindowSize(windowSize)
                return
            
            if self.dupTime >= 3:
                self.state = StateMachine.FAST_RETRANSMIT
                self.algorithm.threshold = self.algorithm.windowSize/2.0
                self.algorithm.setWindowSize(self.algorithm.windowSize/2.0+3)                
                self.algorithm.sendPacket(ackPacket.pck_id)
                return
                
            
            
            
        if self.state == StateMachine.FAST_RETRANSMIT:
                        
            if self.dupTime > 3:
                self.algorithm.setWindowSize(self.algorithm.windowSize+1)
            else:
                self.algorithm.setWindowSize(self.algorithm.threshold)
                self.state = StateMachine.CONGESTION_CONTROL
                
            return
            
            
            
    def timeout(self):
        print "timeout!!!!!!!!"
        self.algorithm.threshold = self.algorithm.windowSize/2
        self.algorithm.setWindowSize(1)
        self.state = StateMachine.SLOW_START
        self.algorithm.onTheFly = collections.deque()
        self.algorithm.sendNewPackets()
        
            
            
            

        