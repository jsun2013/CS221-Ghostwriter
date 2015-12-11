import poemClassification
import util
import random
import collections

class poem(util.CSP):
    def __init__(self, author):
        util.CSP.__init__(self)
        self.author = author['author']
        # self.token_num = util.weightedRandomChoice(author['typeTokenCount'])
        self.token_num = 70
        self.line_num = util.weightedRandomChoice(author['linesPerPoem'])
        self.word_num = {}
        self.domain = {} # Domain of our word variables
        # Next two are dict of dicts. The top level dict is keyed by every word
        # in our reduced domain. Each of these is then a dict that is again  
        # keyed by the entire reduced domain, with value = probability that
        # a word appears before/after the top level key.
        self.prev_distribution = {} # Gives a distribution of the of the number of times that
                                    # the inner key comes after the outer key
        self.post_distribution = {} # Reverse of above
        
        # The following two normalizes the distributions into probability 
        # distributions
        self.prev_prob = {}
        self.post_prob = {}
        self.smoothing = 1 # Laplacian smoothing for prev/post distributions
        
        
        # Create the domain of our variables
        while(len(self.domain)<self.token_num):
            add_word = util.weightedRandomChoice(author['wordDomain'])
            if add_word != '' and add_word not in self.domain:
                self.domain[add_word] = author['wordDomain'][add_word]
        
        # Randomly select the number of words per line
        for line_id in xrange(self.line_num):
            word_num = util.weightedRandomChoice(author['wordsPerLine'])
            self.word_num[line_id] = word_num
#            # Add each variable as (line, word_id)
#            for word_id in xrange(word_num):
#                self.add_variable((line_id, word_id), self.domain)
            
        # Create the prev/post dicts
        for word in self.domain:
            # Create the prev_dict
            self.prev_distribution[word] = collections.defaultdict(lambda: self.smoothing)
            self.prev_prob[word] = collections.defaultdict(float)
            total_prev_pairs = 0
            total_post_pairs = 0
            for next_word in self.domain:
                count = author['wordPairs'][word,next_word]
                if count > 0:
                    self.prev_distribution[word][next_word] = count
                    total_prev_pairs += count
                else:
                    self.prev_distribution[word][next_word] = 1
                    total_prev_pairs += 1
                    
            # Create the post_dict
            self.post_distribution[word] = collections.defaultdict(lambda: self.smoothing)
            self.post_prob[word] = collections.defaultdict(float)
            for before_word in self.domain:
                count = author['wordPairs'][(word, before_word)]
                if  count > 0:
                    self.post_distribution[word][before_word] = count
                    total_post_pairs += count
                else:
                    self.post_distribution[word][before_word] = 1
                    total_post_pairs += 1
                    
            # Normalize the distributions to make probabilities
            self.prev_prob[word].update((next_word, count/float(total_prev_pairs)) for next_word, count in self.prev_distribution[word].items())
            self.post_prob[word].update((before_word, count/float(total_post_pairs)) for before_word, count in self.post_distribution[word].items())
        
    
     
#    
#    
#    """
#    OVERRIDES csp.update_binary_factor_table
#    """
#    def update_binary_factor_table(self, var1, var2, table):
#        """
#        Assumes that all binary factors are between word variables and expects
#        the factor functions to return distributions of COUNTS instead of 
#        PROBABILITIES in |table|
#        
#        So, self.binaryDistributionsList[|var1|][|var2|] will give a list of 
#        the separate distributions defined by all of the binary factors between
#        |var1| and |var2|
#        """
#        self.binaryDistributionsList[var1][var2].append = table
#        
#        for neighbor in self.binaryDistributionsList[var1]:
#            
#        if var2 not in self.binaryFactors[var1]:
#            self.binaryFactors[var1][var2] = table
#        else:
#            currentTable = self.binaryFactors[var1][var2]
#            for i in table:
#                for j in table[i]:
#                    assert i in currentTable and j in currentTable[i]
#                    currentTable[i][j] *= table[i][j]
        
                
        
class generator:
    def __init__(self):
        # Dictionary of authors
        self.authors = {}
        
    """
        @PARAM author: String containing author's name
    """
    def add_authors(self, authorVectors):
        for name, vector in authorVectors.items():
            if name not in self.authors:
                self.authors[name] = vector

    """
        @PARAM author: String containing author's name
    """
    def generate_poem(self, author_name):
        if author_name not in self.authors:
            print "ERROR: Invalid author ({})".format(author_name)
            return
        
        author = self.authors[author_name]
        new_poem = poem(author)
        word_num = 0
        
        '''
            Adds a factor that returns a probability that the current word 
            appears given the previous word. Does not perform smoothing within
            the factor, but the smoothing can be applied within the CSP
        '''
#        def before_factor(prev_word, curr_word):
#
#            for word in poem.domain:
#                if prev_var != None:
#                    count = self.authors[poem.author]['wordPairs'][(assignment[prev_var],word)]
#                    if count > 0:
#                        prev_pairs[word] = count + 1 # with smoothing
#                        total_prev_pairs += count + 1 
#
#                if next_var != None:
#                    count = self.authors[poem.author]['wordPairs'][(word, assignment[next_var])]
#                    if  count > 0:
#                        next_pairs[word] = count + 1
#                        total_next_pairs += count + 1
            

        for line_id in xrange(new_poem.line_num):
            word_num = new_poem.word_num[line_id]
            
            for word_id in xrange(word_num):
                #print "INFO: Adding Word {} Line {})".format(word_id, line_id)
                new_poem.add_variable((line_id, word_id), new_poem.domain)
                # Adding transition binary factors between words
                if word_id > 0:
                    #print "INFO: Adding factor between Word {} and Word {} in Line {})".format(word_id-1, word_id, line_id)
#                    new_poem.add_binary_factor((line_id, word_id-1), (line_id, word_id), \
#                    lambda x,y: author['wordPairs'][(x,y)])
                    #print "INFO: Adding factor between Word {} and Word {} in Line {})".format(word_id-1, word_id, line_id)
                    new_poem.add_binary_factor((line_id, word_id-1), (line_id, word_id), \
                       lambda prev,curr: new_poem.prev_prob[prev][curr])
            #Adding beginning/ending unary factors
            #poem.add_unary_factor((line_id, 0), lambda x: True)
            #poem.add_unary_factor((line_id, word_num-1), lambda x: True)
            
            # Adding transition binary factors between lines
            if line_id > 0:
            #print "INFO: Adding factor between (Line {}, Word {}) and (Line {}, Word {})".format(line_id, 0, line_id-1, prev_word_num-1)
                new_poem.add_binary_factor((line_id, 0), (line_id-1, prev_word_num-1), \
#                    lambda x,y: author['wordPairs'][(x,y)])
                    lambda prev,curr: new_poem.prev_prob[prev][curr])
            prev_word_num = new_poem.word_num[line_id]

        poem_assignment = self.gibbs(new_poem)

        for line in range(new_poem.line_num):
            string = str()
            for word in range(new_poem.word_num[line]):
                string += poem_assignment[(line,word)] + ' '
            print string
        
    def gibbs(self, poem):
        assignment = {}
        epsilon = 5
        
        # Assigns unweighted random words to each variable
        for variable in poem.variables:
            rand_word = random.choice(poem.domain.keys())
            assignment[variable] = rand_word
            print rand_word

        print "\n\n"
        
        

        num_changes = epsilon+1
        loop_count  = 0
        numIters = 10
        # while num_changes > epsilon:
        while loop_count < numIters:
            num_changes = 0
            loop_count += 1
            #print "INFO: Gibbs Sampling, Loop {}".format(loop_count)
            
            for (line_id, word_id) in poem.variables:
                variable = (line_id, word_id)
                test = util.csp_weighted_random_choice(poem,variable,assignment)

#                #print "\n\n"
#                #print "INFO: Sampling word {}".format(variable)
#                #print "INFO: Current assignment is {}".format(assignment)
#                context = poem.get_neighbor_vars(variable)
#                #print "\nINFO: Context for {}: {}".format((line_id, word_id), context)
#
#                # Finding previous word
#                prev = zip(*context)
#
#                if (line_id, word_id-1) in context:
#                    prev_var = (line_id, word_id-1)
#                elif line_id-1 in prev[0]:
#                    prev_var = context[prev[0].index(line_id-1)]
#                else:
#                    prev_var = None
#
#                
#                if (line_id, word_id+1) in context:
#                    next_var = (line_id, word_id+1)
#                elif (line_id+1, 0)  in context:
#                    next_var = (line_id+1, 0)
#                else:
#                    next_var = None
#
#
#                # try each word from our local domain as this variable
#                prev_pairs = {}
#                total_prev_pairs = 0
#                next_pairs = {}
#                total_next_pairs = 0
#                assignment_values = {}
#
#                # Try each word against its preceding and following word
#                for word in poem.domain:
#
#                    if prev_var != None:
#                        count = self.authors[poem.author]['wordPairs'][(assignment[prev_var],word)]
#                        if count > 0:
#                            prev_pairs[word] = count + 1 # with smoothing
#                            total_prev_pairs += count + 1 
#
#                    if next_var != None:
#                        count = self.authors[poem.author]['wordPairs'][(word, assignment[next_var])]
#                        if  count > 0:
#                            next_pairs[word] = count + 1
#                            total_next_pairs += count + 1
#
#                # combine keys
#                for word in next_pairs:
#                    if word not in prev_pairs:
#                        prev_pairs[word] = 1
#                        total_prev_pairs += 1
#                for word in prev_pairs:
#                    if word not in next_pairs:
#                        next_pairs[word] = 1
#                        total_next_pairs += 1
#
#
#                # normalize and multiply
#                for word in prev_pairs:
#                    assignment_values[word] = (float(prev_pairs[word])/total_prev_pairs) * (float(next_pairs[word])/total_next_pairs)
#                
#                if assignment_values:
#                    word_choice = util.weightedRandomChoice(assignment_values)
#                else:
#                    word_choice = random.choice(poem.domain.keys())
#
#                assignment[variable] = word_choice
                assignment[variable] = test
                num_changes += 1

        return assignment

            