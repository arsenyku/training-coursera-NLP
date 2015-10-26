from __future__ import division
import math

M = 12

p_values = [None] * 3

# the dog runs
p_values[0] = 1 * .5 * 1 * 1
# the cat walks
p_values[1] = 1 * .5 * 1 * 1
# the dog runs
p_values[2] = 1 * .5 * 1 * 1

logsum = 0

for p in p_values:
    logsum += math.log(p, 2)
    
print "logsum", logsum

l = logsum/M

Perplexity = 2 ** -l

print "perplexity", Perplexity


l = 1/3 
q3 = 1
q2 = 1/2
q1 = 3/14
ql = l*q3 + l*q2 + l*q1
print "l=%s, q3=%s, q2=%s, q1=%s" % ( l, q3, q2, q1 )
print "ql=", ql

print .3 * 15 /70

print  1/6

def qLI(countTrigram = 1, countBigram=1, countUnigram=1, countCorpus=1,
        l1 = 0.0, l2 = 0.0, l3 = 0.0):
    
    qLI = l1 * (countTrigram/countBigram) + \
           l2 * (countBigram/countUnigram) + \
           l3 * (countUnigram/countCorpus)
    
    return qLI
    
print "-" * 40

l1 = -0.9
l2 = 0.9
l3 = 1

qli = qLI(1,1,100,1000000, l1, l2, l3)
print qli

print "-" * 40

qli = qLI(0,99,100,102, l1, l2, l3)
print qli

#print "-" * 40
#
#uCount = 0
#bCount = 0
#qli = 0
#for i in xrange(1,1000):
#    uCount = i
#    print bCount, uCount, qli
#    for j in xrange(1,uCount):
#        bCount = j
#        qli = qLI(0,bCount,uCount,bCount+uCount, l1, l2, l3)
#        # print bCount, uCount, qli
#        
#        if qli > 1:
#            break;
#        
#    if qli > 1:
#        break;
#
#print bCount, uCount, qli


    


