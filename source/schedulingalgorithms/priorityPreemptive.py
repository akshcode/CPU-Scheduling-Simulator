from source.utils.test import processes
import source.utils.table as table
import source.utils.graph as graph


def run(processes):
    print('running priority scheduling algotithm (preemptive)...')

    gantt = []

    # Initialising the variables
    totalTurnaroundTime = 0
    totalCompletionTime = 0
    totalWaitingTime = 0
    totalResponseTime = 0

    noOfProcesses = len(processes)

    # Sorting the processes on the basis of arrival time
    sortedOne = sorted(processes, key=lambda x: x.arrivalTime)

    readyQueue = []

    # creating the burst array so that we can retrieve the burst time of processes in last
    burstArray = []
    for i in range(noOfProcesses):
        burstArray.append(sortedOne[i].burstTime)

    next = 0  #index of next process which will get inserted in 'readyQueue'
    indexOfCurr = -1  # Index of the current process which is being executed
    preComp = 0  # Point of time from where current process is getting executed
    done = 0  # number of processes executed till now
    start = [] # used to tell whether processes had executed earlier or not
   
    for i in range(noOfProcesses):
        start.append(False)

    while done < noOfProcesses:
        flag = False
        while next < noOfProcesses and totalCompletionTime >= sortedOne[next].arrivalTime:
            flag = True
            readyQueue.append([next, [sortedOne[next].priority, sortedOne[next].burstTime]])
            next += 1

        if flag:
            readyQueue = sorted(readyQueue, key=lambda k: k[1][0])

        index = readyQueue[0][0]

        if indexOfCurr != -1 and indexOfCurr != index:
            gantt.append(
                (sortedOne[indexOfCurr].p_id, (preComp, totalCompletionTime - preComp)))
            preComp = totalCompletionTime
            indexOfCurr = index
        elif indexOfCurr == -1:
            indexOfCurr = index
            preComp = totalCompletionTime

        if not start[index]:
            start[index] = True
            # Response Time
            sortedOne[index].responseTime = totalCompletionTime - \
                sortedOne[index].arrivalTime
            totalResponseTime += sortedOne[index].responseTime

        # Check whether this process will be executed fully first and then a new process will come
        fully = False
        if next == noOfProcesses:
            fully = True
        else:
            t1 = sortedOne[next].arrivalTime - totalCompletionTime
            t2 = sortedOne[index].burstTime
            if t2 <= t1:
                fully = True

        if fully == True:
            # Process with index 'index' will be executed fully
            sortedOne[index].completionTime = totalCompletionTime + \
                sortedOne[index].burstTime
            sortedOne[index].turnaroundTime = sortedOne[index].completionTime - \
                sortedOne[index].arrivalTime
            sortedOne[index].waitingTime = sortedOne[index].turnaroundTime - \
                sortedOne[index].burstTime

            # Updating total
            totalCompletionTime = sortedOne[index].completionTime
            totalTurnaroundTime += sortedOne[index].turnaroundTime
            totalWaitingTime += sortedOne[index].waitingTime

            readyQueue.pop(0)  # First element popped
            done += 1  
            if done != noOfProcesses and len(readyQueue) == 0:
                    totalCompletionTime = sortedOne[next].arrivalTime

        else:
            # Find how much it will run
            how_much = sortedOne[next].arrivalTime - totalCompletionTime

            readyQueue[0][1][1] -= how_much

            # Updating total
            totalCompletionTime += how_much

    # while loop ends here
    if totalCompletionTime != preComp:
        gantt.append(
            (sortedOne[indexOfCurr].p_id, (preComp, totalCompletionTime - preComp)))

    return {
        'name': 'PR-P',
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

