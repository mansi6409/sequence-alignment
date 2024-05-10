import psutil
import time
import sys

def align_sequence(first_seq, second_seq, cost_gap, cost_mismatch):
    xIndex, yIndex = len(first_seq), len(second_seq)
    xAlignedSeq, yAlignedSeq = str(), str()
    alignmentCosts = string_similarity(first_seq, second_seq, cost_gap, cost_mismatch)

    while not (xIndex == 0 and yIndex == 0):
        xTemp, yTemp = '_', '_'
        if (xIndex == 0):
            xAlignedSeq = '_' * yIndex + xAlignedSeq
            yAlignedSeq = second_seq[:yIndex] + yAlignedSeq
            break
        if (yIndex == 0):
            xAlignedSeq = first_seq[:xIndex] + xAlignedSeq
            yAlignedSeq = '_' * xIndex + yAlignedSeq
            break

        
        actions = {
            1: lambda: (yIndex - 1, second_seq[yIndex - 1]),
            2: lambda: (xIndex - 1, first_seq[xIndex - 1]),
            3: lambda: (xIndex - 1, yIndex - 1, first_seq[xIndex - 1], second_seq[yIndex - 1])
        }

        key = next(key for key in actions.keys() if key == 1 and cost_gap + alignmentCosts[xIndex][yIndex-1] == alignmentCosts[xIndex][yIndex]
                                                or key == 2 and cost_gap + alignmentCosts[xIndex-1][yIndex] == alignmentCosts[xIndex][yIndex]
                                                or key == 3 and (cost_mismatch[first_seq[xIndex-1]][second_seq[yIndex-1]] + alignmentCosts[xIndex-1][yIndex-1]) == alignmentCosts[xIndex][yIndex])

        if key == 1:
            yIndex, yTemp = actions[key]()
        elif key == 2:
            xIndex, xTemp = actions[key]()
        elif key == 3:
            xIndex, yIndex, xTemp, yTemp = actions[key]()
            
        xAlignedSeq = xTemp + xAlignedSeq
        yAlignedSeq = yTemp + yAlignedSeq

    return alignmentCosts[len(first_seq)][len(second_seq)], xAlignedSeq, yAlignedSeq

def string_similarity(first_seq, second_seq, cost_gap, cost_mismatch):
    alignmentCosts = [[0 for _ in range(len(second_seq)+1)] for _ in range(len(first_seq)+1)]

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

def create_input(inputFile):
    finalSequences, originalSequence, sequenceLength = list(), list(), list()

    for row in inputFile:
        row = row.split()[0]
        if (row.isalpha()):
            validateSequence = 'Parent'
        else:
            validateSequence =  int(row)

        if (validateSequence == 'Parent'):
            originalSequence.append(row)
            finalSequences.append(row)
            sequenceLength.append(0)
        else:
            value = validateSequence
            string = finalSequences[-1]
            sequenceLength[-1] += 1
            finalSequences[-1] = string[:value+1] + string + string[value+1:]
    return finalSequences[0], finalSequences[1]

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def time_wrapper(): 
    cost_mismatch = {'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
             'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
             'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
             'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}}
    cost_gap = 30
    begin_time = time.time()
    alignmentCost, xAlignedSeq, yAlignedSeq = align_sequence(first_seq, second_seq, cost_gap, cost_mismatch)
    finish_time = time.time()
    time_diff = abs(finish_time - begin_time)
    time_taken = time_diff*1000 
    return time_taken, alignmentCost, xAlignedSeq, yAlignedSeq

if __name__ == '__main__':
    initialMem = process_memory()

    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    if len(sys.argv) < 3:
        sys.exit('Usage: python basic_3.py input_file output_file')

    try:
        f1 = open(inputFile, 'r')
    except FileNotFoundError:
        sys.exit('Input file not found:', inputFile)

    try:
        f2 = open(outputFile, 'w')
        f2.truncate(0)
    except FileNotFoundError:
        sys.exit('Output file not found', outputFile)
        
    first_seq, second_seq = create_input(f1)

    time_taken, alignmentCost, xAlignedSeq, yAlignedSeq = time_wrapper()

    finalMem = process_memory()
    usedMem = abs(finalMem - initialMem)
    original_stdout = sys.stdout
    sys.stdout = f2
    print(alignmentCost, xAlignedSeq, yAlignedSeq, time_taken, usedMem, sep="\n")
    sys.stdout = original_stdout
