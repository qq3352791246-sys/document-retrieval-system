import re
import jieba
from nltk.corpus import stopwords
import nltk

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class TextPreprocessor:
    """文本预处理器"""
    
    def __init__(self, language='chinese'):
        self.language = language
        self.stop_words = set(stopwords.words('english'))
        self.cn_stop_words = {'的', '是', '在', '了', '和', '有', '人', '这', '中', '大', '为', '上', '个', '国', '我', '以', '要', '他', '时', '来', '用', '们', '生', '到', '作', '地', '于', '出', '就', '分', '对', '成', '会', '可', '主', '发', '年', '动', '同', '工', '也', '能', '下', '过', '民', '前', '面', '书', '光', '产', '点', '育', '等', '代', '最', '新', '开', '经', '起', '取', '据', '场', '那', '一', '此', '去', '后', '学', '高', '性', '找', '象', '她', '多', '或', '水', '爱', '等', '七', '十', '几', '某', '本', '课', '第', '一个', '是否'}
    
    @staticmethod
    def clean_text(text):
        """清理文本"""
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def tokenize_chinese(self, text):
        """中文分词"""
        return list(jieba.cut(text))
    
    def tokenize_english(self, text):
        """英文分词"""
        return text.lower().split()
    
    def remove_stopwords(self, tokens):
        """删除停用词"""
        return [t for t in tokens if t not in self.stop_words and t not in self.cn_stop_words and len(t) > 1]
    
    def preprocess(self, text):
        """完整预处理流程"""
        text = self.clean_text(text)
        
        if self.language == 'chinese':
            tokens = self.tokenize_chinese(text)
        else:
            tokens = self.tokenize_english(text)
        
        tokens = self.remove_stopwords(tokens)
        return tokens