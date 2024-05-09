
import re
import psutil
import time
import sys

def validate_input_strings(row):
    if (row.isalpha()):
        regEx = r'[^TCAG]'
        if (re.search(regEx, row)):
            sys.exit('Invalid input')
        else:
            return 'Parent'
    else:
        try:
            value = int(row)
        except:
            sys.exit('Invalid input')
        else:
            return value

def create_input(inputFile):
    finalSequences, originalSequence, sequenceLength = list(), list(), list()
    for row in inputFile:
        row = row.split()[0]
        validateSequence = validate_input_strings(row)
        print("validateSequence - ", validateSequence)

        if (validateSequence == 'Parent'):
            originalSequence.append(row)
            finalSequences.append(row)
            sequenceLength.append(0)
            print("finalSequences - ", finalSequences)
            print("originalSequence - ", originalSequence)
            print("sequenceLength - ", sequenceLength)
        else:
            value = validateSequence
            print("value - ", value)
            string = finalSequences[-1]
            print("string - ", string)
            sequenceLength[-1] += 1
            print("sequenceLength - ", sequenceLength)
            finalSequences[-1] = string[:value+1] + string + string[value+1:]
            print("finalSequences - ", finalSequences)

    sequenceLength = [2 ** sequenceLength[i] * len(originalSequence[i]) for i in (0, 1)]
    if (len(finalSequences[0]) != sequenceLength[0] or len(finalSequences[1]) != sequenceLength[1]):
        sys.exit('Sequence generation error')

    return finalSequences[0], finalSequences[1]

def string_similarity(X, Y, delta, alpha):
    xLen = len(X)
    yLen = len(Y)

    alignmentCosts = [[0] * (yLen+1) for _ in range(xLen+1)]
    alignmentCost = 0
    for xIndex in range(xLen+1):
        alignmentCosts[xIndex][0] = alignmentCost
        alignmentCost += delta

    alignmentCost = 0
    for yIndex in range(yLen+1):
        alignmentCosts[0][yIndex] = alignmentCost
        alignmentCost += delta

    for xIndex in range(1, xLen+1):
        for yIndex in range(1, yLen+1):
            alignmentCosts[xIndex][yIndex] = min(alignmentCosts[xIndex-1][yIndex] + delta,
                                                 alignmentCosts[xIndex][yIndex-1] + delta,
                                                 alignmentCosts[xIndex-1][yIndex-1] + alpha[X[xIndex-1]][Y[yIndex-1]])

    return alignmentCosts

def align_sequence(X, Y, delta, alpha):
    xAlignedSeq = str()
    yAlignedSeq = str()
    
    alignmentCosts = string_similarity(X, Y, delta, alpha)

    xIndex = len(X)
    yIndex = len(Y)

    while not (xIndex == 0 and yIndex == 0):
        if (xIndex == 0):
            xAlignedSeq = '_' * yIndex + xAlignedSeq
            yAlignedSeq = Y[:yIndex] + yAlignedSeq
            break
        elif (yIndex == 0):
            xAlignedSeq = X[:xIndex] + xAlignedSeq
            yAlignedSeq = '_' * xIndex + yAlignedSeq
            break

        xTemp = '_' 
        yTemp = '_'
        
        if (delta + alignmentCosts[xIndex-1][yIndex] == alignmentCosts[xIndex][yIndex]):
            xTemp = X[xIndex-1]
            xIndex -= 1
        elif (delta + alignmentCosts[xIndex][yIndex-1] == alignmentCosts[xIndex][yIndex]):
            yTemp = Y[yIndex-1]
            yIndex -= 1
        elif ((alpha[X[xIndex-1]][Y[yIndex-1]] + alignmentCosts[xIndex-1][yIndex-1]) == alignmentCosts[xIndex][yIndex]):
            xTemp = X[xIndex-1]
            yTemp = Y[yIndex-1]
            xIndex -= 1
            yIndex -= 1
            
        xAlignedSeq = xTemp + xAlignedSeq
        yAlignedSeq = yTemp + yAlignedSeq

    return alignmentCosts[len(X)][len(Y)], xAlignedSeq, yAlignedSeq

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def time_wrapper(): 
    delta = 30
    alpha = {'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
             'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
             'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
             'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}}
    start_time = time.time() 
    print("X - ", X)
    print("Y - ", Y)
    alignmentCost, xAlignedSeq, yAlignedSeq = align_sequence(X, Y, delta, alpha)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000 
    return time_taken, alignmentCost, xAlignedSeq, yAlignedSeq

if __name__ == '__main__':
    initialMem = process_memory()
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    try:
        f1 = open(inputFile, 'r')
    except:
        sys.exit('Input file not found')

    try:
        f2 = open(outputFile, 'w')
        f2.truncate(0)
    except:
        sys.exit('Output file not found')
        
    X, Y = create_input(f1)

    time_taken, alignmentCost, xAlignedSeq, yAlignedSeq = time_wrapper()

    finalMem = process_memory()
    usedMem = abs(finalMem - initialMem)
    original_stdout = sys.stdout
    sys.stdout = f2
    print(alignmentCost, xAlignedSeq, yAlignedSeq, time_taken, usedMem, sep="\n")
    sys.stdout = original_stdout
