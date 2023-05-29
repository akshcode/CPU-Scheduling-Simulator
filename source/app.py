import source.schedulingalgorithms.fcfs as fcfs
import source.schedulingalgorithms.sjfNonPreemptive as sjf
import source.schedulingalgorithms.priorityNonPreemptive as priority
import source.schedulingalgorithms.priorityPreemptive as priorityPreemptive
import source.schedulingalgorithms.roundRobin as rr
import source.schedulingalgorithms.sjfPreemptive as srtf

from source.utils.test import processes
import source.utils.graph as graph
import source.utils.table as table

# the main logic
def main():
    """
        - This function runs sample (random) testcase with 7 process to demonstrate the app
        - Plots the gantt chart for each algorithm
        - Plots the comparision graph for different schedulingalgorithms

    """
    rs_fcfs = fcfs.run(processes)
    rs_sjf = sjf.run(processes)
    rs_pr = priority.run(processes)
    rs_prp = priorityPreemptive.run(processes)
    rs_srtf = srtf.run(processes)
    rs_rr = rr.run(processes)

    print('\n FCFS')
    table.plot(rs_fcfs['processes'])
    graph.plotGantt(rs_fcfs)
    graph.plotTheGraph(rs_fcfs)

    print('\n SJF')
    table.plot(rs_sjf['processes'])
    graph.plotGantt(rs_sjf)
    graph.plotTheGraph(rs_sjf)

    print('\n PR')
    table.plot(rs_pr['processes'])
    graph.plotGantt(rs_pr)
    graph.plotTheGraph(rs_pr)

    print('\n PRP')
    table.plot(rs_prp['processes'])
    graph.plotGantt(rs_prp)
    graph.plotTheGraph(rs_prp)

    print('\n SRTF')
    table.plot(rs_srtf['processes'])
    graph.plotGantt(rs_srtf)
    graph.plotTheGraph(rs_srtf)

    print('\n RR')
    table.plot(rs_rr['processes'])
    graph.plotGantt(rs_rr)
    graph.plotTheGraph(rs_rr)

    graph.plotComparison(
        [rs_fcfs, rs_sjf, rs_srtf, rs_pr, rs_prp, rs_rr])


if __name__ == '__main__':
    main()
