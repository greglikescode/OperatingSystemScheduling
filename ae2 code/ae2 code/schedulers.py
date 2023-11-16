import math

from des import SchedulerDES
from event import Event, EventTypes
from process import ProcessStates

#EDIT

class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        for p in self.processes:
            if cur_event.process_id == p.process_id:
                if cur_event.event_type == EventTypes.PROC_CPU_DONE:
                    return self.processes[p.process_id+1]
                else:
                    return self.processes[p.process_id]

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        run_time = cur_process.run_for(self.quantum,self.time)
        self.time += run_time
        if cur_process.remaining_time <= 0:
            cur_process.process_state = ProcessStates.TERMINATED
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=self.time)
        else:
            cur_process.process_state = ProcessStates.READY
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ, event_time=self.time)
                    



class SJF(SchedulerDES):

    def scheduler_func(self, cur_event):
        # print(cur_event)
        if cur_event.event_type == EventTypes.PROC_ARRIVES:
            shortest_process = None
            for p in self.processes:
                if p.process_state == ProcessStates.READY:
                    if shortest_process == None or p.service_time < shortest_process.service_time:
                        shortest_process = p
            return shortest_process
        else:
            return self.processes[cur_event.process_id]


    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        run_time = cur_process.run_for(self.quantum,self.time)
        self.time += run_time
        if cur_process.remaining_time <= 0:
            cur_process.process_state = ProcessStates.TERMINATED
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=self.time)
        else:
            cur_process.process_state = ProcessStates.READY
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ, event_time=self.time)


class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        for p in self.processes:
            if cur_event.process_id == p.process_id:
                if cur_event.event_type == EventTypes.PROC_CPU_DONE:
                    return self.processes[p.process_id+1]
                else:
                    return self.processes[p.process_id]


    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        run_time = cur_process.run_for(self.quantum,self.time)
        self.time += run_time
        if cur_process.remaining_time <= 0:
            cur_process.process_state = ProcessStates.TERMINATED
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=self.time)
        else:
            cur_process.process_state = ProcessStates.READY
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ, event_time=self.time)

count = 0

class SRTF(SchedulerDES):

    def scheduler_func(self, cur_event):
        shortest_process = None
        for p in self.processes:
            if p.process_state == ProcessStates.READY:
                if shortest_process == None or p.remaining_time < shortest_process.remaining_time:
                    shortest_process = p
        if shortest_process:
            return shortest_process
        else:
            return self.processes[cur_event.process_id+1]
        
    def dispatcher_func(self, cur_process):
        global count
        run_time = None
        cur_process.process_state = ProcessStates.RUNNING
        run_for = min([self.processes[p.process_id].arrival_time-self.time if p.process_state == ProcessStates.NEW else math.inf for p in self.processes])
        run_time = cur_process.run_for(run_for,self.time)
        self.time += run_time
        if cur_process.remaining_time <= 0:
            cur_process.process_state = ProcessStates.TERMINATED
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=self.time)
        else:
            cur_process.process_state = ProcessStates.READY
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ, event_time=self.time)

