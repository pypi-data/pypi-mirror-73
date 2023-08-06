import re

class unicov():
    def __init__(self):
        self

    @classmethod
    def is_float(cls, numStr):
        ''' 字符串是否是浮点数(整数不算小数)
        '''
        flag = False
        numStr = str(numStr).strip().lstrip('-').lstrip('+')  # 去除正数(+)、负数(-)符号
        try:
            reg = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
            res = reg.match(str(numStr))
            if res:
                flag = True
        except Exception as ex:
            print("is_float() - error: " + str(ex))
        return flag

    # 对已经分好词的句子做单位转换, 同一单位g
    def unit_cov_g(self, segments: list):
        for i in range(len(segments)):
            tmp = []
            if 'kg' in segments[i]:
                if segments[i][:-2].isdigit() and segments[i][:-2].isascii():
                    num = int(segments[i][:-2])
                    num *= 1000
                    tmp.append(str(num))
                    tmp.append('g')
                    segments[i] = ''.join(tmp)
                    tmp.clear()
                if segments[i - 2].isdigit() and segments[i - 2].isascii():
                    segments[i - 2] = str(int(segments[i - 2]) * 1000)
                    segments[i] = 'g'
                if segments[i - 1].isdigit() and segments[i - 1].isascii():
                    segments[i - 1] = str(int(segments[i - 1]) * 1000)
                    segments[i] = 'g'
            if 'mg' in segments[i]:
                if segments[i][:-2].isdigit() and segments[i][:-2].isascii():
                    num = int(segments[i][:-2])
                    num /= 1000
                    tmp.append(str(num))
                    tmp.append('g')
                    segments[i] = ''.join(tmp)
                    tmp.clear()
                if segments[i - 2].isdigit() and segments[i - 2].isascii():
                    segments[i - 2] = str(int(segments[i - 2]) / 1000)
                    segments[i] = 'g'
                if segments[i - 1].isdigit() and segments[i - 1].isascii():
                    segments[i - 1] = str(int(segments[i - 1]) / 1000)
                    segments[i] = 'g'
            if '%' in segments[i]:
                if segments[i][:-1].isdigit():
                    num = int(segments[i][:-1])
                    num /= 100.00
                    segments[i] = str(num)
                elif self.is_float(segments[i][:-1]):
                    num = float(segments[i][:-1])
                    num /= 100.00
                    segments[i] = str(num)

        return segments

    # 对已经分好词的句子做单位转换, 同一单位mg
    def unit_cov_mg(self, segments: list):
        for i in range(len(segments)):
            tmp = []
            if 'g' in segments[i]:
                if segments[i][:-1].isdigit() and segments[i][:-1].isascii():
                    num = int(segments[i][:-1])
                    num *= 1000
                    tmp.append(str(num))
                    tmp.append('mg')
                    segments[i] = ''.join(tmp)
                    tmp.clear()
                if segments[i - 2].isdigit() and segments[i - 2].isascii():
                    segments[i - 2] = str(int(segments[i - 2]) * 1000)
                    segments[i] = 'mg'
                if segments[i - 1].isdigit() and segments[i - 1].isascii():
                    segments[i - 1] = str(int(segments[i - 1]) * 1000)
                    segments[i] = 'mg'
            if 'kg' in segments[i]:
                if segments[i][:-2].isdigit() and segments[i][:-2].isascii():
                    num = int(segments[i][:-2])
                    num *= 1000000
                    tmp.append(str(num))
                    tmp.append('mg')
                    segments[i] = ''.join(tmp)
                    tmp.clear()
                if segments[i - 2].isdigit() and segments[i - 2].isascii():
                    segments[i - 2] = str(int(segments[i - 2]) * 1000000)
                    segments[i] = 'mg'
                if segments[i - 1].isdigit() and segments[i - 1].isascii():
                    segments[i - 1] = str(int(segments[i - 1]) * 1000000)
                    segments[i] = 'mg'
            if '%' in segments[i]:
                if segments[i][:-1].isdigit():
                    num = int(segments[i][:-1])
                    num /= 100.00
                    segments[i] = str(num)
                elif self.is_float(segments[i][:-1]):
                    num = float(segments[i][:-1])
                    num /= 100.00
                    segments[i] = str(num)

        return segments

    # 对已经分好词的句子做单位转换, 同一单位kg
    def unit_cov_kg(self, segments: list):
        for i in range(len(segments)):
            tmp = []
            if 'g' in segments[i]:
                if segments[i][:-1].isdigit() and segments[i][:-1].isascii():
                    num = int(segments[i][:-1])
                    num /= 1000
                    tmp.append(str(num))
                    tmp.append('kg')
                    segments[i] = ''.join(tmp)
                    tmp.clear()
                if segments[i - 2].isdigit() and segments[i - 2].isascii():
                    segments[i - 2] = str(int(segments[i - 2]) * 1000)
                    segments[i] = 'kg'
                if segments[i - 1].isdigit() and segments[i - 1].isascii():
                    segments[i - 1] = str(int(segments[i - 1]) * 1000)
                    segments[i] = 'kg'
            if 'mg' in segments[i]:
                if segments[i][:-2].isdigit() and segments[i][:-2].isascii():
                    num = int(segments[i][:-2])
                    num /= 1000000
                    tmp.append(str(num))
                    tmp.append('kg')
                    segments[i] = ''.join(tmp)
                    tmp.clear()
                if segments[i - 2].isdigit() and segments[i - 2].isascii():
                    segments[i - 2] = str(int(segments[i - 2]) / 1000000)
                    segments[i] = 'kg'
                if segments[i - 1].isdigit() and segments[i - 1].isascii():
                    segments[i - 1] = str(int(segments[i - 1]) / 1000000)
                    segments[i] = 'kg'
            if '%' in segments[i]:
                if segments[i][:-1].isdigit():
                    num = int(segments[i][:-1])
                    num /= 100.00
                    segments[i] = str(num)
                elif self.is_float(segments[i][:-1]):
                    num = float(segments[i][:-1])
                    num /= 100.00
                    segments[i] = str(num)

        return segments
