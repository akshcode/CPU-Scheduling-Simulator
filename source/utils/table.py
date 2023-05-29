"""
To display the processses in the tabular format
"""


def plot(processes):
    print('| PID | BURST_TIME | ARRIVAL_TIME | PRIORITY || RESPONSE_TIME | WAITING_TIME | TURNAROUND_TIME | '
          'COMPLETION_TIME |')

    for p in processes:
        print(
            "| {:3} |     {:3}    |     {:4}     |   {:4}   ||     {:3}       |      {:3}     |        {:3}      |    "
            " {:3}     |".format(
                p.p_id, p.burstTime, p.arrivalTime, p.priority, p.responseTime, p.waitingTime, p.turnaroundTime,
                p.completionTime))
