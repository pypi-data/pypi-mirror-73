import re


class Thesaurus():
    def __init__(self, contents: list):
        self.contents = contents
        self.synonym = {}
        return

    def raw_contents(self):
        return self.contents()

    # 检验是否全是中文字符
    @staticmethod
    def is_all_chinese(strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    # 检验是否含有中文字符
    @staticmethod
    def is_contains_chinese(strs):
        for _char in strs:
            if _char and '\u4e00' <= _char <= '\u9fa5':
                return True
        return False

    # 大写率
    @staticmethod
    def upper_rate(word):
        if not word: return 0
        l = len(word)
        n = 0
        for j in word:
            if j.isupper():
                n += 1
        return float(n / l)

    # 推荐词排序
    def sug_words(self, array):
        return sorted(set(array), key=lambda x: self.upper_rate(x), reverse=True)

    # 找出同义词
    def synonymy(self, min_len=2, max_len=20):
        for s in self.contents:
            if len(s) >= 3:
                a, b, ze, tmp = "", [], -1, []  # 当前的分词， key对应同义词列表，key的中英文(0中，1英)， 暂存key的同义词
                i, n = 0, 0
                while i < len(s):
                    # print(s[i])
                    if s[i] == "(":
                        if s[i + 1].encode('UTF-8').isalpha() and self.is_contains_chinese(s[i - 1]) and min_len <= len(
                                s[i - 1]) <= max_len and not s[i-1].isdigit():
                            # print(s[i])
                            a = s[i - 1]
                            b = []
                            tmp = []
                            i += 1
                            n += 1
                            ze = 0
                        elif s[i - 1].encode('UTF-8').isalnum() and self.is_all_chinese(s[i + 1]) and min_len <= len(
                                s[i - 1]) <= max_len and not s[i-1].isdigit():
                            # print(s[i])
                            a = s[i - 1]
                            b = []
                            tmp = []
                            i += 1
                            n += 1
                            ze = 1
                        else:
                            i += 1
                    elif s[i] != "(" and s[i] != ")" and n != 0:
                        if len(s[i]) > 1 and s[i][-1] == ',':
                            tmp.append(s[i][:-1])
                            if ze == 0:
                                b.append(" ".join(tmp).strip())
                            elif ze == 1:
                                b.append("".join(tmp).strip())
                            tmp.clear()
                            i += 1
                        elif s[i] != ",":
                            tmp.append(s[i])
                            i += 1
                        else:
                            if ze == 0:
                                b.append(" ".join(tmp).strip())
                            elif ze == 1:
                                b.append("".join(tmp).strip())
                            tmp.clear()
                            i += 1
                    elif s[i] == ")":
                        if n != 0:
                            if ze == 0:
                                b.append(" ".join(tmp).strip())
                            elif ze == 1:
                                b.append("".join(tmp).strip())
                            i += 1
                            n -= 1
                            if a in self.synonym:
                                self.synonym[a].extend(b)
                                self.synonym[a] = self.sug_words(self.synonym[a]) if ze == 0 else self.synonym[a]
                            else:
                                self.synonym[a] = self.sug_words(b) if ze == 0 else b
                            if b: b = []
                            tmp = []
                        else:
                            i += 1
                    elif s[i] != "(" and s[i] != ")" and n == 0:
                        i += 1

        return self.synonym

    # 同义词词典清洗
    def cleanup(self):
        rm_list = []
        del_list = []
        for key in self.synonym:
            self.synonym[key] = [x.replace('   ', ' ') for x in self.synonym[key]]
            for item in self.synonym[key]:
                if re.search(
                        r'[(研究)(组)(方案)(接受)=分(获益)(少见)(可能)年月日(除外)(总局)(批准)(包括)(认证)期≥≤~><]|^[0-9]*$|^[\s\b]*$|'
                        r'([0-9|\.]+)\s+\-\s+([0-9|\.]+)|^[一二三四五六七八九十]+(\b)*$', item, re.M | re.I):
                    rm_list.append(item)
            for i in rm_list:
                self.synonym[key].remove(i)
            rm_list.clear()
            if not self.synonym[key]:
                del_list.append(key)

        for d in del_list:
            del self.synonym[d]

    # 同义词替换
    def syn_replacez(self, key, index):
        if index == -1:
            for i in range(len(self.contents)):
                self.contents[i] = [key if x in self.synonym[key] else x for x in self.contents[i]]
                #print(self.contents[i])
        else:
            for i in range(len(self.contents)):
                self.contents[i] = [self.synonym[key][index] if x in self.synonym[key] or x == key else x for x in self.contents[i]]
                #print(self.contents[i])
