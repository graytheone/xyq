import re
import nltk
import xyq_nlp
from utils import FILE
from nltk.corpus import gutenberg

#数据清洗
def deal_txt():
    txt = xyq_nlp.load_text(FILE)
#    print(txt)
    pattern1 = re.compile(r'CHAPTER \w+')
    result1 = pattern1.findall(txt)
    txt = txt+"CHAPTER SUGAR"
    pattern2 = re.compile(r'(?<=CHAPTER \w)\w*([\s\S]*?)(?=CHAPTER \w+)')
    result2 = re.findall(pattern2, txt)
    fin = txt.find('CHAPTER')
    result2.insert(0, txt[0:fin])
    return result1, result2

def returnChapter():
    txt = xyq_nlp.load_text(FILE)
    pattern1 = re.compile(r'CHAPTER \w+')
    result1 = pattern1.findall(txt)
    global length
    length = len(result1)
    return result1

def returnTitle():
    txt = xyq_nlp.load_text(FILE)
    fin = txt.find('CHAPTER')
    return txt[0:fin]

def returnContent():
    txt = xyq_nlp.load_text(FILE)
    txt = txt+"CHAPTER SUGAR"
    pattern2 = re.compile(r'(?<=CHAPTER \w)\w*([\s\S]*?)(?=CHAPTER \w+)')
    result2 = re.findall(pattern2, txt)
    fin = txt.find('CHAPTER')
#    result2.insert(0, txt[0:fin])
    return result2

def returnLength():
    txt = xyq_nlp.load_text(FILE)
    pattern1 = re.compile(r'CHAPTER \w+')
    result1 = pattern1.findall(txt)
    length = len(result1)
    return length

def get_numbers(string):
    pattern = re.compile(r'\d+')
    result = pattern.findall(string)
    return result
