import gc
import re
import psutil
import time
import sys

def create_input(inputFile):
    finalSequences, originalSequence, sequenceLength = list(), list(), list()

    for row in inputFile:
        row = row.split()[0]
        if (row.isalpha()):
            validateSequence = 'Parent'
        else:
            validateSequence =  int(row)
        # validateSequence = validate_input_strings(row)
        print("validateSequence - ", validateSequence)

        if(validateSequence != 'Parent'):
            value = validateSequence
            print("value - ", value)
            string = finalSequences[-1]
            print("string - ", string)
            sequenceLength[-1] += 1
            print("sequenceLength - ", sequenceLength)
            finalSequences[-1] = string[:value+1] + string + string[value+1:]
            print("finalSequences - ", finalSequences)
            
        else:
            originalSequence.append(row)
            finalSequences.append(row)
            sequenceLength.append(0)
            print("finalSequences - ", finalSequences)
            print("originalSequence - ", originalSequence)
            print("sequenceLength - ", sequenceLength)

    return finalSequences[0], finalSequences[1]

def string_similarity(X, Y, delta, alpha):
    alignmentCosts = [[0 for _ in range(len(Y)+1)] for _ in range(len(X)+1)]

    xLen, yLen = len(X), len(Y)
    for xIndex in range(xLen+1):
        alignmentCosts[xIndex][0] = xIndex * delta
    for yIndex in range(yLen+1):
        alignmentCosts[0][yIndex] = yIndex * delta

    for xIndex in range(1, xLen+1):
        for yIndex in range(1, yLen+1):
            alignmentCosts[xIndex][yIndex] = min(alignmentCosts[xIndex-1][yIndex] + delta,
                                                 alignmentCosts[xIndex][yIndex-1] + delta,
                                                 alignmentCosts[xIndex-1][yIndex-1] + alpha[X[xIndex-1]][Y[yIndex-1]])

    return alignmentCosts

def align_sequence(X, Y, delta, alpha):
    alignmentCosts = string_similarity(X, Y, delta, alpha)
    xIndex, yIndex = len(X), len(Y)
    xAlignedSeq, yAlignedSeq = str(), str()
    
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


def string_similarity_efficient(seq1, seq2, gap_penalty, scoring_matrix):
    xLen, yLen = len(seq1), len(seq2)
    previous_row = [0] * (yLen + 1)

    for i in range(1, yLen + 1):
        previous_row[i] = previous_row[i - 1] + gap_penalty

    for i in range(1, xLen + 1):
        current_row = [previous_row[0] + gap_penalty] + [0] * yLen
        for j in range(1, yLen + 1):
            substitution_cost = scoring_matrix[seq1[i - 1]][seq2[j - 1]]
            current_row[j] = min(current_row[j - 1] + gap_penalty,
                                 previous_row[j] + gap_penalty,
                                 previous_row[j - 1] + substitution_cost)

        previous_row = current_row

    return current_row



def align_sequence_efficient(X, Y, delta, alpha):
    xLen = len(X)
    yLen = len(Y)
    
    if (xLen == 1 and yLen == 1):
        return (alpha[X[0]][Y[0]], X, Y)
    elif (xLen == 1):
        return align_sequence(X, Y, delta, alpha)
    elif (xLen == 0 and yLen == 0):
        return (0, X, Y)
    elif (xLen == 0):
        return (yLen * delta, '_' * yLen, Y)
    elif (yLen == 0):
        return (xLen * delta, X, '_' * xLen)

    xLeft, xRight = X[:xLen//2], X[xLen//2:]
    
    leftCost = string_similarity_efficient(xLeft, Y, delta, alpha)
    rightCost = string_similarity_efficient(xRight[::-1], Y[::-1], delta, alpha)

    splitIndex = 0
    minAddUpCost = leftCost[0] + rightCost[yLen]

    for k in range(yLen+1):
        addUpCost = leftCost[k] + rightCost[yLen-k]
        if (addUpCost < minAddUpCost):
            minAddUpCost = addUpCost
            splitIndex = k

    _, xLeftAlign, yLeftAlign = align_sequence_efficient(
        xLeft, Y[:splitIndex], delta, alpha)
    _, xRightAlign, yRightAlign = align_sequence_efficient(
        xRight, Y[splitIndex:], delta, alpha)

    return (minAddUpCost, xLeftAlign + xRightAlign, yLeftAlign + yRightAlign)

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
    alignmentCost, X_align, Y_align = align_sequence_efficient(X, Y, delta, alpha)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000 
    return time_taken, alignmentCost, X_align, Y_align

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
    time_taken, alignmentCost, X_align, Y_align = time_wrapper()
    endMemory = process_memory()
    f1.close()
    mem_taken = abs(endMemory - initialMem)
    original_stdout = sys.stdout
    sys.stdout = f2
    print(alignmentCost, X_align, Y_align, time_taken, mem_taken, sep="\n")
    sys.stdout = original_stdout
    f2.close()