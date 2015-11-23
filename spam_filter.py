# -*- coding: utf-8 -*-
import os
import pickle
import sys
import math
import operator

no_of_spam = 0
no_of_ham = 0
ham_mails = {}
spam_mails = {}
ham_tokens = {}
spam_tokens = {}
v1 = 1 #float(sys.argv[1])
v2 = 0.5 #float(sys.argv[2])
TOP_ = 100 #int(sys.argv[3])
UNSEEN = 0.5 #float(sys.argv[4])
#ignore = [",", ">", "<", "/", "\\", "%", ":"]

def divide(a, b):
    return float(float(a)/float(b))

def method1(input_tokens):

    spam_prob = {}
    ham_prob = {}
    for i in input_tokens[:TOP_]:
        # P ( token | spam )
        spam_prob[i] = 0
        if i in spam_tokens:
            spam_prob[i] = divide(spam_tokens[i], no_of_spam)
        # P ( token | ham )
        ham_prob[i] = 0
        if i in ham_tokens:
            ham_prob[i] = divide(ham_tokens[i], no_of_ham)
    sum_ = 0
    for i in input_tokens[:TOP_]:
        if spam_prob[i] == 0 or ham_prob[i] == 0:
            continue
        else:
            sum_ += math.log(divide(spam_prob[i], ham_prob[i]))

    p_s = divide(no_of_spam, no_of_spam + no_of_ham)
    p_h = divide(no_of_ham, no_of_spam + no_of_ham)
    sum_ += math.log(divide(p_s, p_h))
    
    if sum_ > 0:
        return "SPAM"
    else:
        return "HAM"

def assign_probability(token, method):

    # P ( S | token ) =            no_in_spam / no_of_spam 
    #                   _______________________________________________
    #                   no_in_spam / no_of_spam + no_in_ham / no_of_ham

    prob = 0.0
    factor = 1.0

    if token in spam_tokens and token in ham_tokens:
        # present in both
        # Check frequency
        if spam_tokens[token] < 5 and ham_tokens[token] < 5:
            # Treat as unseen
            # TODO: config value ?
            # 0.4 or 0.5
            return UNSEEN
        else:
            no_in_spam = spam_tokens[token]
            no_in_ham = ham_tokens[token]
            prob = divide(divide(no_in_spam, no_of_spam) , \
                    (divide(no_in_spam, no_of_spam) + divide(factor * no_in_ham, no_of_ham)))
    elif token in spam_tokens:
        prob = 0.99
    elif token in ham_tokens:
        prob = 0.01
    else:
        # Treated as unseen
        prob = UNSEEN
        
    return prob

def method2_3(input_tokens, method):

    # P ( S | token )
    spam_prob = {}
    # P ( H | token )
    ham_prob = {}
    input_count = {}
    """
    for i in input_tokens:
        if i not in ignore:
            input_count[i] = 0
            if i in spam_tokens:
                input_count[i] = spam_tokens[i]
    """
    #sorted_tokens = sorted(input_count.items(), key=operator.itemgetter(1), reverse=True)
    #input_tokens = input_count.keys()[:TOP_]
    input_tokens = input_tokens[:TOP_]
    #for i in sorted_tokens[:15]:
    #    input_tokens.append(i[0])
    
    for i in input_tokens:
        spam_prob[i] = assign_probability(i, method)
        ham_prob[i] = 1.0 - spam_prob[i]

        
    # Find probability of sentence or list of tokens
    # P ( S | email ) 
    # P ( S | token1 ) * P ( S | token2 ) * P ( S | token3 )
    mult_spam = 1.0
    mult_ham = 1.0
    for i in input_tokens:
        mult_spam = mult_spam * spam_prob[i]
        mult_ham = mult_ham * ham_prob[i]
    
    n = len(input_tokens)
    p_s = divide(no_of_spam, no_of_spam + no_of_ham)
    p_h = divide(no_of_ham, no_of_spam + no_of_ham)
    if method == 3:
        mult_spam = mult_spam * (p_s ** (1-n))
        mult_ham = mult_ham * (p_h ** (1-n))

    return divide(mult_spam, (mult_spam + mult_ham))

def method4(input_tokens):
    
    a = v1
    b = v2
    # P ( S | token )
    spam_prob = {}
    # P ( H | token )
    ham_prob = {}
    """
    input_count = {}
    for i in input_tokens:
        input_count[i] = 0
        if i in spam_tokens:
            input_count[i] = spam_tokens[i]
    """
    #sorted_tokens = sorted(input_count.items(), key=operator.itemgetter(1), reverse=True)
    #input_tokens = []
    input_tokens = input_tokens[:TOP_]
    #for i in sorted_tokens[:15]:
    #    input_tokens.append(i[0])

    for i in input_tokens:
        no_in_spam = 0
        no_in_ham = 0
        if i in spam_tokens:
            no_in_spam = spam_tokens[i]
        if i in ham_tokens:
            no_in_ham = ham_tokens[i]

        spam_prob[i] = divide(float(a) * b + no_in_spam, a + (no_in_spam + no_in_ham))
        ham_prob[i] = 1.0 - spam_prob[i]

    # Find probability of sentence or list of tokens
    # P ( S | email ) 
    # P ( S | token1 ) * P ( S | token2 ) * P ( S | token3 )
    mult_spam = 1.0
    mult_ham = 1.0
    for i in input_tokens:
        mult_spam = mult_spam * spam_prob[i]
        mult_ham = mult_ham * ham_prob[i]

    n = len(input_tokens)
    p_s = divide(no_of_spam, no_of_spam + no_of_ham)
    p_h = divide(no_of_ham, no_of_spam + no_of_ham)
    mult_spam = mult_spam * (p_s ** (1-n))
    mult_ham = mult_ham * (p_h ** (1-n))

    return divide(mult_spam, (mult_spam + mult_ham))
     
def SpamFilter():

    global ham_mails, spam_mails, ham_tokens, spam_tokens
    global no_of_spam, no_of_ham

    # Mails DICT
    # { email: { "header": ... , "tokens": ... }    
    ham_mails = pickle.load(open("./HAM/all_mails.pickle", "rb"))
    spam_mails = pickle.load(open("./SPAM/all_mails.pickle", "rb"))

    # Token counts
    # { "token": "count" }
    ham_tokens = pickle.load(open("./HAM/countTokens.pickle", "rb"))
    spam_tokens = pickle.load(open("./SPAM/countTokens.pickle", "rb"))

    no_of_spam = len(spam_mails.keys())
    no_of_ham = len(ham_mails.keys())
    total = no_of_spam + no_of_ham
    
    spam_prob = {}
    for i in spam_tokens:
        spam_prob[i] = (float(spam_tokens[i]))/(float(no_of_spam))

    ham_prob = {}
    for i in ham_tokens:
        ham_prob[i] = (float(ham_tokens[i]))/(float(no_of_ham))

    # Get test emails
    easy_ham_mails = pickle.load(open("./HAM_TEST/all_mails.pickle", "rb"))
    easy_spam_mails = pickle.load(open("./SPAM_TEST/all_mails.pickle", "rb"))

    print "Processing Ham"
    ham_gone_ham = {"1": 0, 
                    "2": 0,
                    "3": 0,
                    "4": 0}

    ham_gone_spam = {"1": 0,
                     "2": 0,
                     "3": 0,
                     "4": 0}

    # Find probability for easy ham mails 
    for i in easy_ham_mails:
        input_tokens = easy_ham_mails[i]["tokens"]

        #print "Method One"
        if method1(input_tokens) == "SPAM":
            ham_gone_spam["1"] += 1
        else:
            ham_gone_ham["1"] += 1

        #print "METHOD2", method2_3(input_tokens, 2)        
        if method2_3(input_tokens, 2) < 0.9:
            ham_gone_ham["2"] += 1
        else:
            ham_gone_spam["2"] += 1

        #print "METHOD3", method2_3(input_tokens, 3)
        if method2_3(input_tokens, 3) < 0.9:
            ham_gone_ham["3"] += 1
        else:
            ham_gone_spam["3"] += 1

        #print "METHOD4", method4(input_tokens)
        if method4(input_tokens) < 0.9:
            ham_gone_ham["4"] += 1
        else:
            ham_gone_spam["4"] += 1

    print "Processing Spam"
    spam_gone_spam = {"1": 0,
                      "2": 0,
                      "3": 0,
                      "4": 0}

    spam_gone_ham = {"1": 0,
                     "2": 0,
                     "3": 0,
                     "4": 0}

    # Find probability for easy spam mails
    for i in easy_spam_mails:

        input_tokens = easy_spam_mails[i]["tokens"]
    
        #print "Method One"
        if method1(input_tokens) == "SPAM":
            spam_gone_spam["1"] += 1
        else:
            spam_gone_ham["1"] += 1

        if method2_3(input_tokens, 2) < 0.9:
            spam_gone_ham["2"] += 1
        else:
            spam_gone_spam["2"] += 1

        if method2_3(input_tokens, 3) < 0.9:
            spam_gone_ham["3"] += 1
        else:
            spam_gone_spam["3"] += 1

        if method4(input_tokens) < 0.9:
            spam_gone_ham["4"] += 1
        else:
            spam_gone_spam["4"] += 1


    print "> Results <"
    for i in ["1", "2", "3", "4"]:
        print "#########################################"
        print i
        print ham_gone_ham[i], ham_gone_spam[i]
        print spam_gone_spam[i], spam_gone_ham[i]

if __name__ == "__main__":
    SpamFilter()
