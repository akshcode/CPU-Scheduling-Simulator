"""
        Round Robin Algorithm
"""


from source.utils.test import processes
import source.utils.table as table
import source.utils.graph as graph

# quantum is the time for which a process will run at once (no matter whatever it's burst time is)
def run(processes, quantum=2):

    print('running round robin algorithm...')

    gantt = []

    # Initialising the variables
    totalTurnaroundTime = 0
    totalCompletionTime = 0
    totalWaitingTime = 0
    totalResponseTime = 0

    noOfProcesses = len(processes)

    sortedOne = sorted(processes, key=lambda x: x.arrivalTime)

    readyQueue = []

    next = 1  # index of next process which will get inserted in readyQueue
    indexOfCurr = -1  # index of the current process which is executed
    prevComp = 0  # point of time from where current process is getting executed
    done = 0  # no of processes that are completed
    start = []  # used to tell whether processes with index 'next' had executed earlier or not
    
    for i in range(noOfProcesses):
        start.append(False)

    readyQueue.append([0, sortedOne[0].burstTime])

# looping until all processes get completed
    while done != noOfProcesses:
        firstElement = readyQueue.pop(0)
        index = firstElement[0]

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
            # Response Time (taking max as for first process arrival time cpulb be greater than 0)
            sortedOne[index].responseTime = max(
                0, totalCompletionTime - sortedOne[index].arrivalTime)
            totalResponseTime += sortedOne[index].responseTime

        currentBurst = firstElement[1]

        # as the process will run currently only for the quantum time
        for i in range(min(currentBurst, quantum)):
            totalCompletionTime += 1  # to indicate the completion of one time unit
            #  if there are any new processes that have arrived and can be added to the readyQueue
            while next < noOfProcesses and sortedOne[next].arrivalTime <= totalCompletionTime:
                readyQueue.append([next, sortedOne[next].burstTime])
                next += 1

        currentBurst -= min(currentBurst, quantum)

        if currentBurst == 0:
            sortedOne[index].completionTime = totalCompletionTime
            sortedOne[index].turnaroundTime = sortedOne[index].completionTime - \
                sortedOne[index].arrivalTime
            sortedOne[index].waitingTime = sortedOne[index].turnaroundTime - \
                sortedOne[index].burstTime

            # Updating the total values
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
        else:
            # if the process is not completed, again add it to the readyQueue
            readyQueue.append([index, currentBurst])

# while loop ends here!

# if the last process was interrupted before completing its burst time
    if totalCompletionTime != prevComp:
        gantt.append((sortedOne[indexOfCurr].p_id,
                     (prevComp, totalCompletionTime - prevComp)))
        
        


    return {
        'name': 'ROUND-RB',
        'avgTurnaroundTime': totalTurnaroundTime / len(processes),
        'avgWaitingTime': totalWaitingTime / len(processes),
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
