from __future__ import division
from collections import namedtuple 
import sys
import a4Util as util

UnigramCount = namedtuple("UnigramCount", ["n1", "count"])
BigramCount = namedtuple("BigramCount", ["n1", "n2", "count"])
TrigramCount = namedtuple("TrigramCount", ["n1", "n2", "n3", "count"])
Trigram = namedtuple("Trigram", ["n1", "n2", "n3"])




class ViterbiData:

    '''*****************************************************************************
    Constructor - initializes class attributes
    *****************************************************************************'''
    def __init__(self, emissionCounts=dict(), unigramCounts=dict(), bigramCounts=dict(), trigramCounts=dict()):
        self.__emissionCounts = emissionCounts
        self.__unigramCounts = unigramCounts
        self.__bigramCounts = bigramCounts
        self.__trigramCounts = trigramCounts
        self.__piTable = dict()
        self.SingleRareGroup = True
        
        
        
    def GetPiValue(self, k, uTag, vTag):
        key = (k, uTag, vTag)
        
        if self.__piTable.has_key(key):
            return self.__piTable[key][0]
        else:
            return ()
        
        
    def GetTagValue(self, k, uTag, vTag):
        key = (k, uTag, vTag)
        
        if self.__piTable.has_key(key):
            return self.__piTable[key][1]
        else:
            return ()
        
        
        
    def SetPiValue(self, k, uTag, vTag, pi):
        key = (k, uTag, vTag)
        
        if self.__piTable.has_key(key):
            entry = self.__piTable[ key ]
            entry = ( pi, entry[1] )
        else:
            entry = ( pi, '' )
 
        self.__piTable[ key ] = entry
 
 
        
    def SetTagValue(self, k, uTag, vTag, tag):
        key = (k, uTag, vTag)
        
        if self.__piTable.has_key(key):
            entry = self.__piTable[ key ]
            entry = ( entry[0], tag )
        else:
            entry = ( -sys.maxint, tag )
 
        self.__piTable[ key ] = entry
 
 
        
    def GetPiTable(self):
        return self.__piTable.copy()
    
    
    
    def ClearPiTable(self):
        self.__piTable = dict()
        
        
    def q(self, n1, n2, n3):
        
        trigram = Trigram(n1, n2, n3)
        
        bigramCountList = []
        trigramCountList = []
        
        if (self.__bigramCounts.has_key(trigram.n2)):
            bigramCountList = self.__bigramCounts[trigram.n2]
        else:
            raise Exception("No key for bigram list for %s!" % trigram.n2)
    
    
        if (self.__trigramCounts.has_key(trigram.n3)):
            trigramCountList = self.__trigramCounts[trigram.n3]
        else:
            raise Exception("No key for trigram list for %s!" % trigram.n3)
            
        bigramCount = BigramCount("", "", 0)
        for b in bigramCountList:
            if (b.n1 == trigram.n1):
                bigramCount = b
                break
            
        trigramCount = TrigramCount("", "", "", 0)
        for t in trigramCountList:
            if (t.n2 == trigram.n2 and t.n1 == trigram.n1):
                trigramCount = t
                break
        
        # print "%d / %d" %( trigramCount.count, bigramCount.count)
        
        result = 0
        if (bigramCount.count != 0):
            result = trigramCount.count / bigramCount.count
        
        return result
    
    
    def e(self, word, tag, rareTag="_RARE_"):
    
        if (self.__emissionCounts.has_key(word)):
            emissionCounts = self.__emissionCounts[word]
        else: 
            emissionCounts = self.__emissionCounts[rareTag]
        
        if (False == self.__unigramCounts.has_key(tag)):
            raise Exception("Tag %s was not present in the training corpus" % tag)
            
        tagCount = self.__unigramCounts[tag]

#        taggedCount = 0
#        totalCount = 0
#        
#        for unigramCount in unigramCounts:
#            totalCount += unigramCount.count
#             
#            if (tag == unigramCount.n1):
#                taggedCount = unigramCount.count

        emissionCount = 0

        for entry in emissionCounts:
            if (entry.n1 == tag):
                emissionCount = entry.count
        
        
#        if emissionCount == ():
#            error = "Emission parameter for word %s and tag %s could not be computed." % ( word, tag ) 
#            raise Exception(error)
    
        return emissionCount / tagCount

    
    
    def e2(self, word, tag):
    
        if (self.__emissionCounts.has_key(word)):
            emissionCounts = self.__emissionCounts[word]
        else: 
            rareTag = util.GetRareTag(word)
            emissionCounts = self.__emissionCounts[rareTag]
        
        if (False == self.__unigramCounts.has_key(tag)):
            raise Exception("Tag %s was not present in the training corpus" % tag)
            
        tagCount = self.__unigramCounts[tag]

#        taggedCount = 0
#        totalCount = 0
#        
#        for unigramCount in unigramCounts:
#            totalCount += unigramCount.count
#             
#            if (tag == unigramCount.n1):
#                taggedCount = unigramCount.count

        emissionCount = 0

        for entry in emissionCounts:
            if (entry.n1 == tag):
                emissionCount = entry.count
        
        
#        if emissionCount == ():
#            error = "Emission parameter for word %s and tag %s could not be computed." % ( word, tag ) 
#            raise Exception(error)
    
        return emissionCount / tagCount

    
    
    def MaxPi(self, k=0, uTag="*", vTag="*", sentence=[]):
    
        StartSymbol = "*"
        Vocabulary = ['O', 'I-GENE']
    
        if k == 0 and uTag == StartSymbol and vTag == StartSymbol:
            self.SetPiValue(k, uTag, vTag, 1)
            return 1
        
        tVocab = Vocabulary 
        if k <= 2:
            tVocab = [StartSymbol]
        
        maxPi = -1
        bestT = ""
        
        for tTag in tVocab:
            
            piForKminus1 = self.GetPiValue(k-1, tTag, uTag)
            
            if piForKminus1 == ():
                piForKminus1  = self.MaxPi(k-1, tTag, uTag, sentence)

            qValue = self.q(tTag, uTag, vTag)
            
            if (self.SingleRareGroup):
                eValue = self.e(sentence[k-1], vTag)
            else:
                eValue = self.e2(sentence[k-1], vTag)
        
            piValue = piForKminus1 * qValue * eValue

            # print k, tTag, uTag, vTag, piForKminus1, qValue, eValue, piValue
            
            if piValue > maxPi:
                maxPi = piValue
                bestT = tTag
    
        self.SetPiValue(k, uTag, vTag, maxPi)
        self.SetTagValue(k, uTag, vTag, bestT)
        
        return maxPi

    

    def GetMaxPi(self, sentence=[]):
    
        StartSymbol = "*"
        StopSymbol = "STOP"
        Vocabulary = ['O', 'I-GENE']
    
        vVocab = Vocabulary
    
        for k in xrange(1,len(sentence)+1):
            
            if k == 1:
                uVocab = [StartSymbol]
            else:
                uVocab = Vocabulary
    
            for v in vVocab:
                for u in uVocab:
                    self.MaxPi(k, u, v, sentence)
        
        
        maxPi = -sys.maxint
        bestU = "XXXXXXXXXX"
        bestV = "XXXXXXXXXX"
        
        if len(sentence) < 2:
            uVocab = [StartSymbol]
        else:
            uVocab = Vocabulary
    
        n = len(sentence)
    
        for v in vVocab:
            for u in uVocab:
                piForN  = self.MaxPi(n, u, v, sentence)
                qForStop = self.q(u, v, StopSymbol)
                
                piValue = piForN * qForStop 
                
                if (piValue > maxPi):
                    maxPi = piValue
                    bestU = u
                    bestV = v
        
        return (maxPi, bestU, bestV)
        
    
    def GetTagSequence(self, sentence):
        
        uTag, vTag = self.GetMaxPi(sentence)[1:]
        
        tagSequence = []

        n = len(sentence)
        Yk = ''
        
        tagSequence.insert(0, vTag)
        tagSequence.insert(0, uTag)
    
        for k in xrange(n-2, 0, -1):
            if (k == n-2):
                Ykplus1 = uTag
                Ykplus2 = vTag
            else:
                Ykplus2 = Ykplus1
                Ykplus1 = Yk 
            
            Yk = self.GetTagValue(k+2, Ykplus1, Ykplus2 )
            
            tagSequence.insert(0, Yk)
        
        
        return tagSequence

