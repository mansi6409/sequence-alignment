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

def string_similarity(seq1, seq2, gap_penalty, scoring_matrix):
    alignmentCosts = [[0 for _ in range(len(seq2)+1)] for _ in range(len(seq1)+1)]

    xLen, yLen = len(seq1), len(seq2)
    for xIndex in range(xLen+1):
        alignmentCosts[xIndex][0] = xIndex * gap_penalty

    for yIndex in range(yLen+1):
        alignmentCosts[0][yIndex] = yIndex * gap_penalty

    for xIndex in range(1, xLen+1):
        for yIndex in range(1, yLen+1):
            alignmentCosts[xIndex][yIndex] = min(alignmentCosts[xIndex-1][yIndex] + gap_penalty,
                                                 alignmentCosts[xIndex][yIndex-1] + gap_penalty,
                                                 alignmentCosts[xIndex-1][yIndex-1] + scoring_matrix[seq1[xIndex-1]][seq2[yIndex-1]])
    return alignmentCosts

def align_sequence(seq1, seq2, gap_penalty, scoring_matrix):
    xIndex, yIndex = len(seq1), len(seq2)
    xAlignedSeq, yAlignedSeq = str(), str()
    alignmentCosts = string_similarity(seq1, seq2, gap_penalty, scoring_matrix)

    while not (xIndex == 0 and yIndex == 0):
        xTemp, yTemp = '_', '_'
        if (xIndex == 0):
            xAlignedSeq = '_' * yIndex + xAlignedSeq
            yAlignedSeq = seq2[:yIndex] + yAlignedSeq
            break
        if (yIndex == 0):
            xAlignedSeq = seq1[:xIndex] + xAlignedSeq
            yAlignedSeq = '_' * xIndex + yAlignedSeq
            break
        if (gap_penalty + alignmentCosts[xIndex][yIndex-1] == alignmentCosts[xIndex][yIndex]):
            yTemp = seq2[yIndex-1]
            yIndex -= 1
        elif (gap_penalty + alignmentCosts[xIndex-1][yIndex] == alignmentCosts[xIndex][yIndex]):
            xTemp = seq1[xIndex-1]
            xIndex -= 1
        elif ((scoring_matrix[seq1[xIndex-1]][seq2[yIndex-1]] + alignmentCosts[xIndex-1][yIndex-1]) == alignmentCosts[xIndex][yIndex]):
            xTemp = seq1[xIndex-1]
            yTemp = seq2[yIndex-1]
            xIndex -= 1
            yIndex -= 1
            
        xAlignedSeq = xTemp + xAlignedSeq
        yAlignedSeq = yTemp + yAlignedSeq

    return alignmentCosts[len(seq1)][len(seq2)], xAlignedSeq, yAlignedSeq

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def time_wrapper(): 
    gap_penalty = 30
    scoring_matrix = {'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
             'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
             'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
             'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}}
    start_time = time.time() 
    alignmentCost, xAlignedSeq, yAlignedSeq = align_sequence(seq1, seq2, gap_penalty, scoring_matrix)
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
        
    seq1, seq2 = create_input(f1)

    time_taken, alignmentCost, xAlignedSeq, yAlignedSeq = time_wrapper()

    finalMem = process_memory()
    usedMem = abs(finalMem - initialMem)
    original_stdout = sys.stdout
    sys.stdout = f2
    print(alignmentCost, xAlignedSeq, yAlignedSeq, time_taken, usedMem, sep="\n")
    sys.stdout = original_stdout
