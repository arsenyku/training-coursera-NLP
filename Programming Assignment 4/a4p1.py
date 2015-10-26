import a4Util as u
import sys

StartSymbol = "*"
StopSymbol = "STOP"
TagVocabulary = ['O', 'I-GENE']


def readPreTrainedModel(modelFilename):
    lines = u.readFromFile(modelFilename)
    
    vMap = dict()
    
    for i in xrange(0, len(lines)):
        line = lines[i]
        tokens = line.split()
        
        if len(tokens) != 2:
            print "Invalid line %s: %s" % ( i, line )
            
        vMap[tokens[0]] = float(tokens[1])
        
    return vMap



class FeatureData():
    
    def __init__(self, weightVector):
        self.__v = weightVector
    
    
    
    def getVector(self, tMinus2Tag, tMinus1Tag, sentence, tagIndex, tTag):
        result = dict()
        
        #print tagIndex, sentence

        trigramKey = "TRIGRAM:%s:%s:%s" % ( tMinus2Tag, tMinus1Tag, tTag )
        result[trigramKey] = 1

        if (tagIndex < len(sentence)):
            tagKey = "TAG:%s:%s" % ( sentence[tagIndex], tTag )
            result[tagKey] = 1
        
        return result


    
    def getWeightedFeatureScore(self, tTag, uTag, sentence, k, candidateTag):
        g = self.getVector(tTag, uTag, sentence, k, candidateTag)
        #return sum((self.__v[k] * val for k, val in g.iteritems()))
    
        score = 0
        
        for featureName, val in g.iteritems():
        
            if self.__v.has_key(featureName):
                weight = self.__v[featureName]
            else:
                weight = 0
                
            score += weight * val
            
        return score
            


class PiTable:
    
    
    def __init__(self, featureData):
        self.__f = featureData
        self.__piTable = dict()
    
    
    def Clear(self):
        self.__piTable = dict()

    
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
        
    
    def SetValue(self, k, uTag, vTag, pi, tag):
        key = (k, uTag, vTag)
        
        if self.__piTable.has_key(key):
            entry = self.__piTable[ key ]
            entry = ( pi, tag )
        else:
            entry = ( pi, tag )
 
        self.__piTable[ key ] = entry
 
 
    def getWeightedFeatureScore(self, tTag, uTag, sentence, k, candidateTag):
        return self.__f.getWeightedFeatureScore(tTag, uTag, sentence, k, candidateTag)
 
 
 
    def GetBestTagSequence(self, sentence):
        wordCount = len(sentence) - 1
        n = wordCount

        bestPi = -1
        bestU = ""
        bestS = ""
        
        tagSequence = [ "" ] * (wordCount + 1)
            
        for uTag in ValidTags(n-1):
            for sTag in ValidTags(n):

                piValue = MaxPi(n, uTag, sTag, sentence, self) + self.getWeightedFeatureScore(uTag, sTag, sentence, n+1, StopSymbol)
                
                if piValue > bestPi:
                    
                    bestPi = piValue
                    bestU = uTag
                    bestS = sTag
        
        tagSequence[n] = bestS
        tagSequence[n-1] = bestU
        
        for k in xrange(n-2,0,-1):
#            print k, len(tagSequence), len(sentence)
            
            tagValue = self.GetTagValue(k+2, tagSequence[k+1], tagSequence[k+2])
            tagScore = self.GetPiValue(k+2, tagSequence[k+1], tagSequence[k+2])

            tagSequence[k] = tagValue
            if tagValue == () or tagValue == "":
                print k+2, tagScore, tagSequence[k+1], tagSequence[k+2]
                print sentence
                tagSequence[k] = TagVocabulary[0]
            
        

        return tagSequence
        




def ValidTags(position):

    if position < 1:
        return [StartSymbol]
    
    return TagVocabulary
    
    


def MaxPi(k=0, uTag="*", vTag="*", sentence=[], piTable=None):
    
    x = sentence

    if k == 0 and uTag == StartSymbol and vTag == StartSymbol:
        piTable.SetValue(k, uTag, vTag, 0, "")
        return 0
    
    maxPi = -sys.maxint
    bestTag = ""
    
    for tTag in ValidTags(k-2):
        
        piForKminus1 = piTable.GetPiValue(k-1, tTag, uTag)
        
        if piForKminus1 == ():
            piForKminus1 = MaxPi(k-1, tTag, uTag, sentence, piTable)
            
        piValue = piForKminus1 + piTable.getWeightedFeatureScore(tTag, uTag, x, k, vTag)
        
        if piValue > maxPi:
            maxPi = piValue
            bestTag = tTag 
    
        piTable.SetValue(k, uTag, vTag, maxPi, bestTag)
    
    return maxPi




def ViterbiGLM(featureData, sentence):

    x = sentence

    piTable = PiTable(featureData)
    
    n = len(x)
    
    for k in xrange(1, n):
        
        for u in ValidTags(k-1):
            
            for s in ValidTags(k):

                MaxPi(k, u, s, x, piTable) 
                
    tagSequence = piTable.GetBestTagSequence(sentence)
    
    return tagSequence
    
    
    
    

    

def main():

    print u.now(), "Start"

    modelFile = "tag.model"
    
    inputFile = "gene.dev"
    outputFile = "dev.p1.out"
    
#    inputFile = "short.dev"
#    outputFile = "dev.short.out"

    inputFile = "gene.test"
    outputFile = "gene_test.p1.out"


    weightVector = readPreTrainedModel(modelFile)
    
    lines = u.readFromFile(inputFile)
    
    tagSequences = []

    while len(lines) > 0:       
        sentence, lines = u.GetNextSentence(lines)

        featureData = FeatureData(weightVector)
        tagSequence = ViterbiGLM(featureData, sentence)
        
        tagSequences.append((tagSequence, sentence))
    
    outputText = []

    lines = u.readFromFile(inputFile)

    del (tagSequences[0][0])[0]
    del (tagSequences[0][1])[0]

    for tagSequence, sentence in tagSequences:
        
        for j in xrange(0,len(tagSequence)):

            if len(tagSequence) != len(sentence):
                continue

            tag = tagSequence[j]
            word = sentence[j]


            outputText.append("%s %s" % (word, tag))
            
            
    outputText.append("")
    outputText.append("")
    
    outputText = '\n'.join(outputText)
    
    u.saveToFile(outputFile, outputText)
    
    print u.now(), "Done"
    


if (__name__ == "__main__"):
    main()
