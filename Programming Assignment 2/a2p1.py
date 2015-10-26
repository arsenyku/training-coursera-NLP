from __future__ import division
import json
import a2Util as u

    
'''*****************************************************************************
readCounts

Description:
    <insert description here>
    
Parameters:
    <insert paramters here>
    
Return Values:
    <insert return values here>
*****************************************************************************'''
def readCounts(parseTreeCountsFile="", rareThreshold=5):

    NONTERMINAL_TYPE = "NONTERMINAL"
    BINARY_TYPE = "BINARYRULE"
    UNARY_TYPE = "UNARYRULE"

    lines = u.readFromFile(parseTreeCountsFile)
    
    nonTerminalCounts = u.Count()
    binaryCounts = u.Count()
    unaryCounts = u.Count()
    wordCounts = u.Count()
    
    for line in lines:
        splitLine = line.split()
        
        countToken = int(splitLine[0])
        typeToken = splitLine[1]

        if typeToken == NONTERMINAL_TYPE:

            nonTerminalToken = splitLine[2]
            nonTerminalCounts.Increment(nonTerminalToken, countToken)
            
        elif typeToken == BINARY_TYPE:

            binaryRule = u.BinaryRule(splitLine[2], splitLine[3], splitLine[4])
            binaryCounts.Increment(binaryRule, countToken)
            
        elif typeToken == UNARY_TYPE:

            unaryRule = u.UnaryRule(splitLine[2], splitLine[3])
            unaryCounts.Increment(unaryRule, countToken)
            wordCounts.Increment(unaryRule.Child, countToken)
        
        else:
            print "Unrecognized Line:", line
            continue


    rareWords = []
    
    for word, count in wordCounts.Items():
        if (count < rareThreshold):
            rareWords.append(word)
             
    return nonTerminalCounts, binaryCounts, unaryCounts, wordCounts, rareWords





def replaceLeaves(tree, wordsToReplace, replacement):
    
    for i in xrange(0,len(tree)):
        node = tree[i]
        
        if u.is_sequence(node):
            replaceLeaves(node, wordsToReplace, replacement)
        
        else:
            
            if i == 0:
                continue
            
            for word in wordsToReplace:
                if (node == word):
                    tree[i] = replacement
                    continue
            
    return tree
    



'''*****************************************************************************
Preprocess

Description:
    <insert description here>
    
Parameters:
    <insert paramters here>
    
Return Values:
    <insert return values here>
*****************************************************************************'''
def Preprocess(countsFile="", trainingFile="", adjustedTrainingFile=""):
    if countsFile=="" or trainingFile=="" or adjustedTrainingFile=="":
        return

    RARETAG = '_RARE_'

    print "Preprocess started at", u.now()

    rareWords = readCounts(countsFile)[4]
    
    lines = u.readFromFile(trainingFile)
    
    newTrees = []
    
    processed = 0
    progressThreshold = 100
    
    for line in lines:
        #print "Processing:", line
        
        tree = json.loads(line)
        newTree = replaceLeaves(tree, rareWords, RARETAG)
        outputLine = json.dumps(newTree)
        
        newTrees.append(outputLine)
        
        processed += 1
        if progressThreshold <= processed:
            print u.now(), "Processed", processed
            progressThreshold += 100
        
    outputText = '\n'.join(newTrees)

    u.saveToFile(adjustedTrainingFile, outputText)

    
    print "Preprocess ended at", u.now()
    
    

if (__name__ == "__main__"):

    countsFile="cfg.counts"
    adjustedCountsFile = "parse_train.counts.out"

    Preprocess(countsFile, "parse_train.dat", "parse_train.adjusted.dat")
    
    

    
    
#    rareWords = readCounts(countsFile)[4]
#    u.saveToFile("rarewords.txt", '\n'.join(rareWords))

    
#    tree = json.loads(open("tree.example").readline())
#
#    print tree[2][1][1][1]
#    
#    replaceLeaves(tree, ["is"], "_RARE_")
#    
#    print tree[2][1][1][1]
    




    

