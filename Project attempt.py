import characterUtil
import readUtil
import collections

# Outputs dictionary of style vectors for each author and a list of poem vectors for testing
# Also outputs training set of authors, poem tuples
def styleTrainer():
    testVectors = []
    authorVectors = {} 
    data = readUtil.getTrainingData()
    
    trainingSet = []
    testingSet = []

	# go through each author in data
    for author in data.keys():
            # initialize values for that author... could be simplified by making a vector class...
            halfPoems = len(data[author])/2
            authorVectors[author] = {}
            authorVectors[author]['author'] = author
            authorVectors[author]['numLines'] = 0.0
            authorVectors[author]['avgWordLength'] = 0.0
            authorVectors[author]['avgLineLength'] = 0.0
            authorVectors[author]['rhymePercent'] = 0.0
            authorVectors[author]['wordPairs'] = collections.Counter()
            authorVectors[author]['wordsPerLine']   = collections.Counter()
            authorVectors[author]['linesPerPoem']   = collections.Counter()
            authorVectors[author]['typeTokenCount'] = collections.Counter()
            authorVectors[author]['wordDomain']     = collections.Counter()
            authorVectors[author]['poemStart']      = collections.Counter()

            # go through all of poems
            for index in range(len(data[author])):
                # get stats on the poem
                poemVector = characterUtil.poemCharacter(data[author][index])
			
                # first half is for training
                if index < halfPoems:
                    trainingSet.append(data[author][index])
                    # add those stats to the author
                    authorVectors[author]['numLines'] += poemVector['numLines']
                    authorVectors[author]['avgWordLength'] += poemVector['avgWordLength']
                    authorVectors[author]['avgLineLength'] += poemVector['avgLineLength']
                    authorVectors[author]['rhymePercent'] += poemVector['rhymePercent']
                    authorVectors[author]['wordPairs'].update(poemVector[wordPairs])
                    authorVectors[author]['wordsPerLine'].update(poemVector[wordsPerLine])
                    authorVectors[author]['linesPerPoem'].update(poemVector[linesPerPoem])
                    authorVectors[author]['typeTokenCount'].update(poemVector[typeTokenCount])
                    authorVectors[author]['wordDomain'].update(poemVector[wordDomain])
                    authorVectors[author]['poemStart'].update(poemVector[poemStart])
                    

                # second half goes into testing data
                else:
                    testVectors.append(poemVector)
                    testingSet.append(data[author][index])
    


		# get averages
		authorVectors[author]['numLines'] = authorVectors[author]['numLines']/halfPoems
		authorVectors[author]['avgWordLength'] = authorVectors[author]['avgWordLength']/halfPoems
		authorVectors[author]['avgLineLength'] = authorVectors[author]['avgLineLength']/halfPoems
		authorVectors[author]['rhymePercent'] = authorVectors[author]['rhymePercent']/halfPoems

    return authorVectors, testVectors, trainingSet, testingSet
    
def getFeatureVector(authorVector, poem):
    # Takes in an author vector and a poem string. extracts the feature vector 
    # for this poem. This will mainly take the L1 norm between the poem characteristics
    # and the author characteristics
    phi = {}
    poemVector = characterUtil.poemCharacter(("",poem)) # Don't need author name or word pairs
    phi['numLines'] = abs(poemVector['numLines']-authorVector['numLines'])
    phi['avgWordLength'] = abs(poemVector['avgWordLength']-authorVector['avgWordLength'])
    phi['avgLineLength'] = abs(poemVector['avgLineLength']-authorVector['avgLineLength'])
    phi['rhymePercent'] = abs(poemVector['rhymePercent']-authorVector['rhymePercent'])
    return phi
    
def classifyPoems(authorVectors, testVectors, weights):

	correct = {}
	counter = {}
	for author in authorVectors:
		correct[author] = 0.0
		counter[author] = 0

	for poemVector in testVectors:

		diffVectors = {}
		differences = {}

		for author in authorVectors:
			
			diffVectors[author] = {}
			differences[author] = float('inf')

			for key in poemVector:
				if key != 'author':
					diffVectors[author][key] = abs(poemVector[key] - authorVectors[author][key])

			differences[author] = sum(weights[key]*diffVectors[author][key] for key in weights)

		authorChoice = min(differences, key=differences.get)

		# print poemVector['author'], authorChoice

		if poemVector['author'] == authorChoice:
			correct[poemVector['author']] += 1

		counter[poemVector['author']] += 1
	

	for author in correct:
		correct[author] = correct[author]/counter[author]

	averageCorrect = sum(correct[author] for author in correct)/len(correct)
	#print correct
	#print averageCorrect

	return correct

def predictor(x,weights):
    out = 0
    fw = dotProduct(x,weights)
    if fw < 0:
        out = -1
    elif fw >0:
        out = 1
    
    return out

def learnPredictor(trainExamples, testExamples, featureExtractor, authorVector):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, return the weight vector (sparse feature vector) learned 
    using SGD
    '''
    weights = {}  # feature => weight
    
    def hingeLoss(phi,y,w):
        return max(0, 1-dotProduct(phi,w)*y)
        
    def gradientHingeLoss(phi, y, w):
        out = {}
        margin = dotProduct(phi,w)*y
        if margin < 1:
            increment(out,-y, phi)
        return out
        
    def predictorHelper(x):
        return predictor(featureExtractor(authorVector,x),weights)     

    eta = 0.05 # step size
    numIters = 15
    for num in range(numIters):
        for x,y in trainExamples:
            phi = featureExtractor(authorVector,x)
            for feature in phi:
                if feature not in weights:
                    weights[feature] = 0
            increment(weights, -eta, gradientHingeLoss(phi,y,weights))        
        print "Iter: %1d Train Error: %0.3f        Test Error: %0.3f" % (num, evaluatePredictor(trainExamples, predictorHelper), evaluatePredictor(testExamples, predictorHelper))
    return weights
    
def dotProduct(d1, d2):
    """
    @param dict d1: a feature vector represented by a mapping from a feature (string) to a weight (float).
    @param dict d2: same as d1
    @return float: the dot product between d1 and d2
    """
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())
        
def increment(d1, scale, d2):
    """
    Implements d1 += scale * d2 for sparse vectors.
    @param dict d1: the feature vector which is mutated.
    @param float scale
    @param dict d2: a feature vector.
    """
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale

def evaluatePredictor(examples, predictor):
    '''
    predictor: a function that takes an x and returns a predicted y.
    Given a list of examples (x, y), makes predictions based on |predict| and returns the fraction
    of misclassiied examples.
    '''
    error = 0
    for x, y in examples:
        if predictor(x) != y:
            error += 1
    return 1.0 * error / len(examples)

def getBinarySet(trainingSet, author):
    # Returns a list of training set for each author such that the author's poem's
    # are labeled +1 and the others are labeled -1
    outputSet = []
    for cur_author,poem in trainingSet:
        if cur_author == author:
            outputSet.append((poem,1))
        else:            
            outputSet.append((poem,-1))
    return outputSet
            


###############################################################################
# Main

authorVectors, testVectors, trainingSet, testingSet = styleTrainer()
authorWeights = {}
for author in authorVectors.keys():
    binaryTrainingSet = getBinarySet(trainingSet,author)
    binaryTestingSet = getBinarySet(testingSet,author)
    
    authorWeights[author] = learnPredictor(binaryTrainingSet,binaryTestingSet,getFeatureVector,authorVectors[author])    

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

