"""
Author: Joseph Rios

Description:
    Tests to see if a WB puzzle outputs the right solution
    and records the runtimes for filtering and solving.

Usage:
    python tester.py <words-file> <num-trials>
    python tester.py <words-file> <num-trials> <num-threads>
"""
import sys
import time
import csv
import serial
import thread
num_thread = 0

def serial_test(wordFile,numTrials):
    solutions = []
    data = []
    with open("solutions.txt",'r') as f:
        data = f.readlines()
    for line in data:
        solutions.append(line.split())
    TOTAL = 5#len(solutions)
    puzzleSize = [0 for i in range(TOTAL)]
    loadTime = [0 for i in range(TOTAL)]
    loadSize = [0 for i in range(TOTAL)]
    solveTime = [0 for i in range(TOTAL)]
    success = [False for i in range(TOTAL)]
    for i in range(TOTAL):
        #Load ith puzzle/hint
        data = []
        with open("puzzles//"+str(i)+".txt",'r') as f:
            data = f.readlines()
        hint = list(map(lambda x: int(x),data[0].split()))
        puzzle = list(map(lambda x: x.strip().upper(), data[1:]))
        rLst = [0 for j in range(26)]
        for line in puzzle:
            for char in line:
                puzzleSize[i]+=1
                rLst[ord(char)-65]+=1
        #Average Load Time for numTrials
        total = 0
        for j in range(numTrials):
            serial.words = []
            t = time.time()
            serial.loadRelevantWords(wordFile,rLst)
            total+=(time.time()-t)
        loadTime[i] = total/numTrials
        loadSize[i] = len(serial.words)
        #Average Solve Time for numTrials
        total = 0
        for j in range(numTrials):
            t = time.time()
            result = serial.solve(puzzle,hint)
            total+=(time.time()-t)
        solveTime[i] = total/numTrials
        #Make sure program output a correct solution
        for soln in result:
            currSoln = solutions[i]
            flag = True
            for word in soln:
                if(word in currSoln):
                    currSoln.remove(word)
                else:
                    flag = False
                    break
            if(flag):
                success[i] = True
                break
    #print(puzzleSize)
    #print(loadSize)
    #print(loadTime)
    #print(solveTime)
    #print(success)
    recordResults(puzzleSize,loadSize,loadTime,solveTime,success)

def th_test(wordFile,numTrials):
    solutions = []
    data = []
    thread.numThreads=int(num_thread)
    with open("solutions.txt",'r') as f:
        data = f.readlines()
    for line in data:
        solutions.append(line.split())
    TOTAL = 5#len(solutions)
    puzzleSize = [0 for i in range(TOTAL)]
    loadTime = [0 for i in range(TOTAL)]
    loadSize = [0 for i in range(TOTAL)]
    solveTime = [0 for i in range(TOTAL)]
    success = [False for i in range(TOTAL)]
    for i in range(TOTAL):
        #Load ith puzzle/hint
        data = []
        with open("puzzles//"+str(i)+".txt",'r') as f:
            data = f.readlines()
        hint = list(map(lambda x: int(x),data[0].split()))
        puzzle = list(map(lambda x: x.strip().upper(), data[1:]))
        rLst = [0 for j in range(26)]
        for line in puzzle:
            for char in line:
                puzzleSize[i]+=1
                rLst[ord(char)-65]+=1
        #Average Load Time for numTrials
        total = 0
        for j in range(numTrials):
            thread.words = []
            t = time.time()
            thread.loadRelevantWords(wordFile,rLst)
            total+=(time.time()-t)
        loadTime[i] = total/numTrials
        loadSize[i] = len(thread.words)
        #Average Solve Time for numTrials
        total = 0
        for j in range(numTrials):
            t = time.time()
            result = thread.solve(puzzle,hint)
            total+=(time.time()-t)
        solveTime[i] = total/numTrials
        #Make sure program output a correct solution
        for soln in result:
            currSoln = solutions[i]
            flag = True
            for word in soln:
                if(word in currSoln):
                    currSoln.remove(word)
                else:
                    flag = False
                    break
            if(flag):
                success[i] = True
                break
    #print(puzzleSize)
    #print(loadSize)
    #print(loadTime)
    #print(solveTime)
    #print(success)
    recordResults(puzzleSize,loadSize,loadTime,solveTime,success)

def recordResults(puzzleSize,loadSize,loadTime,solveTime,success):
    for i in range(len(success)):
        if(success[i]):
            success[i] = 1
        else:
            success[i] = 0
    with open("results.csv",'w',newline='') as csvfile:
        w = csv.writer(csvfile,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
        w.writerow(["Puzzle Size"]+puzzleSize)
        w.writerow(["Load Size"]+loadSize)
        w.writerow(["Load Time"]+loadTime)
        w.writerow(["Solve Time"]+solveTime)
        w.writerow(["Success"]+success)


if(__name__=="__main__"):
    if(len(sys.argv)==4):
        num_thread = int(sys.argv[3])
        th_test(sys.argv[1],int(sys.argv[2]))
    elif(len(sys.argv)==3):
        serial_test(sys.argv[1],int(sys.argv[2]))
    else:
        print("Invalid Number of Arguments")
