from __future__ import division
from collections import namedtuple
import a3Util as u
import a3p1

AlignmentByPosition = namedtuple("AlignmnentByPosition", "j, iCondition, lCondition, mCondition")

class IBM2(a3p1.IBM1):
    
    '''*****************************************************************************
    Constructor - initializes class attributes
    *****************************************************************************'''
    def __init__(self):
        self.__qMap = dict()
        a3p1.IBM1.__init__(self)


    def Train(self, sourceCorpusFile, targetCorpusFile, iterations, tFile):
        
        sourceLines = u.readFromFile(sourceCorpusFile)
        targetLines = u.readFromFile(targetCorpusFile)
        
        if (len(sourceLines) != len(targetLines)):
            print "Source(%s) and target(%s) corpus lengths differ." % (len(sourceLines), len(targetLines))

        if (tFile == ""):
            print u.now(), "Initializing"
            self._IBM1__Initialize(sourceLines, targetLines)
        else:
            print u.now(), "Loading Initial T Values"
            self.LoadTValues(tFile)

        for s in xrange(0, iterations):
            
            for x in xrange(0,9):
                print "Iteration", s, ":", x, "2 8 8", self.GetQValue(x, 2, 8, 8)

            start1 = u.now()
            print start1, "Computing Counts for iteration", s+1
            self._IBM1__ComputeCounts(sourceLines, targetLines)
            
            start2 = u.now()
            print start2, "Computing t values for iteration", s+1
            self._IBM1__ComputeTValues(sourceLines, targetLines)
            
            start3 = u.now()
            print start3, "Computing q values for iteration", s+1
            self.__ComputeQValues(sourceLines, targetLines)
                        
            end = u.now()
            
            print u.now(), "Iteration", s+1, "complete."
            print u.now(), "Started count computations at %s." % start1
            print u.now(), "Started t value computations at %s." % start2
            print u.now(), "Started q value computations at %s." % start3
            print u.now(), "Iteration", s+1, "finished at %s" % end

            
        return self._IBM1__tMap




    def Align(self, sourceFile, targetFile):

        sourceLines = u.readFromFile(sourceFile)
        targetLines = u.readFromFile(targetFile)
        
        if (len(sourceLines) != len(targetLines)):
            print "Source(%s) and target(%s) corpus lengths differ." % (len(sourceLines), len(targetLines))
            
        lineCount = min(len(sourceLines), len(targetLines))
            
        # SentenceIndex, EnglishIndex, ForeignIndex

        alignments = []
        
        for k in xrange(0, lineCount):
        
            sourceWords = sourceLines[k].split()
            sourceWords.insert(0, self.NULLTAG)

            targetWords = targetLines[k].split()
            targetWords.insert(0,self.NULLTAG)

            mk = len(sourceWords) - 1
            lk = len(targetWords) - 1

            for i in xrange(1, mk+1):
                
                bestAlignment = a3p1.Alignment(0, 0, "", 0, "", 0)
                                
                for j in xrange(0, lk+1):

                    fi = sourceWords[i]
                    ej = targetWords[j]

                    tValue = self._IBM1__tMap[ a3p1.WordMap(fi, ej) ]
                    #qValue = self.__qMap[ AlignmentByPosition(j, i, lk, mk) ]
                    qValue = self.GetQValue(j, i, lk, mk)
                    score = tValue * qValue

                    if (bestAlignment.Score < score):
                        bestAlignment = a3p1.Alignment(score, k+1, fi, i, ej, j)

                alignments.append(bestAlignment)

        return alignments
    
    
    
#
#    def __Initialize(self, sourceLines, targetLines, tFile=""):
#        
#        lineCount = min(len(sourceLines), len(targetLines))
#                    
#        tMap = dict()
#        qMap = dict()
#        nMap = u.Count()
#        
#        if tFile != "":
#            self.LoadTValues(tFile)
#        
#        for k in xrange(0, lineCount):
#            
#            sourceWords = sourceLines[k].split()
#            uniqueSourceWords = u.uniqueWords(sourceWords)
#            
#            targetWords = targetLines[k].split()
#            targetWords.insert(0,self.NULLTAG)
#            uniqueTargetWords = u.uniqueWords(targetWords)
#            
#            #print "Mapping %sth sentence: %s source words, %s target words" % (i, len(sourceWords), len(targetWords))
#            
#            if (tFile == ""):
#                for sourceWord in uniqueSourceWords:
#                    for targetWord in uniqueTargetWords:
#                        nMap.Increment(targetWord, len(sourceWords))
#            
#                for sourceWord in sourceWords:
#                    for targetWord in targetWords:
#                        tMap[a3p1.WordMap(sourceWord, targetWord)] = 1 / nMap.GetCount(targetWord)
#                    
#                    
#            sourceWords.insert(0,self.NULLTAG)
#
#            mk = len(sourceWords) - 1
#            lk = len(targetWords) - 1
#                    
#            for i in xrange(1, mk+1):
#                for j in xrange(0, lk+1):
#
#                    qMap[AlignmentByPosition(j, i, lk, mk)] = 1 / ( lk + 1 ) 
#        
#
#        if (tFile == ""):
#            self._IBM1__tMap = tMap
#            self._IBM1__nMap = nMap
#        
#        self.__qMap = qMap
#
#        return self._IBM1__tMap, self.__qMap, self._IBM1__nMap
#    
    
    
    def __ComputeQValues(self, sourceLines, targetLines):
        
        lineCount = min(len(sourceLines), len(targetLines))
        
        progress = u.Progress(lineCount, 1000)
        progress.PreText = "Processed q values"

        for k in xrange(0, lineCount):
            
            sourceWords = sourceLines[k].split()
            sourceWords.insert(0,self.NULLTAG)
            
            targetWords = targetLines[k].split()
            targetWords.insert(0,self.NULLTAG)
 
            mk = len(sourceWords) - 1
            lk = len(targetWords) - 1
            
            
            for i in xrange(1, mk + 1):
                for j in xrange(0,lk + 1):

                    numerator = self._IBM1__alignedToTargetByPosition.GetCount(( j, i, lk, mk ))
                    denominator = self._IBM1__alignedToAnyByPosition.GetCount(( i, lk, mk ))
                    
                    if denominator == 0:
                        print "No alignment count for k=%s, j=%s, i=%s, l=%s, m=%s" % (k, j, i, lk, mk)

                    else:
                        self.SetQValue(j, i, lk, mk, numerator/denominator)
                        #self.__qMap[AlignmentByPosition(j, i, lk, mk)] = numerator / denominator
        
            
            progress.Increment()


    
    def SetQValue(self, targetWordIndex, sourceWordIndex, targetSentenceLength, sourceSentenceLength, qValue):

        j = targetWordIndex
        i = sourceWordIndex
        lk = targetSentenceLength
        mk = sourceSentenceLength
        
        key = AlignmentByPosition(j, i, lk, mk)

        self.__qMap[ key ] = qValue

    
    def GetQValue(self, targetWordIndex, sourceWordIndex, targetSentenceLength, sourceSentenceLength):
        
        j = targetWordIndex
        i = sourceWordIndex
        lk = targetSentenceLength
        mk = sourceSentenceLength
        
        key = AlignmentByPosition(j, i, lk, mk)
        
        result = 1 / ( lk + 1 )
        
        if (self.__qMap.has_key(key)):
            result = self.__qMap[key]


        return result



    def ComputeDelta(self, sentenceId, sourceWordIndex, targetWordIndex, sourceWords, targetWords):

        k = sentenceId
        i = sourceWordIndex
        j = targetWordIndex

        mk = len(sourceWords) - 1
        lk = len(targetWords) - 1
        
        fi = sourceWords[i]
        ej = targetWords[j]

        tValue = self._IBM1__tMap[a3p1.WordMap(fi, ej)]
        qValue = self.GetQValue(j, i, lk, mk)
        #qValue = self.__qMap[AlignmentByPosition(j, i, lk, mk)]

        numerator = qValue * tValue

        denominator = 0
        for index in xrange(0,lk+1):
            tValue = self._IBM1__tMap[a3p1.WordMap(fi, targetWords[index])]
            qValue = self.GetQValue(index, i, lk, mk)
            #qValue = self.__qMap[AlignmentByPosition(index, i, lk, mk)]
            
            denominator += qValue * tValue
            
        if denominator == 0:
            print "No T values for k=%s, i=%s, j=%s, l=%s, m=%s, fi=%s, ej=%s" % (k, i, j, lk, mk, fi, ej)
        
        return numerator / denominator
        


        
    def SaveQValues(self, qFile):
        outputLines = []    
        for key, val in self.__qMap.items():
            outputLines.append("%s %s %s %s %s" % 
                ( key.j, key.iCondition, key.lCondition, key.mCondition, val) )
                
        outputText = '\n'.join(outputLines)
        u.saveToFile(qFile, outputText)
        
        
        
    def LoadQValues(self, qFile):
        lines = u.readFromFile(qFile)
        i = 0
        
        for line in lines:
            i += 1
            
            qMapLine = line.split()
            
            if len(qMapLine) != 5:
                print "Invalid line %s: %s" % ( i, line )  
            
            key = AlignmentByPosition(int(qMapLine[0]), int(qMapLine[1]), int(qMapLine[2]), int(qMapLine[3]))
            val = float(qMapLine[4])
            self.__qMap[key] = val 
            
        return self.__qMap
        
        
    def LoadQValues2(self, qFile):
        lines = u.readFromFile(qFile)
        i = 0
        
        qMap = dict()
        
        for line in lines:
            i += 1
            
            qMapLine = line.split()
            
            if len(qMapLine) != 5:
                print "Invalid line %s: %s" % ( i, line )  
            
            key = AlignmentByPosition(qMapLine[0], qMapLine[1], qMapLine[2], qMapLine[3])
            val = float(qMapLine[4])
            qMap[key] = val 
            
        return qMap
    
    def QMap(self):
        return self.__qMap
        


if (__name__ == "__main__"):
                    
    sourceCorpusFile = "corpus.es"
    targetCorpusFile = "corpus.en"
    
#    sourceAlignmentFile = "dev.es"
#    targetAlignmentFile = "dev.en"
#    aFile = "dev.p2.out"
#    aFile = "dev.p2.fromsave.out"
    
#    sourceCorpusFile = "shortcorpus.es"
#    targetCorpusFile = "shortcorpus.en"
    
#    sourceAlignmentFile = "short.es"
#    targetAlignmentFile = "short.en"
#    aFile = "short.p2.out"

    tFile = "tValues.txt"
    newTFile = "tValues.p2.txt"
    qFile = "qValues.txt"

    sourceAlignmentFile = "test.es"
    targetAlignmentFile = "test.en"
    aFile = "alignment_test.p2.out" 
    
    model = IBM2()

#    print u.now(), "Training start"
#    tMap = model.Train(sourceCorpusFile, targetCorpusFile, 5, tFile)
#
#    print u.now(), "Saving t values"
#    model.SaveTValues(newTFile)
#
#    print u.now(), "Saving q values"
#    model.SaveQValues(qFile)
 
    print u.now(), "Loading t values"
    tMap = model.LoadTValues(newTFile)

    print u.now(), "Loading q values"
    #qMap0 = model.QMap()
    #qMap1 = model.LoadQValues2(qFile)
    qMap = model.LoadQValues(qFile)


    print u.now(), "Aligning words"
    alignments = model.Align(sourceAlignmentFile, targetAlignmentFile)
    
    
    print u.now(), "Saving alignments to", aFile
    a3p1.SaveAlignments(aFile, alignments)
    
#    print u.now(), "Found %s alignments" % len(alignments)
    print u.now(), "Done"

    
#    for key in tMap.keys():
#        if key.eCondition == "cyprus":
#            print key.f, tMap[key]
    
    print u.now(), "Found %s possible alignment pairings" % len(tMap)

