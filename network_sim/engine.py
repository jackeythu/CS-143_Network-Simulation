'''
    Simulation Engine (Event Priority Queue)
'''

import heapq
import record
from element import DataPacket

class SimEngine:
    def __init__(self, maxtime):
        self.queue = []
        self.MAXTIME = maxtime
        self.curTime = 0
        self.recorder = record.Record()
        
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
        self.curTime = event.time
#         with open('L1_buffer1', 'a') as myFile:
#             myFile.write('[{}]: {}, {}\n'.format(event.time, event.type, event.reactor.name))
        event.execute()
#         print event.type, event.reactor.name
#         with open('L1_buffer1', 'a') as myFile:
# #             myFile.write('!!!{}, {}\n'.format(event.type, event.reactor.name))
#             myFile.write('b1\n')
#             for time, packet in self.parse.links['L1'].buffer1.buffer:
#                 if isinstance(packet, DataPacket):
#                     myFile.write('{}, {}\n'.format(time, packet.pck_id))
#             myFile.write('b2\n')
#             for time, packet in self.parse.links['L1'].buffer2.buffer:
#                 if isinstance(packet, DataPacket):
#                     myFile.write('{}, {}\n'.format(time, packet.pck_id))        
#             myFile.write('**********************\n')

            


    def run(self):
        while len(self.queue) > 0 and self.curTime < self.MAXTIME:
            
            self.execute_top()
#             print "!!!",self.curTime
            
            
            
            
            