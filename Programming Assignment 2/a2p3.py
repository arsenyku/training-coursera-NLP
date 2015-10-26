from __future__ import division
import json
import a2Util as u
import a2p1, a2p2


class VertMarkovGrammar(a2p2.Grammar):
    
    def __init__(self, nonTerminalCounts, binaryCounts, unaryCounts, wordCounts):
        a2p2.Grammar.__init__(self, nonTerminalCounts, binaryCounts, unaryCounts, wordCounts)

 
    def FindMaxPi(self, spanStart, spanEnd, nonTerminal, splitSentence):
        
        if spanStart == spanEnd:
            return self.PiTable().GetValue(spanStart, spanEnd, nonTerminal)

        maxPi = a2p2.MaxProbability(0, None, None)
            
        for rule in self.RBinary:
            
            if rule.Parent != nonTerminal:
                continue
            
            for splitPoint in xrange(spanStart, spanEnd):
                
                qForSplit = self.q(rule)

                if qForSplit == 0:
                    piForLeftSplit = a2p2.MaxProbability(0, None, None)
                    piForRightSplit = a2p2.MaxProbability(0, None, None)

                else:
                
                    piForLeftSplit = self.PiTable().GetValue(spanStart, splitPoint, rule.Left)
                    if (piForLeftSplit.RuleBackPointer == None):
                        piForLeftSplit = self.FindMaxPi(spanStart, splitPoint, rule.Left, splitSentence)
                        
                    
                    if piForLeftSplit == 0:
                        piForRightSplit = a2p2.MaxProbability(0, None, None)
                        
                    else:
                        piForRightSplit = self.PiTable().GetValue(splitPoint+1, spanEnd, rule.Right)
                        if (piForRightSplit.RuleBackPointer == None):
                            piForRightSplit = self.FindMaxPi(splitPoint+1, spanEnd, rule.Right, splitSentence)

                piForSplit = qForSplit * piForLeftSplit.P * piForRightSplit.P
                
                if maxPi.P <= piForSplit:
                    maxPi = a2p2.MaxProbability(piForSplit, rule, splitPoint)
        
        self.PiTable().SetValue(spanStart, spanEnd, nonTerminal, maxPi.P, maxPi.RuleBackPointer, maxPi.SplitBackPointer)

        return maxPi
            
            


def ParseFile(fileToParse="", adjustedCountsFile="", resultFile=""):
    if fileToParse=="" or adjustedCountsFile=="" or resultFile=="":
        return
    
    counts = a2p1.readCounts(adjustedCountsFile)
    
    nonTerminalCounts = counts[0]
    binaryCounts = counts[1]
    unaryCounts = counts[2]
    wordCounts = counts[3]
    
    print u.now(), "Building Grammar"
    grammar = VertMarkovGrammar(nonTerminalCounts, binaryCounts, unaryCounts, wordCounts)
    print u.now(), "Grammar created"
    
    lines = u.readFromFile(fileToParse)
    
    outputLines = []

    progress = 0
    
    for sentence in lines:
        
        progress += 1
        print "%s Parsing (%s/%s): %s" % ( u.now(), progress, len(lines), sentence[:-1]) 
        
        tree = grammar.ComputeParseTree(sentence)
        outputLine = json.dumps(tree)
        outputLines.append(outputLine)
        
        
    outputText = '\n'.join(outputLines)

    print u.now(), "Saving output to", resultFile
    u.saveToFile(resultFile, outputText)
    
    print u.now(), "Done"
    
    


            
if (__name__ == "__main__"):
            
#    countsFile="cfg.vert.counts"
#    trainingFile = "parse_train_vert.dat"
#    adjustedTrainingFile = "parse_train.vert.adjusted"
#
#    a2p1.Preprocess(countsFile, trainingFile, adjustedTrainingFile)
#
#    targetFile = "parse_dev.dat"
#    adjustedCountsFile = "cfg.vert.adjusted.counts"
#    resultFile = "parse_dev.vert.out"

    targetFile = "parse_test.dat"
    adjustedCountsFile = "cfg.vert.adjusted.counts"
    resultFile = "parse_test.p3.out"

#
#    targetFile = "test.dat"
#    adjustedCountsFile = "cfg.vert.adjusted.counts"
#    resultFile = "test.vert.out"

    start = u.now()

#    targetFile = "shorttest.dat"
#    adjustedCountsFile = "cfg.vert.adjusted.counts"
#    resultFile = "shorttest.vert.out"

#    targetFile = "shorttest.dat"
#    adjustedCountsFile = "parse_train.counts.out"
#    resultFile = "shorttest.out"

    #a2p2.ParseFile(targetFile, adjustedCountsFile, resultFile)

    ParseFile(targetFile, adjustedCountsFile, resultFile)
    
    end = u.now()
    
    print "Start %s / End %s" % ( start, end )








