'''
CMSC 125 : Machine Problem 3: Memory Management and Allocation Strategies
Programmed by: Dianne M. Mondido

'''

class JobInfo:
    def __init__(self, jobStream, jobTime, jobSize):
        self.__jobStream = jobStream
        self.__jobTime = jobTime
        self.__jobSize = jobSize
    
    def jobStream(self):
        return self.__jobStream

    def jobTime(self):
        return self.__jobTime

    def jobSize(self):
        return self.__jobSize
    
    def updateTime(self):
        self.__jobTime -= 1
        if self.__jobTime <= 0:
            self.__jobTime = 0

     

class MemoryBlock:
    def __init__(self, memoryBlock, memorySize):
        self.__memoryBlock = memoryBlock
        self.__memorySize = memorySize
    
    def memoryBlock(self):
        return self.__memoryBlock
    
    def memorySize(self):
        return self.__memorySize



# First Fit Memory Allocation
class FirstFit:
    def __init__(self, memory:[MemoryBlock], job:[JobInfo]):
        self.__memory = memory
        self.__job = job
        self.__allocation = {}  # ({memory : job})
        self.__jobCount = 0     # For the total assigned jobs
        self.__totalTime = 140  # total time from the given jobs based on the MP3
        self.__timer = 1        # For the time
        self.__sumIF = {}       # Total Internal Fragmentation per block ({ memory : job })
        self.__sumBlock = 0  
        self.__totalHUP = {}    # Total Heavily Used Partition ({ memoryBlock : jobSize })
        self.__totalUP = {}     # Total Unused Partition ({ memoryBlock : differenceSize})
        self.__totalWT = 0
       
    
    # This is for the internal fragmentation portion
    def sumIF(self, memory:MemoryBlock, job:JobInfo):
        self.__sumBlock = 0

        # This is for the initial allocation of jobs at time 1
        if memory.memoryBlock() not in self.__sumIF:
            self.__sumBlock = (memory.memorySize() - job.jobSize()) + self.__sumBlock
            self.__sumIF.update({memory.memoryBlock() : self.__sumBlock})
            self.__totalHUP.update({memory.memoryBlock() : job.jobSize()})
            self.__totalUP.update({memory.memoryBlock() : self.__sumBlock})
            
        # This is for the proceeding allocation of jobs after time 1
        else:
            if job.jobStream() not in self.__allocation.values():
                temp = memory.memorySize() - job.jobSize()
                self.__sumBlock = temp + self.__sumIF[memory.memoryBlock()]
                self.__sumIF.update({memory.memoryBlock() : self.__sumBlock})
                # If current jobSize <= value, change the value on that key to the least size.
                # Since the least jobSize means it is the most heavily used partition of that memory
                if job.jobSize() <= self.__totalHUP[memory.memoryBlock()] :
                    self.__totalHUP.update({memory.memoryBlock() : job.jobSize()})
                # If temp <= value, change the value on that key to the least size.
                # Since the least difference of memorySize and jobSize means it is not mostly used
                if temp <= self.__totalUP[memory.memoryBlock()] :
                    self.__totalUP.update({memory.memoryBlock() : temp})

    def firstFit(self):
        tempList = self.__job
        countJob = 0
        print(f'\n------------------- AT TIME t = {str(self.__timer)} -------------------')
        for job in tempList:
            for memory in self.__memory:
                # If memorySize >= jobSize, then allocate it to the self.__allocation dict, 
                # and then break the current loop
                if memory.memorySize() >= job.jobSize():
                    if memory not in self.__allocation:
                        self.__allocation.update({memory : job})
                        self.sumIF(memory,job)
                        self.__jobCount += 1
                        break
        
        for key,value in self.__allocation.items():
            self.__totalWT += value.jobTime()
            print(f'Job {str(value.jobStream())} has been allocated in memory block {str(key.memoryBlock())} and will reside for {str(value.jobTime())} ms')
            
                    
        
        while len(tempList) -1 >= 2:
            self.__timer += 1
            print(f'\n------------------- AT TIME t = {str(self.__timer)} -------------------')
            for memory,job in self.__allocation.items():
                # If value from the dictionary is not empty,
                # Then proceed to this statement
                if job != None:
                    job.updateTime()
                    if job.jobTime() > 0:
                        self.__jobCount += 1
                    # If time == 1, then remove it from the jobList named tempList
                    # Also remove the value from the self.__allocation dictionary
                    else:
                        tempList.remove(job)
                        self.__allocation.update({memory:None})
                        # Search a new job to allocate that memory.
                        for job2 in tempList:
                            if job2 not in self.__allocation.values():
                                # If it finds a memory allocation, then we update our dictionary value
                                if memory.memorySize() >= job2.jobSize():
                                    countJob += 1
                                    self.__allocation.update({memory : job2})
                                    self.sumIF(memory,job2)
                                    self.__jobCount += 1
                                    break
                else:
                    continue
            for key,value in self.__allocation.items():
                if value != None:
                    self.__totalWT += value.jobTime()
                    print(f'Job {str(value.jobStream())} has been allocated in memory block {str(key.memoryBlock())} and will reside for {str(value.jobTime())} ms')
                    
                    
        self.status()
            
    
    def status(self):
        print(f'\n===================================== FIRST FIT ===================================== ')
        print(f'AVERAGE THROUGHPUT (TOTAL ASSIGNED JOB COUNT/ TOTAL TIME: {str(round(self.__jobCount/self.__timer, 2))} jobs per unit of time')
        print(f'AVERAGE WAITING QUEUE (TOTAL WQ LENGTH/ TOTAL TIME: {str(round(self.__totalTime/self.__timer,2))} jobs per unit of time')
        print(f'AVERAGE WAITING TIME (TOTAL WT/ #JOBS): {str(round(self.__totalWT/self.__jobCount,2))} jobs per unit of time\n')
        print(f'TOTAL UNUSED PARTITION ((TOTAL USED MEMORY / 50000) * 100): {str(round(((sum(self.__totalUP.values()))/50000)*100, 2))}% out of 50,000 memory capacity')
        print(f'TOTAL HEAVILY USED PARTITION ((TOTAL EXHAUSTED MEMORY / 50000) * 100): {str(round(((sum(self.__totalHUP.values()))/50000)*100, 2))}% out of 50,000 memory capacity\n')
        print(f'----------------------------- INTERNAL FRAGMENTATION -----------------------------')
        print(f'Note: I.F. refers to free spaces in each allocation, where current job\'s size < block\'s size\n')

        for memory in self.__memory:
            print(f'Block {str(memory.memoryBlock())}\'s total internal fragmentation (sum[block.size - job.size]): {str(round(self.__sumIF[memory.memoryBlock()], 2))} units of memory')
            print(f'Block {str(memory.memoryBlock())}\'s average internal fragmentation (sum / totalTime): {str(round(self.__sumIF[memory.memoryBlock()]/self.__timer, 2 ))} units of memory per unit of time\n')
        

# Best Fit Memory Allocation:
# Note: They are somewhat similar to First Fit. The only difference is how it is allocated,
#       the dictionary keys and values, and the internal fragmentation calculation
class BestFit:
    def __init__(self, memory:[MemoryBlock], job:[JobInfo]):
        self.__memory = sorted(memory, key = lambda m:m.memorySize(), reverse = True)
        self.__job = job
        self.__allocation = {}  # ({job : memory})
        self.__jobCount = 0     # For the total assigned jobs
        self.__totalTime = 140  # constant based on the MP3 given jobs
        self.__timer = 1        # For the timer
        self.__sumBlock = 0
        self.__sumIF = {}       # Total Internal Fragmentation per block ({ memory : diffSize })
        self.__totalHUP = {}    # Total Heavily Used Partition ({ memoryBlock : jobSize })
        self.__totalUP = {}     # Total Unused Partition ({ memoryBlock : differenceSize})
        self.__totalWT = 0
    
    
    def sumIF(self, memory:MemoryBlock, job:JobInfo):
        self.__sumBlock = 0
        if memory.memoryBlock() not in self.__sumIF:
            self.__sumBlock = (memory.memorySize() - job.jobSize()) + self.__sumBlock
            self.__sumIF.update({memory.memoryBlock() : [self.__sumBlock]}) # value is a list because we are storing the job and memory size difference in that block
            self.__totalHUP.update({memory.memoryBlock() : job.jobSize()})
            self.__totalUP.update({memory.memoryBlock() : self.__sumBlock})
            
        else:
            temp = (memory.memorySize() - job.jobSize())
            # Since self.__sumIf value is a list, we will search if temp is reocurring, given that
            # it might not be finished on that time. This is to make the job and memory sizes unique
            if temp not in self.__sumIF[memory.memoryBlock()]:
                self.__sumIF[memory.memoryBlock()].append(temp)
            # Same concept with first fit
            if self.__totalHUP[memory.memoryBlock()] >= job.jobSize():
                self.__totalHUP.update({memory.memoryBlock() : job.jobSize()})
            if self.__totalUP[memory.memoryBlock()] >= temp:
                self.__totalUP.update({memory.memoryBlock() : temp})
            

    def bestFit(self):
        tempList = self.__memory
        print(f'\n------------------- AT TIME t = {str(self.__timer)} -------------------')
        for job in self.__job:
            bestBlock = 9999
            for memory in tempList:
                if memory.memorySize() >= job.jobSize():
                    diffSize = memory.memorySize() - job.jobSize()
                    # The least value of partition difference means that it is closely fit
                    # The smaller the difference, the better.
                    if diffSize <= bestBlock:
                        bestBlock = diffSize
                        if memory not in self.__allocation.values():
                            self.__allocation.update({job:memory})

        for key,value in self.__allocation.items():
            self.__totalWT += key.jobTime()
            print(f'Job {str(key.jobStream())} has been allocated in memory block {str(value.memoryBlock())} and will reside for {str(key.jobTime())} ms')
            self.sumIF(value,key)   # key = job and value = memory
            
        self.__jobCount += len(self.__allocation)

        while len(self.__allocation) >= 1:
            if len(self.__allocation) == 1 and list(self.__allocation.keys())[0].jobTime() - 1 == 0:
                break
            self.__timer += 1
            tempDict = {**self.__allocation}    # This is to avoid runtime error
            print(f'\n-------------------------- AT TIME t = {str(self.__timer)} --------------------------')
            for job,memory in tempDict.items():
                # If value from the dictionary is not empty,
                # Then proceed to this statement
                if job != None:
                    job.updateTime()    
                    if job.jobTime() > 0:
                        continue
                    # We remove first all jobs that are finished before allocating them
                    # This is to ensure that each free memory will be allocated for the best job
                    else:
                        self.__job.remove(job)
                        self.__allocation.pop(job)
            for job in self.__job:
                bestBlock = 9999
                if job not in self.__allocation:
                    for memory in tempList:
                        if memory.memorySize() >= job.jobSize():
                            diffSize = memory.memorySize() - job.jobSize()
                            if diffSize <= bestBlock:
                                bestBlock = diffSize
                                if memory not in self.__allocation.values():
                                    self.__allocation.update({job:memory})
            
            self.__jobCount += len(self.__allocation)

            for key,value in self.__allocation.items():
                self.__totalWT += key.jobTime()
                print(f'Job {str(key.jobStream())} has been allocated in memory block {str(value.memoryBlock())} and will reside for {str(key.jobTime())} ms')
                self.sumIF(value,key)

        self.status()
            
    
    def status(self):
        print(f'\n===================================== BEST FIT ===================================== ')
        print(f'AVERAGE THROUGHPUT (TOTAL ASSIGNED JOB COUNT/ TOTAL TIME: {str(round(self.__jobCount/self.__timer, 2))} jobs per unit of time')
        print(f'AVERAGE WAITING QUEUE (TOTAL WQ LENGTH/ TOTAL TIME: {str(round(self.__totalTime/self.__timer,2))} jobs per unit of time')
        print(f'AVERAGE WAITING TIME (TOTAL WT/ #JOBS): {str(round((self.__totalWT)/self.__jobCount,2))} jobs per unit of time\n')
        print(f'TOTAL UNUSED PARTITION ((TOTAL USED MEMORY / 50000) * 100): {str(round(((sum(self.__totalUP.values()))/50000)*100, 2))}% out of 50,000 memory capacity')
        print(f'TOTAL HEAVILY USED PARTITION ((TOTAL EXHAUSTED MEMORY / 50000) * 100): {str(round(((sum(self.__totalHUP.values()))/50000)*100, 2))}% out of 50,000 memory capacity\n')
        print(f'----------------------------- INTERNAL FRAGMENTATION -----------------------------')
        print(f'Note: I.F. refers to free spaces in each allocation, where current job\'s size < block\'s size\n')

        for memory in self.__memory:
            print(f'Block {str(memory.memoryBlock())}\'s total internal fragmentation (sum[block.size - job.size]): {str((sum(self.__sumIF[memory.memoryBlock()])))} units of memory')
            print(f'Block {str(memory.memoryBlock())}\'s average internal fragmentation (sum / totalTime): {str(round(sum(self.__sumIF[memory.memoryBlock()])/self.__timer, 2 ))} units of memory per unit of time\n')



# Worst Fit Memory Allocation
# Note: Similar to the Best Fit allocation, the only difference would be the allocation process.
class WorstFit:
    def __init__(self, memory:[MemoryBlock], job:[JobInfo]):
        self.__memory = sorted(memory, key = lambda m:m.memorySize(), reverse = True)
        self.__job = job
        self.__allocation = {}  # ({job : memory})
        self.__jobCount = 0     # For the total assigned jobs
        self.__totalTime = 140  # constant given in the description of MP
        self.__timer = 1        # For the timer
        self.__sumBlock = 0
        self.__sumIF = {}       # Total Internal Fragmentation per block ({ memory : diffSize })
        self.__sumBlock = 0  
        self.__totalHUP = {}    # Total Heavily Used Partition ({ memoryBlock : jobSize })
        self.__totalUP = {}     # Total Unused Partition ({ memoryBlock : differenceSize})
        self.__totalWT = 0
        self.__temp = job


    def sumIF(self, memory:MemoryBlock, job:JobInfo):
        self.__sumBlock = 0
        if memory.memoryBlock() not in self.__sumIF:
            self.__sumBlock = (memory.memorySize() - job.jobSize()) + self.__sumBlock
            self.__sumIF.update({memory.memoryBlock() : [self.__sumBlock]})
            self.__totalHUP.update({memory.memoryBlock() : job.jobSize()})
            self.__totalUP.update({memory.memoryBlock() : self.__sumBlock})

            
        else:
            temp = (memory.memorySize() - job.jobSize())
            if temp not in self.__sumIF[memory.memoryBlock()]:
                self.__sumIF[memory.memoryBlock()].append(temp)
            if self.__totalHUP[memory.memoryBlock()] >= job.jobSize():
                self.__totalHUP.update({memory.memoryBlock() : job.jobSize()})
            if self.__totalUP[memory.memoryBlock()] >= temp:
                self.__totalUP.update({memory.memoryBlock() : temp})
        


    def worstFit(self):
        tempList = self.__memory
        print(f'\n------------------- AT TIME t = {str(self.__timer)} -------------------')
        for job in self.__job:
            worstBlock = 0
            for memory in tempList:
                if memory.memorySize() >= job.jobSize():
                    diffSize = memory.memorySize() - job.jobSize()
                    # Instead of finding the least difference, the largest difference will be chosen
                    if diffSize >= worstBlock:
                        worstBlock = diffSize
                        if memory not in self.__allocation.values():
                            self.__jobCount += 1
                            self.__allocation.update({job:memory})
                        else:
                            worstBlock = 0
                    else:
                        worstBlock = diffSize
            
        for key,value in self.__allocation.items():
            self.__totalWT += key.jobTime()
            self.sumIF(value,key) 
            print(f'Job {str(key.jobStream())} has been allocated in memory block {str(value.memoryBlock())} and will reside for {str(key.jobTime())} ms')
                   
        while len(self.__allocation) >= 1:
            if len(self.__allocation) == 1 and list(self.__allocation.keys())[0].jobTime() - 1 == 0:
                break  
            self.__timer += 1
            tempDict = {**self.__allocation}
            print(f'\n-------------------------- AT TIME t = {str(self.__timer)} --------------------------')
            for job,memory in tempDict.items():
                if job != None:
                    job.updateTime()
                    if job.jobTime() > 0:
                        self.__jobCount += 1
                    else:
                        self.__job.remove(job)
                        self.__allocation.pop(job)
            for job2 in self.__job:
                worstBlock = 0
                if job2 not in self.__allocation:
                    for memory2 in tempList:
                        if memory2.memorySize() >= job2.jobSize():
                            diffSize = memory2.memorySize() - job2.jobSize()
                            if diffSize >= worstBlock:
                                worstBlock = diffSize
                                if memory2 not in self.__allocation.values():
                                    self.__jobCount += 1
                                    self.sumIF(memory2,job2)
                                    self.__allocation.update({job2:memory2})
                                else:
                                    worstBlock = 0
                            else:
                                worstBlock = diffSize
            
            for key,value in self.__allocation.items():
                self.sumIF(memory,job)
                self.__totalWT += key.jobTime()
                print(f'Job {str(key.jobStream())} has been allocated in memory block {str(value.memoryBlock())} and will reside for {str(key.jobTime())} ms')
            

        self.status()
            
    
    def status(self):
        print(f'\n===================================== WORST FIT ===================================== ')
        print(f'AVERAGE THROUGHPUT (TOTAL ASSIGNED JOB COUNT/ TOTAL TIME: {str(round(self.__jobCount/self.__timer, 2))} jobs per unit of time')
        print(f'AVERAGE WAITING QUEUE (TOTAL WQ LENGTH/ TOTAL TIME: {str(round(self.__totalTime/self.__timer,2))} jobs per unit of time')
        print(f'AVERAGE WAITING TIME (TOTAL WT/ #JOBS): {str(round((self.__totalWT + self.__totalTime) /self.__jobCount,2))} jobs per unit of time')
        print(f'TOTAL UNUSED PARTITION ((TOTAL USED MEMORY / 50000) * 100): {str(round(((sum(self.__totalUP.values()))/50000)*100, 2))}% out of 50,000 memory capacity')
        print(f'TOTAL HEAVILY USED PARTITION ((TOTAL EXHAUSTED MEMORY / 50000) * 100): {str(round(((sum(self.__totalHUP.values()))/50000)*100, 2))}% out of 50,000 memory capacity\n')
        print(f'----------------------------- INTERNAL FRAGMENTATION -----------------------------')
        print(f'Note: I.F. refers to free spaces in each allocation, where current job\'s size < block\'s size\n')

        for memory in self.__memory:
            try:
                print(f'Block {str(memory.memoryBlock())}\'s total internal fragmentation (sum[block.size - job.size]): {str((sum(self.__sumIF[memory.memoryBlock()])))} units of memory')
                print(f'Block {str(memory.memoryBlock())}\'s average internal fragmentation (sum / totalTime): {str(round(sum(self.__sumIF[memory.memoryBlock()])/self.__timer, 2 ))} units of memory per unit of time\n')
            except:
                print(f'Block {str(memory.memoryBlock())} was not allocated')



def main():

    memoryBlockList = []
    jobList = []
    
    with open('./memoryList.txt') as f:
        # read the header line first
        f.readline()
        # read each line
        for line in f.readlines():
            row = line.split()
            memoryBlockList.append(MemoryBlock(int(row[0]), int(row[1])))

    with open('./jobList.txt') as f:
        # read the header line first
        f.readline()
        # read each line
        for line in f.readlines():
            row = line.split()
            jobList.append(JobInfo(int(row[0]), int(row[1]), int(row[2])))


    print(f'Choose Algorithm [1] Worst Fit\t [2] Best Fit\t [3] First Fit')
    key = input("")
    if key == '1':
        wf = WorstFit(memoryBlockList, jobList).worstFit()
    elif key == '2':
        bf = BestFit(memoryBlockList, jobList).bestFit()
    elif key == '3':
        ff = FirstFit(memoryBlockList, jobList).firstFit()
    else:
        print("Invalid Key. Please try again.\n")

main()
