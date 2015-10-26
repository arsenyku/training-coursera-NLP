from __future__ import division
''' --------------------------------------------------------------------------------------------------
Using the counts produced by count freqs.py, write a function that computes emission parameters

           Count(y ; x)
e(x|y) =  --------------
             Count(y)
             
- We need to predict emission probabilities for words in the test data that do not occur in the training
data. One simple approach is to map infrequent words in the training data to a common class and to
treat unseen words as members of this class. Replace infrequent words (Count(x) < 5) in the orig-
inal training data file with a common symbol RARE . Then re-run count freqs.py to produce
new counts. 

- As a baseline, implement a simple gene tagger that always produces the tag y* = arg max e(x|y)
                                                                                       y
for each word x. Make sure your tagger uses the RARE word probabilities for rare and unseen words.
Your tagger should read in the counts file and the file gene.dev (which is gene.key without the
tags) and produce output in the same format as the training file. For instance
                               Nations I-ORG 
Write your output to a file called gene dev.p1.out and locally evaluate by running 
                python eval gene tagger.py gene.key gene dev.p1.out
                
The expected result should match the result above. When you are ready to submit, run your model on
gene.test and write the output to gene test.p1.out. Run python submit.py to submit.
-------------------------------------------------------------------------------------------------- '''

import time
from collections import namedtuple

TagCount = namedtuple('TagCount', 'Tag Count')

'''*****************************************************************************
saveToFile

Description:
    This function takes any string and writes it to a file.
    
Parameters:
    filename = the file to be written
    
    text = the text to be written into the file
    
Return Values:
    None 
*****************************************************************************'''
def saveToFile(filename="", text=""):
    if filename=="":
        return
    
    outFileHandle = open(filename,"w")
    outFileHandle.write(text)
    outFileHandle.close()
    
    
    
    
'''*****************************************************************************
readFromFile

Description:
    This function reads a text file and returns a list containing the lines of 
    the file
    
Parameters:
    filename = the file to be read
    
Return Values:
    A list of the lines of the file 
*****************************************************************************'''
def readFromFile(filename=""):
    if filename=="":
        return
    
    # Open and read the contents of the database
    inFileHandle = open(filename)
    lines = inFileHandle.readlines()
    inFileHandle.close()
    
    return lines




    
    
'''*****************************************************************************
getRareWords

Description:
    <insert description here>
    
Parameters:
    <insert paramters here>
    
Return Values:
    <insert return values here>
*****************************************************************************'''
def getRareWords(wordCountsFile="", threshold=5):

    WordCountType = "WORDTAG"

    lines = readFromFile(wordCountsFile)
    
    result = []
    wordCounts = dict()
    
    for line in lines:
        splitLine = line.split()
        
        wordCount = int(splitLine[0])
        countType = splitLine[1]
        
        if (countType != WordCountType):
            continue
        
        word = splitLine[3]
        
        if (False == wordCounts.has_key(word)):
            wordCounts[word] = 0
            
        wordCounts[word] += wordCount
        
    for word in wordCounts.keys():
        
        wordCount = wordCounts[word]
        
        if wordCount < threshold:
            result.append(word)
        
    return result



'''*****************************************************************************
replaceRareWords

Description:
    <insert description here>
    
Parameters:
    <insert paramters here>
    
Return Values:
    <insert return values here>
*****************************************************************************'''
def replaceRareWords(rareWords=[], original="", newfile="", replacement="_RARE_"):
    if original=="" or newfile=="":
        return
    
    output = []
    
    originalLines = readFromFile(original)
    
    replaced = 0
    
    for line in originalLines:
        splitLine = line.split()
        
        if (len(splitLine) < 2):
            output.append("")
            continue
        
        word = splitLine[0]
        tag = splitLine[1]
        
        newLine = "%s %s" % (word, tag)
        
        if word in rareWords:
            newLine = "%s %s" % (replacement, tag)
            replaced += 1

        output.append(newLine)
        
    outputText = '\n'.join(output)
    
    saveToFile(newfile, outputText)
    
    return replaced
    

'''*****************************************************************************
readAdjustedWordCounts

Description:
    <insert description here>
    
Parameters:
    <insert paramters here>
    
Return Values:
    <insert return values here>
*****************************************************************************'''
def readAdjustedWordCounts(wordCountFile="", emissionCounts=dict(), unigramCounts=dict()):
    if wordCountFile=="":
        return
    
    WordCountType = "WORDTAG"
    UnigramCountType = "1-GRAM"

    lines = readFromFile(wordCountFile)
    
    for line in lines:
        splitLine = line.split()
        
        count = int(splitLine[0])
        countType = splitLine[1]
        tag = splitLine[2]
        
        if (countType == WordCountType):
            word = splitLine[3]
            
            if False == emissionCounts.has_key(word):
                emissionCounts[word] = []
            
            wordTagCountList = emissionCounts[word]
            wordTagCountList.append(TagCount(tag, count))
            
        elif(countType == UnigramCountType):
            
            unigramCounts[tag] = count  
   
            
        
'''*****************************************************************************
getBestTag

Description:
    <insert description here>
    
Parameters:
    <insert paramters here>
    
Return Values:
    <insert return values here>
*****************************************************************************'''
def getBestTag(word="", emissionCounts=dict(), unigramCounts=dict(), rareTag="_RARE_", details=False):
    
    countList = []
    if (emissionCounts.has_key(word)):
        countList = emissionCounts[word]
    else:
        countList = emissionCounts[rareTag]
        
    maxEmission = 0
    bestTags = []
    
    for tag, count in countList:
        
        unigramCount = unigramCounts[tag]
        
        emission = count / unigramCount
        
        if (emission > maxEmission):
            maxEmission = emission
            bestTags = []
            bestTags.append(tag)
        
        elif (emission == maxEmission):
            bestTags.append(tag)

        if details:
            print tag, count, unigramCount, emission

    return bestTags
    

'''*****************************************************************************
TagGenes

Description:
    <insert description here>
    
Parameters:
    <insert paramters here>
    
Return Values:
    <insert return values here>
*****************************************************************************'''
def TagGenes(inputFile="", outputFile="", countsFile=""):
    if inputFile=="" or outputFile=="":
        return
    
    emissionCounts = dict()
    unigramCounts = dict()
    readAdjustedWordCounts(countsFile, emissionCounts, unigramCounts)

    lines = readFromFile(inputFile)
    
    outputLines = []
    
    for line in lines:
        word = line.strip()
        
        if word == "":
            outputLines.append(word)
            continue
        
        bestTag = getBestTag(word, emissionCounts, unigramCounts)[0]
        
        outputLines.append(" ".join((word, bestTag)))
        
    outputLines.append('')
    
    outputText = '\n'.join(outputLines)
    
    saveToFile(outputFile, outputText)
    
    
'''*****************************************************************************
Preprocess

Description:
    <insert description here>
    
Parameters:
    <insert paramters here>
    
Return Values:
    <insert return values here>
*****************************************************************************'''
def Preprocess(countsFile="", trainingFile="", adjustedTrainingFile="", rareTag="_RARE_"):
    if countsFile=="" or trainingFile=="" or adjustedTrainingFile=="":
        return

    rare = getRareWords(countsFile)
    print "Found %s rare words" % ( len(rare) )
        
    # ---------------------------------------------------------------------------------
            
    start = time.time()
    print "Start %s" % time.strftime("%H:%M:%S", time.localtime(start))
        
    replaced = replaceRareWords(rare, trainingFile, adjustedTrainingFile, rareTag)
        
    end = time.time()
    print "End %s" % time.strftime("%H:%M:%S", time.localtime(end))
        
    elapsed = end - start 
    print "Replaced %s words.  Elapsed: %ss" % ( replaced, elapsed )
        
    # ---------------------------------------------------------------------------------


if (__name__ == "__main__"):
    import os
#    Preprocess("gene.counts", "gene.train", "gene.adjusted.train")
#    os.system("python count_freqs.py gene.adjusted.train > gene.adjusted.counts")

#    rare = getRareWords("gene.counts")
#    print "Found %s rare words" % ( len(rare) )
#        
#        # ---------------------------------------------------------------------------------
#            
#        start = time.time()
#        print "Start %s" % time.strftime("%H:%M:%S", time.localtime(start))
#        
#        replaced = replaceRareWords(rare, "gene.train", "gene.adjusted.train", "_RARE_")
#        
#        end = time.time()
#        print "End %s" % time.strftime("%H:%M:%S", time.localtime(end))
#        
#        elapsed = end - start 
#        print "Replaced %s words.  Elapsed: %ss" % ( replaced, elapsed )
#        
#        # ---------------------------------------------------------------------------------

#    emissionCounts = dict()
#    unigramCounts = dict()
#    readAdjustedWordCounts("gene.adjusted.counts", emissionCounts, unigramCounts)
    
#    print "I-GENE: %s" % unigramCounts["I-GENE"]
#    print "O: %s" % unigramCounts["O"]

#    for word in emissionCounts.keys():
#        countList = emissionCounts[word]
#        if len(countList) > 1:
#            print "%s %s %s" % (word, countList[0].Tag, countList[0].Count)
#            print "%s %s %s" % (word, countList[1].Tag, countList[1].Count)
#
#    print "Found %s tags, %s emissions." % ( len(unigramCounts), len(emissionCounts))
#    
#    print "zinc", getBestTag("zinc", emissionCounts, unigramCounts)
#    print "frame", getBestTag("frame", emissionCounts, unigramCounts)
#    print rare[5], getBestTag(rare[5], emissionCounts, unigramCounts)
#    print rare[14]
#    print getBestTag(rare[14], emissionCounts, unigramCounts, details=True)

    TagGenes("gene.dev", "gene_dev.p1.out", "gene.adjusted.counts")
    TagGenes("gene.test", "gene_test.p1.out", "gene.adjusted.counts")
    
    print "Done"
    
    
    
