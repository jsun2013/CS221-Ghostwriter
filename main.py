from poemClassification import *
from gen2 import *


# Learn weights for each author
authorVectors, testVectors, trainingSet, testingSet = styleTrainer()
"""
authorWeights = {}
for author in authorVectors.keys():
    binaryTrainingSet = getBinarySet(trainingSet,author)
    binaryTestingSet = getBinarySet(testingSet,author)
    
    authorWeights[author] = learnPredictor(binaryTrainingSet,binaryTestingSet,getFeatureVector,authorVectors[author])    

# Test weights
errors = {'Coleridge':0,'Frost':0,'Kerouac':0,'Seuss':0,'Dante':0}
count = {'Coleridge':0.0,'Frost':0.0,'Kerouac':0.0,'Seuss':0.0,'Dante':0}
for (correctAuthor,poem) in testingSet:
    count[correctAuthor]+=1
    bestScore = 0
    bestAuthor = None
    for curAuthor in authorVectors.keys():
        phi = getFeatureVector(authorVectors[curAuthor],poem)
        w = authorWeights[curAuthor]
        score = dotProduct(phi,w)
        if score>bestScore:
            bestScore = score
            bestAuthor = curAuthor
    
    # Done with computing scores
    if bestAuthor != correctAuthor:
        errors[correctAuthor] += 1

for author in errors.keys():
    errors[author] = errors[author]/count[author]
"""

test = generator()
test.add_authors(authorVectors)
test.generate_poem('Dante')