from __future__ import division

''' ------------------------------------------------------------------------------------------
Using the counts produced by count freqs.py, write a function that computes parameters

                       Count(yi-2 , yi-1 , yi )
q(yi |yi-1 , yi-2 ) = -------------------------
                         Count(yi-2 , yi-1 )

for a given trigram yi-2 yi-1 yi. Make sure your function works for the boundary cases q(y1 |*,*),
q(y2|*,y1) and q(STOP|yn-1, yn).

Using the maximum likelihood estimates for transitions and emissions, implement the Viterbi algo-
rithm to compute

                     arg max p(x1...xn , y1...yn ).
                     y1...yn

Be sure to replace infrequent words (Count(x) < 5) in the original training data file and in the decod-
ing algorithm with a common symbol RARE . 

------------------------------------------------------------------------------------------ '''

import sys
import ViterbiData as v
import a1p1



'''*****************************************************************************
readAdjustedWordCounts

Description:
    <insert description here>
    
Parameters:
    <insert paramters here>
    
Return Values:
    <insert return values here>
*****************************************************************************'''

def readAdjustedWordCounts(wordCountFile=""):
    if wordCountFile=="":
        return
    
    emissionCounts=dict()
    unigramCounts=dict()
    bigramCounts=dict()
    trigramCounts=dict()
    
    WordCountType = "WORDTAG"
    UnigramCountType = "1-GRAM"
    BigramCountType = "2-GRAM"
    TrigramCountType = "3-GRAM"

    lines = a1p1.readFromFile(wordCountFile)
    
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
            wordTagCountList.append(v.UnigramCount(tag, count))
            
        elif(countType == UnigramCountType):
            
            unigramCounts[tag] = count  
   
        elif(countType == BigramCountType):

            bigramCount = v.BigramCount(splitLine[2], splitLine[3], count)
            
            if (False==bigramCounts.has_key( bigramCount.n2 )):
                bigramCounts[ bigramCount.n2 ] = []
                
            bigramCountList = bigramCounts[ bigramCount.n2 ]
            
            bigramCountList.append(bigramCount)  

        elif(countType == TrigramCountType):

            trigramCount = v.TrigramCount(splitLine[2], splitLine[3], splitLine[4], count)
             
            if (False==trigramCounts.has_key( trigramCount.n3 )):
                trigramCounts[ trigramCount.n3 ] = []
                
            trigramCountList = trigramCounts[ trigramCount.n3 ]
            
            trigramCountList.append(trigramCount)
            

    return v.ViterbiData(emissionCounts, unigramCounts, bigramCounts, trigramCounts)

            
            




def TagGenes(inputFile="", outputFile="", wordCountsFile="", singleRareGroup=True):
    if inputFile=="" or outputFile=="":
        return

    vitData = readAdjustedWordCounts(wordCountsFile)
    
    vitData.SingleRareGroup = singleRareGroup

    lines = a1p1.readFromFile(inputFile)
    
    outputLines = []
    sentence = []
    
    for line in lines:
        word = line.strip()
        
        if word != "":
            sentence.append(word)
        
        else:
        
            tagSequence = vitData.GetTagSequence(sentence)

            for i in xrange(0, len(sentence)):
                taggedWord = "%s %s" % ( sentence[i], tagSequence[i] )
                outputLines.append(taggedWord)
            
            sentence = []
            vitData.ClearPiTable()
            outputLines.append('')
    
    outputLines.append('')
    
    outputText = '\n'.join(outputLines)
    
    a1p1.saveToFile(outputFile, outputText)





if (__name__ == "__main__"):

    wordCountsFile="gene.adjusted.counts"
    
#    a1p1.Preprocess("gene.counts", "gene.train", "gene.adjusted.train")
    
    
    print "Start"

    TagGenes("gene.dev","gene_dev.p2.out",wordCountsFile)
    TagGenes("gene.test","gene_test.p2.out",wordCountsFile)

    print "Done Tag Genes"

#    emissionCounts=dict()
#    unigramCounts=dict()
#    bigramCounts=dict()
#    trigramCounts=dict()
#    
#    readAdjustedWordCounts(wordCountsFile, emissionCounts, unigramCounts, bigramCounts, trigramCounts)
#    vit = v.ViterbiData(emissionCounts, unigramCounts, bigramCounts, trigramCounts)
#    
#    sentence = ['Anti', '-', 'nucleolin', 'mAb', 'was', 'used', 'to'] #, 'confirm', 'the', 'antigenic', 'properties', 'of', 'this', 'p95', 'component', '.']

#    sentence = ['Perfusion', 'technique', 'for', 'perfusion', '-', 'assisted', 'direct', 'coronary', 'artery', 'bypass', '(', 'PADCAB', ').']
#
#    sentence = ['The', 'amount', 'of', 'drained', 'effusion', 'was', 'measured', ',', 'and', 'fluid', 'was', 'sent', 'for', 'diagnostic', 'assessment', '.']
#
#
    O = "O"
    G = "I-GENE"
    Start = "*"
    Stop = "STOP"

    vit = readAdjustedWordCounts(wordCountsFile)
#
#    q = vit.q(Start, Start, G)
#    e = vit.e("STAT5A",G)
#    
#    print q , e, q*e
    
#
#    sentence = ['in', 'response', 'to', 'IL', '-', '2', 'but'] #, 'as', 'yet']
#    sentence = ['Anti', '-', 'nucleolin', 'mAb', 'was', 'used', 'to'] #, 'confirm', 'the', 'antigenic', 'properties', 'of', 'this', 'p95', 'component', '.']
#


#    sentence = ['STAT5A', 'mutations', 'in', 'the', 'Src', 'homology', '2', '(', 'SH2', ')', 'and', 'SH3', 'domains', 'did', 'not', 'alter', 'the', 'BTK', '-', 'mediated', 'tyrosine', 'phosphorylation', '.']
#
#    print vit.GetTagSequence(sentence)
#
#    maxPi, uTag, vTag = vit.GetMaxPi(sentence)
#
#
#    print "*" * 40
#    piTable = vit.GetPiTable()
#    
#    piTableKeys = sorted(piTable, key=lambda kvalue: kvalue[0]) 
#    
#    for key in piTableKeys:
#        print key, piTable[key][0]
#
#    q = vit.q(Start, Start, G)
#    e = vit.e("STAT5A", G)
#    print q, e, q*e

    
#    n = len(sentence)
#    Yk = ''
#    
#    tagSequence = []
#
#    tagSequence.insert(0, vTag)
#    tagSequence.insert(0, uTag)
#
#    for k in xrange(n-2, 0, -1):
#        if (k == n-2):
#            Ykplus1 = uTag
#            Ykplus2 = vTag
#        else:
#            Ykplus2 = Ykplus1
#            Ykplus1 = Yk 
#        
#        Yk = vit.GetTagValue(k+2, Ykplus1, Ykplus2 )
#        
#        tagSequence.insert(0, Yk)
    
#    tagSequence = vit.GetTagSequence(uTag, vTag, sentence)
    
    
    #print n, len(tagSequence)
#    print sentence
#    print tagSequence


#    s = ['IL', '-', '2']
    
#    print vit.MaxPi(0, Start, O, s)
#    print MaxPi(s, Start, O, vit)
    
#    print MaxPi(s, O, G, vit)
#    print MaxPi(s, G, G, vit)

    
    
#    piValue, tags = GetMaxPi(sentence, vit)

#    print piValue, tags
#
#    piValue, tags = MaxPi(sentence, "O", "O", vit)
#    
#    print piValue, tags
#    
#
#    
#    print MaxPi(sentence, "I-GENE", "I-GENE", vit)
#
#    print vit.q("I-GENE", "I-GENE", "I-GENE")
#    print vit.e("-", "I-GENE")
#    
#    print vit.q("O", "O", "I-GENE")
#    
#    print vit.e("bovine", "I-GENE")
#    print vit.e("bovine", "O")
#
#    print ComputeTrigramParameter("O", "O", "O", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("O", "O", "I-GENE", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("O", "I-GENE", "O", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("O", "I-GENE", "I-GENE", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("I-GENE", "O", "O", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("I-GENE", "O", "I-GENE", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("I-GENE", "I-GENE", "O", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("I-GENE", "I-GENE", "I-GENE", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("*", "*", "I-GENE", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("*", "*", "O", bigramCounts, trigramCounts)
#
#    print "*" * 40
#    
#    print ComputeTrigramParameter("O", "O", "STOP", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("O", "I-GENE", "STOP", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("I-GENE", "O", "STOP", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("I-GENE", "I-GENE", "STOP", bigramCounts, trigramCounts)
#
#    print "*" * 40
#
#    print ComputeTrigramParameter("*", "I-GENE", "O", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("*", "O", "I-GENE", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("*", "O", "O", bigramCounts, trigramCounts)
#    print ComputeTrigramParameter("*", "I-GENE", "I-GENE", bigramCounts, trigramCounts)



#    for k in bigramCounts.keys():
#        bigramCountList = bigramCounts[k]
#        for b in bigramCountList:
#            print b 
#
#    print "*" * 40
#        
#    for k in trigramCounts.keys():
#        print "Key = %s" % k
#        trigramCountList = trigramCounts[k]
#        for t in trigramCountList:
#            print t 

