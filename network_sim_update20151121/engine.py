'''
    Simulation Engine (Event Priority Queue)
'''

import heapq
import record
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
        '''
            [Zilong]
            Fixed a bug here.
            Original: self.curTime += event.time
        '''
        self.curTime = event.time
        event.execute()

    def run(self):
        while len(self.queue) > 0 and self.curTime < self.MAXTIME:
            self.execute_top()