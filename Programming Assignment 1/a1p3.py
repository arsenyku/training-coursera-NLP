import time, os
import utility as u
import a1p1
import a1p2
import ViterbiData



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

    rare = a1p1.getRareWords(countsFile)
    print "Found %s rare words" % ( len(rare) )
    
    
    numeric, allCaps, lastCap, rare = u.CategorizeRareWords(rare)
        
    tempOutput1 = "temporaryfile.1"
    tempOutput2 = "temporaryfile.2"
        
    # ---------------------------------------------------------------------------------

    start = time.time()
    print "Start %s" % time.strftime("%H:%M:%S", time.localtime(start))
        
    print "Replacing Numeric Words"
    replaced = replaceWords(numeric, trainingFile, tempOutput1, "_NUMERIC_")
        
    end = time.time()
    print "End %s" % time.strftime("%H:%M:%S", time.localtime(end))
        
    elapsed = end - start 
    print "Replaced %s words.  Elapsed: %ss" % ( replaced, elapsed )

    # ---------------------------------------------------------------------------------

    start = time.time()
    print "Start %s" % time.strftime("%H:%M:%S", time.localtime(start))
        
    print "Replacing AllCaps Words"
    replaced = replaceWords(allCaps, tempOutput1, tempOutput2, "_ALLCAPS_")
        
    end = time.time()
    print "End %s" % time.strftime("%H:%M:%S", time.localtime(end))

    elapsed = end - start 
    print "Replaced %s words.  Elapsed: %ss" % ( replaced, elapsed )

    # ---------------------------------------------------------------------------------

    start = time.time()
    print "Start %s" % time.strftime("%H:%M:%S", time.localtime(start))
        
    print "Replacing Ends-in-Capital Words"
    replaced = replaceWords(lastCap, tempOutput2, tempOutput1, "_LASTCAP_")
        
    end = time.time()
    print "End %s" % time.strftime("%H:%M:%S", time.localtime(end))

    elapsed = end - start 
    print "Replaced %s words.  Elapsed: %ss" % ( replaced, elapsed )

    # ---------------------------------------------------------------------------------

    start = time.time()
    print "Start %s" % time.strftime("%H:%M:%S", time.localtime(start))
        
    print "Replacing uncategorized rare Words"
    replaced = replaceWords(rare, tempOutput1, adjustedTrainingFile, "_RARE_")
    print "Replaced %s words" % replaced
        
    end = time.time()
    print "End %s" % time.strftime("%H:%M:%S", time.localtime(end))
        
    elapsed = end - start 
    print "Replaced %s words.  Elapsed: %ss" % ( replaced, elapsed )
        
    # ---------------------------------------------------------------------------------
    
    
    os.remove(tempOutput1)
    os.remove(tempOutput2)
    print "Cleanup done."
    



'''*****************************************************************************
replaceRareWords

Description:
    <insert description here>
    
Parameters:
    <insert paramters here>
    
Return Values:
    <insert return values here>
*****************************************************************************'''
def replaceWords(wordsToReplace=[], original="", newfile="", replacement="_REPLACEMENT_"):
    if original=="" or newfile=="":
        return
    
    output = []
    
    originalLines = a1p1.readFromFile(original)
    
    replaced = 0
    
    for line in originalLines:
        splitLine = line.split()
        
        if (len(splitLine) < 2):
            output.append("")
            continue
        
        word = splitLine[0]
        tag = splitLine[1]
        
        newLine = "%s %s" % (word, tag)
        
        if word in wordsToReplace:
            newLine = "%s %s" % (replacement, tag)
            replaced += 1

        output.append(newLine)
        
    outputText = '\n'.join(output)
    
    a1p1.saveToFile(newfile, outputText)
    
    return replaced
    





if (__name__ == "__main__"):

    wordCountsFile="gene.adjusted.p3.counts"

    #Preprocess("gene.counts", "gene.train", "gene.adjusted.p3.train")
    
    print "Start"

    a1p2.TagGenes("gene.dev","gene_dev.p3.out",wordCountsFile, singleRareGroup=False)
    a1p2.TagGenes("gene.test","gene_test.p3.out",wordCountsFile, singleRareGroup=False)

    print "Done Tag Genes"




















