"""
    Count tokens for Spam emails
"""
import pickle
all_mails = pickle.load(open("./SPAM/all_mails.pickle", "rb"))

count_dict = {}
for file_name in all_mails:
    all_tokens = all_mails[file_name]["tokens"]
    for token in all_tokens:
        if count_dict.has_key(token):
            count_dict[token] += 1
        else:
            count_dict[token] = 1

with open("./SPAM/countTokens.pickle", "wb") as temp:
    pickle.dump(count_dict, temp)
