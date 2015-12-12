from poemClassification import *
from gen2 import *


# Learn weights for each author
authorVectors, testVectors, trainingSet, testingSet = styleTrainer()
    
authorWeights = getWeights(authorVectors,trainingSet,testingSet)

# Test weights
errors = {'Coleridge':0,'Frost':0,'Kerouac':0,'Seuss':0,'Dante':0}
count = {'Coleridge':0.0,'Frost':0.0,'Kerouac':0.0,'Seuss':0.0,'Dante':0}
for (correctAuthor,poem) in testingSet:
    count[correctAuthor]+=1
    bestAuthor = classifyPoem(authorWeights,poem)
    
    # Done with computing scores
    if bestAuthor != correctAuthor:
        errors[correctAuthor] += 1

for author in errors.keys():
    errors[author] = errors[author]/count[author]

gen = generator()
gen.add_authors(authorVectors)
gen.generate_poem('Kerouac',True)
    