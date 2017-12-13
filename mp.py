"""
Authors: Joseph Rios, Kyle Finter, Mckenzie Riley, Leonard Museau
Description: Outputs possible solutions to WordBrain Puzzles
Usage:
    Command: python v2.1.py <puzzle-file>.txt
    File Format:
    <List of lengths of hints separated by spaces>
    <Lines of the puzzle>
"""
import sys
import time
from multiprocessing import Pool

words = []
processList = []
numProcesses = 4

def solve(puzzle,hint):
    """
    Input: a puzzle (list of strings) and list of hints (list of int)
    Output: a list of lists of paths that match each of the hints and map to valid english words
        + Path: a list of pairs representing coordinates in the puzzle
    """
    result = []
    hintSet = set(hint)
    maxHint = max(hint)
    if(len(hint)==1):
        for path in getPaths(puzzle,hintSet,maxHint):
            result.append([ptw(puzzle,path)])
    else:
        argsList = []
        validPaths = getPaths(puzzle,hintSet,maxHint)
        for path in validPaths:
            newPuzzle = remove(puzzle,path)
            newHint = hint[:]
            newHint.remove(len(path))
            argsList.append((newPuzzle,newHint,words))
        resultList = p.starmap(topmpSolve,argsList)
        for i in range(len(validPaths)):
            path = validPaths[i]
            solutions = resultList[i]
            for soln in solutions:
                result.append([ptw(puzzle,path)]+soln)
    return result
        
def topmpSolve(puzzle,hint,wordList):
    global words
    words = wordList
    return mpSolve(puzzle,hint)


def mpSolve(puzzle,hint):
    hintSet = set(hint)
    maxHint = max(hint)
    result = []
    if(len(hint)==1):
        for path in getPaths(puzzle,hintSet,maxHint):
            result.append([ptw(puzzle,path)])
    else:
        for path in getPaths(puzzle,hintSet,maxHint):
            newPuzzle = remove(puzzle,path)
            newHint = hint[:]
            newHint.remove(len(path))
            for soln in mpSolve(newPuzzle,newHint):
                result.append([ptw(puzzle,path)]+soln)
    return result

def getPaths(puzzle,hintSet,maxHint):
    """
    Helper function for getPathR
    Input: A puzzle (list of strings), a set of hints (for const time lookups), and the maxHint of the hint list
    Output: A list of paths that are valid words (appropriate length and an english word)
    + Works by calling getPathR on each tile with a letter in it
    + It also combines each list of paths from getPathR into result
    """
    result = []
    for x in range(len(puzzle)):
        for y in range(len(puzzle[x])):
            if(puzzle[x][y]!=" "):
                result+=getPathR(puzzle,hintSet,maxHint,[(x,y)])
    return result
"""
def mpGetPaths(puzzle,hintSet,maxHint,coords,wordList):
    global words
    words = wordList
    localResult = []
    for each in coords:
        localResult+=getPathR(puzzle,hintSet,maxHint,[each])
    return localResult
"""

def getPathR(puzzle,hintSet,maxHint,currPath):
    """
    Recursive Get Path Function
    Input:  A puzzle (list of strings)
            A hintSet (a set of hints)
            A maxHint (precomputed maximum of the hintSet)
            A currPath (path so far, initially is just one tile)
    Output: A list of paths that are valid words
    """
    x,y = currPath[-1]
    result = []
    #Distributing Coords for edge cases
    #Consider Revision Here
    if(x==0):
        dirx=[0,1]
    elif(x==len(puzzle)-1):
        dirx=[-1,0]
    else:
        dirx=[-1,0,1]
    if(y==0):
        diry=[0,1]
    elif(y==len(puzzle[0])-1):
        diry=[-1,0]
    else:
        diry=[-1,0,1]
    #Iterate over possible directions
    for i in dirx:
        for j in diry:
            #Ignore Previously visited squares
            if((x+i,y+j) not in currPath):
                #If a valid length and word, add path
                if((len(currPath)+1 in hintSet) and
                   (isAWord(ptw(puzzle,currPath+[(x+i,y+j)])))):
                    #Need to make a copy of currPath
                    result.append(currPath[:]+[(x+i,y+j)])
                #If less than max and possible word, continue exploring
                #Should be possible to enter both of the IFs
                if((len(currPath)+1<maxHint) and 
                   (couldBeAWord(ptw(puzzle,currPath+[(x+i,y+j)])))):
                    #Need to make a copy of currPath
                    result+=getPathR(puzzle,hintSet,maxHint,currPath[:]+[(x+i,y+j)])
    return result
                
def remove(puzzle,path):
    """
    Input:  A list of strings representing a puzzle, and 
            A list of pairs representing a list path
    Output: A puzzle with the path replaced with spaces
            and shifted down.
    """
    new = puzzle[:]
    #Convert each string to list, because strings are immutable
    for i in range(len(new)):
        new[i] = list(new[i])
    #Replace all coords with a space
    for (x,y) in path:
        new[x][y] = " "
    #Shift down the elements with spaces below them
    shift=True
    while(shift):
        shift=False
        for i in range(1,len(new)):
            for j in range(len(new[i])):
                #If current spot is blank and the one above it isn't
                if(new[i][j]==" " and new[i-1][j]!=" "):
                    new[i][j]=new[i-1][j]
                    new[i-1][j]=" "
                    shift=True
    #Rejoin into a list of strings
    for i in range(len(new)):
        new[i] = "".join(new[i])
    return new

def ptw(puzzle,path):
    #Path to word
    #print(path)
    result = ""
    for (x,y) in path:
        result+=puzzle[x][y]
    return result

def isAWord(s):
    if(' ' in s):
        return False
    first = 0
    last = len(words)
    if(s<words[first] or s>words[last-1]):
        return False
    found = False
    while(first<=last and not found):
        mid = (first+last)//2
        if(words[mid]==s):
            found = True
        elif(s<words[mid]):
            last = mid-1
        else:
            first = mid+1
    return found

def couldBeAWord(s):
    if(' ' in s):
        return False
    first = 0
    last = len(words)
    if(s<words[first][:len(s)] or s>words[last-1][:len(s)]):
        return False
    found = False
    while(first<=last and not found):
        mid = (first+last)//2
        curr = words[mid][:len(s)]
        if(curr==s):
            found = True
        elif(s<curr):
            last = mid-1
        else:
            first = mid+1
    return found

def distribute(lst,n):
    #Returns a list of n partitions of a list
    l = len(lst)//n
    index = 0
    result = []
    for i in range(n):
        if(i<len(lst)%n):
            result.append(lst[index:index+l+1])
            index+=l+1
        else:
            result.append(lst[index:index+l])
            index+=l
    return result

def loadRelevantWords(wordFile,puzzle,hint):
    #Current Version Takes less than 0.1s
    #Consider Revising to a hard anagram, may not be worth it
    #For Example: If a puzzle has only 1 't' in it, don't include
    #             words with 2 or more t's
    global p,numProcesses,words
    listOfWords = list(open(wordFile).read().split('\n'))
    listOfWords = distribute(listOfWords,numProcesses)
    argsLst = []
    for each in listOfWords:
        argsLst.append((each,puzzle,hint))
    result = p.starmap(mpLoadWords,argsLst)
    for each in result:
        words+=each
    words.sort()

def mpLoadWords(wordList,puzzle,hint):
    hintSet = set(hint)
    colSet = [set() for i in range(len(puzzle[0]))]
    rLst = [0 for i in range(26)]
    for line in puzzle:
        for n,char in enumerate(line):
            rLst[ord(char)-65]+=1
            colSet[n].add(char)
    localResult = []
    for word in wordList:
        tempLst = rLst[:]
        word = word.strip().upper()#should already be uppercase
        prev = list(range(len(puzzle[0]))) #All the columns
        flag = True
        for char in word:
            if(tempLst[ord(char)-65]==0):
                flag = False
                break
            else:
                tempLst[ord(char)-65]-=1
                flag2 = False
                nextSet = set()
                for col in prev:
                    if(char in colSet[col]):
                        nextSet.add(col)
                        nextSet.add(col-1)
                        nextSet.add(col+1)
                if(flag2):
                    flag = False
                    break
                nextSet.discard(-1)
                nextSet.discard(len(puzzle[0]))
                prev = list(nextSet)
        if(flag and len(word) in hintSet):
            localResult.append(word)
    return localResult
                    

def main(fileName):
    puzzle = [] #list of strings
    hint = [] #list of integers
    data = [] #list of lines from the file
    #A puzzle should consist of a list of hints and a grid of letters
    with open(fileName,'r') as f:
        data = f.readlines()
    hint = list(map(lambda x: int(x),data[0].split()))
    puzzle = list(map(lambda x: x.strip().upper(), data[1:]))
    t = time.time()
    loadRelevantWords("words2.txt",puzzle,hint)
    print(len(words),"words loaded in",time.time()-t,"seconds")
    #for path in getPaths(puzzle,hint):
    #    print(ptw(puzzle,path))
    t = time.time()
    for soln in solve(puzzle,hint):
        print(soln)
    print("Solved in",time.time()-t,"seconds")

if(__name__=="__main__"):
    if(len(sys.argv)==3):
        numProcesses = int(sys.argv[2])
        p = Pool(numProcesses)
        main(sys.argv[1])
    else:
        print("Invalid number of arguments")

