"""
        Shortest Remaining Time First (SJF Preemptive Version)
"""

from source.utils.test import processes
import source.utils.table as table
import source.utils.graph as graph


def run(processes):

    print('running shortest remaining time first algorithm...')

    # Creating an empty list for the gantt chart
    gantt = []

    # Initialisation
    totalTurnaroundTime = 0
    totalCompletionTime = 0
    totalWaitingTime = 0
    totalResponseTime = 0

    noOfProcesses = len(processes)

    # Sorting on the basis of arrival time
    sortedOne = sorted(processes, key=lambda x: x.arrivalTime)

    readyQueue = []
    
    next = 0  # Tells the index of next process which will get inserted in 'readyQueue'
    indexOfCurr = -1  # Index of the current process which is being executed
    prevComp = 0  # Point of time from where current process is getting executed
    done = 0  # no of processes that have executed completely
    start = []  # Used to tell whether process had executed earlier or not

    for i in range(noOfProcesses):
        start.append(False)

    while done != noOfProcesses:
        flag = False
        while next < noOfProcesses and totalCompletionTime >= sortedOne[next].arrivalTime:
            flag = True
            readyQueue.append([next, sortedOne[next].burstTime])
            next += 1

        if flag:
            readyQueue = sorted(readyQueue, key=lambda k: k[1])

        elem = readyQueue.pop(0)
        index = elem[0]

        if indexOfCurr != -1 and indexOfCurr != index:
            gantt.append(
                (sortedOne[indexOfCurr].p_id, (prevComp, totalCompletionTime - prevComp)))
            prevComp = totalCompletionTime
            indexOfCurr = index
        elif indexOfCurr == -1:
            indexOfCurr = index
            prevComp = totalCompletionTime

        if not start[index]:
            start[index] = True
            # Response Time
            sortedOne[index].responseTime = totalCompletionTime - \
                sortedOne[index].arrivalTime
            totalResponseTime += sortedOne[index].responseTime

        inside = False
        while elem[1] > 0 and not inside:
            elem[1] -= 1
            totalCompletionTime += 1
            while next < noOfProcesses and sortedOne[next].arrivalTime <= totalCompletionTime:
                inside = True
                readyQueue.append([next, sortedOne[next].burstTime])
                next += 1

        if elem[1] != 0:
            readyQueue.append(elem)
        else:
            sortedOne[index].completionTime = totalCompletionTime
            sortedOne[index].turnaroundTime = sortedOne[index].completionTime - \
                sortedOne[index].arrivalTime
            sortedOne[index].waitingTime = sortedOne[index].turnaroundTime - \
                sortedOne[index].burstTime

            # Updating total
            totalTurnaroundTime += sortedOne[index].turnaroundTime
            totalWaitingTime += sortedOne[index].waitingTime

            done += 1

            if done != noOfProcesses and len(readyQueue) == 0:
                gantt.append(
                    (sortedOne[indexOfCurr].p_id, (prevComp, totalCompletionTime - prevComp)))
                totalCompletionTime = sortedOne[next].arrivalTime
                readyQueue.append([next, sortedOne[next].burstTime])
                index = next
                indexOfCurr = next
                prevComp = totalCompletionTime
                next += 1

        readyQueue = sorted(readyQueue, key=lambda b: b[1])

# while loop ends here
    if totalCompletionTime != prevComp:
        gantt.append(
            (sortedOne[indexOfCurr].p_id, (prevComp, totalCompletionTime - prevComp)))

    return {
        'name': 'SRTF',
        'avgTurnaroundTime': totalTurnaroundTime / len(processes),
        'avgWaitingTime':    totalWaitingTime / len(processes),
        'avgResponseTime': totalResponseTime / len(processes),
        'processes': sortedOne,
        'gantt': gantt
    }


def main():
    result = run(processes)
    print("Avg Waiting Time: {}".format(result['avgWaitingTime']))
    print("Avg Turnaround Time: {}".format(result['avgTurnaroundTime']))
    print("Avg Response Time: {}".format(result['avgResponseTime']))
    table.plot(result['processes'])
    graph.plotGantt(result)


if __name__ == '__main__':
    main()
