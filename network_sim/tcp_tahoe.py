from constants import *
from events import *
from math import floor
import collections

class TcpTahoe:
    
    def __init__(self):
        self.refresh_ratio = 0.5
        self.lastACKID = -1
        self.duplicate_pck_id = -1
        self.duplicate_count = 0
        self.ssthresh = 200
        self.first_acked = True
        self.window_size = 150
        self.rtt = 0
        self.time_out = 20
        self.onTheFly = collections.deque()
#         self.time_out_event = None
        
    def setFlow(self, flow):
        self.flow = flow
        self.engine = self.flow.engine
        
    def react_to_flow_start(self, event):
        self.send_new_packets()
        
    def sendPacket(self, pck_id):
        if pck_id < self.flow.amount:
            packet = self.flow.generatePacket(pck_id)
            self.flow.sourceSend(packet)
            '''
                Create Timeout Event for every packet
            '''
            event = Event.CreateEventPacketTimeOut(self.engine.getCurrentTime() + self.time_out, self.flow, pck_id)
            self.engine.push_event(event)
            
    def send_new_packets(self):
#         send_flag = False
        while len(self.onTheFly) <= self.window_size:
#             send_flag = True
            if len(self.onTheFly) == 0: 
                self.sendPacket(self.lastACKID+1)
                self.onTheFly.append(self.lastACKID+1)
            else:
                self.sendPacket(self.onTheFly[-1] + 1)
                self.onTheFly.append(self.onTheFly[-1] + 1)
                
#         if send_flag and not self.time_out_event:
#             self.reset_timer()
    
    def react_to_time_out(self, event):
#         if event == self.time_out_event:
#             self.react_to_time_out_func()
        if event.pck_id <= self.lastACKID:
            pass
        else:
            print '[TCP]: Packet Time Out!'
            self.react_to_time_out_func()
    
    def react_to_time_out_func(self):
        print '[TCP]: Time Out Handled!'
        self.ssthresh = max(self.window_size / 2, 2)
        self.change_window_size(1)
             
#         if len(self.onTheFly) > 0:
#             self.reset_timer()
        self.onTheFly.clear()
            
        self.send_new_packets()
#         self.last_reset = self.engine.getCurrentTime()

    def change_window_size(self, new_window_size):
        self.window_size = new_window_size
        self.engine.recorder.record_window_size(self.flow, self.engine.getCurrentTime(), self.window_size)
        
    def react_to_routing_table_update(self, event):
        print "{} start to update rt at [{}]".format(self.name, self.engine.getCurrentTime())
        self.broadcastRequestPacket() 
        event = Event(self.engine.getCurrentTime() + self.updateTime, self, EVENT_ROUTINGTABLE_UPDATE)
        self.engine.push_event(event)   

#     def reset_timer(self):
#         event = Event(self.engine.getCurrentTime() + self.time_out, self.flow, EVENT_PACKET_TIMEOUT)
#         self.time_out_event = event
#         self.engine.push_event(event)
                
    def react_to_ack(self, ack_packet):
        
        '''
            Compute for new time_out
        '''
        if self.first_acked:
            self.rtt = self.engine.getCurrentTime() - ack_packet.timestamp
            self.first_acked = False
        else:
            cur_rtt = self.engine.getCurrentTime() - ack_packet.timestamp
            self.rtt = cur_rtt * self.refresh_ratio + self.rtt * (1 - self.refresh_ratio)
        
        self.time_out = self.rtt * 5
        if self.time_out < 10:
            self.time_out = 10
        
        
        id = ack_packet.pck_id

        if id <= self.lastACKID:
            pass
        else:
            '''
                Handle Duplicate Ack
            '''
            if id == self.duplicate_pck_id:
                self.duplicate_count = self.duplicate_count + 1
            else:
                self.duplicate_pck_id = id
                self.duplicate_count = 1
            

            if self.duplicate_count == 3:
                '''
                    Handle the situation that has 3 duplicate ack packets
                '''
                self.react_to_time_out_func()
            else:                
                '''
                    Increase the window size according to current status
                '''
                if self.window_size < self.ssthresh:
                    self.change_window_size(self.window_size + 1)
                else:
                    self.change_window_size(self.window_size + (1.0 / self.window_size))
                
                '''
                    Pop out all packets that should already been Acked
                '''
                self.lastACKID  = max(self.lastACKID, id - 1)
                while len(self.onTheFly) > 0 and self.onTheFly[0] <= self.lastACKID:
                    self.onTheFly.popleft()
                
                '''
                    Start to send new packets
                '''
                self.send_new_packets()
                
                self.engine.recorder.record_pkts_received(self.flow, self.engine.getCurrentTime(), self.lastACKID)     