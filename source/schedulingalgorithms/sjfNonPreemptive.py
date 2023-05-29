"""
        SJF (Shortest Job First) (Non-Preemptive)
"""

from source.utils.test import processes
import source.utils.table as table
import source.utils.graph as graph


def run(processes):

    print('running shortest job first algorithm.....')

    # Creating an empty list for the gantt chart
    gantt = []

    # Initialising variables
    totalCompletionTime = 0
    totalWaitingTime = 0
    totalResponseTime = 0
    totalTurnaroundTime = 0

    # Sorting the processes on basis of arrival time
    sortedOne = sorted(processes, key=lambda x: x.arrivalTime)

    # Calculating info about all processes
    for i in range(len(sortedOne)):
        index = -1  # process which is to be executed
        burstSorted = []

        for j in range(i, len(sortedOne)):
            # Getting all the processes who has arrived till the totalCompletionTime
            if sortedOne[j].arrivalTime <= totalCompletionTime:
                burstSorted.append((j, sortedOne[j].burstTime))

        # Sorting all the processes in the list according to the burst time
        burstSorted = sorted(burstSorted, key=lambda x: x[1])

        # If there are no elements in the sorted burst array
        if len(burstSorted) == 0:
            index = i
            for j in range(i + 1, len(sortedOne)):
                if sortedOne[j].arrivalTime == sortedOne[index].arrivalTime and sortedOne[j].burstTime < sortedOne[index].burstTime:
                    index = j
        else:
            index = burstSorted[0][0]

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

        # Update Total
        totalCompletionTime = sortedOne[index].completionTime
        totalTurnaroundTime += sortedOne[index].turnaroundTime
        totalWaitingTime += sortedOne[index].waitingTime
        totalResponseTime += sortedOne[index].responseTime

        # swapping
        sortedOne[i], sortedOne[index] = sortedOne[index], sortedOne[i]

    return {
        'name': 'SJF',
        'avgWaitingTime': totalWaitingTime / len(sortedOne),
        'avgResponseTime': totalResponseTime / len(sortedOne),
        'avgTurnaroundTime': totalTurnaroundTime / len(sortedOne),
        'processes': sortedOne,
        'gantt': gantt
    }


# If this file is executed directly -> run temporary test-cases
def main():
    result = run(processes)
    print("Avg Waiting Time: {}".format(result['avgWaitingTime']))
    print("Avg Turnaround Time: {}".format(result['avgTurnaroundTime']))
    print("Avg Response Time: {}".format(result['avgResponseTime']))
    table.plot(result['processes'])
    graph.plotGantt(result)


if __name__ == '__main__':
    main()
