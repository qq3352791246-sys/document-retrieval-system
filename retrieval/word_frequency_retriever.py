"""基于词频的检索器"""
from collections import Counter
from data_source.text_preprocessor import TextPreprocessor


class WordFrequencyRetriever:
    """基于词频的检索器"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.documents = {}
        self.index = {}
    
    def build_index(self, documents):
        """构建词频索引"""
        self.documents = documents
        self.index = {}
        
        for doc_id, content in documents.items():
            tokens = self.preprocessor.preprocess(content)
            self.index[doc_id] = Counter(tokens)
    
    def search(self, query, top_k=10):
        """基于词频搜索"""
        query_tokens = self.preprocessor.preprocess(query)
        query_freq = Counter(query_tokens)
        
        results = []
        for doc_id, token_freq in self.index.items():
            score = sum(query_freq[token] * token_freq[token] for token in query_tokens)
            if score > 0:
                results.append({
                    'doc_id': doc_id,
                    'score': score,
                    'content': self.documents[doc_id][:200]
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]