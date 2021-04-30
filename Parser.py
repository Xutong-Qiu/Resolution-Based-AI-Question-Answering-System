import nltk
from nltk.stem import WordNetLemmatizer

#### run the following once to install or download necessary libraries###
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

verbose = True
new = True     # set to true when analyzing new syntax
lemmatizer = WordNetLemmatizer()

def parser(sentence):
    
    tokens = nltk.word_tokenize(sentence)   
    standardTags = nltk.tag.pos_tag(tokens)               # the standard tag set has a zillion tags   
    tags = nltk.tag.pos_tag(tokens, tagset='universal')   # 'universal' is a simplified tag set
    syntax = [item[1] for item in tags]

    if(syntax == ['NOUN', 'VERB', 'ADJ', '.']):  # Jack is smart.
        modifier = [item[0] for item in tags if item[1] == 'ADJ'][0]
        noun = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN'][0]
        if(tags[0][0].lower() == noun):
            fopl = modifier +'(' + noun + ')'
        else:
            fopl = 'All(X) ' + noun + '(X) -> ' + modifier + '(X)'

    elif(syntax == ['NOUN', 'VERB', 'ADV', 'ADJ', '.']):
        modifier = [item[0] for item in tags if item[1] == 'ADJ'][0]
        noun = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN'][0]
        if(tags[0][0].lower() == noun):
            fopl = '~' + modifier +'(' + noun + ')'
        else:
            fopl = 'All(X) ~ ( ' + noun + '(X) -> ' + modifier + '(X) )'

    elif(syntax == ['NOUN', 'VERB', 'DET', 'ADJ', '.']):
        modifier = [item[0] for item in tags if item[1] == 'ADJ'][0]
        noun = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN'][0]
        fopl = modifier +'(' + noun + ')'

    elif(syntax == ['NOUN', 'VERB', 'NOUN', '.']):
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
        noun = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        if(verb == 'be'):
            if(tags[0][0].lower() == noun[0]):
                fopl = noun[1] + '(' + noun[0] + ')'
            else:
                fopl = 'All(X) ' + noun[0] + '(X) -> ' + noun[1] + '(X)'
        else:
            if(tags[0][0].lower() == noun[0]):
                fopl = verb + '(' + noun[0] + ',' + noun[1] + ')'
            else:
                 fopl = 'All(X) ' + noun[0] + '(X) -> ' + verb + '(' + noun[0] + ',' + noun[1] + ')'

    elif(syntax == ['NOUN', 'VERB', 'ADJ', 'CONJ', 'ADJ', '.']): # Jack is smart and/or kind.
        # 'CONJ' can be 'and', 'or'
        modifiers = [item for item in tags if item[1] == 'ADJ']
        noun = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN'][0]
        conj = [item[0] for item in tags if item[1] == 'CONJ'][0]
        if(conj == 'or'):
            symbol = ' | '
        elif(conj == 'and'):
            symbol = ' & '
        else:
            return('invalid symbol')
        fopl = modifiers[0][0] +'(' + noun + ')' + symbol + modifiers[1][0] +'(' + noun + ')'

    elif(syntax == ['NOUN', 'VERB', 'DET', 'NOUN', '.']): # Jack is a student. 
        # 'VERB' is 'is' 
         nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        # noun = [item[0] for item in tags if item[1] == 'NOUN'][0]
         verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
         det = [item[0] for item in tags if item[1] == 'DET'][0]
         if verb == 'be':
            fopl = nouns[1] + '(' + nouns[0] + ')'
         else:
            if det == 'all' or det == 'every':
                fopl = 'All(X) ' + nouns[1] + '(X) & ' + nouns[0] + '(X)'
            elif det == 'some':
                fopl = 'Ex(X) ' + nouns[1] + '(X) | ' + nouns[0] + '(X)'
            else:
                verb = lemmatizer.lemmatize(verb, 'v')
                fopl = verb + '(' + nouns[0] + ',' + nouns[1] + ')'

    elif(syntax == ['DET', 'NOUN', 'VERB', 'DET', 'NOUN', '.']): # A dog chases a car.
        # VERB is not 'is' (to be or not to be)
         verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
         nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
         fopl = verb + '(' + nouns[0] + ',' + nouns[1] + ')'

    elif(syntax == ['DET', 'NOUN', 'VERB', 'NOUN', '.']): 
        # All men are mortals. ∀(x) ((man(x)) → (mortal(x)))
        # No cat loves fish. ¬∃(X) ((cat(X) → (love(X, dog)))
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
        (det, _) = tags[0]
        if(det == 'All') or (det == 'Every'):
            if verb == 'be':
                fopl = 'All(X) ' + nouns[0] + '(X) -> ' + nouns[1] + '(X)'
            else:
                fopl = 'All(X) ' + nouns[0] + '(X) -> ' + verb + '(X,' + nouns[1]+ ')'
        elif det == 'Some':
            if verb == 'be':
                fopl = 'Ex(X) ' + nouns[0] + '(X) -> ' + nouns[1] + '(X)'
            else:
                fopl = 'Ex(X) ' + nouns[0] + '(X) -> ' + verb + '(X,' + nouns[1]+ ')'
        elif det == 'No':
            if verb == 'be':
                fopl = 'All(X) ' + nouns[0] + '(X) -> ~' + nouns[1] + '(X)'
            else:
                fopl = 'All(X) ' + nouns[0] + '(X) -> ~' + verb + '(X,' + nouns[1]+ ')'

    elif((syntax == ['ADV', 'DET', 'NOUN', 'VERB', 'NOUN', '.'] or 
    syntax == ['ADV', 'DET', 'NOUN', 'ADP', 'NOUN', '.']) and
    ((tokens[0] == 'Not' and tokens[1] == 'all') or ((tokens[0] == 'Not' and tokens[1] == 'every')))):
    # 'Not every cat likes dogs.'
    # 'Not all cats like dogs.'
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB' or item[1] == 'ADP'][0]
        if(verb == 'is') or (verb == 'are'):
            fopl = 'Ex(X) ~ ( ' + nouns[0] + '(X) -> ' + nouns[1] + '(X) )'
        else:
            fopl = 'Ex(X) ~ ( ' + nouns[0] + '(X) -> ' + verb + '(X,' + nouns[1]+ ') )'

    elif(syntax == ['DET', 'NOUN', 'VERB', 'ADV', 'ADJ', '.']):
        # All flowers are not fragrant.
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
        adj = [item[0] for item in tags if item[1] == 'ADJ'][0]
        adv = [item[0] for item in tags if item[1] == 'ADV'][0]
        if verb == 'be':
            if(tokens[0] == 'All' or tokens[0] == 'Every') and (adv == 'not'):
                fopl = 'All(X) ~ ( ' + nouns[0] + '(X) -> ' + adj + '(X) )'
            elif(tokens[0] == 'Some') and (adv == 'not'):
                fopl = 'Ex(X) ~ ( ' + nouns[0] + '(X) -> ' + adj + '(X) )'
            elif(tokens[0] == 'No') and (adv == 'not'):
                fopl = 'All(X) ' + nouns[0] + '(X) -> ' + adj + '(X)'
            else:
                fopl = 'undefined'
        else:
            fopl = 'undefined'
            
    elif(syntax == ['DET', 'NOUN', 'VERB', 'ADV', 'VERB', '.']):
        # All flowers are not fragrant.
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB']
        adv = [item[0] for item in tags if item[1] == 'ADV'][0]
        if verb[0] == 'do':
            if(tokens[0] == 'All' or tokens[0] == 'Every') and (adv == 'not'):
                fopl = 'All(X) ~ ( ' + nouns[0] + '(X) -> ' + verb[1] + '(X) )'
            elif(tokens[0] == 'Some') and (adv == 'not'):
                fopl = 'Ex(X) ~ ( ' + nouns[0] + '(X) -> ' + verb[1] + '(X) )'
            elif(tokens[0] == 'No') and (adv == 'not'):
                fopl = 'All(X) ' + nouns[0] + '(X) -> ' + verb[1] + '(X)'
            else:
                fopl = 'undefined'
        else:
            fopl = 'undefined'
    
    elif(syntax == ['DET', 'NOUN', 'VERB', 'ADJ', '.'] and tokens[0] == 'All' and 
    (tokens[2] == 'are' or tokens[2] == 'is')):
        # All water is precious.        All dogs are nice.
        # fopl = 'All(x) ' + tokens[3] + '(' + tokens[1] + ')' 
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        fopl = 'All(X) ' + nouns[0] + '(X) -> ' + tokens[3] + '(X)'

    elif(syntax == ['DET', 'NOUN', 'VERB', 'ADJ', '.'] and tokens[0] == 'Some' and 
    (tokens[2] == 'are' or tokens[2] == 'is')):
        # Some water is expensive.      Some cats are nice.
        # fopl = '∃(x) ' + tokens[3] + '(' + tokens[1] + ')' 
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        fopl = 'Ex(X) ' + nouns[0] + '(X) -> ' + tokens[3] + '(X)'

    elif(syntax == ['NOUN', 'VERB', 'DET', 'ADJ', 'NOUN', '.']): # Jack is a smart student.
        # 'VERB' is 'is' -- need to distinguish not 'is'
         modifier = [item[0] for item in tags if item[1] == 'ADJ'][0]
         nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
         fopl = modifier + '(' + nouns[0] + ') & ' + nouns[1] + '(' + nouns[0] + ')'

    # New edit
    elif(syntax == ['NOUN', 'VERB', 'NOUN', 'CONJ', 'NOUN', '.'] or
        syntax == ['NOUN', 'VERB', 'DET', 'NOUN', 'CONJ', 'DET', 'NOUN', '.'] or
        syntax == ['DET', 'NOUN', 'VERB', 'NOUN', 'CONJ', 'NOUN', '.'] or
        syntax == ['DET', 'NOUN', 'VERB', 'DET', 'NOUN', 'CONJ', 'DET', 'NOUN', '.'] or
        syntax == ['NOUN', 'VERB', 'DET', 'DET', 'NOUN', 'CONJ', 'DET', 'NOUN', '.']) : 
        # Bill loves cheese and bacon.
        # Tom buys a notebook and a pencil.
        # 'CONJ' can be 'and', 'or'
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
        conj = [item[0] for item in tags if item[1] == 'CONJ'][0]
        if(conj == 'or'):
            symbol = ' | '
        elif(conj == 'and'):
            symbol = ' & '
        else:
            return('invalid symbol')
        fopl = verb +'(' + nouns[0] + ',' + nouns[1] + ')' + symbol + verb +'(' + nouns[0] + ',' + nouns[2] + ')'

    elif(syntax == ['DET', 'NOUN', 'DET', 'VERB', 'DET', 'NOUN', 'VERB', 'ADJ', '.'] or
        syntax == ['DET', 'NOUN', 'DET', 'VERB', 'NOUN', 'VERB', 'ADJ', '.']):
        # All student that finishes the homework is excellent.
        # Some student that take mathematics is smart.
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
        modifier = [item for item in tags if item[1] == 'ADJ'][0][0]
        if (tokens[0] == 'All' or tokens[0] == 'Every'):
            fopl = 'All(X) ' + nouns[0] + '(X) ' + '& ' + verb + '(X,' + nouns[1] +') -> ' + modifier + '(X)'
        else:
            fopl = 'Ex(X) ' + nouns[0] + '(X) ' + '& ' + verb + '(X,' + nouns[1] +') -> ' + modifier + '(X)'
    
    elif(syntax == ['DET', 'NOUN', 'DET', 'VERB', 'DET', 'NOUN', 'VERB', 'NOUN', '.'] or
        syntax == ['DET', 'NOUN', 'DET', 'VERB', 'NOUN', 'VERB', 'NOUN', '.'] or 
        syntax == ['DET', 'NOUN', 'DET', 'VERB', 'DET', 'NOUN', 'VERB', 'DET', 'NOUN', '.'] or
        syntax == ['DET', 'NOUN', 'DET', 'VERB', 'NOUN', 'VERB', 'DET', 'NOUN', '.']):
        # Every person that buys a computer plays games.
        # Some student that take mathematics passes mathematics.
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verbs = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB']
        if (tokens[0] == 'All' or tokens[0] == 'Every'):
            fopl = 'All(X) ' + nouns[0] + '(X) ' + '& ' + verbs[0] + '(X,' + nouns[1] +') -> ' + verbs[1] + '(X,' + nouns[2] +')'
        else:
            fopl = 'Ex(X) ' + nouns[0] + '(X) ' + '& ' + verbs[0] + '(X,' + nouns[1] +') -> ' + verbs[1] + '(X,' + nouns[2] +')'

    elif(tokens[0] == 'If'):
        # If Tom buys a car, then Mary is happy.
        # Split the sentence, s[0] will be the if part, s[1] will be the then part
        s = sentence.split(', then ')
        s[0] = s[0][3:] + '.'
        fopl = parser(s[0]) + ' -> ' + parser(s[1])

    elif(syntax == ['NOUN', 'VERB', 'ADV', 'VERB', 'DET', 'NOUN', 'VERB', '.']):
        if lemmatizer.lemmatize(tags[1][0], 'v') == 'do' and tags[2][0] == 'not':
            nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
            verbs = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB']

            fopl = 'All(X) ' + verbs[2] + '(' + nouns[1] + ',X)' + ' -> ~' + verbs[1] + '(' + nouns[0] + ',X)'
        else:
            fopl = 'undefined'    

    elif(syntax == ['NOUN', 'VERB', 'DET', 'NOUN', 'VERB', 'ADV', 'VERB', '.']):
        if lemmatizer.lemmatize(tags[4][0], 'v') == 'do' and tags[5][0] == 'not':
            nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
            verbs = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB']

            fopl = 'All(X) ~' + verbs[2] + '(' + nouns[1] + ',X)' + ' -> ' + verbs[0] + '(' + nouns[0] + ',X)'
        else:
            fopl = 'undefined'      

    elif(syntax == ['DET', 'NOUN', 'NOUN', 'VERB', 'NOUN', 'CONJ', 'NOUN', '.']):
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
        conj = [item[0] for item in tags if item[1] == 'CONJ'][0]
        symbol = ''
        if(conj == 'or'):
            symbol = ' | '
        elif(conj == 'and'):
            symbol = ' & '
        else:
            return('invalid symbol')
        if(verb == 'be'):
            fopl = ('All(X) ' + nouns[1] + '(X,' + nouns[0] + ')' + ' -> ' 
            + nouns[2] + '(X)' + symbol + nouns[3] + '(X)')
        else:
            fopl = 'undefined'

    elif(syntax == ['NOUN', 'CONJ', 'NOUN', 'CONJ', 'NOUN', 'VERB', 'NOUN', 'ADP', 'NOUN', '.']):
        conjs = [item[0] for item in tags if item[1] == 'CONJ']
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        symbols = [' & ', ' & ']
        for i in range(0, 2):
            if conjs[i] != 'or' and conjs[i] != 'and':
                return('invalid symbol')
            if(conjs[i] == 'or'):
                symbols[i] = ' | '
        if verb == 'be':
            fopl = (nouns[3] + '(' + nouns[0] + ',' + nouns[4] + ')'
                    + symbols[0] + nouns[3] + '(' + nouns[1] + ',' + nouns[4]
                    + ')' + symbols[1] + nouns[3] + '(' + nouns[2] + ',' + nouns[4] + ')')
        else:
            fopl = 'undefined'

    elif(new):  
        fopl = 'undefined'    

    else:
        return ('Syntax not recognized: ', syntax)
        
    if(verbose):
        print('sentence: ', sentence)
        print('tokens: ', tokens)
        print('standard tags: ', standardTags)
        print('simple tags:  ', tags)
        print('syntax: ', syntax)
        print('fopl: ', fopl)
        print()
    
    return fopl

# Testing sentences

# parser('Cats are lazy.')
# parser('Socrates is mortal.')

'''
parser('Jack is a student.')
parser('Cats love some fish.')
parser('Humans are mammals.')
parser('Sparrow is a bird.')
parser('Socrates is mortal.')
parser('Socrates is mortal and Greek.')
parser('Socrates is mortal or Greek.')
parser('Socrates is a philospher.')
parser('A dog chases a car.')
parser('Socrates is a mortal philospher.')
parser('Joe climbs a ladder.')
parser('Joe climbs a ladder.')

print('***Multiple sentences***\n')
text = 'A dog chases a car. Socrates is a mortal philospher. '
sentences = nltk.sent_tokenize(text)
for sentence in sentences:
    parser(sentence)
    
print("***Quantifiers***")
parser('Some cats are nice.')
parser('All dogs are nice.')
parser('All water is precious.')
parser('Some water is expensive.')
parser('All men are mortals.')
parser('No cats loves dog.')
parser('Some cats catch mice.')
parser('Every dog loves humans.')
parser('Not all cats like dogs.')
parser('Not every cat likes dogs.')


parser('All men are mortals.')
parser('No cats loves dog.')
# parser('A cat loves fish.') # ['DET', 'NOUN', 'VERB', 'ADJ', '.'], nlkt library error.
parser('Some cats catch mice.')

# syllogism
#text = 'All people are mortal. Socrates is a person. Therefore, Socrates is mortal.'
#sentences = nltk.sent_tokenize(text)
#for sentence in sentences:
#   parser(sentence)

parser('Bill loves coffee and bacon.')
parser('Bill loves coffee or bacon.')
parser('Tom buys the a notebook and a pencil.')
parser('All student that finishes the homework is excellent.')
parser('Some student that take mathematics is smart.')
parser('All person that buys a computer plays games.')
parser('Some student that takes mathematics loves mathematics.')
parser('If Tom buys a car, then Mary is happy.')
parser('All flowers are not fragrant.')
parser('Some flowers are not fragrant.')
parser('No flower is not fragrant.')
parser('No dog does not bark.')
'''

# Sample Result

parser('All skiers love snow.')
parser('No climber likes rain.')
parser('Tony likes rain and snow.')
parser('Bill does not like whatever Tony likes.')
parser('Bill likes whatever Tony does not like.')
parser('All Alpine members are skiers or climbers.')
parser('Tony and Bill and John are members of Alpine.')
