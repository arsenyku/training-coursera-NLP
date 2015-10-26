from __future__ import division
import a3Util as u
from collections import namedtuple

WordMap = namedtuple("WordMap", "f, eCondition")
Alignment = namedtuple("Alignmnent", "Score SentenceIndex SourceWord SourceIndex TargetWord TargetIndex")

# Source = Spanish
# Target = English

class IBM1:
    
    '''*****************************************************************************
    Constructor - initializes class attributes
    *****************************************************************************'''
    def __init__(self):
        self.__tMap = dict()
        self.__nMap = u.Count()
        
        self.__alignedToTargetByPosition = u.Count()
        self.__alignedToAnyByPosition = u.Count()
        self.__alignedToTargetByWord = u.Count()
        self.__alignedToAnyByWord = u.Count()

        self.NULLTAG = "_NULL_"
        

    def Train(self, sourceCorpusFile, targetCorpusFile, iterations):
        
        sourceLines = u.readFromFile(sourceCorpusFile)
        targetLines = u.readFromFile(targetCorpusFile)
        
        if (len(sourceLines) != len(targetLines)):
            print "Source(%s) and target(%s) corpus lengths differ." % (len(sourceLines), len(targetLines))

        print u.now(), "Initializing"
        self.__Initialize(sourceLines, targetLines)

        for s in xrange(0, iterations):
            
            start1 = u.now()
            print start1, "Computing Counts for iteration", s+1
            self.__ComputeCounts(sourceLines, targetLines)
            
            start2 = u.now()
            print start2, "Computing t values for iteration", s+1
            self.__ComputeTValues(sourceLines, targetLines)
                        
            end = u.now()
            
            print u.now(), "Iteration", s+1, "complete."
            print u.now(), "Started count computations at %s." % start1
            print u.now(), "Started t value computations at %s." % start2
            print u.now(), "Finished at %s" % end

            
        return self.__tMap


    def Align(self, sourceFile, targetFile):

        sourceLines = u.readFromFile(sourceFile)
        targetLines = u.readFromFile(targetFile)
        
        if (len(sourceLines) != len(targetLines)):
            print "Source(%s) and target(%s) corpus lengths differ." % (len(sourceLines), len(targetLines))
            
        lineCount = min(len(sourceLines), len(targetLines))
            
        # SentenceIndex, EnglishIndex, ForeignIndex

        alignments = []
        
        for k in xrange(0, lineCount):
            sourceLine = sourceLines[ k ]
            targetLine = targetLines[ k ]

            sourceWords = sourceLine.split()
            sourceWords.insert(0, self.NULLTAG)
            
            targetWords = targetLine.split()
            targetWords.insert(0, self.NULLTAG)

            mk = len(sourceWords)
            lk = len(targetWords)

            for i in xrange(1, mk):
                
                bestAlignment = Alignment(0, 0, "", 0, "", 0)
                                
                for j in xrange(0, lk):
                    
                    fi = sourceWords[i]
                    ej = targetWords[j]
                    
                    tValue = self.__tMap[ WordMap(fi, ej) ]
                    
                    if (bestAlignment.Score < tValue):
                        bestAlignment = Alignment(tValue, k+1, fi, i, ej, j)
            
                alignments.append(bestAlignment)
        
        return alignments
            

    def __Initialize(self, sourceLines, targetLines):
        
        lineCount = min(len(sourceLines), len(targetLines))
                    
        tMap = dict()
        nMap = u.Count()
        
        for i in xrange(0, lineCount):
            
            sourceWords = sourceLines[i].split()
            uniqueSourceWords = u.uniqueWords(sourceWords)
            
            targetWords = targetLines[i].split()
            targetWords.insert(0,self.NULLTAG)
            uniqueTargetWords = u.uniqueWords(targetWords)
            
            #print "Mapping %sth sentence: %s source words, %s target words" % (i, len(sourceWords), len(targetWords))
                
            for sourceWord in uniqueSourceWords:
                for targetWord in uniqueTargetWords:
                    nMap.Increment(targetWord, len(sourceWords))
        
            for sourceWord in sourceWords:
                for targetWord in targetWords:
                    tMap[WordMap(sourceWord, targetWord)] = 1 / nMap.GetCount(targetWord)
        
        
        self.__tMap = tMap
        self.__nMap = nMap
        
        return tMap, nMap
    
    
    
    
    
    def __ComputeCounts(self, sourceLines, targetLines):
        
        self.__alignedToTargetByPosition = u.Count()
        self.__alignedToAnyByPosition = u.Count()
        self.__alignedToTargetByWord = u.Count()
        self.__alignedToAnyByWord = u.Count()
        
        lineCount = min(len(sourceLines), len(targetLines))
        
        progress = u.Progress(lineCount, 100)
       
        for k in xrange(0, lineCount):
            
            sourceWords = sourceLines[k].split()
            sourceWords.insert(0, self.NULLTAG)

            targetWords = targetLines[k].split()
            targetWords.insert(0,self.NULLTAG)

            
            mk = len(sourceWords) - 1
            lk = len(targetWords) - 1
            
            for i in xrange(1, mk+1):
                for j in xrange(0, lk+1):
                    
                    ej = targetWords[j]
                    fi = sourceWords[i]
                    
                    delta = self.ComputeDelta(k, i, j, sourceWords, targetWords)
                    
                    self.__alignedToTargetByWord.Increment((ej, fi),delta)
                    self.__alignedToAnyByWord.Increment((ej),delta)
                    
                    #print "ComputeCounts:", k, j, i, lk, mk, delta
                    self.__alignedToTargetByPosition.Increment((j, i, lk, mk),delta)
                    self.__alignedToAnyByPosition.Increment((i, lk, mk),delta)


            progress.Increment()



    
    def __ComputeTValues(self, sourceLines, targetLines):
        
        lineCount = min(len(sourceLines), len(targetLines))
        
        progress = u.Progress(lineCount, 1000)

        for i in xrange(0, lineCount):
            
            sourceWords = sourceLines[i].split()
            #uniqueSourceWords = u.uniqueWords(sourceWords)
            
            targetWords = targetLines[i].split()
            targetWords.insert(0,self.NULLTAG)
            #uniqueTargetWords = u.uniqueWords(targetWords)
            
            #print "Mapping %sth sentence: %s source words, %s target words" % (i, len(sourceWords), len(targetWords))
                
            for sourceWord in sourceWords:
                for targetWord in targetWords:

                    e = targetWord
                    f = sourceWord

                    numerator = self.__alignedToTargetByWord.GetCount(( e, f ))
                    denominator = self.__alignedToAnyByWord.GetCount( e )
                    
                    if denominator == 0:
                        print "No alignment count for %s" % targetWord
                    
                    self.__tMap[WordMap(f, e)] = numerator / denominator
        
            
            progress.Increment()


#        try:
#            key = WordMap("chipre", "cyprus")
#            val = self.__tMap[key]
#            print key, val
#        except:
#            pass 

        return self.__tMap


    def ComputeDelta(self, sentenceId, sourceWordIndex, targetWordIndex, sourceWords, targetWords):
    
        k = sentenceId
        i = sourceWordIndex
        j = targetWordIndex

        lk = len(targetWords)
        
        fi = sourceWords[i]
        ej = targetWords[j]

        denominator = self.__tMap[WordMap(fi, self.NULLTAG)]

        for index in xrange(0,lk):
            denominator += self.__tMap[WordMap(fi, targetWords[index])]
            
        numerator = self.__tMap[WordMap(fi, ej)]
        
        if denominator == 0:
            print "No T values for k=%s, i=%s, j=%s, fi=%s, ej=%s" % (k, i, j, fi, ej)
        
        return numerator / denominator
        
        
        
        
    def SaveTValues(self, tFile):
        outputLines = []    
        for key, val in self.__tMap.items():
            outputLines.append("%s %s %s" % ( key.f, key.eCondition, val) )
                
        outputText = '\n'.join(outputLines)
        u.saveToFile(tFile, outputText)
        
        
        
    def LoadTValues(self, tFile):
        lines = u.readFromFile(tFile)
        i = 0
        
        for line in lines:
            i += 1
            
            tMapLine = line.split()
            
            if len(tMapLine) != 3:
                print "Invalid line %s: %s" % ( i, line )  
            
            key = WordMap(tMapLine[0], tMapLine[1])
            val = float(tMapLine[2])
            self.__tMap[key] = val 
            
        return self.__tMap
            
        
def SaveAlignments(alignmentFile, alignments):
    # SentenceIndex, EnglishIndex, ForeignIndex

    outputLines = []    
    for alignment in alignments:
        outputLines.append("%s %s %s" % 
            ( alignment.SentenceIndex, alignment.TargetIndex, alignment.SourceIndex ))

    outputText = '\n'.join(outputLines)
    u.saveToFile(alignmentFile, outputText)
 


if (__name__ == "__main__"):
                    
    sourceCorpusFile = "corpus.es"
    targetCorpusFile = "corpus.en"
    
    sourceAlignmentFile = "dev.es"
    targetAlignmentFile = "dev.en"
    aFile = "dev.out"
    
#    sourceCorpusFile = "short.es"
#    targetCorpusFile = "short.en"
    
#    sourceAlignmentFile = "short.es"
#    targetAlignmentFile = "short.en"

    tFile = "tValues.txt"

#    sourceAlignmentFile = "test.es"
#    targetAlignmentFile = "test.en"
#    aFile = "alignment_test.p1.out" 
    
    model = IBM1()

    tMap = model.Train(sourceCorpusFile, targetCorpusFile,5)

    model.SaveTValues(tFile)
#
#    print u.now(), "Loading t values"
#    tMap = model.LoadTValues(tFile)
    
    print u.now(), "Aligning words"
    alignments = model.Align(sourceAlignmentFile, targetAlignmentFile)
    
    print u.now(), "Saving alignments"
    SaveAlignments(aFile, alignments)
    
    print u.now(), "Found %s alignments" % len(alignments)
    print u.now(), "Done"

    
#    for key in tMap.keys():
#        if key.eCondition == "cyprus":
#            print key.f, tMap[key]
    
    print u.now(), "Found %s possible alignment pairings" % len(tMap)

    
    
    #for mapCount in tMap.Items():
    #    print mapCount

