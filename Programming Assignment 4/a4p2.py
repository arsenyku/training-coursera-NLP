import a4Util as u
import a4p1 as p1
import sys

TagVocabulary = ['O', 'I-GENE']
#TagVocabulary = ['O', 'I', 'V', 'X', 'L']



class FeatureData():
    
    def __init__(self, weightVector):
        self.__v = weightVector
    
    
    def getFeatureVectors(self, sentence, tagSequence):
        n = len(sentence) - 1
 
        x = sentence
        y = tagSequence
    
        for i in xrange(1,n):
        
            if i == 0:
                tMinus2 = p1.StartSymbol
                tMinus1 = p1.StartSymbol
            elif i == 1:
                tMinus2 = p1.StartSymbol
                tMinus1 = y[0]
            else:
                tMinus2 = y[i-2]
                tMinus1 = y[i-1]
        
            t = y[i]
            
            self.getFeatureVector(tMinus2, tMinus1, x, i, t)
            
            
    
    def getFeatureVector(self, tMinus2Tag, tMinus1Tag, sentence, tagIndex, tTag):
        result = dict()
        
        #print tagIndex, sentence

        trigramKey = "TRIGRAM:%s:%s:%s" % ( tMinus2Tag, tMinus1Tag, tTag )
        result[trigramKey] = 1

        if (tagIndex < len(sentence)):
            tagKey = "TAG:%s:%s" % ( sentence[tagIndex], tTag )
            result[tagKey] = 1
        
        return result




    def increaseWeight(self, tMinus2Tag, tMinus1Tag, sentence, tagIndex, tTag):
        g = self.getFeatureVector(tMinus2Tag, tMinus1Tag, sentence, tagIndex, tTag)
    
        for featureName in g.keys():
        
            if False == self.__v.has_key(featureName):
                self.__v[featureName] = 0

            self.__v[featureName] += 1


    
    def decreaseWeight(self, tMinus2Tag, tMinus1Tag, sentence, tagIndex, tTag):
        g = self.getFeatureVector(tMinus2Tag, tMinus1Tag, sentence, tagIndex, tTag)
    
        for featureName in g.keys():
        
            if False == self.__v.has_key(featureName):
                self.__v[featureName] = 0

            self.__v[featureName] -= 1



    
    def getWeightedFeatureScore(self, tMinus2Tag, tMinus1Tag, sentence, tagIndex, tTag):
        g = self.getFeatureVector(tMinus2Tag, tMinus1Tag, sentence, tagIndex, tTag)
        #return sum((self.__v[k] * val for k, val in g.iteritems()))
    
        score = 0
        
        for featureName, val in g.iteritems():
        
            if self.__v.has_key(featureName):
                weight = self.__v[featureName]
            else:
                weight = 0
                
            score += weight * val
            
        return score
            



    def getBestTagSequence(self, sentence):
        
        candidates = gen(sentence)
        n = len(sentence)
        
        maxScore = -sys.maxint
        bestTagSequence = None
        
        for y in candidates:

            score = 0            
            for i in xrange(1,n):
                
                if i == 0:
                    tMinus2 = p1.StartSymbol
                    tMinus1 = p1.StartSymbol
                elif i == 1:
                    tMinus2 = p1.StartSymbol
                    tMinus1 = y[0]
                else:
                    tMinus2 = y[i-2]
                    tMinus1 = y[i-1]

                t = y[i]
                
                score += self.getWeightedFeatureScore(tMinus2, tMinus1, sentence, i, t)
                
            if score > maxScore:
                maxScore = score
                bestTagSequence = y
                
        return bestTagSequence
    


def gen(sentence):
    n = len(sentence) - 1
    vocabSize = len(TagVocabulary)
    
    resultSize = vocabSize ** n 
    result = []
    
    #tagSequence = [""] * n+1
    seqTags = [0] * n
    seqTags.insert(0, "_")

    #for i in xrange(0, resultSize):
    while len(result) < resultSize:
        seq = map(lambda a: TagVocabulary[a], seqTags[1:])
        seq.insert(0, "_")
        result.append(seq)

        increment(seqTags)

    return result


def increment(sequence):
    n = len(sequence) - 1
    vocabEnd = len(TagVocabulary) - 1
    
    
    if sequence[n] != vocabEnd:
        sequence[n] += 1
    
    else:
        i = n
        while i > 0 and sequence[i] == vocabEnd:
            sequence[i] = 0
            i -= 1
        
        if i > 0:
            sequence[i] += 1

    return sequence
        



def readTrainingSetFile(filename):
    lines = u.readFromFile(filename)

    trainingSet = []

    while len(lines) > 0:       
        trainingSentence, lines = u.GetNextSentence(lines)
        
        x = []
        y = []
        
        for pair in trainingSentence[1:]:
            splitPair = pair.split()
            
            x.append(splitPair[0])
            y.append(splitPair[1])

        
        trainingSet.append ( (x,y) )
        
    return trainingSet



    

def perceptron(trainingSet, featureData, iterations):
    n = len(trainingSet)
    
    for i in xrange(0,n):
        x = trainingSet[i][0]
        y = trainingSet[i][1]

        z = featureData.getBestTagSequence(x)
        
        if z != y:  
            pass
            
            

    


def main():

    print u.now(), "Start"

    modelFile = "tag.model"
    trainingFile = "gene.train"
    
    inputFile = "gene.dev"
    outputFile = "dev.p1.out"
    
    lines = u.readFromFile(inputFile)
    
    #weightVector = p1.readPreTrainedModel(modelFile)

    # Empty weight vector means a vector of 0s
    weightVector = dict()

    featureData = FeatureData(weightVector)
    
    trainingSet = readTrainingSetFile(trainingFile)

    perceptron(trainingSet, featureData, 5)


#    tagSequences = []
#
#    while len(lines) > 0:       
        #sentence, lines = u.GetNextSentence(lines)
        
#    genX = gen(["", "hello", "there", "foo", "bar", "bacon"])

    
    print u.now(), "Done"
    



if (__name__ == "__main__"):
    main()