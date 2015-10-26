import time
import a3Util as u
import a3p1, a3p2_opt
from collections import namedtuple

SlotAssignment = namedtuple("SlotAssignment", "Left Right")


class SentenceAlignment():
    NULLTAG = "_NULL_"
    
    '''*****************************************************************************
    Constructor - initializes class attributes
    *****************************************************************************'''
    def __init__(self, sourceWords, targetWords):
        
#        sourceWords = sourceSentence.split()
#        targetWords = targetSentence.split()
        
        if (len(sourceWords) < 1):
            raise Exception("Sentence alignment is invalid with a blank source sentence.")
        
        if (len(targetWords) < 1):
            raise Exception("Sentence alignment is invalid with a blank target sentence.")

        if sourceWords[0] != self.NULLTAG:
            sourceWords.insert(0, self.NULLTAG)
            
        if targetWords[0] != self.NULLTAG:
            targetWords.insert(0, self.NULLTAG)
            
        self.__sourceWords = sourceWords
        self.__targetWords = targetWords
        self.__alignment = dict()
        
        lk = len(targetWords) - 1
        
        for j in xrange(0, lk + 1):
            self.__alignment[j] = []
            
        
    def Align(self, sourceIndex, targetIndex):
        
        i = sourceIndex
        j = targetIndex
        
        mk = len(self.__sourceWords) - 1
        lk = len(self.__targetWords) - 1
        
        if (i > mk):
            raise Exception("Invalid source index %s.  Legal max is %s." % ( i, mk ))
        
        if (j > lk):
            raise Exception("Invalid target index %s.  Legal max is %s." % ( j, lk ))
        
        alignment = self.__alignment[j]
        
        if not (i in alignment):
            alignment.append(i)
            
            
    def isAligned(self, sourceIndex, targetIndex):
        i = sourceIndex
        j = targetIndex
        
        if not self.__alignment.has_key(j):
            return False
        
        alignment = self.__alignment[j]
        
        return i in alignment
    
   
   
    def SourceLength(self):
        return len(self.__sourceWords) - 1
        
    def TargetLength(self):
        return len(self.__targetWords) - 1
        
        

def LoadAlignments(alignmentFile, sourceFile, targetFile):
    lines = u.readFromFile(alignmentFile)
    sourceLines = u.readFromFile(sourceFile)
    targetLines = u.readFromFile(targetFile)
    
    lineIndex = 0

    alignments = dict()
    
    for line in lines:
        lineIndex += 1
        
        alignmentLine = line.split()
        
        if len(alignmentLine) != 3:
            print "Invalid line %s: %s" % ( lineIndex, line )  
        
        k = int(alignmentLine[0])
        i = int(alignmentLine[2])
        j = int(alignmentLine[1])
        
        sourceLine = sourceLines[k-1].split()
        sourceLine.insert(0, SentenceAlignment.NULLTAG)

        targetLine = targetLines[k-1].split()
        targetLine.insert(0, SentenceAlignment.NULLTAG)

        if (alignments.has_key( k )):
            alignment = alignments[ k ]
        else:
            alignment = SentenceAlignment(sourceLine, targetLine)

        alignment.Align(i, j)
        
        alignments[ k ] = alignment
        
    return alignments


        
        
        
        


def ComputeAlignments(sourceCorpusFile, targetCorpusFile, sourceSentencesFile, targetSentencesFile, model1TFile="", model2TFile="", model2QFile=""):
    model1 = a3p1.IBM1()
    model2 = a3p2_opt.IBM2A()
    
    timestamp = time.time()
    
    if (model1TFile==""):
        model1TFile = "temporary.%s.model1.tfile" % timestamp
        
    if (model2TFile==""):
        model2TFile = "temporary.%s.model2.tfile" % timestamp
        
    if (model2QFile==""):
        model2QFile = "temporary.%s.model2.qfile" % timestamp
    
    model1.Train(sourceCorpusFile, targetCorpusFile,5)
    model1.SaveTValues(model1TFile)

    model2.Train(sourceCorpusFile, targetCorpusFile, 5, model1TFile)
    model2.SaveTValues(model2TFile)
    model2.SaveQValues(model2QFile)
    model2Alignments = model2.Align(sourceSentencesFile, targetSentencesFile)
    
    return model2Alignments
    



def ComputeIntersect(alignment1, alignment2):
    
    lk1 = alignment1.TargetLength()
    lk2 = alignment2.TargetLength()
    
    intersect = []
    
    for j1 in xrange(0, lk1+1):
        
        for j2 in xrange(0, lk2+1):
            
            if alignment1.isAligned(j2, j1) and alignment2.isAligned(j1, j2):
                match = SlotAssignment(j1, j2)
                if not (match in intersect):
                    intersect.append(match)
                    
    return intersect
        


def ComputeUnion(alignment1, alignment2):
    lk1 = alignment1.TargetLength()
    lk2 = alignment2.TargetLength()
    
    union = []
    
    for j1 in xrange(0, lk1+1):
        
        for j2 in xrange(0, lk2+1):
            
            if alignment1.isAligned(j2, j1) or alignment2.isAligned(j1, j2):
                match = SlotAssignment(j1, j2)
                if not (match in union):
                    union.append(match)
                    
    return union

    
    
def CheckDiagonalAdjacency( alignedPair, assignedSlotsLeft, assignedSlotsRight ):
    
    l = alignedPair.Left
    r = alignedPair.Right
    
    adjacentSlots = []
    adjacentSlots.append(SlotAssignment( l - 1, r - 1 ))
    adjacentSlots.append(SlotAssignment( l - 1, r + 1 ))
    adjacentSlots.append(SlotAssignment( l + 1, r - 1 ))
    adjacentSlots.append(SlotAssignment( l + 1, r + 1 ))
    
    for slot in adjacentSlots:
        if (slot.Left in assignedSlotsLeft) and (slot.Right in assignedSlotsRight):
            return True
        
    return False
        
        
        
def CheckLeftAdjacency( alignedPair, assignedSlotsLeft, assignedSlotsRight ):
    
    l = alignedPair.Left
    r = alignedPair.Right
    
    adjacentSlots = []
    adjacentSlots.append(SlotAssignment( l - 1, r ))
    adjacentSlots.append(SlotAssignment( l + 1, r ))
    
    for slot in adjacentSlots:
        if (slot.Left in assignedSlotsLeft) and (slot.Right in assignedSlotsRight):
            return True
        
    return False
        

def CheckRightAdjacency( alignedPair, assignedSlotsLeft, assignedSlotsRight ):
    
    l = alignedPair.Left
    r = alignedPair.Right
    
    adjacentSlots = []
    adjacentSlots.append(SlotAssignment( l, r - 1 ))
    adjacentSlots.append(SlotAssignment( l, r + 1 ))
    
    for slot in adjacentSlots:
        if (slot.Left in assignedSlotsLeft) and (slot.Right in assignedSlotsRight):
            return True
        
    return False
        

    
    
def GrowAlignment(alignment1, alignment2):
    union = ComputeUnion(alignment1, alignment2)
    intersect = ComputeIntersect(alignment1, alignment2)
    
    fullAlignmentLeft = []
    fullAlignmentRight = []
    fullAlignmentRank = []
    
    rank = 0
    
    # Starting point is the intersection
    
    for alignedPair in intersect:
        fullAlignmentLeft.append( alignedPair.Left )
        fullAlignmentRight.append( alignedPair.Right )
        fullAlignmentRank.append(rank) 
    

    candidates = union[:]
        
    toRemove = []
    
    rank -= 1

    checkDiagonals = True

    while(checkDiagonals):

        # Add points which are diagonally adjacent as long as the
        # source word has not been aligned AND the target word has not been aligned     
        
        for alignedPair in candidates:
            
            j1 = alignedPair.Left
            j2 = alignedPair.Right
            
            
            if (j1 in fullAlignmentLeft) and (j2 in fullAlignmentRight):
                toRemove.append(alignedPair)
                continue
            
            
            if (j1 in fullAlignmentLeft) or (j2 in fullAlignmentRight):
                continue
            
            isAdjacent = CheckDiagonalAdjacency( alignedPair, fullAlignmentLeft, fullAlignmentRight )
            
            if isAdjacent:
                fullAlignmentLeft.append(j1)
                fullAlignmentRight.append(j2)
                fullAlignmentRank.append(rank)
                toRemove.append(alignedPair)
        
        if (len(toRemove) < 1):
            checkDiagonals = False

        for pairToRemove in toRemove:
            candidates.remove( pairToRemove )
            
        toRemove = []
    
    rank -= 1
    
    
#    #Add points which are horizontally adjacent as long as the target word has not been aligned
#    #Add points which are vertically adjacent as long as the source word has not been aligned
#
#    for alignedPair in candidates:
#        
#        j1 = alignedPair.Left
#        j2 = alignedPair.Right
#        
#        
#        if (j1 in fullAlignmentLeft) and (j2 in fullAlignmentRight):
#            toRemove.append(alignedPair)
#            continue
#        
#        
#        isLeftAdjacent = CheckLeftAdjacency( alignedPair, fullAlignmentLeft, fullAlignmentRight )
#        isRightAdjacent = CheckRightAdjacency( alignedPair, fullAlignmentLeft, fullAlignmentRight )
#        
#        addPair = False
#        
#        if (j1 in fullAlignmentLeft) and isRightAdjacent:
#            addPair = True
#        
#        if (j2 in fullAlignmentRight) and isLeftAdjacent:
#            addPair = True
#        
#        
#        if addPair:
#            fullAlignmentLeft.append(j1)
#            fullAlignmentRight.append(j2)
#            fullAlignmentRank.append(rank)
#            toRemove.append(alignedPair)
#            
#        
#            
#    for pairToRemove in toRemove:
#        candidates.remove( pairToRemove )
#        
#    toRemove = []
#    
#    rank -= 1

    # Add points if neither the source nor target word has been
    # previously aligned.  Adjacency is no longer checked.

    for alignedPair in candidates:
        
        j1 = alignedPair.Left
        j2 = alignedPair.Right
        
        
        if (j1 in fullAlignmentLeft) and (j2 in fullAlignmentRight):
            toRemove.append(alignedPair)
            continue
        
        if (j1 in fullAlignmentLeft) or (j2 in fullAlignmentRight):
            continue
        
        fullAlignmentLeft.append(j1)
        fullAlignmentRight.append(j2)
        fullAlignmentRank.append(rank)
        toRemove.append(alignedPair)
        
    for pairToRemove in toRemove:
        candidates.remove( pairToRemove )
        
    toRemove = []

    rank -= 1

            
    for pairToRemove in toRemove:
        candidates.remove( pairToRemove )    

#    print "leftover:", len(candidates)
#    print "union:", len(union)

    return (fullAlignmentLeft, fullAlignmentRight, fullAlignmentRank, union, intersect)
    
    
    
def Align(sourceIndices, targetIndices, ranks, sentenceId):

    k = sentenceId
    alignments = []
    for i in xrange(0,len(ranks)):
        
        r = ranks[i]
        sourceIndex = sourceIndices[i]
        targetIndex = targetIndices[i]
        
        alignments.append( a3p1.Alignment(r, k, "", sourceIndex, "", targetIndex) )
        
    alignments = sorted(alignments, key=lambda a: -a.Score )
    alignments = u.uniqueList( alignments )
    
    #print alignments
    
    return alignments


    
    

#    unions[k] = union
#    intersects[k] = intersect
    

    

if (__name__ == "__main__"):
                    
    esCorpusFile = "corpus.es"
    enCorpusFile = "corpus.en"  

    esSentencesFile = "dev.es"
    enSentencesFile = "dev.en"

    enSourceM1TFile = "p3.enSource.m1.tfile"
    enSourceM2TFile = "p3.enSource.m2.tfile"
    enSourceM2QFile = "p3.enSource.m2.qfile"

    esSourceM1TFile = "p3.esSource.m1.tfile"
    esSourceM2TFile = "p3.esSource.m2.tfile"
    esSourceM2QFile = "p3.esSource.m2.qfile"

    esTargetAlignmentsFile = "p3.esTarget.afile"
    enTargetAlignmentsFile = "p3.enTarget.afile"
    
    finalAlignmentsFile = "dev.p3.out"
    
    
#    enTargetAlignmentsFile = "p3.test.enTarget.afile"
#    esTargetAlignmentsFile = "p3.test.esTarget.afile"
#    enSentencesFile = "test.en"
#    esSentencesFile = "test.es"
#    finalAlignmentsFile = "alignment_test.p3.out"

    
#    print u.now(), "Computing Alignments with Spanish source / English target - p(f|e)"
#    alignments_esSource = ComputeAlignments(esCorpusFile, enCorpusFile, esSentencesFile, enSentencesFile, 
#                                            esSourceM1TFile, esSourceM2TFile, esSourceM2QFile)
#
#    print u.now(), "Saving to", esSourceAlignmentsFile
#    a3p1.SaveAlignments(esSourceAlignmentsFile, alignments_esSource)
#
#    print u.now(), "Computing Alignments with English source / Spanish Target - p(e|f)"
#    alignments_enSource = ComputeAlignments(enCorpusFile, esCorpusFile, enSentencesFile, esSentencesFile, 
#                                            enSourceM1TFile, enSourceM2TFile, enSourceM2QFile)
#
#    print u.now(), "Saving to", enSourceAlignmentsFile
#    a3p1.SaveAlignments(enSourceAlignmentsFile, alignments_enSource)

###########################################################

#    print u.now(), "Load Model p(f|e)"
#    enTargetModel = a3p2_opt.IBM2A()
#    enTargetModel.LoadTValues(esSourceM2TFile)
#    enTargetModel.LoadQValues(esSourceM2QFile)
#    
#    print u.now(), "Load Model p(e|f)"
#    esTargetModel = a3p2_opt.IBM2A()
#    esTargetModel.LoadTValues(enSourceM2TFile)
#    esTargetModel.LoadQValues(enSourceM2QFile)
#    
#    print u.now(), "Getting first alignments"
#    alignments_enTarget = enTargetModel.Align(esSentencesFile, enSentencesFile)
#    alignments_esTarget = esTargetModel.Align(enSentencesFile, esSentencesFile)
#    
#    a3p1.SaveAlignments(enTargetAlignmentsFile, alignments_enTarget)
#    a3p1.SaveAlignments(esTargetAlignmentsFile, alignments_esTarget)
    
###########################################################
    

    
    print u.now(), "Loading..."

#    alignments_enTarget = LoadAlignments(esSourceAlignmentsFile, esSentencesFile, enSentencesFile)
#    alignments_esTarget = LoadAlignments(enSourceAlignmentsFile, enSentencesFile, esSentencesFile)

    alignments_enTarget = LoadAlignments(enTargetAlignmentsFile, esSentencesFile, enSentencesFile)
    alignments_esTarget = LoadAlignments(esTargetAlignmentsFile, enSentencesFile, esSentencesFile)
    

    if len(alignments_enTarget) != len(alignments_esTarget):
        print "Sentence counts do not match: %s for p(f|e) model, %s for p(e|f) model" % \
            ( len(alignments_enTarget), len(alignments_esTarget) )
            
    sentenceCount = len(alignments_esTarget)
    
    fullAlignments = []

    progress = u.Progress(sentenceCount, 50)
    
    print "Growing Alignments"    
    for k in xrange(1, sentenceCount+1):
        fullAlignment = GrowAlignment(alignments_enTarget[k], alignments_esTarget[k])
        
        if k == 1: uuu = fullAlignment[3]
        
        enIndices = fullAlignment[0]
        esIndices = fullAlignment[1]
        ranks = fullAlignment[2]
        
        fullAlignment = Align(esIndices, enIndices, ranks, k)
        
        fullAlignments += fullAlignment
        
        progress.Increment()


    a3p1.SaveAlignments(finalAlignmentsFile, fullAlignments)
        
    for x in uuu:
        print x.Right, x.Left 
        
#    print "Union"
#    for p in unions[1]:
#        print p
#        
#    print "Intersect"
#    for p in intersects[1]:
#        print p
#        
    
    
    
#
#    sentenceCount = len(m2_alignments_enSource)
#            
#    for k in xrange(0, sentenceCount):
#        
#        alignments_enSource = m2_alignments_enSource[k]
#        alignments_esSource = m2_alignments_esSource[k]
#        
        
    print "Done"    




#    union = ComputeUnion(model2_esSource_alignments, model2_enSource_alignments)
#    intersect = ComputeIntersect(model2_esSource_alignments, model2_enSource_alignments)
    
    
        
    
    
    
    
    