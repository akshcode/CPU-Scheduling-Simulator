# Defining the Process Class
class Process:
    """
    Arguments:
    1) p_id - ID of the process
    2) arrivalTime - Time at which process arrives
    3) burstTime - CPU Time
    4) priority - Priority of the process (by default 1)

    """

    def __init__(self, p_id, arrivalTime, burstTime, priority=1):
        self.p_id = p_id
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.priority = priority

        self.waitingTime = 0
        self.completionTime = 0
        self.turnaroundTime = 0
        self.responseTime = 0
        self.completed = False
