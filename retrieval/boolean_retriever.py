"""布尔检索实现"""
import re


class BooleanQueryParser:
    """布尔查询解析器"""
    
    def __init__(self):
        self.tokens = []
        self.pos = 0
    
    def parse(self, query):
        """解析布尔查询字符串"""
        self.tokens = self._tokenize(query)
        self.pos = 0
        
        if not self.tokens:
            return None
        
        result = self._parse_or_expr()
        
        if self.pos < len(self.tokens):
            raise ValueError(f"解析错误: 位置 {self.pos}")
        
        return result
    
    def _tokenize(self, query):
        """分词"""
        query = query.upper()
        query = re.sub(r'\s+', ' ', query.strip())
        tokens = []
        
        for token in query.split():
            if token in ['AND', 'OR', 'NOT']:
                tokens.append(('OP', token))
            else:
                tokens.append(('TERM', token))
        
        return tokens
    
    def _current_token(self):
        """获取当前token"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def _consume(self, expected_type=None):
        """消耗一个token"""
        token = self._current_token()
        if expected_type and token and token[0] != expected_type:
            raise ValueError(f"期望 {expected_type}，得到 {token[0]}")
        self.pos += 1
        return token
    
    def _parse_or_expr(self):
        """解析OR表达式"""
        left = self._parse_and_expr()
        
        while self._current_token() and self._current_token() == ('OP', 'OR'):
            self._consume()
            right = self._parse_and_expr()
            left = ('OR', left, right)
        
        return left
    
    def _parse_and_expr(self):
        """解析AND表达式"""
        left = self._parse_not_expr()
        
        while self._current_token() and self._current_token() == ('OP', 'AND'):
            self._consume()
            right = self._parse_not_expr()
            left = ('AND', left, right)
        
        return left
    
    def _parse_not_expr(self):
        """解析NOT表达式"""
        if self._current_token() and self._current_token() == ('OP', 'NOT'):
            self._consume()
            term = self._parse_primary()
            return ('NOT', term)
        
        return self._parse_primary()
    
    def _parse_primary(self):
        """解析基本表达式"""
        token = self._current_token()
        
        if not token:
            raise ValueError("意外的查询结束")
        
        if token[0] == 'TERM':
            self._consume()
            return ('TERM', token[1])
        else:
            raise ValueError(f"意外的token: {token}")


class BooleanRetriever:
    """布尔检索引擎"""
    
    def __init__(self, inverted_index):
        """初始化布尔检索引擎"""
        self.index = inverted_index
        self.parser = BooleanQueryParser()
        self.total_docs = set(inverted_index.get_all_documents())
    
    def search(self, query):
        """执行布尔查询"""
        try:
            ast = self.parser.parse(query)
            if ast is None:
                return []
            
            result = self._evaluate(ast)
            return sorted(list(result))
        
        except Exception as e:
            print(f"查询错误: {e}")
            return []
    
    def _evaluate(self, ast):
        """评估AST"""
        if ast[0] == 'TERM':
            term = ast[1].lower()
            postings = self.index.get_postings_list(term)
            return set(postings)
        
        elif ast[0] == 'AND':
            left = self._evaluate(ast[1])
            right = self._evaluate(ast[2])
            return left & right
        
        elif ast[0] == 'OR':
            left = self._evaluate(ast[1])
            right = self._evaluate(ast[2])
            return left | right
        
        elif ast[0] == 'NOT':
            operand = self._evaluate(ast[1])
            return self.total_docs - operand
        
        return set()


class BooleanQueryOptimizer:
    """布尔查询优化器"""
    
    def __init__(self, index):
        self.index = index
    
    def analyze_query(self, query):
        """分析查询的复杂度"""
        and_count = query.upper().count(' AND ')
        or_count = query.upper().count(' OR ')
        not_count = query.upper().count(' NOT ')
        terms = re.findall(r'\b(?!AND|OR|NOT)\S+\b', query.upper())
        
        return {
            'and_count': and_count,
            'or_count': or_count,
            'not_count': not_count,
            'term_count': len(terms),
            'estimated_complexity': and_count * 2 + or_count + not_count * 3
        }