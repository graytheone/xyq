import nltk
from nltk.corpus import gutenberg
from nltk.parse import CoreNLPParser
from collections import Counter
from pprint import pprint
import numpy as np
import unicodedata
# 这里要放一个contractions.py
import txt_related
from contractions import CONTRACTION_MAP
import re
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
import spacy
import csv
from textblob import TextBlob
from utils import FILE
from stanfordcorenlp import StanfordCoreNLP

#获取去除停用词之后的清洗后的文本
def getCleanText():
    stopword_list = nltk.corpus.stopwords.words('english')
    ori_text = load_text(FILE)
    clean_text = remove_special_characters(ori_text)
    exp_text = expand_contractions(clean_text, CONTRACTION_MAP)
    lem_text = lemmatize_text(exp_text)
    main_text = remove_stopwords(lem_text, stopword_list)
    return main_text

#获得命名实体
def getNamedEntity():
    nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-10-05', port=9000)
    # ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
    sentimentP = {}  # polarity
    sentimentS = {}  # subjectivity
    texts = txt_related.returnContent()  # 获得文本内容
    all = Counter()
    eachChapter = []
    f = open('df_sentiment.csv', 'w+', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(['character', 'chapter', 'polarity', 'subjectivity'])

    file = open('df_theme.csv', 'w+', encoding='utf-8', newline='')
    csv_write = csv.writer(file)
    csv_write.writerow(['character', 'chapter', 'sentence'])
    cha = 1
    relevance = []
    for text in texts:  # 每章需要拆分为各个句子
        sents = sent_tokenize(text)
        characters = []
        for sent in sents:  # 对各个句子进行分词实体识别
            tags = nlp.ner((sent))
            character = [tag[0] for tag in tags if tag[1] == "PERSON"]  # 只对PERSON进行识别
            if (character != []):
                if character[0] not in sentimentP.keys():
                    sentimentP[character[0]] = []
                    sentimentS[character[0]] = []
                blob = TextBlob(sent)
                sentimentP[character[0]].append(round(blob.sentiment.polarity, 2))
                sentimentS[character[0]].append(round(blob.sentiment.subjectivity, 2))
                #            if(len(len(character) != 1)):
                characters = characters + character
                if len(character) == 1:
                    relevance.append([character[0], character[0]])
                    csv_write.writerow([character[0], cha, sent])
                if len(character) > 1:
                    for i in range(len(character)):
                        for j in range(len(character) - i):
                            relevance.append([character[i], character[j]])
                    for i in range(len(character)):
                        csv_write.writerow([character[i], cha, sent])

        for key in sentimentP.keys():
            cnt = 0
            length = len(sentimentP[key])
            for i in range(len(sentimentP[key])):
                csv_writer.writerow([key, round(cha + cnt / length, 2), sentimentP[key][i], sentimentS[key][i]])
                cnt = cnt + 1
        cha = cha + 1
        sentimentP = {}  # polarity
        sentimentS = {}  # subjectivity
        all.update(characters)  # 对整体的人进行分词
        li = Counter(characters)  # 对每章的角色进行实体提取
        eachChapter.append(li.most_common())

    tops = all.most_common()  # 出现次数最多的角色
    tops = [top[0] for top in tops]
    with open('df_character.csv', 'w+', encoding='utf-8', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(tops)

        coordinate = [[0 for i in range(len(tops))] for j in range(len(tops))]
        for name1, name2 in relevance:
            pos1 = tops.index(name1)
            pos2 = tops.index(name2)
            coordinate[pos1][pos2] = coordinate[pos1][pos2] + 1
            coordinate[pos2][pos1] = coordinate[pos2][pos1] + 1
        #print(coordinate)

    with open('df_relevance.csv', 'w+', encoding='utf-8', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(tops)
        for i in range(len(coordinate)):
            csv_writer.writerow(coordinate[i])

    with open('df_frenquency.csv', 'w+', encoding='utf-8', newline='') as file:  # 将算出的人物频率图放到csv里
        csv_writer = csv.writer(file)
        chapters = txt_related.returnChapter()
        csv_writer.writerow(chapters)
        #    csv_writer.writerow(tops)
        count = 0
        for chapter in eachChapter:  # 输出top里面有没有在某章中出现
            names = [name[0] for name in chapter]
            times = [time[1] for time in chapter]
            calTime = []
            for i in range(len(tops)):
                if tops[i] in names:
                    calTime.append(times[names.index(tops[i])])
                else:
                    calTime.append(0)
            calTime.insert(0, tops[count])
            # print(calTime)
            count = count + 1
            csv_writer.writerow(calTime)
    nlp.close()

#
def sentimentAnalysis():
    chapters = txt_related.returnChapter()
    contents = txt_related.returnContent()
    for content in contents:
        print(content)

def mains():
    sentimentP, sentimentS = getNamedEntity()
    print(sentimentP)
    print(sentimentS)


def mainn():
    stopword_list = nltk.corpus.stopwords.words('english')

    ori_text = load_text()
    clean_text = remove_special_characters(ori_text)
    exp_text = expand_contractions(clean_text, CONTRACTION_MAP)
    lem_text = lemmatize_text(exp_text)
    main_text = remove_stopwords(lem_text, stopword_list)

    words = main_text.split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    for i in range(10):
        word, count = items[i]
        print("{0:<10}{1:>5}".format(word, count))  # 打印前十个元素
    return items[0]

# 加载文本
def load_text(filename):
    if(filename == None or filename == ''):
        text = gutenberg.raw(fileids='carroll-alice.txt')
    else:
        with open(filename, 'w') as f:
            text = f.read()
    return text


# 去除特殊字符
def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text


# 去除停用词
def remove_stopwords(text, stopwords, is_lower_case=False):
    tokenizer = ToktokTokenizer()
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopwords]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopwords]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


# 扩展缩写词
def expand_contractions(text, contraction_mapping):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


# 词性还原
def lemmatize_text(text):
    nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text


def F(corpus, html_stripping=True, contraction_expansion=True,
                     accented_char_removal=True, text_lower_case=True,
                     text_lemmatization=True, special_char_removal=True,
                     stopword_removal=True, remove_digits=True):
    normalized_corpus = []
    # normalize each document in the corpus
    for doc in corpus:

        # expand contractions
        if contraction_expansion:
            doc = expand_contractions(doc)
        # lowercase the text
        if text_lower_case:
            doc = doc.lower()
        # remove extra newlines
        doc = re.sub(r'[\r|\n|\r\n]+', ' ', doc)
        # lemmatize text
        if text_lemmatization:
            doc = lemmatize_text(doc)
        # remove special characters and\or digits
        if special_char_removal:
            # insert spaces between special characters to isolate them
            special_char_pattern = re.compile(r'([{.(-)!}])')
            doc = special_char_pattern.sub(" \\1 ", doc)
            doc = remove_special_characters(doc, remove_digits=remove_digits)
            # remove extra whitespace
        doc = re.sub(' +', ' ', doc)
        # remove stopwords
        if stopword_removal:
            doc = remove_stopwords(doc, is_lower_case=text_lower_case)

        normalized_corpus.append(doc)

    return normalized_corpus
