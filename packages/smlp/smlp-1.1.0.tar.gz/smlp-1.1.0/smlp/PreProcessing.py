from abc import ABCMeta, abstractmethod
import re
import jieba
import jieba.analyse
import math
from tqdm import tqdm
from pprint import pprint

from textrank4zh import TextRank4Keyword, TextRank4Sentence


class PreProcessing():
    def __init__(self, enable_SW=True, enable_userdict=True):
        #if enable_userdict: jieba.load_userdict("smlp/data/token.dict")
        #if enable_SW: jieba.analyse.set_stop_words('data/stopwords.txt')
        self

    def strQ2B(self, ustring):
        """全角转半角"""
        rstring = ""
        for uchar in ustring:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                inside_code -= 65248

            rstring += chr(inside_code)
        return rstring

    # 分句
    def cut_sent(self, para):
        para = re.sub('([。！？?])([^”’])', r"\1\n\2", para)  # 单字符断句符
        para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
        para = re.sub('(…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
        para = re.sub('([。！？?][”’])([^，。！？?])', r'\1\n\2', para)
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        para = para.rstrip()  # 段尾如果有多余的\n就去掉它
        # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
        return para.split("\n")

    # 文本清理，包括全角转半角，清洗()外的内容，分句
    def cleanup1(self, filepath: str):
        f = open(filepath, "r", encoding='utf-8')
        text = f.read()
        text = self.strQ2B(text)
        return text

    # 文本清理，包括全角转半角，清洗()外的内容，分句
    def cleanup(self, filepath: str):
        f = open(filepath, "r", encoding='utf-8')
        text = f.read()
        text = self.strQ2B(text)
        text = self.cut_sent(text)
        for i in range(len(text)):
            patten = re.compile(r'([\w\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            patten = re.compile(r'([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5\w]+\s+)')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            patten = re.compile(r'([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5\w]+)')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            patten = re.compile(r'([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            patten = re.compile(r'([a-zA-Z0-9]+)\s+([-_—]+)')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            patten = re.compile(r'([-_—]+)\s+([a-zA-Z0-9]+)')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            patten = re.compile(r'([0-9]+)\s+([0-9]+)\s*')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            text[i] = text[i].replace(',', ', ').replace(',  ', ', ')
        clean_content = [x for x in text if x]

        return clean_content

    def clean_txt(self, text: str):
        text = self.strQ2B(text)
        patten = re.compile(r'([\w\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)')
        text = patten.sub(r'\1\2', text).strip()
        patten = re.compile(r'([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5\w]+\s+)')
        text = patten.sub(r'\1\2', text).strip()
        patten = re.compile(r'([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5\w]+)')
        text = patten.sub(r'\1\2', text).strip()
        patten = re.compile(r'([0-9]+)\s+([0-9]+)\s*')
        clean_content = patten.sub(r'\1\2', text).strip()

        return clean_content

    def cleanup_txt(self, text: str):
        text = self.strQ2B(text)
        text = self.cut_sent(text)
        for i in range(len(text)):
            patten = re.compile(r'([\w\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            patten = re.compile(r'([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5\w]+\s+)')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            patten = re.compile(r'([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5\w]+)')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            patten = re.compile(r'([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            patten = re.compile(r'([a-zA-Z0-9]+)\s+([-_—]+)')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            patten = re.compile(r'([-_—]+)\s+([a-zA-Z0-9]+)')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            patten = re.compile(r'([0-9]+)\s+([0-9]+)\s*')
            text[i] = patten.sub(r'\1\2', text[i]).strip()
            text[i] = text[i].replace(',', ', ').replace(',  ', ', ')
        clean_content = [x for x in text if x]

        return clean_content

    # 为每个分句做分词处理
    def seg(self, contents: list, dictpath='default'):
        # text = seg.cut('我爱北京天安门')  # 进行分词
        if dictpath != 'default':
            jieba.load_userdict(dictpath)
        sentences = []
        # pp = PreProcessing()
        for i in contents:
            segments = jieba.cut(i, cut_all=False, use_paddle=True)
            segments = list(segments)
            sentences.append(segments)

        return sentences

    def clean(self, content: str, rex=1, no_html_tags=True, lowercase=True, nospace=True):

        # 过滤不了\\ \ 中文（）还有————
        r1 = u'[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】▌—（）［］：《》？“”‘’！[\\]^_`{|}~]+'  # 用户也可以在此进行自定义过滤字符
        # 者中规则也过滤不完全
        r2 = "[+.!/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+"
        # \\\可以过滤掉反向单杠和双杠，/可以过滤掉正向单杠和双杠，第一个中括号里放的是英文符号，第二个中括号里放的是中文符号，第二个中括号前不能少|，否则过滤不完全
        r3 = "[.!//_,$&%^*()<>+\"'?@#-|:~{}]+|[——！\\\\，。=？、：“”‘’《》【】￥……（）]+"
        # 去掉括号和括号内的所有内容
        r4 = "\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*()<>+""'?@|:~{}#]+|[0-9’——！\\\，。=？、：“”‘’￥……（）《》【】]+"

        switcher = {
            1: r1,
            2: r2,
            3: r3,
            4: r4
        }

        if no_html_tags:
            cleanr = re.compile('<.*?>')
            content = re.sub(cleanr, ' ', content)  # 去除html标签

        if lowercase:
            content = content.lower()

        if nospace:
            content = content.replace(' ', '')

        if isinstance(rex, int):
            try:
                clean_content = re.sub(switcher[rex], '', content)
            except KeyError:
                print("无法找到目标正则表达式")

        else:
            clean_content = re.sub(rex, '', content)

        return clean_content

    def cut(self, text: str):
        return jieba.cut(text, cut_all=False, use_paddle=True)  # 使用paddle模式

    def idf(self, contents: list, file_path='wdic.txt'):
        all_dict = {}
        total = 0
        # class_path = corpus_path + "\\"  # 拼出分类子目录的路径
        # print(class_path)
        # seg_dir = seg_path + "/"  # 拼出分词后语料分类目录
        # if not os.path.exists(seg_dir):  # 是否存在目录，如果没有创建
        #    os.makedirs(seg_dir)
        # print(seg_dir)
        # file_list = os.listdir(class_path)  # 获取class_path下的所有文件
        stopwords = open("data/stopwords.txt", 'rb').readlines()
        for content in tqdm(contents):  # 遍历类别目录下文件
            # fullname = class_path + file_path  # 拼出文件名全路径
            # print(fullname)
            content = content.replace("\r\n", "")  # 删除换行和多余的空格
            content = content.replace(" ", "")
            content_seg = jieba.cut(content, cut_all=False, use_paddle=True)  # 为文件内容分词

            outstr = []

            for word in content_seg:
                if word not in stopwords:
                    if word != '\t' and word != '\n':
                        # outstr.append(word)
                        outstr.append(word)
            for word in outstr:
                if ' ' in word:
                    word.remove(' ')
            temp_dict = {}
            total += 1
            for word in outstr:
                # print(word)
                temp_dict[word] = 1
                # print(temp_dict)
            for key in temp_dict:
                num = all_dict.get(key, 0)
                all_dict[key] = num + 1
            # savefile(seg_dir+file_path,"".join(outstr))  # 将处理后的文件保存到分词后语料目录

        # idf_dict字典就是生成的IDF语料库
        idf_dict = {}
        for key in tqdm(all_dict):
            # print(all_dict[key])
            w = key
            p = '%.10f' % (math.log10(total / (all_dict[key] + 1)))
            if w > u'\u4e00' and w <= u'\u9fa5':
                idf_dict[w] = p
        print('IDF字典构造结束')
        fw = open(file_path, 'w', encoding='utf-8')

        for k in idf_dict:
            if k != '\n':
                # print(k)
                fw.write(k + ' ' + idf_dict[k] + '\n')
        fw.close()

    def tfidf(self, text, file_name='data/wdic.txt', topK=20, withWeight=True, allowPOS=()):
        jieba.analyse.set_idf_path(file_name)
        pprint(jieba.analyse.extract_tags(text, topK=topK, withWeight=withWeight, allowPOS=allowPOS))
        # print(",".join(tags))

    def textrank(self, text, allow_speech_tags=['n', 'nrfg', 'ns', 'nt', 'nz', 'eng'], window=2):

        tr4w = TextRank4Keyword(stop_words_file='data/stopwords.txt', allow_speech_tags=allow_speech_tags)
        tr4w.analyze(text=text, lower=True,
                     window=window)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

        print('关键词：')
        for item in tr4w.get_keywords(20, word_min_len=1):
            print(item.word, item.weight)

        print()
        print('关键短语：')
        for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
            print(phrase)

        tr4s = TextRank4Sentence()
        tr4s.analyze(text=text, lower=True)

        print()
        print('摘要：')
        for item in tr4s.get_key_sentences(num=3):
            print(item.index, item.weight, item.sentence)  # index是语句在文本中位置，weight是权重

        '''
        tr4w = TextRank4Keyword(stop_words_file='data/stopwords.txt')

        tr4w.analyze(text=text, vertex_source="no_stop_words", lower=True, window=2)

        print()
        print('sentences:')
        for s in tr4w.sentences:
            print(s)  # py2中是unicode类型。py3中是str类型。

        print()
        print('words_no_filter')
        for words in tr4w.words_no_filter:
            print('/'.join(words))  # py2中是unicode类型。py3中是str类型。

        print()
        print('words_no_stop_words')
        for words in tr4w.words_no_stop_words:
            print('/'.join(words))  # py2中是unicode类型。py3中是str类型。

        print()
        print('words_all_filters')
        for words in tr4w.words_all_filters:
            print('/'.join(words))  # py2中是unicode类型。py3中是str类型。
        '''
