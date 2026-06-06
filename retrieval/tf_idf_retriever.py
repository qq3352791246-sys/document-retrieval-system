"""基于TF-IDF的检索器"""
from sklearn.feature_extraction.text import TfidfVectorizer
from data_source.text_preprocessor import TextPreprocessor
import numpy as np


class TFIDFRetriever:
    """基于TF-IDF的检索器"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.vectorizer = None
        self.tfidf_matrix = None
        self.doc_ids = []
        self.documents = {}
    
    def build_index(self, documents):
        """构建幷-IDF索引"""
        self.documents = documents
        self.doc_ids = list(documents.keys())
        
        processed_docs = []
        for doc_id in self.doc_ids:
            tokens = self.preprocessor.preprocess(documents[doc_id])
            processed_docs.append(' '.join(tokens))
        
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.tfidf_matrix = self.vectorizer.fit_transform(processed_docs)
    
    def search(self, query, top_k=10):
        """基于TF-IDF搜索"""
        if self.vectorizer is None:
            return []
        
        query_tokens = self.preprocessor.preprocess(query)
        query_text = ' '.join(query_tokens)
        
        query_vector = self.vectorizer.transform([query_text])
        scores = query_vector.dot(self.tfidf_matrix.T).toarray().flatten()
        
        results = []
        for idx, score in enumerate(scores):
            if score > 0:
                doc_id = self.doc_ids[idx]
                results.append({
                    'doc_id': doc_id,
                    'score': float(score),
                    'content': self.documents[doc_id][:200]
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]