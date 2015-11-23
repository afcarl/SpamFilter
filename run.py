import os

print "Tokenizing HAM Training emails"
os.system("python ham_stanford.py")
print "Tokenizing SPAM Training emails"
os.system("python spam_stanford.py")
print "Counting Tokens"
os.system("python count_ham_tokens.py")
os.system("python count_spam_tokens.py")
print "Running Tests"
os.system("python ham_test_stanford.py")
os.system("python spam_test_stanford.py")
print "SPAM Filtering emails"
os.system("python spam_filter.py")
