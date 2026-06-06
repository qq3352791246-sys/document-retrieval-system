"""混合检索"""
import time
from .boolean_retriever import BooleanRetriever


class HybridRetriever:
    """混合检索引擎"""
    
    def __init__(self, inverted_index, tfidf_retriever):
        """初始化混合检索引擎"""
        self.boolean_retriever = BooleanRetriever(inverted_index)
        self.tfidf_retriever = tfidf_retriever
        self.index = inverted_index
    
    def search(self, query, top_k=10, use_boolean=True):
        """混合搜索"""
        start_time = time.time()
        
        if use_boolean:
            try:
                filtered_docs = set(self.boolean_retriever.search(query))
            except:
                filtered_docs = set(self.index.get_all_documents())
        else:
            filtered_docs = set(self.index.get_all_documents())
        
        all_results = self.tfidf_retriever.search(query, top_k=len(filtered_docs) * 2)
        
        results = [r for r in all_results if r['doc_id'] in filtered_docs]
        results = results[:top_k]
        
        response_time = (time.time() - start_time) * 1000
        
        return {
            'query': query,
            'results': results,
            'filtered_count': len(filtered_docs),
            'response_time': response_time
        }