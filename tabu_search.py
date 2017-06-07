#-*- encoding: utf-8 -*-
import itertools
from copy import deepcopy
# b = copy.deepcopy(a)

JOB=[
    [4, 88],[8, 68],[6, 94],[5, 99],[1, 67],[2, 89],[9, 77],[7, 99],[0, 86],[3, 92],
    [5, 72],[3, 50],[6, 69],[4, 75],[2, 94],[8, 66],[0, 92],[1, 82],[7, 94],[9, 63],
    [9, 83],[8, 61],[0, 83],[1, 65],[6, 64],[5, 85],[7, 78],[4, 85],[2, 55],[3, 77],
    [7, 94],[2, 68],[1, 61],[4, 99],[3, 54],[6, 75],[5, 66],[0, 76],[9, 63],[8, 67],
    [3, 69],[4, 88],[9, 82],[8, 95],[0, 99],[2, 67],[6, 95],[5, 68],[7, 67],[1, 86],
    [1, 99],[4, 81],[5, 64],[6, 66],[8, 80],[2, 80],[7, 69],[9, 62],[3, 79],[0, 88],
    [7, 50],[1, 86],[4, 97],[3, 96],[0, 95],[8, 97],[2, 66],[5, 99],[6, 52],[9, 71],
    [4, 98],[6, 73],[3, 82],[2, 51],[1, 71],[5, 94],[7, 85],[0, 62],[8, 95],[9, 79],
    [0, 94],[6, 71],[3, 81],[7, 85],[1, 66],[2, 90],[4, 76],[5, 58],[8, 93],[9, 97],
    [3, 50],[0, 59],[1, 82],[8, 67],[7, 56],[9, 96],[6, 58],[4, 81],[5, 59],[2, 96]
]

JOBsq=[
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
    [20, 21, 22, 23, 24, 25, 26, 27, 28, 29], 
    [30, 31, 32, 33, 34, 35, 36, 37, 38, 39], 
    [40, 41, 42, 43, 44, 45, 46, 47, 48, 49], 
    [50, 51, 52, 53, 54, 55, 56, 57, 58, 59], 
    [60, 61, 62, 63, 64, 65, 66, 67, 68, 69], 
    [70, 71, 72, 73, 74, 75, 76, 77, 78, 79], 
    [80, 81, 82, 83, 84, 85, 86, 87, 88, 89], 
    [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
]


Result={
    0:[80, 91, 22, 44, 64, 16, 77, 37, 8, 59],
    1:[50, 61, 32, 92, 23, 4, 74, 84, 17, 49],
    2:[31, 73, 14, 85, 55, 45, 5, 66, 28, 99],
    3:[40, 90, 11, 72, 82, 63, 34, 58, 29, 9],
    4:[0, 70, 41, 51, 62, 13, 33, 86, 97, 27],
    5:[10, 52, 3, 75, 25, 36, 87, 67, 47, 98],
    6:[71, 81, 2, 12, 53, 24, 35, 96, 46, 68],
    7:[30, 60, 83, 94, 76, 56, 26, 7, 48, 18],
    8:[1, 21, 43, 93, 54, 65, 15, 88, 78, 39],
    9:[20, 42, 6, 57, 38, 95, 89, 79, 69, 19]
}

j1 =[
    [0,13], [1,56], [2,45],
    [0,32], [1,34], [2,11],
    [2,62], [0,23], [1,33],
]
jsq1 = [
    [0,1,2],
    [3,4,5],
    [6,7,8]
]

res = {
    0:[0,3,7],
    1:[4,1,8],
    2:[6,2,5]
}

#뒤에서부터 index를 찾는 함수.
def rindex(mylist, myvalue):
    return len(mylist) - mylist[::-1].index(myvalue) - 1

#arc를 string으로 바꿔줌. (12, 34) =>'12, 34'
def arc_into_string(arc):
    arc = sorted(arc)
    return ','.join(str(a) for a in arc)

#특정 operation의 time을 알려줌
def get_time(opNum, jobs):
    return jobs[opNum][1]

#특정 operation이 속한 job의 number를 알려줌
def get_job(opNum, numOfOpInEachJob):
    for i in range(0,numOfOpInEachJob):
        if opNum >= i*numOfOpInEachJob and opNum < (i+1)*numOfOpInEachJob:
            return i
#특정 operation이 수행될 수 있는 machine number를 알려줌.
def get_machine(opNum, jobs, numOfOpInEachJob =10):
    return jobs[opNum][0]

#Cmax를 구하는 알고리즘
#result에서 machine 1에서 10까지 돌면서 operation을 수행해나감.
#각 operation이 수행되려면 1)같은 machine에서의 선행 operation, 2)같은 job에서의 선행 operation이 둘 다 수행완료되어야 함.
#각 operation이 기다렸던 이전 operation(같은 machine에서의 선행 operation과 같은 job에서의 선행 operation 중 더 늦게 끝난 operation)
#   을 기록함.(나중에 Longest Path를 찾기 위함)
#만약 무한 루프가 발생할 경우 (500번 이상 반복할 때 ) 알고리즘을 종료함.
def faster_CMAX(JOB, JOBsq, resMatrix, numOfOpInEachJob=10):

    jobLen = len(JOBsq) #job의 개수
    mLen = len(list(resMatrix.keys())) #machine의 개수
    opNum = len(JOB) #operation의 number
    firstOps = [x[0] for x in JOBsq]#각 job의 첫 번쨰 operation
    #numOfOpInEachJob = 10 #각 job에서 Operation 개수
    jobSeqTime = [0]*jobLen
    jobDone = [[] for i in range(0,jobLen)] #완료된 operation을 차례로 넣음.
    finishTime = [0]* opNum #index 번호 노드가 끝나는 시간.
    waitedNode = [0]* opNum #index 번호 노드가 기다렸던 노드.


    mDoneIdx = [-1]* mLen
    # print 'Cmax statrted..'
    numRepeat = 0
    while not all(mdx >= numOfOpInEachJob - 1 for mdx in mDoneIdx):
        numRepeat = numRepeat+1
        if numRepeat > 100:
            return[100000, []]
        #최대 mdx 값은 8.
        # print mDoneIdx
        for m in range(0,mLen): #각 job에 대해서 진행시켜나가기
            # print 'jobsq', JOBsq
            schedule = resMatrix[m]
            if mDoneIdx[m] == numOfOpInEachJob - 1:
                continue

            curOp = schedule[mDoneIdx[m] + 1] #현재 operation number
            isCurOpFirstOp = curOp in firstOps
            jobOfCurOp = get_job(curOp, numOfOpInEachJob)  #현재 operation의 job번호
            timeCurOp = get_time(curOp, JOB) #현재 operation 걸리는 시간.

            jobDoneForCurOp = jobDone[jobOfCurOp] #현재 operation이 속해있는 job들의 집합.(jobNum, 끝나는 누적시간.)

            if (isCurOpFirstOp): #Job의 first Operation이므로, 그냥 수행하면 됨. 그런데 finishTime은 머신의 이전 작업의 finishTime을 봐야함.
                
                prevMachineOp = schedule[mDoneIdx[m]] #현 operation이 수행되고 있는 machine 내에서 이전 operation.

                if (mDoneIdx[m] != -1): 
                    finishTime[curOp] = timeCurOp + finishTime[prevMachineOp]
                    waitedNode[curOp] = prevMachineOp
                else: #first operation이면서 머신의 첫번째 작업일 때.
                    finishTime[curOp] = timeCurOp
                    waitedNode[curOp] = -1

                jobSeqTime[jobOfCurOp] = finishTime[curOp]
                jobDone[jobOfCurOp].append(curOp)
                mDoneIdx[m] = mDoneIdx[m] + 1

            else: #first Operation이 아니므로 그전 Operation이 끝났는지 체크해야 함. 물론
                prevJobOp = curOp - 1  #현 operation이 속해있는 job 내에서 이전 operation.
                prevMachineOp = schedule[mDoneIdx[m]] #현 operation이 수행되고 있는 machine 내에서 이전 operation.

                if prevJobOp in jobDone[jobOfCurOp]: #job에서의 이전 operation이 끝났을 경우.
                    finishTime[curOp] = timeCurOp + max( finishTime[prevJobOp], finishTime[prevMachineOp])
                    waitedNode[curOp] = prevMachineOp if finishTime[prevMachineOp] > finishTime[prevJobOp] else prevJobOp
                    jobSeqTime[jobOfCurOp] = finishTime[curOp]
                    jobDone[jobOfCurOp].append(curOp)
                    mDoneIdx[m] = mDoneIdx[m] + 1
                else:
                    
                    waitedNode[curOp] = prevJobOp
                
    maxPath = []
    
    # maxPath를 구하기 
    indexOfMaxJob = jobSeqTime.index(max(jobSeqTime))
    curJob = JOBsq[indexOfMaxJob][-1]
    # print 'jobsq', JOBsq
    while(curJob != -1):
        maxPath.append(curJob)
        curJob = waitedNode[curJob]
    return [max(jobSeqTime), maxPath]




def tabu_search(jobs, jobsq, result, numOfOpInEachJob, num_of_search_iteration):

    size_of_tabu_list = 100
    cmax, lngestPath = faster_CMAX(jobs, jobsq, result, 10)
    aspiration_level = 0;
    best_solution_so_far = 0
    tabu_list = [] #서로 바꿀 arc가 tabu list에 있는경우.
    tabu_cmax_list= [] #cmax값이 tabu list에 있는경우.
    best_result = []
    all_move = []

    temporary_cmax = 0
    temporary_path = []
    
    same_path_num = 0 #같은 길 내에서의 move를 얼마나 했는지를 기록..
    
    for j in range(0,num_of_search_iteration):
        print '\n\n < iteartion ', j + 1, ' >\n'
        # print 'current cmax value : ', temporary_cmax
        # print 'current longest path : ', temporary_path
        # print 'current lngest path of cmax value so far is :', lngestPath
        allNeighbors = []
        allNeighbors = list(itertools.combinations(lngestPath,2))

        candidates = []

        for i in range(0, len(allNeighbors)):
            op = allNeighbors[i]
            areTheyInTheSameMachine = get_machine(op[0], jobs) == get_machine(op[1], jobs)
            areTheyInTheSameJob = abs(op[0] - op[1]) < numOfOpInEachJob
            if ( areTheyInTheSameMachine and not areTheyInTheSameJob): #같은 Job 안에 있는 operation 이라는 뜻.
                candidates.append(op)

        # print 'all possible neighbors are' , candidates
        feasible_move_list = []
        for cand in candidates:

            res = changeTwoNodesInResult(jobs, result, cand[0], cand[1])
            cmaxtmp, pathtmp = faster_CMAX(jobs, jobsq, res, 10)

            if len(pathtmp) == 0: # 무한루프가 발생했을 경우 => feasible solution이 아님.
                continue
            feasible_move_list.append([cmaxtmp, deepcopy(pathtmp), cand])


        feasible_move_list = sorted(feasible_move_list, key=lambda each: each[0], reverse=False)
        # print ' - all feasible move -'
        # for k in feasible_move_list:
        #     print k 
        print ' > number of all feasible move : ', len(feasible_move_list)

        for i in range(0, len(feasible_move_list)):
            nb = feasible_move_list[i]
            arc = nb[2]
            curcmax = nb[0]
            curlpath = nb[1]
            arcstr = arc_into_string(nb[2])
            same_path = lngestPath[-1] == curlpath[-1] and lngestPath[0] == curlpath[0]

            tabuCondition = arcstr not in tabu_list
            tabuCondition2 = curcmax not in tabu_cmax_list
            lastOne =  i == len(feasible_move_list)-1

            if tabuCondition or curcmax < aspiration_level or lastOne:
                if same_path:
                    same_path_num = same_path_num + 1
                else:
                    same_path_num = 0

                if lastOne:
                    tabu_list = []
                    tabu_cmax_list = []

                #tabu list update
                tabu_list.append(arcstr)
                if len(tabu_list) > size_of_tabu_list:
                    del(tabu_list[0])

                print ' > these two node will change : ',arc

                
                #chagen result matrix for this move.
                result = changeTwoNodesInResult(jobs, result, arc[0], arc[1])
                
                #record all move (all move is history for whole tabu search.)
                if arcstr in all_move:
                    lastidx = rindex(all_move, arcstr)
                    if lastidx > 0:
                        if all_move[lastidx-1] == all_move[-1]:
                            continue
                all_move.append(arcstr)


                #tabu cmax list update.
                tabu_cmax_list.append(curcmax)
                if len(tabu_cmax_list) > 2:
                    del(tabu_cmax_list[0])

                if cmax > curcmax:

                    cmax = curcmax
                    aspiration_level = cmax
                    lngestPath = curlpath

                best_result = deepcopy(result)

                temporary_path = curlpath
                temporary_cmax = curcmax
                print ' > current C-max value is : ', curcmax
                break

        print ' > cmax until current iteration is  :', cmax



    print ' * all history of tabu search :'
    print all_move,'\n'
    print [cmax, lngestPath]
    print '\n\n===== Result of tabu search for Job-Shop Problem.====\n'
    print ' 0. # of iteration : ', num_of_search_iteration
    print ' 1. cmax : ', cmax
    print ' 2. longest Path for this cmax : ', lngestPath
    print ' 3. Result matrix for lowest cmax'
    print ' {'
    for k in best_result:
        print '   ',k,':',result[k], ','
    print ' }'

    return [cmax, lngestPath]

def changeTwoNodesInResult(jobs, result, node1, node2, isPrint=False): #node1 and node two must be an integer.

    res = deepcopy(result)
    m1 = get_machine(node1, jobs)
    m2 = get_machine(node2, jobs)
    if isPrint:
        print res[m1]
        print 'changing two nodes..', node1, node2
    idx1 = res[m1].index(node1)
    idx2 = res[m2].index(node2)

    res[m1][idx1] = node2
    res[m2][idx2] = node1
    if isPrint:
        print res[m1]
    return res



tabu_search(JOB, JOBsq, Result, 10, 1000)



