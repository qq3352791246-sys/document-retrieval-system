"""短语搜索实现"""


class PhraseSearcher:
    """短语搜索引擎"""
    
    def __init__(self, inverted_index):
        """初始化短语搜索引擎"""
        self.index = inverted_index
    
    def search_phrase(self, phrase_tokens):
        """搜索精确短语"""
        if not phrase_tokens:
            return {}
        
        first_term = phrase_tokens[0]
        postings = self.index.get_postings(first_term)
        
        if not postings:
            return {}
        
        result = {}
        
        for doc_id, positions in postings.items():
            valid_positions = []
            
            for start_pos in positions:
                match = True
                for offset, term in enumerate(phrase_tokens[1:], 1):
                    expected_pos = start_pos + offset
                    term_postings = self.index.get_postings(term)
                    if doc_id not in term_postings or expected_pos not in term_postings[doc_id]:
                        match = False
                        break
                
                if match:
                    valid_positions.append(start_pos)
            
            if valid_positions:
                result[doc_id] = valid_positions
        
        return result
    
    def search_proximity(self, terms, distance=5):
        """邻近搜索"""
        if not terms or len(terms) < 2:
            return {}
        
        first_term = terms[0]
        postings = self.index.get_postings(first_term)
        
        if not postings:
            return {}
        
        result = {}
        
        for doc_id, positions in postings.items():
            valid_positions = []
            
            for start_pos in positions:
                valid = True
                for term in terms[1:]:
                    term_postings = self.index.get_postings(term)
                    
                    if doc_id not in term_postings:
                        valid = False
                        break
                    
                    found = False
                    for term_pos in term_postings[doc_id]:
                        if abs(term_pos - start_pos) <= distance:
                            found = True
                            break
                    
                    if not found:
                        valid = False
                        break
                
                if valid:
                    valid_positions.append(start_pos)
            
            if valid_positions:
                result[doc_id] = valid_positions
        
        return result