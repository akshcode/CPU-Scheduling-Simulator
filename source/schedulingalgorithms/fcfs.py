"""
        First Come First Serve
"""

from source.utils.test import processes
import source.utils.table as table
import source.utils.graph as graph


def run(processes):
    print("running fcfs algorithm......")

    # Creating an empty list for the gantt chart
    gantt = []

    # Initialising variables
    totalCompletionTime = 0
    totalWaitingTime = 0
    totalResponseTime = 0
    totalTurnaroundTime = 0

    # Sorting on the basis of arrival time
    sortedOne = sorted(processes, key=lambda x: x.arrivalTime)

    # Calculating info about all processes
    for i in range(len(sortedOne)):
        
        # If there is a process with already greater arrival time than the total completion time
        if sortedOne[i].arrivalTime > totalCompletionTime:
            totalCompletionTime = sortedOne[i].arrivalTime

        # Calculate for each
        sortedOne[i].completionTime = totalCompletionTime + \
            sortedOne[i].burstTime
        sortedOne[i].turnaroundTime = sortedOne[i].completionTime - \
            sortedOne[i].arrivalTime
        sortedOne[i].waitingTime = sortedOne[i].turnaroundTime - \
            sortedOne[i].burstTime
        sortedOne[i].responseTime = totalCompletionTime - sortedOne[i].arrivalTime

        gantt.append(
            (sortedOne[i].p_id, (totalCompletionTime, sortedOne[i].burstTime)))

        # Updating all the values
        totalCompletionTime = sortedOne[i].completionTime
        totalTurnaroundTime += sortedOne[i].turnaroundTime
        totalWaitingTime += sortedOne[i].waitingTime
        totalResponseTime += sortedOne[i].responseTime

    return {
        'name': 'FCFS',
        'avgTurnaroundTime': totalTurnaroundTime / len(sortedOne),
        'avgWaitingTime': totalWaitingTime / len(sortedOne),
        'avgResponseTime': totalResponseTime / len(sortedOne),
        'processes': sortedOne,
        'gantt': gantt
    }


# If this file is executed directly -> run temporary test-cases
def main():
    result = run(processes)
    print("Average Waiting Time: {}".format(result['avgWaitingTime']))
    print("Average Turnaround Time: {}".format(result['avgTurnaroundTime']))
    print("Average Response Time: {}".format(result['avgResponseTime']))
    table.plot(result['processes'])
    graph.plotGantt(result)


if __name__ == '__main__':
    main()
