"""倒排索引实现"""
from collections import defaultdict


class InvertedIndex:
    """倒排索引结构"""
    
    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(list))
        self.documents = {}
        self.doc_term_freq = defaultdict(lambda: defaultdict(int))
        self.term_doc_freq = defaultdict(int)
        self.total_docs = 0
    
    def add_document(self, doc_id, tokens):
        """添加文档到倒排索引"""
        self.documents[doc_id] = True
        self.total_docs = len(self.documents)
        
        seen_terms = set()
        
        for position, token in enumerate(tokens):
            self.index[token][doc_id].append(position)
            self.doc_term_freq[doc_id][token] += 1
            
            if token not in seen_terms:
                self.term_doc_freq[token] += 1
                seen_terms.add(token)
    
    def get_postings(self, term):
        """获取词项的倒排表"""
        return dict(self.index.get(term, {}))
    
    def get_postings_list(self, term):
        """获取词项出现的文档列表"""
        return sorted(self.index[term].keys())
    
    def get_term_frequency(self, term, doc_id):
        """获取词项在文档中的频率"""
        return self.doc_term_freq[doc_id].get(term, 0)
    
    def get_document_frequency(self, term):
        """获取词项的文档频率"""
        return self.term_doc_freq[term]
    
    def get_all_terms(self):
        """获取所有词项"""
        return set(self.index.keys())
    
    def get_all_documents(self):
        """获取所有文档ID"""
        return sorted(self.documents.keys())


class IndexBuilder:
    """倒排索引构建器"""
    
    def __init__(self, preprocessor):
        self.preprocessor = preprocessor
        self.inverted_index = InvertedIndex()
    
    def build(self, documents):
        """构建倒排索引"""
        for doc_id, content in documents.items():
            tokens = self.preprocessor.preprocess(content)
            self.inverted_index.add_document(doc_id, tokens)
        
        return self.inverted_index
    
    def print_statistics(self):
        """打印索引统计信息"""
        print(f"=== 倒排索引统计 ===")
        print(f"文档总数: {self.inverted_index.total_docs}")
        print(f"词项总数: {len(self.inverted_index.index)}")
        avg_terms = sum(len(self.inverted_index.doc_term_freq[d]) 
                       for d in self.inverted_index.documents) / max(self.inverted_index.total_docs, 1)
        print(f"平均每文档词项数: {avg_terms:.2f}")
        
        top_terms = sorted(self.inverted_index.term_doc_freq.items(), 
                          key=lambda x: x[1], reverse=True)[:10]
        print(f"\n最频繁的个词项:")
        for term, freq in top_terms:
            print(f"  '{term}': {freq} 个文档")