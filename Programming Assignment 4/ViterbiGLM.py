import sys
import a4Util as u



class ViterbiData:

    '''*****************************************************************************
    Constructor - initializes class attributes
    *****************************************************************************'''
    def __init__(self, emissionCounts=dict(), unigramCounts=dict(), bigramCounts=dict(), trigramCounts=dict()):
        self.__piTable = dict()
        self.__weightVector = ()
        
        
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
        



def MaxPi(v, g, x):
    pass





#
#
#import a4Util as u
#import operator
#
#def readPreTrainedModel(modelFilename):
#    lines = u.readFromFile(modelFilename)
#    
#    vMap = dict()
#    
#    for i in xrange(0, len(lines)):
#        line = lines[i]
#        tokens = line.split()
#        
#        if len(tokens) != 2:
#            print "Invalid line %s: %s" % ( i, line )
#            
#        vMap[tokens[0]] = tokens[1]
#        
#    return vMap
#
#
#def dotProduct(vector1, vector2):
#    return sum(map( operator.mul, vector1, vector2))
#
#
#def Gen(x, tags):
#    pass
#
#def gTrigram(history, tag):
#    
#    
#
#
#if (__name__ == "__main__"):
#    
#    preTrainedModelFile = "tag.model"
#    
#    vMap = readPreTrainedModel(preTrainedModelFile)
#    
#    for feature, weight in vMap.items():
#        if feature[0:3] != "TAG":
#            print weight, feature   
