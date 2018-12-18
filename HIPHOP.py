import requests
import jieba
import re
import json
import operator
from xpinyin import Pinyin
import downSong

musicbox = downSong.wangyiyun()
pinyinbox = Pinyin()

RhymeDct = {'ui': '7', 'uan': '3', 'ian': '3', 'iu': '13', 'en': '8', 'ue': '16', 'ing': '9', 'a': '1', 'ei': '7',
            'eng': '9', 'uo': '6', 'ye': '12', 'in': '8', 'ou': '13', 'ao': '5', 'uang': '4', 'ong': '9', 'ang': '4',
            'ai': '2', 'ua': '1', 'uai': '2', 'an': '3', 'iao': '5', 'ia': '1', 'ie': '12', 'iong': '9', 'i': '11',
            'er': '10', 'e': '6', 'u': '14', 'un': '8', 'iang': '4', 'o': '6', 'qu': '15', 'xu': '15', 'yu': '15'}

# 词语转拼音
def _analysis_words(words):
    word_py = pinyinbox.get_pinyin((u'{}'.format(words)))
    lst_words = word_py.split('-')
    r = []
    for i in lst_words:
        while True:
            if not i:
                break
            token = RhymeDct.get(i, None)
            if token:
                r.append(token)
                break
            i = i[1:]
    if len(r) == len(words):
        return '-'.join(r)

def _match_(Awords,Bwords):
    Awordslist = Awords.split('-')
    Bwordslist = Bwords.split('-')
    while len(Awordslist)>1:
        if operator.eq(Awordslist,Bwordslist):
            return True
        Awordslist.pop(0)
    return False


# 存储指定押韵的词语
def ProcessLyrics():
    with open('keyword.json','w',encoding='utf-8') as f1:
        f1.write("[")
        with open('Lyrics.txt', 'r',encoding='utf-8') as f2:
            lrc = f2.read()
            seg_list = list(jieba.cut(lrc, cut_all=True))
            for i in seg_list:
                    if _analysis_words(i)!=None:
                        f1.write("{'"+_analysis_words(i)+"':'"+i+"'},")
            f2.close()
        f1.write("]")
        f1.close()


def Findkey(strA):
    result={}
    list = []
    with open('keyword.json', 'r',encoding='utf-8') as f:
        list=eval(f.readlines()[0])
        f.close()

    for item in list:
        for strB in item:
            if _match_(strA,strB):
                key=item.get(strB)
                number=result.get(key)
                if number !=None and number>=1:
                    result[key]=number+1
                else:
                    result.update({key:1})

    print(result)

musicbox.DownloadMusicByListID(996728953)

# ProcessLyrics()

# key=input("请输入关键词:")
# str=_analysis_words(key)
# print("匹配押韵的词：")
# Findkey(str)