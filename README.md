# CMSC-123--Memory-Management-and-Allocation-Strategies
Lab Exercise 3 - On Memory Management and Allocation Strategies
At one large batch-processing computer installation, the management wants to decide what storage placement strategy will yield the best possible performance. The installation runs a large real storage computer under **fixed partition multiprogramming**. Each user program runs in a single group of **contiguous storage locations**. Users state their storage requirements and time units for CPU usage on their Job Control Card (it used to, and still does work this way, although cards are not used nowadays). The OS allocates to each user the appropriate partition and starts up the user's job. The job remains in memory until completion. A total of 50,000 memory locations are available, divided into fixed blocks as indicated in the table above.
+a)Write an event-driven simulation to help you decide which storage placement strategy should be used at this installation. Your program would use the job stream and memory partitioning as indicated. Run the program until all jobs have been executed with the memory as is (in order by address). This will give you the **first-fit** type performance results.
+b) Do the same as (a), but this time implement the **worst-fit** placement scheme.
+c)Sort the memory partitions by size and run the program a second time; this will give you the **best-fit** performance results. For all parts (a),  (b) and (c) you are investigating the performance of the system using a typical job stream by measuring: 
1.Throughput (how many jobs are processed per given time unit) 
2. Storage utilization (percentage of partitions never used, percentage of partitions heavily used, etc.) 
3. Waiting queue length 
4. Waiting time in queue 
5. Internal fragmentation
d)Look at the results from the first-fit, worst-fit and best-fit. Explain what the results indicate about the performance of the system for this job mix and memory organization. Is one method of partitioning better than the other? Why or why not? Could you recommend one method over the other based on your sample run? Would this hold in all cases? Write some conclusions and recommendations.
