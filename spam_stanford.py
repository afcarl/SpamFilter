# -*- coding: utf-8 -*-
import nltk
import bs4
import os
import pickle
import sys

unparsed = []

def recurse(element):
    if isinstance(element, bs4.element.NavigableString):
        try:
            tokens = nltk.word_tokenize(element.strip())
        except:
            unparsed.append(element.strip())
            return
        for token in tokens:
            try:
                print token.lower()
            except:
                pass
        return
    else:
        if element is None:
            return
        for tempelement in element.contents:
            if tempelement != "\n":
                recurse(tempelement)

def parsehtml(l):
    t = "".join(l)
    temp = bs4.BeautifulSoup(t)
    temp = temp.find("html")
    recurse(temp)

all_mails = {}
all_files = []
dir_name = "./SPAM/mails/"

if os.path.isfile(dir_name + "file_token"):
    os.system("rm " + dir_name + "file_token")

for root, dirs, files in os.walk(dir_name):
    all_files = files

cnt = 0
for file_name in all_files:
    cnt += 1
    print cnt, "/", len(all_files)
    file_name = dir_name + file_name
    if file_name == "script.py":
        continue
    f = open(file_name)
    all_tokens = set()
    temp = f.readlines()
    for i in xrange(len(temp)):
        if temp[i] == "\n":
            break

    headers = {}
    for j in xrange(i):
        t = temp[j].split(" ")
        t = map(lambda x: x.strip(), t)
        headers[t[0].strip(":")] = " ".join(t[1:])

    # Open temp token file
    f_token = open(dir_name + "file_token", "w")
    org_stdout = sys.stdout
    sys.stdout = f_token
    try:
        subject = nltk.word_tokenize(headers["Subject"])
        for token in subject:
            print token.lower()
    except:
        pass

    temp = filter(lambda a: a != "\n", temp[i:])

    for i in xrange(len(temp)):
        if temp[i].strip().lower().__contains__("<html>") or temp[i].strip().lower().__contains__("<x-html>"):
            break
        try:
            tokens = nltk.word_tokenize(temp[i])
        except:
            unparsed.append(temp[i].lower())
        else:
            for token in tokens:
                print token.lower()

    parsehtml(temp[i:])
    f_token.close()
    sys.stdout = org_stdout
    os.system("java -cp ../stanford-corenlp/jar/stanford-corenlp-3.5.2.jar edu.stanford.nlp.process.PTBTokenizer " + \
                dir_name + "file_token > final_tokens")
    
    with open("./final_tokens", "r") as jumbo:
        for lines in jumbo:
            try:
                tok = lines.split()[0]
                all_tokens.add(tok)
            except:
                pass
        
    all_mails[file_name] = {"headers": headers, "tokens": list(all_tokens)}
    
with open('./SPAM/all_mails.pickle', 'wb') as mails:
    pickle.dump(all_mails, mails)

# need this ?
with open('./SPAM/unparsed.pickle', 'wb') as unp:
    pickle.dump(unparsed, unp)
