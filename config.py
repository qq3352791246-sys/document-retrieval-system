import os
from datetime import timedelta

class Config:
    """应用配置"""
    SECRET_KEY = 'your-secret-key-change-in-production'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    CORPUS_FOLDER = os.path.join(os.path.dirname(__file__), 'corpus')
    RESULT_FOLDER = os.path.join(os.path.dirname(__file__), 'results')
    
    # 作者信息
    AUTHOR_NAME = "张三"
    AUTHOR_ID = "2024001"
    
    # 检索参数
    TOP_K = 10
    MIN_SCORE = 0.1
    
    # 确保目录存在
    os.makedirs(CORPUS_FOLDER, exist_ok=True)
    os.makedirs(RESULT_FOLDER, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
