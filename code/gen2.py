import poemClassification
import util
import random
import collections
import sys
import copy

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
        
        self.neighborFactors = {} # self.neighborFactors[var1] returns a list tuples. 
                                    # The first element in the tuple is a neighbor variable.
                                    # The second element is a factor function that returns
                                    #  a distribution given the neighbor assignment.
        
        
        
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
            self.prev_distribution[word] = collections.defaultdict(int)
            self.prev_prob[word] = collections.defaultdict(float)
            total_prev_pairs = 0
            total_post_pairs = 0
            for next_word in self.domain:
                count = author['wordPairs'][word,next_word]
                if count > 0:
                    self.prev_distribution[word][next_word] = count
                    total_prev_pairs += count
                    
            # Create the post_dict
            self.post_distribution[word] = collections.defaultdict(int)
            self.post_prob[word] = collections.defaultdict(float)
            for before_word in self.domain:
                count = author['wordPairs'][(before_word, word)]
                if  count > 0:
                    self.post_distribution[word][before_word] = count
                    total_post_pairs += count
                    
            # Normalize the distributions to make probabilities
            self.prev_prob[word].update((next_word, count/float(total_prev_pairs)) for next_word, count in self.prev_distribution[word].items())
            self.post_prob[word].update((before_word, count/float(total_post_pairs)) for before_word, count in self.post_distribution[word].items())
    
    """
    OVERRIDES csp.get_neighborFactors
    """    
    def get_neighborFactors(self, var):
        """
        Returns a list of variables which are neighbors of |var|.
        """
        return [neighbor for neighbor,_ in self.neighborFactors[var]]
    
    """
    Overides csp.add_binary_factor
    """
    def add_binary_factor(self, var1, var2, factor_func1, factor_func2):
#        util.CSP.add_binary_factor(self,var1,var2,factor_func1)

        if var1 not in self.neighborFactors:
            self.neighborFactors[var1] = [(var2, factor_func1)]
        else:
            self.neighborFactors[var1].append((var2, factor_func1))
        if var2 not in self.neighborFactors:
            self.neighborFactors[var2] = [(var1, factor_func1)]
        else:
            self.neighborFactors[var2].append((var1, factor_func1))
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
    def generate_poem(self, author_name,print_flag):
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
                        lambda prev: new_poem.prev_distribution[prev],
                        lambda curr: new_poem.post_distribution[curr])
            #Adding beginning/ending unary factors
            #poem.add_unary_factor((line_id, 0), lambda x: True)
            #poem.add_unary_factor((line_id, word_num-1), lambda x: True)

            def disallow_repeats(val):
                distr = collections.defaultdict(lambda: 5)
                distr[val] = 0
                return distr
            
            # Adding transition binary factors between lines
            if line_id > 0:
            #print "INFO: Adding factor between (Line {}, Word {}) and (Line {}, Word {})".format(line_id, 0, line_id-1, prev_word_num-1)
                new_poem.add_binary_factor((line_id, 0), (line_id-1, prev_word_num-1), \
#                    lambda x,y: author['wordPairs'][(x,y)])
                    lambda prev: new_poem.prev_distribution[prev],
                    lambda curr: new_poem.post_distribution[curr])
                # Don't let words be repeated for now
                new_poem.add_binary_factor((line_id, 0), (line_id-1, prev_word_num-1), \
#                    lambda x,y: author['wordPairs'][(x,y)])
                    disallow_repeats,
                    disallow_repeats)
            prev_word_num = new_poem.word_num[line_id]

        poem_assignment = self.gibbs(new_poem)
        
        
        poem_out = str()
        for line in range(new_poem.line_num):
            string = str()
            for word in range(new_poem.word_num[line]):
                string += poem_assignment[(line,word)] + ' '
            if print_flag:
                print string
            string += "\n"
            poem_out += string
        return poem_out
        
    def gibbs(self, poem):
        assignment = {}
        epsilon = 5
        
        # Assigns unweighted random words to each variable
        for variable in poem.variables:
            rand_word = random.choice(poem.domain.keys())
            assignment[variable] = rand_word
#            print rand_word
#
#        print "\n\n"
        
        print "Generating Poem...\n"
        sys.stdout.flush()
        

        num_changes = epsilon+1
        loop_count  = 0
        numIters = 15
        # while num_changes > epsilon:
        while loop_count < numIters:
            num_changes = 0
            loop_count += 1
            #print "INFO: Gibbs Sampling, Loop {}".format(loop_count)
            
            for (line_id, word_id) in poem.variables:
                variable = (line_id, word_id)
                test = poem_weighted_random_choice(poem,variable,assignment)
                assignment[variable] = test
                num_changes += 1

        return assignment

def poem_weighted_random_choice(poem, var, assignment):
        """
        Given a |poem| csp, a word variable |var|, and a current |assignment|,
        Returns a new assignment for |var| based on a weighted random choice 
        given the neighboring variable assignments
        """
        distributions = [] 
        probability = {}
        poss_words = set()
        
        # Assemble the distributions with smoothing
        for neighbor, factor_func in poem.neighborFactors[var]:
            neighbor_val = assignment[neighbor]
            cur_distribution = copy.deepcopy(factor_func(neighbor_val))
            distributions.append(cur_distribution)
            
            #Take union of the words
            poss_words = poss_words | set(cur_distribution.keys())
        
        # There is a chance we will have no possible words. In this case, just 
        # reseed everything so we take a random choice
        if not poss_words:
            return random.choice(poem.domain.keys())
        else:
            # Perform smoothing
            for distribution in distributions:           
                # Perform Smoothing on the two distributions based on the union
                for possibility in poss_words:
                    if distribution[possibility] == 0:
                        distribution[possibility] = 1
                    else:
                        distribution[possibility] += 1
           
            # Create the joint probability distr by converting the distributions to
            # probabilities and elem-wise multiplication. Don't need to deepcopy again
            for distribution in distributions:
               normalize_distribution(distribution)
               if not probability:
                   probability = distribution
               else:
                   for elem in probability.keys():
                       probability[elem] *= distribution[elem]
           
            # Renormalize probabilities and then call weighted random choice
            normalize_distribution(probability)
            
            
            new_val = util.weightedRandomChoice(probability)
            return new_val 
        
def normalize_distribution(distribution):
    """
    Normalizes a |distribution| dict to be a probability distribution
    """
    totalSum = sum(distribution.itervalues())
    distribution.update((key, val/float(totalSum)) for key, val in distribution.items())
        