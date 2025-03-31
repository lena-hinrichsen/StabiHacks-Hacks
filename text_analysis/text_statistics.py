import codecs
import nltk as nltk
from HanTa import HanoverTagger as ht
from pathlib import Path
import os

"""
def extract_nouns(fulltext):
    f = open(path)
    raw = f.read()
    textfile = codecs.open(fulltext, "r", "utf-8")
    text = textfile.read()
    textfile.close()
    sentences = nltk.sent_tokenize(raw, language='german')
    nouns = []
    tagger = ht.HanoverTagger('morphmodel_ger.pgz')
    for x in range(0, len(sentences)):
        tokenized_sent = nltk.tokenize.word_tokenize(sentences[x], language='german')
        tags = tagger.tag_sent(tokenized_sent)
        for y in range(0, len(tags)):
            if tags[y][2] == 'NN':
                nouns.append(tags[y][0])
            if tags[y][2] == 'NE':
                nouns.append(tags[y][0])
    print(nouns)
    nouns_in_txt = codecs.open('C:/Users/hinri/PycharmProjects/WD_analysis/nouns.txt', "w", encoding='utf-8')
    for x in range(0, len(nouns)):
        nouns_in_txt.write(str(nouns[x]) + '\n')
    nouns_in_txt.close()
    return nouns
"""


def extract_nouns_per_page(path):
    textfile = codecs.open(path, "r", "utf-8")
    text = textfile.read()
    textfile.close()
    sentences = nltk.sent_tokenize(text, language='german')
    #print(sentences)
    nouns = []
    proper_nouns = []
    nouns_lemmas = []
    proper_nouns_lemmas = []
    tagger = ht.HanoverTagger('morphmodel_ger.pgz')
    for x in range(0, len(sentences)):
        tokenized_sent = nltk.tokenize.word_tokenize(sentences[x], language='german')
        #print(tokenized_sent)
        tags = tagger.tag_sent(tokenized_sent)
        nouns_from_sent = [lemma for (word, lemma, pos) in tags if pos == "NN"]
        nouns_lemmas.extend(nouns_from_sent)
        #print(nouns_lemmas)
        proper_nouns_from_sent = [lemma for (word, lemma, pos) in tags if pos == "NE"]
        proper_nouns_lemmas.extend(proper_nouns_from_sent)
        #print(tags)
        # if you want to know which tags are possible in case tagset is not documented:
        """
        for z in range(0, len(tags)):
            #print(tags[z][2])
            if tags[z][2] not in all_tags:
                all_tags.append(tags[z][2])
         """
        for y in range(0, len(tags)):
            if tags[y][2] == 'NN':
                nouns.append(tags[y][0])
            if tags[y][2] == 'NE':
                proper_nouns.append(tags[y][0])
    #print(nouns)
    # all_tags.sort()
    # print('all_tags = ')
    return nouns, proper_nouns, nouns_lemmas, proper_nouns_lemmas


all_tags = []


def analyze():
    rootdir = 'sbbget\\sbbget_downloads\\download_temp'
    for subdir, dirs, files in os.walk(rootdir):
        if subdir.endswith('_FULLTEXT'):
            name_of_dir = os.path.basename(subdir)
            current_page = (os.path.basename(name_of_dir)[5:9])
            path = Path(subdir)
            current_ppn_path = path.parent.absolute()
            current_ppn = os.path.basename(current_ppn_path)
            fulltext_path = subdir + '\\' + current_page.zfill(8) + '.txt'
            if os.path.isfile(fulltext_path):
                # print('current_page = ' + current_page)
                # print('current_ppn = ' + current_ppn)
                os.makedirs('text_analysis\\results\\' + str(current_ppn) + '\\' + str(current_page))
                file_for_nouns = 'text_analysis\\results\\' + str(current_ppn) + '\\' + str(current_page) + '\\' \
                                 + str(current_ppn) + '_' + str(current_page) + '_nouns.txt'
                file_for_proper_nouns = 'text_analysis\\results\\' + str(current_ppn) + '\\' + str(current_page) \
                                        + '\\' + str(current_ppn) + '_' + str(current_page) + '_proper_nouns.txt'
                file_for_lemmas_nouns = 'text_analysis\\results\\' + str(current_ppn) + '\\' + str(current_page) \
                                        + '\\' + str(current_ppn) + '_' + str(current_page) + '_nouns_lemmatized.txt'
                file_for_lemmas_proper_nouns = 'text_analysis\\results\\' + str(current_ppn) + '\\' \
                                               + str(current_page) + '\\' + str(current_ppn) + '_' \
                                               + str(current_page) + '_proper_nouns_lemmatized.txt'
                # print('file for nouns = ' + str(file_for_nouns))
                nouns_and_proper_nouns = extract_nouns_per_page(fulltext_path)
                nouns = nouns_and_proper_nouns[0]
                proper_nouns = nouns_and_proper_nouns[1]
                nouns_lemmas = nouns_and_proper_nouns[2]
                proper_nouns_lemmas = nouns_and_proper_nouns[3]
                with open(file_for_nouns, "w", encoding='utf-8') as f:
                    for x in range(0, len(nouns)):
                        f.write(nouns[x] + '\n')
                with open(file_for_proper_nouns, "w", encoding='utf-8') as g:
                    for x in range(0, len(proper_nouns)):
                        g.write(proper_nouns[x] + '\n')
                with open(file_for_lemmas_nouns, "w", encoding='utf-8') as h:
                    for x in range(0, len(nouns_lemmas)):
                        h.write(nouns_lemmas[x] + '\n')
                with open(file_for_lemmas_proper_nouns, "w", encoding='utf-8') as i:
                    for x in range(0, len(proper_nouns_lemmas)):
                        i.write(proper_nouns_lemmas[x] + '\n')
        print("next")
    all_tags.sort()
    print(all_tags)

analyze()
