import poemClassification
import util
import random

class poem(util.CSP):
    def __init__(self, author):
        util.CSP.__init__(self)
        self.author = author['author']
        self.token_num = util.weightedRandomChoice(author['typeTokenCount'])
        self.domain = random.sample(author['wordDomain'], self.token_num)
        
        self.line_num = util.weightedRandomChoice(author['linesPerPoem'])
        self.word_num = {}
        for line_id in xrange(self.line_num):
            word_num = util.weightedRandomChoice(author['wordsPerLine'])
            self.word_num[line_id] = word_num
        
class generator:
    def __init__(self):
        # Dictionary of authors
        self.authors = {}
        
        # Dictionary of poems
        self.poems = {}
        
        # Poem classifier
        self.classifier = {}
        
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
        if author not in self.authors:
            print "ERROR: Invalid author ({})".format(author)
            return
        
        author = self.authors[author_name]
        new_poem = poem(author)
        word_num = 0
        for line_id in xrange(new_poem.line_num):
            for word_id in xrange(word_num):
                poem.add_variable((line_id, word_id), poem.domain)
                # Adding transition binary factors between words
                if word_id > 0:
                    poem.add_binary_factor((line_id, word_id-1), (line_id, word_id), \
                        lambda x,y: author['wordPairs'][(x,y)])
            
            #Adding beginning/ending unary factors
            #poem.add_unary_factor((line_id, 0), lambda x: True)
            #poem.add_unary_factor((line_id, word_num-1), lambda x: True)
            
            # Adding transition binary factors between lines
            if line_id > 0:
                pass
                new_poem.add_binary_factor((line_id, 0), (line_id-1, prev_word_num-1), \
                    lambda x,y: author['wordPairs'][(x,y)])
            prev_word_num = new_poem.word_num[line_id]