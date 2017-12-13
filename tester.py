"""
Author: Joseph Rios

Description:
    Tests to see if a WB puzzle outputs the right solution
    and records the runtimes for filtering and solving.

Usage:
    python tester.py <words-file> <type-flag> <amt-flag> <num-trials>
    type-flag: -serial for serial.py
               -thXX for XX threads of thread.py
               -mpXX for XX processes of mp.py
    amt-flag:  -all for every file
               -eXX for XX of each puzzle size
"""
import sys
import time
import csv
import serial
import thread
import mp

amt = None

def test(wordFile,numTrials):
    global words
    solutions = []
    data = []
    with open("solutions.txt",'r') as f:
        data = f.readlines()
    for line in data:
        solutions.append(line.split())
    TOTAL = len(solutions)
    puzzleSize = []
    loadTime = [] 
    loadSize = [] 
    solveTime = []
    success = []
    sizes = dict()
    for i in range(TOTAL):
        print(i,"of",TOTAL)
        sys.stdout.flush()
        #Load ith puzzle/hint
        data = []
        with open("puzzles//"+str(i)+".txt",'r') as f:
            data = f.readlines()
        hint = list(map(lambda x: int(x),data[0].split()))
        puzzle = list(map(lambda x: x.strip().upper(), data[1:]))
        #Decide whether or not to continue based on how many have been done so far
        sz = len(puzzle)*len(puzzle[0])
        if(sz not in sizes):
            sizes[sz] = 1
        else:
            sizes[sz]+=1
        if(amt!=False and sizes[sz]>amt):
            continue
        else:
            puzzleSize.append(sz)
        #Average Load Time for numTrials
        total = 0
        for j in range(numTrials):
            words = []
            t = time.time()
            loadWords(wordFile,puzzle,hint)
            total+=(time.time()-t)
        loadTime.append(total/numTrials)
        loadSize.append(len(serial.words))
        #Average Solve Time for numTrials
        total = 0
        for j in range(numTrials):
            t = time.time()
            result = solve(puzzle,hint)
            total+=(time.time()-t)
        solveTime.append(total/numTrials)
        #Make sure program output a correct solution
        flag2 = False
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
                success.append(True)
                flag2 = True
                break
        if(not flag2):
            success.append(False)
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
    if(len(sys.argv)==5):
        #Check Type Flag
        if(sys.argv[2]=="-serial"):
            loadWords = serial.loadRelevantWords
            solve = serial.solve
            words = serial.words
        elif(sys.argv[2][:3]=="-th"):
            loadWords = thread.loadRelevantWords
            solve = thread.solve
            words = thread.words
            thread.numThreads = int(sys.argv[2][3:])
        elif(sys.argv[2][:3]=="-mp"):
            loadWords = mp.loadRelevantWords
            solve = mp.solve
            words = mp.words
            mp.numProcesses = int(sys.argv[2][3:])
        else:
            print("Invalid Type Flag")
            sys.exit()
        #Check Amount Flag
        if(sys.argv[3]=="-all"):
            amt = False
        elif(sys.argv[3][:2]=="-e"):
            amt = int(sys.argv[3][2:])
        else:
            print("Invalid Amount Flag")
            sys.exit()
        test(sys.argv[1],int(sys.argv[4]))
    else:
        print("Invalid Number of Arguments")
        print("Usage: python tester.py <words-file> <type-flag> <amt-flag> <num-trials>")
        print("type-flag:")
        print("\t-serial for serial.py")
        print("\t-thXX for XX threads of thread.py")
        print("\t-mpXX for XX processes of mp.py")
        print("amt-flag:")
        print("\t-all for every file")
        print("\t-eXX for XX of each puzzle size")
