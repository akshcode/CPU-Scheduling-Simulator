"""
        Priority Scheduling (Non-Preemptive)
"""

from source.utils.test import processes
import source.utils.graph as graph
import source.utils.table as table

# Priority is selected on the basis that lower number means higher priority
def run(processes):
    print('running non preemptive priority scheduling algorithm')
    gantt = []

    # Initiaising the variables
    totalTurnaroundTime = 0
    totalCompletionTime = 0
    totalWaitingTime = 0
    totalResponseTime = 0

    # Sorting the processes on the basis of arrival time
    sortedOne = sorted(processes, key=lambda x: x.arrivalTime)

    for i in range(len(sortedOne)):
        #process which is to be executed
        index = -1
        prioritySorted = []
        for j in range(i, len(sortedOne)):
            if sortedOne[j].arrivalTime <= totalCompletionTime:
                prioritySorted.append((j, sortedOne[j].priority))

        # sorting the arrived processes on the basis of priority
        prioritySorted = sorted(prioritySorted, key=lambda x: x[1])

        if len(prioritySorted) == 0:
            index = i
            for j in range(i + 1, len(sortedOne)):
                if sortedOne[j].arrivalTime == sortedOne[index].arrivalTime and sortedOne[j].priority < sortedOne[index].priority:
                    index = j
        else:
            index = prioritySorted[0][0]

        # If there is a process with already greater arrival time than the total completion time
        if sortedOne[index].arrivalTime > totalCompletionTime:
            totalCompletionTime = sortedOne[index].arrivalTime

        sortedOne[index].completionTime = totalCompletionTime + \
            sortedOne[index].burstTime
        sortedOne[index].turnaroundTime = sortedOne[index].completionTime - \
            sortedOne[index].arrivalTime
        sortedOne[index].waitingTime = sortedOne[index].turnaroundTime - \
            sortedOne[index].burstTime
        sortedOne[index].responseTime = totalCompletionTime - sortedOne[index].arrivalTime

        gantt.append(
            (sortedOne[index].p_id, (totalCompletionTime, sortedOne[index].burstTime)))

        # Updating the total values
        totalCompletionTime = sortedOne[index].completionTime
        totalTurnaroundTime += sortedOne[index].turnaroundTime
        totalWaitingTime += sortedOne[index].waitingTime
        totalResponseTime += sortedOne[index].responseTime

        # this will happen in the case when priority sorted list is empty and index is not equal to i
        sortedOne[i], sortedOne[index] = sortedOne[index], sortedOne[i]

    return {
        'name': 'Priority-Non Preemptive',
        'avgTurnaroundTime': totalTurnaroundTime / len(sortedOne),
        'avgWaitingTime': totalWaitingTime / len(sortedOne),
        'avgResponseTime': totalResponseTime / len(sortedOne),
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
