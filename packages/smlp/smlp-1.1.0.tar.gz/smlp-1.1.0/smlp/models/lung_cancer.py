
class Config(object):

    """配置参数"""
    def __init__(self, rex, lowercase=True, nospace=True, enable_SW=True, enable_userdict=True, no_html_tags=True):
        self.model_name = 'lung_cancer'
        self.data_path = '/data/test.txt'                                # 数据集
        self.label = "lung_cancer"
        self.rex = rex             # 数据清洗正则表达式
        self.lowercase = lowercase		# 是否小写
        self.nospace = nospace			# 是否去除空格
        self.enable_SW = enable_SW      # 是否使用停止词
        self.enable_userdict = enable_userdict      # 是否使用用户词典
        self.no_html_tags = no_html_tags    # 是否去除html标签
        self.save_path = '/saved_dict/' + self.model_name + '.ckpt'        # 模型训练结果
