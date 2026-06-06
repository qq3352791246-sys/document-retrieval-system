"""倒排索引统计分析"""


class IndexStatistics:
    """倒排索引统计分析工具"""
    
    def __init__(self, inverted_index):
        self.index = inverted_index
    
    def get_index_size(self):
        """获取索引大小"""
        total_postings = sum(len(set(positions)) 
                            for postings in self.index.index.values() 
                            for positions in postings.values())
        
        return {
            'total_documents': self.index.total_docs,
            'total_terms': len(self.index.index),
            'total_postings': total_postings,
            'avg_postings_per_term': total_postings / max(len(self.index.index), 1),
            'avg_terms_per_doc': sum(len(self.index.doc_term_freq[d]) 
                                    for d in self.index.documents) / max(self.index.total_docs, 1)
        }
    
    def get_term_statistics(self, term):
        """获取词项统计"""
        postings = self.index.get_postings(term)
        doc_freq = self.index.get_document_frequency(term)
        
        tf_values = [len(positions) for positions in postings.values()]
        
        return {
            'term': term,
            'document_frequency': doc_freq,
            'collection_frequency': sum(tf_values),
            'avg_tf': sum(tf_values) / len(tf_values) if tf_values else 0,
            'max_tf': max(tf_values) if tf_values else 0,
            'documents': sorted(postings.keys())
        }
    
    def get_top_terms(self, k=20):
        """获取最频繁的词项"""
        terms = sorted(self.index.term_doc_freq.items(), 
                      key=lambda x: x[1], reverse=True)
        return terms[:k]
    
    def get_vocabulary_distribution(self):
        """获取词汇分布"""
        doc_freqs = list(self.index.term_doc_freq.values())
        
        return {
            'total_terms': len(doc_freqs),
            'min_df': min(doc_freqs) if doc_freqs else 0,
            'max_df': max(doc_freqs) if doc_freqs else 0,
            'avg_df': sum(doc_freqs) / len(doc_freqs) if doc_freqs else 0,
            'median_df': sorted(doc_freqs)[len(doc_freqs)//2] if doc_freqs else 0,
            'hapax_count': sum(1 for df in doc_freqs if df == 1)
        }