# Step 1: Data Preprocessing
import re  # regular expression
from collections import Counter
import numpy as np
import pandas as pd


# Implement the function process_data which
# 1) Reads in a corpus
# 2) Changes everything to lowercase
# 3) Returns a list of words.

# a get_count function that returns a dictionary of word vs frequency
def get_count(words):
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count


# implement get_probs function
# to calculate the probability that any word will appear if randomly selected from the dictionary

def get_probs(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs


# Now we implement 4 edit word functions

# DeleteLetter:removes a letter from a given word
def DeleteLetter(word):
    delete_list = []
    split_list = []
    for i in range(len(word)):
        split_list.append((word[0:i], word[i:]))
    for a, b in split_list:
        delete_list.append(a + b[1:])
    return delete_list


delete_word_l = DeleteLetter(word="cans")

# SwitchLetter:swap two adjacent letters


def SwitchLetter(word):
    split_l = []
    switch_l = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_l if len(b) >= 2]
    return switch_l


switch_word_l = SwitchLetter(word="eta")

# replace_letter: changes one letter to another


def replace_letter(word):
    split_l = []
    replace_list = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    replace_list = [a + l + (b[1:] if len(b) > 1 else '')
                    for a, b in split_l if b for l in alphabets]
    return replace_list


replace_l = replace_letter(word='can')

# insert_letter: adds additional characters


def insert_letter(word):
    split_l = []
    insert_list = []
    for i in range(len(word) + 1):
        split_l.append((word[0:i], word[i:]))
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_list = [a + l + b for a, b in split_l for l in letters]
    # print(split_l)
    return insert_list


# combining the edits
# switch operation optional
def edit_one_letter(word, allow_switches=True):
    edit_set1 = set()
    edit_set1.update(DeleteLetter(word))
    if allow_switches:
        edit_set1.update(SwitchLetter(word))
    edit_set1.update(replace_letter(word))
    edit_set1.update(insert_letter(word))
    return edit_set1


# edit two letters
def edit_two_letters(word, allow_switches=True):
    edit_set2 = set()
    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w, allow_switches=allow_switches)
            edit_set2.update(edit_two)
    return edit_set2


# get corrected word
def get_corrections(word, probs, vocab, n=2):
    suggested_word = []
    best_suggestion = []
    suggested_word = list(
        (word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(
            vocab))
    best_suggestion = [[s, probs[s]] for s in list(reversed(suggested_word))]
    return best_suggestion

def nlp(sentence):
    # my_word = input("Enter any word:")s
    w = []  # words
    with open('D:/handwriting/SimpleHTR-master/OCR/NLP dataset/sample.txt', 'r', encoding="utf8") as f:
        file_name_data = f.read()
        file_name_data = file_name_data.lower()
        w = re.findall('\w+', file_name_data)

    v = set(w)  # vocabulary
    # print(f"The first 10 words in our dictionary are: \n{w[0:10]}")
    # print(f"The dictionary has {len(v)} words ")
    word_count = get_count(w)
    # print(f"The dictionary has  {len(word_count)} key values pairs")
    # print("\n")

    #print(sentence)
    words = sentence.split()
    # print(words)
    probs = get_probs(word_count)
    crct_sentence = words
    a = []
    for i in range(0, len(words)):
        with open('D:/handwriting/SimpleHTR-master/OCR/NLP dataset/sample.txt') as myfile:
            if words[i] in myfile.read():
                continue
        tmp_corrections = get_corrections(words[i], probs, v, 2)
        # print("\n")
        if np.array(tmp_corrections).ndim==1:
            tmp_corrections = [tmp_corrections]
        #print(tmp_corrections)
        crct_sentence[i] = tmp_corrections[0][0]
        #print(tmp_corrections)
        a.append(tmp_corrections[0][1])
        # print(tmp_corrections[0][0])
    #     for i, word_prob in enumerate(tmp_corrections):
    #         print(f"word {i}: {word_prob[0]}, probability {word_prob[1]:.6f}")
    #         # crct_sentence.append(word_prob[0])
    # listToStr = ' '.join([str(elem) for elem in crct_sentence])
    #print(listToStr)
    #listToStr = listToStr.strip()
    #my_word = my_word.strip()
    #sentence = sentence.replace(a,listToStr)
    #print(sentence)
    # li = list(sentence.split(" "))
    # for i in range(len(li)):
    #     if li[i]==a:
    #         li[i]=listToStr
    prob = sum(a) / len(a)
    crct_sentence = ' '.join([str(elem) for elem in crct_sentence])
    return crct_sentence
    

#a, prob = nlp("MAre")
# listToStr = ' '.join([str(elem) for elem in a])
#print(a, prob)