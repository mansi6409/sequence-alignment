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

def string_similarity(first_seq, second_seq, cost_gap, cost_mismatch):
    alignmentCosts = [[0 for _ in range(len(Y)+1)] for _ in range(len(first_seq)+1)]

    xLen, yLen = len(first_seq), len(second_seq)
    for xIndex in range(xLen+1):
        alignmentCosts[xIndex][0] = xIndex * cost_gap
    for yIndex in range(yLen+1):
        alignmentCosts[0][yIndex] = yIndex * cost_gap

    for xIndex in range(1, xLen+1):
        for yIndex in range(1, yLen+1):
            tempMin = min(alignmentCosts[xIndex-1][yIndex] + cost_gap,
                                                 alignmentCosts[xIndex][yIndex-1] + cost_gap)
            alignmentCosts[xIndex][yIndex] = min(tempMin,
                                                 alignmentCosts[xIndex-1][yIndex-1] + cost_mismatch[first_seq[xIndex-1]][second_seq[yIndex-1]])

    return alignmentCosts

def align_sequence(first_seq, second_seq, cost_gap, cost_mismatch):
    alignmentCosts = string_similarity(first_seq, second_seq, cost_gap, cost_mismatch)
    xIndex, yIndex = len(first_seq), len(second_seq)
    xAlignedSeq, yAlignedSeq = str(), str()
    
    while not (xIndex == 0 and yIndex == 0):
        if (xIndex == 0):
            xAlignedSeq = '_' * yIndex + xAlignedSeq
            yAlignedSeq = second_seq[:yIndex] + yAlignedSeq
            break
        elif (yIndex == 0):
            xAlignedSeq = first_seq[:xIndex] + xAlignedSeq
            yAlignedSeq = '_' * xIndex + yAlignedSeq
            break
        
        xTemp = '_' 
        yTemp = '_'
        
        if (cost_gap + alignmentCosts[xIndex-1][yIndex] == alignmentCosts[xIndex][yIndex]):
            xTemp = first_seq[xIndex-1]
            xIndex -= 1
        elif (cost_gap + alignmentCosts[xIndex][yIndex-1] == alignmentCosts[xIndex][yIndex]):
            yTemp = second_seq[yIndex-1]
            yIndex -= 1
        elif ((cost_mismatch[first_seq[xIndex-1]][second_seq[yIndex-1]] + alignmentCosts[xIndex-1][yIndex-1]) == alignmentCosts[xIndex][yIndex]):
            xTemp = first_seq[xIndex-1]
            yTemp = second_seq[yIndex-1]
            xIndex -= 1
            yIndex -= 1
            
        xAlignedSeq = xTemp + xAlignedSeq
        yAlignedSeq = yTemp + yAlignedSeq

    return alignmentCosts[len(first_seq)][len(second_seq)], xAlignedSeq, yAlignedSeq


def string_similarity_efficient(first_seq, second_seq, cost_gap, cost_mismatch):
    xLen, yLen = len(first_seq), len(second_seq)
    previous_row = [0] * (yLen + 1)

    for i in range(1, yLen + 1):
        previous_row[i] = previous_row[i - 1] + cost_gap

    for i in range(1, xLen + 1):
        current_row = [previous_row[0] + cost_gap] + [0] * yLen
        for j in range(1, yLen + 1):
            substitution_cost = cost_mismatch[first_seq[i - 1]][second_seq[j - 1]]
            tempMin = min(current_row[j - 1] + cost_gap,
                                 previous_row[j] + cost_gap)
            current_row[j] = min(tempMin,
                                 previous_row[j - 1] + substitution_cost)

        previous_row = current_row

    return current_row



def align_sequence_efficient(first_seq, second_seq, cost_gap, cost_mismatch):
    xLen = len(first_seq)
    yLen = len(second_seq)
    
    if (xLen == 1 and yLen == 1):
        return (cost_mismatch[first_seq[0]][second_seq[0]], first_seq, second_seq)
    elif (xLen == 1):
        return align_sequence(first_seq, second_seq, cost_gap, cost_mismatch)
    elif (xLen == 0 and yLen == 0):
        return (0, first_seq, second_seq)
    elif (xLen == 0):
        return (yLen * cost_gap, '_' * yLen, second_seq)
    elif (yLen == 0):
        return (xLen * cost_gap, first_seq, '_' * xLen)

    xLeft, xRight = first_seq[:xLen//2], first_seq[xLen//2:]
    
    leftCost = string_similarity_efficient(xLeft, second_seq, cost_gap, cost_mismatch)
    rightCost = string_similarity_efficient(xRight[::-1], second_seq[::-1], cost_gap, cost_mismatch)

    splitIndex = 0
    minAddUpCost = leftCost[0] + rightCost[yLen]

    for k in range(yLen+1):
        addUpCost = leftCost[k] + rightCost[yLen-k]
        if (addUpCost < minAddUpCost):
            minAddUpCost = addUpCost
            splitIndex = k

    _, xLeftAlign, yLeftAlign = align_sequence_efficient(
        xLeft, second_seq[:splitIndex], cost_gap, cost_mismatch)
    _, xRightAlign, yRightAlign = align_sequence_efficient(
        xRight, second_seq[splitIndex:], cost_gap, cost_mismatch)

    return (minAddUpCost, xLeftAlign + xRightAlign, yLeftAlign + yRightAlign)

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

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

if __name__ == '__main__':
    initialMem = process_memory()
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    if len(sys.argv) < 3:
            sys.exit('Usage: python efficient_3.py input_file output_file')
    
    try:
        f1 = open(inputFile, 'r')
    except FileNotFoundError:
        sys.exit('Input file not found:', inputFile)

    try:
        f2 = open(outputFile, 'w')
        f2.truncate(0)
    except FileNotFoundError:
        sys.exit('Output file not found', outputFile)
    
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